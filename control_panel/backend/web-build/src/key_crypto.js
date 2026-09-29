import * as asn1js from 'asn1js';
import { p256 } from '@noble/curves/nist.js';
import { sha256 } from '@noble/hashes/sha2.js';

const EC_PUBLIC_KEY_OID = '1.2.840.10045.2.1';
const PRIME256V1_OID = '1.2.840.10045.3.1.7';
const PRIVATE_KEY_LIMIT = 16 * 1024;
const PUBLIC_KEY_LIMIT = 2 * 1024;
const utf8 = new TextEncoder();

function requireSecureRandom() {
    if (typeof globalThis.crypto?.getRandomValues !== 'function') {
        throw new Error('crypto.getRandomValues is required to generate or use a login key');
    }
}

function bytesToArrayBuffer(bytes) {
    return Uint8Array.from(bytes).buffer;
}

function toBase64(bytes) {
    let binary = '';
    for (let offset = 0; offset < bytes.length; offset += 0x8000) {
        binary += String.fromCharCode(...bytes.subarray(offset, offset + 0x8000));
    }
    return btoa(binary);
}

function fromBase64(text) {
    if (typeof text !== 'string' || text.length === 0 || text.length > 4 * Math.ceil(PRIVATE_KEY_LIMIT / 3) || !/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(text)) {
        throw new Error('invalid key PEM base64');
    }
    const binary = atob(text);
    const bytes = Uint8Array.from(binary, (character) => character.charCodeAt(0));
    if (toBase64(bytes) !== text) throw new Error('non-canonical key PEM base64');
    return bytes;
}

function encodePem(type, der) {
    const base64 = toBase64(der);
    const lines = base64.match(/.{1,64}/g) || [];
    return `-----BEGIN ${type}-----\n${lines.join('\n')}\n-----END ${type}-----\n`;
}

function decodePem(pemText, type, maxBytes) {
    if (typeof pemText !== 'string' || pemText.length === 0 || pemText.length > maxBytes) {
        throw new Error('invalid key PEM size');
    }
    const match = pemText.match(new RegExp(`^-----BEGIN ${type}-----\\s*([A-Za-z0-9+/=\\r\\n]+?)\\s*-----END ${type}-----\\s*$`));
    if (!match) throw new Error(`invalid ${type} PEM`);
    const encoded = match[1].replace(/[\r\n]/g, '');
    const der = fromBase64(encoded);
    if (der.length === 0 || der.length > maxBytes) throw new Error('invalid key DER size');
    return der;
}

function parseDER(bytes, label) {
    const parsed = asn1js.fromBER(bytes, { maxDepth: 16, maxNodes: 128, maxContentLength: PRIVATE_KEY_LIMIT });
    if (parsed.offset !== bytes.length || parsed.offset < 0 || parsed.result.error) {
        throw new Error(`invalid ${label} DER`);
    }
    return parsed.result;
}

function expectSequence(value, label) {
    if (!(value instanceof asn1js.Sequence)) throw new Error(`invalid ${label} ASN.1 sequence`);
    return value.valueBlock.value;
}

function expectInteger(value, expected, label) {
    if (!(value instanceof asn1js.Integer) || value.valueBlock.valueDec !== expected) {
        throw new Error(`invalid ${label} version`);
    }
}

function expectP256Algorithm(value) {
    const algorithm = expectSequence(value, 'algorithm identifier');
    if (algorithm.length !== 2 || !(algorithm[0] instanceof asn1js.ObjectIdentifier) || !(algorithm[1] instanceof asn1js.ObjectIdentifier)) {
        throw new Error('invalid EC algorithm identifier');
    }
    if (algorithm[0].getValue() !== EC_PUBLIC_KEY_OID || algorithm[1].getValue() !== PRIME256V1_OID) {
        throw new Error('key must use ECDSA P-256');
    }
}

