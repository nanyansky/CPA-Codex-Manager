"""
配置管理 - 完全基于数据库存储
所有配置都从数据库读取，不再使用环境变量或 .env 文件
"""

import os
from typing import Optional, Dict, Any, Type, List
from enum import Enum
from pydantic import BaseModel, field_validator
from pydantic.types import SecretStr
from dataclasses import dataclass
from ..app_meta import APP_NAME, APP_VERSION


class SettingCategory(str, Enum):
    """设置分类"""
    GENERAL = "general"
    DATABASE = "database"
    WEBUI = "webui"
    LOG = "log"
    OPENAI = "openai"
    PROXY = "proxy"
    REGISTRATION = "registration"
    EMAIL = "email"
    TEMPMAIL = "tempmail"
    CUSTOM_DOMAIN = "moe_mail"
    SECURITY = "security"
    CPA = "cpa"
    NOTIFY = "notify"


@dataclass
class SettingDefinition:
    """设置定义"""
    db_key: str
    default_value: Any
    category: SettingCategory
    description: str = ""
    is_secret: bool = False


# 所有配置项定义（包含数据库键名、默认值、分类、描述）
SETTING_DEFINITIONS: Dict[str, SettingDefinition] = {
    # 应用信息
    "app_name": SettingDefinition(
        db_key="app.name",
        default_value=APP_NAME,
        category=SettingCategory.GENERAL,
        description="应用名称"
    ),
    "app_version": SettingDefinition(
        db_key="app.version",
        default_value=APP_VERSION,
        category=SettingCategory.GENERAL,
        description="应用版本"
    ),
    "debug": SettingDefinition(
        db_key="app.debug",
        default_value=False,
        category=SettingCategory.GENERAL,
        description="调试模式"
    ),

    # 数据库配置
    "database_url": SettingDefinition(
        db_key="database.url",
        default_value="data/database.db",
        category=SettingCategory.DATABASE,
        description="数据库路径或连接字符串"
    ),

    # Web UI 配置
    "webui_host": SettingDefinition(
        db_key="webui.host",
        default_value="0.0.0.0",
        category=SettingCategory.WEBUI,
        description="Web UI 监听地址"
    ),
    "webui_port": SettingDefinition(
        db_key="webui.port",
        default_value=8000,
        category=SettingCategory.WEBUI,
        description="Web UI 监听端口"
    ),
    "webui_secret_key": SettingDefinition(
        db_key="webui.secret_key",
        default_value="your-secret-key-change-in-production",
        category=SettingCategory.WEBUI,
        description="Web UI 密钥",
        is_secret=True
    ),
    "webui_access_password": SettingDefinition(
        db_key="webui.access_password",
        default_value="admin123",
        category=SettingCategory.WEBUI,
        description="Web UI 访问密码",
        is_secret=True
    ),

    # 日志配置
    "log_level": SettingDefinition(
        db_key="log.level",
        default_value="INFO",
        category=SettingCategory.LOG,
        description="日志级别"
    ),
    "log_file": SettingDefinition(
        db_key="log.file",
        default_value="logs/app.log",
        category=SettingCategory.LOG,
        description="日志文件路径"
    ),
    "log_retention_days": SettingDefinition(
        db_key="log.retention_days",
        default_value=30,
        category=SettingCategory.LOG,
        description="日志保留天数"
    ),

    # OpenAI 配置
    "openai_client_id": SettingDefinition(
        db_key="openai.client_id",
        default_value="app_EMoamEEZ73f0CkXaXp7hrann",
        category=SettingCategory.OPENAI,
        description="OpenAI OAuth 客户端 ID"
    ),
    "openai_auth_url": SettingDefinition(
        db_key="openai.auth_url",
        default_value="https://auth.openai.com/oauth/authorize",
        category=SettingCategory.OPENAI,
        description="OpenAI OAuth 授权 URL"
    ),
    "openai_token_url": SettingDefinition(
        db_key="openai.token_url",
        default_value="https://auth.openai.com/oauth/token",
        category=SettingCategory.OPENAI,
        description="OpenAI OAuth Token URL"
    ),
    "openai_redirect_uri": SettingDefinition(
        db_key="openai.redirect_uri",
        default_value="http://localhost:1455/auth/callback",
        category=SettingCategory.OPENAI,
        description="OpenAI OAuth 回调 URI"
    ),
    "openai_scope": SettingDefinition(
        db_key="openai.scope",
        default_value="openid email profile offline_access",
        category=SettingCategory.OPENAI,
        description="OpenAI OAuth 权限范围"
    ),

    # 代理配置
    "proxy_enabled": SettingDefinition(
        db_key="proxy.enabled",
        default_value=False,
        category=SettingCategory.PROXY,
        description="是否启用代理"
    ),
    "proxy_type": SettingDefinition(
        db_key="proxy.type",
        default_value="http",
        category=SettingCategory.PROXY,
        description="代理类型 (http/socks5)"
    ),
    "proxy_host": SettingDefinition(
        db_key="proxy.host",
        default_value="127.0.0.1",
        category=SettingCategory.PROXY,
        description="代理服务器地址"
    ),
    "proxy_port": SettingDefinition(
        db_key="proxy.port",
        default_value=7890,
        category=SettingCategory.PROXY,
        description="代理服务器端口"
    ),
    "proxy_username": SettingDefinition(
        db_key="proxy.username",
        default_value="",
        category=SettingCategory.PROXY,
        description="代理用户名"
    ),
    "proxy_password": SettingDefinition(
        db_key="proxy.password",
        default_value="",
        category=SettingCategory.PROXY,
        description="代理密码",
        is_secret=True
    ),
    "proxy_dynamic_enabled": SettingDefinition(
        db_key="proxy.dynamic_enabled",
        default_value=False,
        category=SettingCategory.PROXY,
        description="是否启用动态代理"
    ),
    "proxy_dynamic_api_url": SettingDefinition(
        db_key="proxy.dynamic_api_url",
        default_value="",
        category=SettingCategory.PROXY,
        description="动态代理 API 地址，返回代理 URL 字符串"
    ),
    "proxy_dynamic_api_key": SettingDefinition(
        db_key="proxy.dynamic_api_key",
        default_value="",
        category=SettingCategory.PROXY,
        description="动态代理 API 密钥（可选）",
        is_secret=True
    ),
    "proxy_dynamic_api_key_header": SettingDefinition(
        db_key="proxy.dynamic_api_key_header",
        default_value="X-API-Key",
        category=SettingCategory.PROXY,
        description="动态代理 API 密钥请求头名称"
    ),
    "proxy_dynamic_result_field": SettingDefinition(
        db_key="proxy.dynamic_result_field",
        default_value="",
        category=SettingCategory.PROXY,
        description="从 JSON 响应中提取代理 URL 的字段路径（留空则使用响应原文）"
    ),

    # 注册配置
    "registration_max_retries": SettingDefinition(
        db_key="registration.max_retries",
        default_value=3,
        category=SettingCategory.REGISTRATION,
        description="注册最大重试次数"
    ),
    "registration_timeout": SettingDefinition(
        db_key="registration.timeout",
        default_value=120,
        category=SettingCategory.REGISTRATION,
        description="注册超时时间（秒）"
    ),
    "registration_default_password_length": SettingDefinition(
        db_key="registration.default_password_length",
        default_value=12,
        category=SettingCategory.REGISTRATION,
        description="默认密码长度"
    ),
    "registration_sleep_min": SettingDefinition(
        db_key="registration.sleep_min",
        default_value=5,
        category=SettingCategory.REGISTRATION,
        description="注册间隔最小值（秒）"
    ),
    "registration_sleep_max": SettingDefinition(
        db_key="registration.sleep_max",
        default_value=30,
        category=SettingCategory.REGISTRATION,
        description="注册间隔最大值（秒）"
    ),
    "registration_check_ip_location": SettingDefinition(
        db_key="registration.check_ip_location",
        default_value=True,
        category=SettingCategory.REGISTRATION,
        description="注册前是否检查 IP 地理位置"
    ),

    # 邮箱服务配置
    "email_service_priority": SettingDefinition(
        db_key="email.service_priority",
        default_value={"tempmail": 0, "moe_mail": 1},
        category=SettingCategory.EMAIL,
        description="邮箱服务优先级"
    ),

    # Tempmail.lol 配置
    "tempmail_base_url": SettingDefinition(
        db_key="tempmail.base_url",
        default_value="https://api.tempmail.lol/v2",
        category=SettingCategory.TEMPMAIL,
        description="Tempmail API 地址"
    ),
    "tempmail_timeout": SettingDefinition(
        db_key="tempmail.timeout",
        default_value=30,
        category=SettingCategory.TEMPMAIL,
        description="Tempmail 超时时间（秒）"
    ),
    "tempmail_max_retries": SettingDefinition(
        db_key="tempmail.max_retries",
        default_value=3,
        category=SettingCategory.TEMPMAIL,
        description="Tempmail 最大重试次数"
    ),

    # 自定义域名邮箱配置
    "custom_domain_base_url": SettingDefinition(
        db_key="custom_domain.base_url",
        default_value="",
        category=SettingCategory.CUSTOM_DOMAIN,
        description="自定义域名 API 地址"
    ),
    "custom_domain_api_key": SettingDefinition(
        db_key="custom_domain.api_key",
        default_value="",
        category=SettingCategory.CUSTOM_DOMAIN,
        description="自定义域名 API 密钥",
        is_secret=True
    ),

    # 安全配置
    "encryption_key": SettingDefinition(
        db_key="security.encryption_key",
        default_value="your-encryption-key-change-in-production",
        category=SettingCategory.SECURITY,
        description="加密密钥",
        is_secret=True
    ),

    # Team Manager 配置
    "tm_enabled": SettingDefinition(
        db_key="tm.enabled",
        default_value=False,
        category=SettingCategory.GENERAL,
        description="是否启用 Team Manager 上传"
    ),
    "tm_api_url": SettingDefinition(
        db_key="tm.api_url",
        default_value="",
        category=SettingCategory.GENERAL,
        description="Team Manager API 地址"
    ),
    "tm_api_key": SettingDefinition(
        db_key="tm.api_key",
        default_value="",
        category=SettingCategory.GENERAL,
        description="Team Manager API Key",
        is_secret=True
    ),

    # Telegram 通知配置
    "tg_notify_enabled": SettingDefinition(
        db_key="notify.telegram.enabled",
        default_value=False,
        category=SettingCategory.NOTIFY,
        description="是否启用 Telegram 通知"
    ),
    "tg_bot_token": SettingDefinition(
        db_key="notify.telegram.bot_token",
        default_value="",
        category=SettingCategory.NOTIFY,
        description="Telegram Bot Token",
        is_secret=True
    ),
    "tg_chat_id": SettingDefinition(
        db_key="notify.telegram.chat_id",
        default_value="",
        category=SettingCategory.NOTIFY,
        description="Telegram Chat ID"
    ),

    # CPA 上传配置
    "cpa_enabled": SettingDefinition(
        db_key="cpa.enabled",
        default_value=False,
        category=SettingCategory.CPA,
        description="是否启用 CPA 上传"
    ),
    "cpa_api_url": SettingDefinition(
        db_key="cpa.api_url",
        default_value="",
        category=SettingCategory.CPA,
        description="CPA API 地址"
    ),
    "cpa_api_token": SettingDefinition(
        db_key="cpa.api_token",
        default_value="",
        category=SettingCategory.CPA,
        description="CPA API Token",
        is_secret=True
    ),

    # 验证码配置
    "email_code_timeout": SettingDefinition(
        db_key="email_code.timeout",
        default_value=30,
        category=SettingCategory.EMAIL,
        description="验证码等待超时时间（秒）"
    ),
    "email_code_poll_interval": SettingDefinition(
        db_key="email_code.poll_interval",
        default_value=3,
        category=SettingCategory.EMAIL,
        description="验证码轮询间隔（秒）"
    ),

}

