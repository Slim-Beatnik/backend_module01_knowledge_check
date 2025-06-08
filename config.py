class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+mysqlconnector://root:test@localhost/repair_shop_db"
    )
    DEBUG = True


class TestingConfig:
    pass


class ProductionConfig:
    pass
