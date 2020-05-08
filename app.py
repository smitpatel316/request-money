from flask import Flask

from controllers.event import event
from controllers.user import user

app = Flask(__name__)


@app.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    header["Access-Control-Allow-Headers"] = "*"
    header["Access-Control-Allow-Methods"] = "*"
    return response


@app.route("/")
def index():
    return "Service is running!"


app.register_blueprint(user)
app.register_blueprint(event)

if __name__ == "__main__":
    app.run(debug=True)