function parsePrivateKey(pemText) {
    const der = decodePem(pemText, 'PRIVATE KEY', PRIVATE_KEY_LIMIT);
    const privateInfo = expectSequence(parseDER(der, 'PKCS#8'), 'PKCS#8');
    if (privateInfo.length < 3 || privateInfo.length > 4) throw new Error('invalid PKCS#8 field count');
    expectInteger(privateInfo[0], 0, 'PKCS#8');
    expectP256Algorithm(privateInfo[1]);
    if (!(privateInfo[2] instanceof asn1js.OctetString)) throw new Error('invalid PKCS#8 private key field');

    const ecPrivateDER = new Uint8Array(privateInfo[2].getValue());
    const ecPrivate = expectSequence(parseDER(ecPrivateDER, 'EC private key'), 'EC private key');
    if (ecPrivate.length < 2 || ecPrivate.length > 4) throw new Error('invalid EC private key field count');
    expectInteger(ecPrivate[0], 1, 'EC private key');
    if (!(ecPrivate[1] instanceof asn1js.OctetString)) throw new Error('invalid EC private scalar');
    const secretKey = new Uint8Array(ecPrivate[1].getValue());
    if (secretKey.length !== 32) throw new Error('P-256 private scalar must be 32 bytes');

    const publicKey = p256.getPublicKey(secretKey, false);
    for (const optional of ecPrivate.slice(2)) {
        if (optional.idBlock.tagClass !== 3 || (optional.idBlock.tagNumber !== 0 && optional.idBlock.tagNumber !== 1)) {
            secretKey.fill(0);
            throw new Error('unsupported EC private key field');
        }
        if (optional.idBlock.tagNumber === 0) {
            const parameters = optional.valueBlock.value?.[0];
            if (!(parameters instanceof asn1js.ObjectIdentifier) || parameters.getValue() !== PRIME256V1_OID) {
                secretKey.fill(0);
                throw new Error('EC private key parameters are not P-256');
            }
        } else {
            const bitString = optional.valueBlock.value?.[0];
            if (!(bitString instanceof asn1js.BitString) || bitString.valueBlock.unusedBits !== 0 || !equalBytes(bitString.valueBlock.valueHexView, publicKey)) {
                secretKey.fill(0);
                throw new Error('EC private key public component does not match its scalar');
            }
        }
    }
    return { secretKey, publicKey };
}

function parsePublicKey(pemText) {
    const der = decodePem(pemText, 'PUBLIC KEY', PUBLIC_KEY_LIMIT);
    const subjectPublicKeyInfo = expectSequence(parseDER(der, 'SPKI'), 'SPKI');
    if (subjectPublicKeyInfo.length !== 2) throw new Error('invalid SPKI field count');
    expectP256Algorithm(subjectPublicKeyInfo[0]);
    const bitString = subjectPublicKeyInfo[1];
    if (!(bitString instanceof asn1js.BitString) || bitString.valueBlock.unusedBits !== 0) {
        throw new Error('invalid SPKI public point');
    }
    const point = p256.Point.fromBytes(new Uint8Array(bitString.valueBlock.valueHexView)).toBytes(false);
    const canonicalDER = encodeSPKI(point);
    return { point, der: canonicalDER, pem: encodePem('PUBLIC KEY', canonicalDER) };
}

function encodeSPKI(publicPoint) {
    const algorithm = new asn1js.Sequence({
        value: [
            new asn1js.ObjectIdentifier({ value: EC_PUBLIC_KEY_OID }),
            new asn1js.ObjectIdentifier({ value: PRIME256V1_OID }),
        ],
    });
    const pointBits = new asn1js.BitString({ unusedBits: 0, valueHex: bytesToArrayBuffer(publicPoint) });
    const subjectPublicKeyInfo = new asn1js.Sequence({ value: [algorithm, pointBits] });
    return new Uint8Array(subjectPublicKeyInfo.toBER(false));
}

function encodePrivateKey(secretKey) {
    const ecPrivate = new asn1js.Sequence({
        value: [
            new asn1js.Integer({ value: 1 }),
            new asn1js.OctetString({ valueHex: bytesToArrayBuffer(secretKey) }),
        ],
    });
    const algorithm = new asn1js.Sequence({
        value: [
            new asn1js.ObjectIdentifier({ value: EC_PUBLIC_KEY_OID }),
            new asn1js.ObjectIdentifier({ value: PRIME256V1_OID }),
        ],
    });
    const privateInfo = new asn1js.Sequence({
        value: [
            new asn1js.Integer({ value: 0 }),
            algorithm,
            new asn1js.OctetString({ valueHex: ecPrivate.toBER(false) }),
        ],
    });
    return new Uint8Array(privateInfo.toBER(false));
}

function encodeBase64URL(bytes) {
    return toBase64(bytes).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
}

function decodeBase64URL(value, expectedLength) {
    if (typeof value !== 'string' || value.length !== expectedLength || !/^[A-Za-z0-9_-]+$/.test(value)) {
        throw new Error('invalid canonical base64url');
    }
    const base64 = value.replace(/-/g, '+').replace(/_/g, '/') + '='.repeat((4 - value.length % 4) % 4);
    const decoded = Uint8Array.from(atob(base64), (character) => character.charCodeAt(0));
    if (encodeBase64URL(decoded) !== value) throw new Error('invalid canonical base64url');
    return decoded;
}

function validFingerprint(value) {
    return typeof value === 'string' && /^[0-9a-f]{64}$/.test(value);
}

