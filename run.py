from settings import development, production
from todo import create_app

app = create_app(development, production)

if __name__ == "__main__":
    app.run()
