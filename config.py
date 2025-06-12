class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+mysqlconnector://root:test@localhost/repair_shop_db"
    )
    DEBUG = True
    CACH_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300


class TestingConfig:
    pass


class ProductionConfig:
    pass