function challengeMessage(challenge, proofKind) {
    if (!challenge || !Number.isSafeInteger(challenge.auth_version) || challenge.auth_version <= 0) {
        throw new Error('invalid challenge auth_version');
    }
    decodeBase64URL(challenge.id, 22);
    decodeBase64URL(challenge.nonce, 43);
    const version = String(challenge.auth_version);
    switch (proofKind) {
        case 'login':
            if (challenge.purpose !== 'LOGIN' || !validFingerprint(challenge.key_fingerprint) || challenge.new_key_fingerprint) throw new Error('login proof does not match challenge');
            return `xirang-control-panel-login-v1\n${challenge.id}\n${challenge.nonce}\n${version}\n${challenge.key_fingerprint}`;
        case 'bootstrap':
            if (challenge.purpose !== 'BOOTSTRAP' || challenge.key_fingerprint || !validFingerprint(challenge.new_key_fingerprint)) throw new Error('bootstrap proof does not match challenge');
            return `xirang-control-panel-bootstrap-v1\n${challenge.id}\n${challenge.nonce}\n${version}\n${challenge.new_key_fingerprint}`;
        case 'key_rotate':
            if (challenge.purpose !== 'KEY_ROTATE' || !validFingerprint(challenge.key_fingerprint) || !validFingerprint(challenge.new_key_fingerprint)) throw new Error('key rotation proof does not match challenge');
            return `xirang-control-panel-key-rotate-v1\n${challenge.id}\n${challenge.nonce}\n${version}\n${challenge.key_fingerprint}\n${challenge.new_key_fingerprint}`;
        case 'new_key':
            if (challenge.purpose !== 'KEY_ROTATE' || !validFingerprint(challenge.key_fingerprint) || !validFingerprint(challenge.new_key_fingerprint)) throw new Error('new key proof does not match challenge');
            return `xirang-control-panel-new-key-proof-v1\n${challenge.id}\n${challenge.nonce}\n${version}\n${challenge.new_key_fingerprint}`;
        default:
            throw new Error('unknown proof kind');
    }
}

function equalBytes(left, right) {
    if (left.length !== right.length) return false;
    for (let i = 0; i < left.length; i++) {
        if (left[i] !== right[i]) return false;
    }
    return true;
}

export async function generatePrivateKeyPem() {
    requireSecureRandom();
    const { secretKey } = p256.keygen();
    try {
        return encodePem('PRIVATE KEY', encodePrivateKey(secretKey));
    } finally {
        secretKey.fill(0);
    }
}

export function generateRandomUUID() {
    requireSecureRandom();
    const bytes = globalThis.crypto.getRandomValues(new Uint8Array(16));
    bytes[6] = (bytes[6] & 0x0f) | 0x40;
    bytes[8] = (bytes[8] & 0x3f) | 0x80;
    const hexValue = Array.from(bytes, (byte) => byte.toString(16).padStart(2, '0')).join('');
    return `${hexValue.slice(0, 8)}-${hexValue.slice(8, 12)}-${hexValue.slice(12, 16)}-${hexValue.slice(16, 20)}-${hexValue.slice(20)}`;
}

export function derivePublicKeyPem(privatePem) {
    requireSecureRandom();
    const { secretKey, publicKey } = parsePrivateKey(privatePem);
    try {
        return encodePem('PUBLIC KEY', encodeSPKI(publicKey));
    } finally {
        secretKey.fill(0);
    }
}

export async function fingerprintPublicKeyPem(publicPem) {
    const { der } = parsePublicKey(publicPem);
    return Array.from(sha256(der), (byte) => byte.toString(16).padStart(2, '0')).join('');
}

export async function signChallenge(privatePem, challenge, proofKind) {
    requireSecureRandom();
    const { secretKey } = parsePrivateKey(privatePem);
    try {
        const message = utf8.encode(challengeMessage(challenge, proofKind));
        const digest = sha256(message);
        const signature = p256.sign(digest, secretKey, { prehash: false, lowS: true, extraEntropy: false, format: 'compact' });
        if (signature.length !== 64) throw new Error('P-256 signature must be 64 bytes');
        return encodeBase64URL(signature);
    } finally {
        secretKey.fill(0);
    }
}

export function verifyChallenge(publicPem, message, encodedSignature) {
    try {
        const publicKey = parsePublicKey(publicPem).point;
        const signature = decodeBase64URL(encodedSignature, 86);
        const digest = sha256(utf8.encode(message));
        return p256.verify(signature, digest, publicKey, { prehash: false, lowS: false, format: 'compact' });
    } catch {
        return false;
    }
}

export function buildChallengeMessage(challenge, proofKind) {
    return challengeMessage(challenge, proofKind);
}
