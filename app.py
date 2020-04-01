from bookapp import create_app
from configs.config import TestConfig

if __name__ == "__main__":
    app = create_app(TestConfig)
    app.run()
