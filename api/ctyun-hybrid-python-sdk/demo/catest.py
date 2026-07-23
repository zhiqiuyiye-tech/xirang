import re
import tempfile
import os


def fix_certificate_format(cert_path):
    """修复证书格式问题"""

    with open(cert_path, 'r') as f:
        original_content = f.read()

    print("原始内容:")
    print(original_content[:500])

    # 修复步骤
    content = original_content

    # 1. 去除多余空格和空行
    content = re.sub(r'\r\n', '\n', content)  # 统一换行符
    content = re.sub(r'\n\s*\n', '\n', content)  # 去除空行
    content = content.strip()

    # 2. 确保有正确的PEM头尾
    if not content.startswith('-----BEGIN'):
        # 尝试找到证书开始位置
        begin_match = re.search(r'-----BEGIN[^-]*-----', content)
        if begin_match:
            content = content[begin_match.start():]
        else:
            content = '-----BEGIN CERTIFICATE-----\n' + content

    if not content.endswith('-----END CERTIFICATE-----'):
        # 尝试找到证书结束位置
        end_match = re.search(r'-----END[^-]*-----', content)
        if end_match:
            content = content[:end_match.end()]
        else:
            content = content + '\n-----END CERTIFICATE-----'

    # 3. 确保Base64内容格式正确
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        line = line.strip()
        if line and not line.startswith('-----'):
            # 确保每行是64字符（PEM标准）
            if len(line) > 64:
                # 长行分割
                for i in range(0, len(line), 64):
                    fixed_lines.append(line[i:i + 64])
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    content = '\n'.join(fixed_lines)

    # 创建临时修复文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.crt') as f:
        f.write(content)
        fixed_path = f.name

    print("修复后内容:")
    print(content[:500])
    print(f"✅ 修复文件保存到: {fixed_path}")

    return fixed_path


# 使用修复后的证书
if __name__ == '__main__':
    try:
        fixed_cert_path = fix_certificate_format('/Users/lishijun/Documents/pythonworkspace/ctyun-hybrid-python-sdk/demo/ca.crt')

        import requests

        response = requests.get('https://ct-global.ctapi-internal.ctyun.local:40117', verify=fixed_cert_path)
        print(f"✅ 请求成功: {response.status_code}")

        # 清理临时文件
        os.unlink(fixed_cert_path)

    except Exception as e:
        print(f"❌ 仍然失败: {e}")