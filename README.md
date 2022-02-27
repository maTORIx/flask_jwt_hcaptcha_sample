# Flask WTF hcaptcha field sample

Sample hcaptcha field inherited from recaptcha field, intended for use with flask_jwt.

It works by setting "HCAPTCHA_SITE_KEY" and "HCAPTCHA_SECRET_KEY" in the config of your flask application.
Like this
```
from flask import Flask
app = Flask(__name__)
app.config["HCAPTCHA_SITE_KEY"] = "YOUR_SITE_KEY"
app.config["HCAPTCHA_SECRET_KEY"] = "YOUR_SECRET_KEY"
```

Note: If you use this code as is, RECAPTCHA_PUBLIC_KEY will be overwritten by HCAPTCHA_SITE_KEY, and the recaptcha field will not work properly.
