from fastapi import Request
from app.controllers.v1.base import new_router
from app.utils import utils

# 认证依赖项
# router = new_router(dependencies=[Depends(base.verify_token)])
router = new_router()


@router.get("/manifest.json")
def get_manifest_json(request: Request):
    return {
        "schema_version": "v1",
        "display_name": "MoneyPrinterTurbo",
        "namespace": 'monkey_tools_money_printer_turbo',
        "auth": {
            "type": "none"
        },
        "api": {
            "type": "openapi",
            "url": "/openapi.json"
        },
        "contact_email": "dev@inf-monkeys.com",
    }
