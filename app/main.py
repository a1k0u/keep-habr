from flask import Flask
import json

from app.api.view import api

app = Flask(__name__)
app.register_blueprint(api)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
