from flaskApp import create_app
from flaskApp.config import Config

app = create_app()
if __name__ == '__main__':

    app.run()


