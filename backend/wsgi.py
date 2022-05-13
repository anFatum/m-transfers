from app import create_app

from app.configs import get_config
import os

application = create_app(get_config(config=os.getenv("ENV", "prod")))
