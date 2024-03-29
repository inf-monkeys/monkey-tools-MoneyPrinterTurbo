"""Application implementation - ASGI."""

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from fastapi.staticfiles import StaticFiles

from app.config import config
from app.models.exception import HttpException
from app.router import root_api_router
from app.utils import utils


def exception_handler(request: Request, e: HttpException):
    return JSONResponse(
        status_code=e.status_code,
        content=utils.get_response(e.status_code, e.data, e.message),
    )


def validation_exception_handler(request: Request, e: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=utils.get_response(
            status=400, data=e.errors(), message="field required"
        ),
    )


def get_application() -> FastAPI:
    """Initialize FastAPI application.

    Returns:
       FastAPI: Application object instance.

    """
    instance = FastAPI(
        title=config.project_name,
        description=config.project_description,
        version=config.project_version,
        debug=False,
    )
    instance.include_router(root_api_router)
    instance.add_exception_handler(HttpException, exception_handler)
    instance.add_exception_handler(RequestValidationError, validation_exception_handler)
    return instance


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom API",
        version="1.0.0",
        description="This is a custom API with some extensions",
        routes=app.routes,
    )

    openapi_schema["paths"]["/api/v1/videos"]["post"][
        "x-monkey-tool-name"
    ] = "generate_video_by_moneyprinterturbo"
    openapi_schema["paths"]["/api/v1/videos"]["post"][
        "x-monkey-tool-display-name"
    ] = "MonkeyPrinterTrubo 视频生成"
    openapi_schema["paths"]["/api/v1/videos"]["post"]["x-monkey-tool-categories"] = [
        "video"
    ]
    openapi_schema["paths"]["/api/v1/videos"]["post"][
        "x-monkey-tool-description"
    ] = "只需提供一个视频 主题 或 关键词 ，就可以全自动生成视频文案、视频素材、视频字幕、视频背景音乐，然后合成一个高清的短视频。"
    openapi_schema["paths"]["/api/v1/videos"]["post"][
        "x-monkey-tool-icon"
    ] = "emoji:📷:#98ae36"
    openapi_schema["paths"]["/api/v1/videos"]["post"]["x-monkey-tool-input"] = [
        {
            "displayName": "视频主题",
            "name": "video_subject",
            "type": "string",
            "default": "",
            "required": True,
            "description": "如: 生命的意义是什么",
        },
        {
            "displayName": "视频文案",
            "name": "video_script",
            "type": "string",
            "default": "",
            "description": "视频文案 ①可不填，使用AI生成  ②合理使用标点断句，有助于生成字幕]",
            "required": False,
        },
        {
            "displayName": "视频关键词",
            "name": "video_terms",
            "type": "string",
            "required": False,
            "default": "",
            "description": "视频关键词 ①可不填，使用AI生成 ②用**英文逗号**分隔，只支持英文",
        },
        {
            "displayName": "视频 Aspect Ratio",
            "name": "video_aspect",
            "type": "options",
            "options": [
                {"name": "9:16", "value": "9:16"},
                {"name": "16:9", "value": "16:9"},
                {"name": "1:1", "value": "1:1"},
            ],
            "default": "9:16",
            "required": False,
        },
        {
            "displayName": "视频拼接模式",
            "name": "video_concat_mode",
            "type": "options",
            "default": "random",
            "required": False,
            "options": [
                {"name": "random", "value": "random"},
                {"name": "sequential", "value": "sequential"},
            ],
        },
        {
            "displayName": "视频片段最大时长(秒)",
            "name": "video_clip_duration",
            "type": "options",
            "required": False,
            "default": 3,
            "options": [
                {"name": "2", "value": 2},
                {"name": "3", "value": 3},
                {"name": "4", "value": 4},
                {"name": "5", "value": 5},
                {"name": "6", "value": 6},
            ],
        },
        {
            "displayName": "同时生成视频数量",
            "name": "video_count",
            "type": "options",
            "required": False,
            "default": 1,
            "options": [
                {"name": "1", "value": 1},
                {"name": "2", "value": 2},
                {"name": "3", "value": 3},
                {"name": "4", "value": 4},
                {"name": "5", "value": 5},
            ],
        },
        {
            "displayName": "视频文案语言",
            "name": "video_language",
            "type": "options",
            "required": False,
            "default": "",
            "options": [
                {"name": "自动判断", "value": "auto"},
                {"name": "zh-CN", "value": "zh-CN"},
                {"name": "zh-TW", "value": "zh-TW"},
                {"name": "en-US", "value": "en-US"},
            ],
        },
        {
            "displayName": "朗读声音",
            "name": "voice_name",
            "type": "options",
            "required": False,
            "default": "female-zh-CN-XiaoxiaoNeural",
            "options": [
                {"name": "女性-中文-Xiaoxiao", "value": "female-zh-CN-XiaoxiaoNeural"},
                {"name": "女性-中文-Xiaoyi", "value": "female-zh-CN-XiaoyiNeural"},
                {
                    "name": "女性-中文-liaoning-Xiaobei",
                    "value": "female-zh-CN-liaoning-XiaobeiNeural",
                },
                {
                    "name": "女性-中文-shaanxi-Xiaoni",
                    "value": "female-zh-CN-shaanxi-XiaoniNeural",
                },
                {"name": "男性-中文-Yunjian", "value": "male-zh-CN-YunjianNeural"},
                {"name": "男性-中文-Yunxi", "value": "male-zh-CN-YunxiNeural"},
                {"name": "男性-中文-Yunxia", "value": "male-zh-CN-YunxiaNeural"},
                {"name": "男性-中文-Yunyang", "value": "male-zh-CN-YunyangNeural"},
                {"name": "女性-英文-Ana", "value": "female-en-US-AnaNeural"},
                {"name": "女性-英文-Aria", "value": "female-en-US-AriaNeural"},
                {"name": "女性-英文-Ava", "value": "female-en-US-AvaNeural"},
                {"name": "女性-英文-Emma", "value": "female-en-US-EmmaNeural"},
                {"name": "女性-英文-Jenny", "value": "female-en-US-JennyNeural"},
                {"name": "女性-英文-Michelle", "value": "female-en-US-MichelleNeural"},
                {"name": "男性-英文-Andrew", "value": "male-en-US-AndrewNeural"},
                {"name": "男性-英文-Brian", "value": "male-en-US-BrianNeural"},
                {
                    "name": "男性-英文-Christopher",
                    "value": "male-en-US-ChristopherNeural",
                },
                {"name": "男性-英文-Eric", "value": "male-en-US-EricNeural"},
                {"name": "男性-英文-Guy", "value": "male-en-US-GuyNeural"},
                {"name": "男性-英文-Roger", "value": "male-en-US-RogerNeural"},
                {"name": "男性-英文-Steffan", "value": "male-en-US-SteffanNeural"},
            ],
        },
        {
            "displayName": "背景音乐",
            "name": "bgm_type",
            "type": "options",
            "required": False,
            "default": "",
            "options": [
                {"name": "无背景音乐 No BGM", "value": "none"},
                {"name": "随机背景音乐 Random BGM", "value": "random"},
                {"name": "自定义背景音乐 Custom BGM", "value": "custom"},
            ],
        },
        {
            "displayName": "背景音乐音量",
            "name": "bgm_volume",
            "type": "number",
            "required": False,
            "default": 0.2,
            "description": "0.2表示20%，背景声音不宜过高",
        },
        {
            "displayName": "自定义背景音乐链接",
            "name": "bgm_file",
            "type": "file",
            "required": False,
            "typeOptions": {
                "multipleValues": False,
                "accept": ".mp3",
                "maxSize": 1024 * 1024 * 10,
            },
            "displyaOptions": {"show": {"bgm_type": ["custom"]}},
        },
        {
            "displayName": "是否开启字幕",
            "name": "subtitle_enabled",
            "type": "boolean",
            "required": False,
            "default": False,
        },
        {
            "displayName": "字幕位置",
            "name": "subtitle_position",
            "type": "options",
            "required": False,
            "default": "bottom",
            "options": [
                {"name": "底部（bottom，推荐）", "value": "bottom"},
                {"name": "居中（center）", "value": "center"},
                {"name": "顶部（top）", "value": "top"},
            ],
            "displyaOptions": {"show": {"subtitle_enabled": [True]}},
        },
        {
            "displayName": "字幕字体",
            "name": "font_name",
            "type": "options",
            "required": False,
            "default": "STHeitiLight.ttc",
            "options": [
                {"name": "STHeitiLight.ttc", "value": "STHeitiLight.ttc"},
                {"name": "STHeitiMedium.ttc", "value": "STHeitiMedium.ttc"},
            ],
            "displyaOptions": {"show": {"subtitle_enabled": [True]}},
        },
        {
            "displayName": "字幕颜色",
            "name": "text_fore_color",
            "type": "string",
            "required": False,
            "default": "#FFFFFF",
            "displyaOptions": {"show": {"subtitle_enabled": [True]}},
        },
        {
            "displayName": "字幕背景颜色",
            "name": "text_background_color",
            "type": "string",
            "required": False,
            "default": "transparent",
            "displyaOptions": {"show": {"subtitle_enabled": [True]}},
        },
        {
            "displayName": "字幕大小",
            "name": "font_size",
            "type": "number",
            "required": False,
            "default": 30,
            "displyaOptions": {"show": {"subtitle_enabled": [True]}},
        },
        {
            "displayName": "描边颜色",
            "name": "stroke_color",
            "type": "string",
            "required": False,
            "default": "#000000",
            "displyaOptions": {"show": {"subtitle_enabled": [True]}},
        },
        {
            "displayName": "描边粗细",
            "name": "stroke_width",
            "type": "number",
            "required": False,
            "default": 1.5,
            "displyaOptions": {"show": {"subtitle_enabled": [True]}},
        },
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = get_application()
app.openapi = custom_openapi
public_dir = utils.public_dir()
app.mount("/", StaticFiles(directory=public_dir, html=True), name="")


@app.on_event("shutdown")
def shutdown_event():
    logger.info("shutdown event")


@app.on_event("startup")
def startup_event():
    logger.info("startup event")
