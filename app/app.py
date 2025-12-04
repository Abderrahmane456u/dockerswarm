from flask import Flask
import os

app = Flask(__name__)


def read_secret(path="/run/secrets/app_secret"):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception:
        return "(no secret)"


@app.route("/")
def index():
    hostname = os.getenv("HOSTNAME")
    secret = read_secret()
    return f"Hello from Docker Swarm! Container: {hostname} | secret={secret}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
