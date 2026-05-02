from flask import Flask
from app.routes import api
from webcam.camera import run_webcam
from utils.db import init_db
from app.dashboard import dashboard, stats, timeline
import threading

app = Flask(__name__)

# API
app.register_blueprint(api)

# Dashboard routes
app.add_url_rule('/dashboard', 'dashboard', dashboard)
app.add_url_rule('/stats', 'stats', stats)
app.add_url_rule('/timeline', 'timeline', timeline)


def run_flask():
    app.run(host='0.0.0.0', port=5001)


if __name__ == "__main__":
    init_db()

    threading.Thread(target=run_flask).start()
    run_webcam()
