"""
Entry point for the simplest application structure, ever.

"""

from bookapp import create_app

if __name__ == "__main__":
    app = create_app()
    app.run()