# 属性名到数据库键名的映射（用于向后兼容）
DB_SETTING_KEYS = {name: defn.db_key for name, defn in SETTING_DEFINITIONS.items()}

# 类型定义映射
SETTING_TYPES: Dict[str, Type] = {
    "debug": bool,
    "webui_port": int,
    "log_retention_days": int,
    "proxy_enabled": bool,
    "proxy_port": int,
    "proxy_dynamic_enabled": bool,
    "registration_max_retries": int,
    "registration_timeout": int,
    "registration_default_password_length": int,
    "registration_sleep_min": int,
    "registration_sleep_max": int,
    "registration_check_ip_location": bool,
    "email_service_priority": dict,
    "tempmail_timeout": int,
    "tempmail_max_retries": int,
    "tm_enabled": bool,
    "cpa_enabled": bool,
    "email_code_timeout": int,
    "email_code_poll_interval": int,
    "tg_notify_enabled": bool,
}

# 需要作为 SecretStr 处理的字段
SECRET_FIELDS = {name for name, defn in SETTING_DEFINITIONS.items() if defn.is_secret}


def _convert_value(attr_name: str, value: str) -> Any:
    """将数据库字符串值转换为正确的类型"""
    if value is None:
        return None

    target_type = SETTING_TYPES.get(attr_name, str)

    if target_type == bool:
        return value.lower() in ("true", "1", "yes", "on")
    elif target_type == int:
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0
    elif target_type == float:
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    elif target_type in (dict, list):
        try:
            import json
            return json.loads(value)
        except (ValueError, TypeError, json.JSONDecodeError):
            return {} if target_type == dict else []
    else:
        return value


