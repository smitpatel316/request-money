from flask import Flask

from controllers.event import event
from controllers.user import user

app = Flask(__name__)


@app.route("/")
def index():
    return "Service is running!"


app.register_blueprint(user)
app.register_blueprint(event)

if __name__ == "__main__":
    app.run(debug=True)
