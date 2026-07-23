import requests
from requests.exceptions import SSLError

def safe_request_with_self_signed_cert():
    try:
        response = requests.get(
            'https://ct-global.ctapi.ctyun.local:40117/v4/vpc/list',
            verify='ca.crt',
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    except SSLError as e:
        print(f"SSL 错误: {e}")
        # 可以在这里添加重试逻辑或降级处理

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")

    return None

if __name__ == '__main__':
    # 使用示例
    result = safe_request_with_self_signed_cert()