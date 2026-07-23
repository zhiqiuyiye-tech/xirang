from ctyun_hybrid_sdk.core.logger import get_default_logger, INFO, ERROR
from ctyun_hybrid_sdk.core.hybrid_signer import HybridSigner

if __name__ == '__main__':
    logger = get_default_logger()
    signer = HybridSigner(logger)
    access_key="xxx"
    secret_key="xxxx"
    query="page=1&pageSize=10&regionId=cn-north-1"
    header = {
        "test1":"test1",
        "test2":"test2"
    }
    body="{\"key\":\"value\"}"
    signer.sign(query=query, headers=header, body=body, access_key=access_key,secret_key=secret_key)