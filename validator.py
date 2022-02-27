from flask_wtf.recaptcha.validators import Recaptcha, RECAPTCHA_ERROR_CODES
from flask import current_app, request
from wtforms import ValidationError
import urllib.parse
import urllib.request
import json


class Hcaptcha(Recaptcha):
    def __call__(self, form, field):
        if current_app.testing:
            return True

        if request.json:
            response = request.json.get("h-captcha-response", "")
        else:
            response = request.form.get("h-captcha-response", "")
        remote_ip = request.remote_addr

        if not response:
            raise ValidationError(field.gettext(self.message))

        if not self._validate_recaptcha(response, remote_ip):
            field.recaptcha_error = "incorrect-captcha-sol"
            raise ValidationError(field.gettext(self.message))

    def _validate_recaptcha(self, response, remote_addr):
        """Performs the actual validation."""
        try:
            private_key = current_app.config["RECAPTCHA_PRIVATE_KEY"]
        except KeyError:
            raise RuntimeError("No RECAPTCHA_PRIVATE_KEY config set") from None

        verify_server = current_app.config.get("RECAPTCHA_VERIFY_SERVER")
        if not verify_server:
            raise ValidationError("No RECAPTCHA_VALIDATION_SERVER config set.")

        data = urllib.parse.urlencode(
            {"secret": private_key, "remoteip": remote_addr, "response": response}
        ).encode("utf-8")
        http_response = urllib.request.urlopen(verify_server, data)

        if http_response.code != 200:
            return False

        json_resp = json.loads(http_response.read())

        if json_resp["success"]:
            return True

        for error in json_resp.get("error-codes", []):
            if error in RECAPTCHA_ERROR_CODES:
                raise ValidationError(RECAPTCHA_ERROR_CODES[error])

        return False
