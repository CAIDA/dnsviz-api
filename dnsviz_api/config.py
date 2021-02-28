import os

class Config:
    DEBUG=False
    TESTING=False
    USE_TALISMAN=True

    def __repr__(self):
        config_str = "-- Application Config --"
        for key in dir(self):
            if not key.startswith('__'):
                config_str += f'\n{key}: {getattr(self, key)}'
        return config_str


class DevelopmentConfig(Config):
    DEBUG=True
    USE_TALISMAN=False
    APP_MODE="development"


class ProductionConfig(Config):
    APP_MODE="production"