def _serialize_value(value: Any) -> str:
    """将值序列化为字符串以便存储到数据库"""
    if value is None:
        return ""
    elif isinstance(value, SecretStr):
        return value.get_secret_value()
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, (dict, list)):
        import json
        return json.dumps(value, ensure_ascii=False)
    else:
        return str(value)


def _load_settings_from_db() -> Dict[str, Any]:
    """从数据库加载所有设置"""
    from ..database.session import get_db
    from ..database import crud

    # 先使用默认值初始化
    settings_dict = {
        attr_name: definition.default_value
        for attr_name, definition in SETTING_DEFINITIONS.items()
    }

    try:
        with get_db() as db:
            for attr_name, definition in SETTING_DEFINITIONS.items():
                db_key = definition.db_key
                db_setting = crud.get_setting(db, db_key)
                if db_setting is not None:
                    raw_value = db_setting.value
                    converted_value = _convert_value(attr_name, raw_value)
                    settings_dict[attr_name] = converted_value
    except Exception as e:
        print(f"Warning: Failed to load settings from database: {e}")
        # 如果数据库读取失败，使用默认值

    return settings_dict


def _save_settings_to_db(**kwargs):
    """保存设置到数据库"""
    from ..database.session import get_db
    from ..database import crud

    try:
        with get_db() as db:
            for attr_name, value in kwargs.items():
                if attr_name in DB_SETTING_KEYS:
                    db_key = DB_SETTING_KEYS[attr_name]
                    serialized_value = _serialize_value(value)
                    crud.set_setting(db, db_key, serialized_value)
    except Exception as e:
        raise RuntimeError(f"Failed to save settings to database: {e}")


