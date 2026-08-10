{{/*
Common labels
*/}}
{{- define "control-panel.labels" -}}
app.kubernetes.io/name: control-panel
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "control-panel.selectorLabels" -}}
app.kubernetes.io/name: control-panel
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
secretValue returns the value for a Secret key, preserving stability across
upgrades. Priority:
  1. .Values.secrets.<key> if pinned (caller passes it non-empty)
  2. the existing deployed Secret's value (lookup) - so upgrades reuse the
     value generated on first install instead of regenerating it
  3. a freshly generated random value (first install, or the key was missing)
Regenerating on upgrade would break admin login (the password retrievable from
the Secret would no longer match the bcrypt hash seeded once into the DB) and
rotate AES_KEY/JWT (invalidating encrypted worker creds + sessions). lookup
returns empty during `helm template` and on first install. We use hasKey so a
Secret that exists but is missing the key falls back to a fresh gen instead of
rendering an empty string (which would crash the pod on the required-env check).
Usage: include "control-panel.secretValue" (dict "Release" .Release "key" "AES_KEY" "pinned" .Values.secrets.aesKey "gen" (randBytes 32 | b64enc))
*/}}
{{- define "control-panel.secretValue" -}}
{{- $v := . -}}
{{- if $v.pinned -}}
{{- $v.pinned -}}
{{- else -}}
{{- $existing := lookup "v1" "Secret" $v.Release.Namespace "control-panel-secrets" -}}
{{- if and $existing (hasKey $existing.data $v.key) -}}
{{- index $existing.data $v.key -}}
{{- else -}}
{{- $v.gen -}}
{{- end -}}
{{- end -}}
{{- end -}}
