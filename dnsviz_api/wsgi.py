import os

from dotenv import load_dotenv

import config
from dnsviz_api.app import create_app

load_dotenv()

if os.getenv('FLASK_ENV') == "development":
    app_config = config.DevelopmentConfig()
else:
    app_config = config.Config()

app = create_app(app_config)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)