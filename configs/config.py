from pathlib import Path


class TestConfig(object):
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 12
    MAIL_FROM_EMAIL = "test@example.com"    # Even though the email system will not be set up
    SECRET_KEY = "imaginarycryptic2ey"
    # TODO: Would never EVER! use sqlite in production!
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{str(Path(__file__).parent.parent / "bookrequests.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# TODO: Would be in a separate untracked file
class ProductionConfig(TestConfig):
    # Override where necessary
    DEBUG = False
    TESTING = False
