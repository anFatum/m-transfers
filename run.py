from app.configs import get_config
from app import create_app


if __name__ == '__main__':
    cfg = get_config("dev")
    app = create_app(cfg)
    app.run(debug=cfg.DEBUG)