def init_default_settings():
    """初始化默认设置到数据库（如果不存在）"""
    from ..database.session import get_db
    from ..database import crud

    try:
        with get_db() as db:
            for attr_name, definition in SETTING_DEFINITIONS.items():
                db_key = definition.db_key
                existing = crud.get_setting(db, db_key)
                if existing is None:
                    default_value = _serialize_value(definition.default_value)
                    crud.set_setting(db, db_key, default_value, category=definition.category.value, description=definition.description)
    except Exception as e:
        print(f"Warning: Failed to initialize default settings: {e}")


class Settings(BaseModel):
    """应用配置模型 - 完全基于数据库"""

    # 应用信息
    app_name: str = APP_NAME
    app_version: str = APP_VERSION
    debug: bool = False

    # 数据库配置
    database_url: str = "data/database.db"

    # Web UI 配置
    webui_host: str = "0.0.0.0"
    webui_port: int = 8000
    webui_secret_key: SecretStr = SecretStr("your-secret-key-change-in-production")
    webui_access_password: SecretStr = SecretStr("admin123")

    # 日志配置
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    log_retention_days: int = 30

    # OpenAI OAuth 配置
    openai_client_id: str = "app_EMoamEEZ73f0CkXaXp7hrann"
    openai_auth_url: str = "https://auth.openai.com/oauth/authorize"
    openai_token_url: str = "https://auth.openai.com/oauth/token"
    openai_redirect_uri: str = "http://localhost:1455/auth/callback"
    openai_scope: str = "openid email profile offline_access"

    # 代理配置
    proxy_enabled: bool = False
    proxy_type: str = "http"
    proxy_host: str = "127.0.0.1"
    proxy_port: int = 7890
    proxy_username: Optional[str] = None
    proxy_password: Optional[SecretStr] = None
    proxy_dynamic_enabled: bool = False
    proxy_dynamic_api_url: str = ""
    proxy_dynamic_api_key: Optional[SecretStr] = None
    proxy_dynamic_api_key_header: str = "X-API-Key"
    proxy_dynamic_result_field: str = ""

    @property
    def proxy_url(self) -> Optional[str]:
        """获取完整的代理 URL"""
        if not self.proxy_enabled:
            return None

        if self.proxy_type == "http":
            scheme = "http"
        elif self.proxy_type == "socks5":
            scheme = "socks5"
        else:
            return None

        auth = ""
        if self.proxy_username and self.proxy_password:
            auth = f"{self.proxy_username}:{self.proxy_password.get_secret_value()}@"

        return f"{scheme}://{auth}{self.proxy_host}:{self.proxy_port}"

    # 注册配置
    registration_max_retries: int = 3
    registration_timeout: int = 120
    registration_default_password_length: int = 12
    registration_sleep_min: int = 5
    registration_sleep_max: int = 30
    registration_check_ip_location: bool = True

    # 邮箱服务配置
    email_service_priority: Dict[str, int] = {"tempmail": 0, "moe_mail": 1}

    # Tempmail.lol 配置
    tempmail_base_url: str = "https://api.tempmail.lol/v2"
    tempmail_timeout: int = 30
    tempmail_max_retries: int = 3

    # 自定义域名邮箱配置
    custom_domain_base_url: str = ""
    custom_domain_api_key: Optional[SecretStr] = None

    # 安全配置
    encryption_key: SecretStr = SecretStr("your-encryption-key-change-in-production")

    # Team Manager 配置
    tm_enabled: bool = False
    tm_api_url: str = ""
    tm_api_key: Optional[SecretStr] = None

    # Telegram 通知配置
    tg_notify_enabled: bool = False
    tg_bot_token: Optional[SecretStr] = None
    tg_chat_id: str = ""

    # CPA 上传配置
    cpa_enabled: bool = False
    cpa_api_url: str = ""
    cpa_api_token: SecretStr = SecretStr("")

    # 验证码配置
    email_code_timeout: int = 30
    email_code_poll_interval: int = 3

