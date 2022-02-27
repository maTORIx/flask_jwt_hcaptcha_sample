from flask import current_app
from flask_wtf import RecaptchaField
from .validator import Hcaptcha

HCAPTCHA_VERIFY_SERVER = "https://hcaptcha.com/siteverify"
HCAPTCHA_SCRIPT = "https://js.hcaptcha.com/1/api.js"
HCAPTCHA_DIV_CLASS = "h-captcha"


def set_config():
    if current_app.config.get("HCAPTCHA_CONFIG_SETUP_FINISHED", False):
        return

    SITE_KEY = current_app.config.get("HCAPTCHA_SITE_KEY", None)
    SECRET_KEY = current_app.config.get("HCAPTCHA_SECRET_KEY", None)
    if SITE_KEY is None:
        raise RuntimeError("No HCAPTCHA_SITE_KEY config set")
    elif SECRET_KEY is None:
        raise RuntimeError("No HCAPTCHA_SECRET_KEY config set")

    current_app.config["RECAPTCHA_PUBLIC_KEY"] = SITE_KEY
    current_app.config["RECAPTCHA_PRIVATE_KEY"] = SECRET_KEY
    current_app.config["RECAPTCHA_VERIFY_SERVER"] = HCAPTCHA_VERIFY_SERVER
    current_app.config["RECAPTCHA_SCRIPT"] = HCAPTCHA_SCRIPT
    current_app.config["RECAPTCHA_DIV_CLASS"] = HCAPTCHA_DIV_CLASS
    current_app.config["HCAPTCHA_CONFIG_SETUP_FINISHED"] = True


class HcaptchaField(RecaptchaField):
    def __init__(self, label="", validators=None, **kwargs):
        set_config()
        validators = validators or [Hcaptcha()]
        super().__init__(label, validators, **kwargs)