# 全局配置实例
_settings: Optional[Settings] = None


def _apply_runtime_env_overrides(settings_dict: Dict[str, Any]) -> Dict[str, Any]:
    """仅对运行时通知通道保留环境变量兜底，不写回数据库。"""
    merged = dict(settings_dict)

    if not merged.get("tg_bot_token"):
        merged["tg_bot_token"] = os.environ.get("TG_BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN") or ""
    if not merged.get("tg_chat_id"):
        merged["tg_chat_id"] = os.environ.get("TG_CHAT_ID") or os.environ.get("TELEGRAM_CHAT_ID") or ""

    return merged


def get_settings() -> Settings:
    """
    获取全局配置实例（单例模式）
    完全从数据库加载配置
    """
    global _settings
    if _settings is None:
        # 先初始化默认设置（如果数据库中没有的话）
        init_default_settings()
        # 从数据库加载所有设置
        settings_dict = _apply_runtime_env_overrides(_load_settings_from_db())
        _settings = Settings(**settings_dict)
    return _settings


def update_settings(**kwargs) -> Settings:
    """
    更新配置并保存到数据库
    """
    global _settings
    if _settings is None:
        _settings = get_settings()

    # 创建新的配置实例
    updated_data = _settings.model_dump()
    updated_data.update(kwargs)
    updated_data = _apply_runtime_env_overrides(updated_data)
    _settings = Settings(**updated_data)

    # 保存到数据库
    _save_settings_to_db(**kwargs)

    return _settings


def get_database_url() -> str:
    """
    获取数据库 URL（处理相对路径）
    """
    settings = get_settings()
    url = settings.database_url

    # 如果 URL 是相对路径，转换为绝对路径
    if url.startswith("sqlite:///"):
        path = url[10:]  # 移除 "sqlite:///"
        if not os.path.isabs(path):
            # 转换为相对于项目根目录的路径
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            abs_path = os.path.join(project_root, path)
            return f"sqlite:///{abs_path}"

    return url


def get_setting_definition(attr_name: str) -> Optional[SettingDefinition]:
    """获取设置项的定义信息"""
    return SETTING_DEFINITIONS.get(attr_name)


def get_all_setting_definitions() -> Dict[str, SettingDefinition]:
    """获取所有设置项的定义"""
    return SETTING_DEFINITIONS.copy()
