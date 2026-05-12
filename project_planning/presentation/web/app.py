import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, redirect, url_for
from infrastructure.config import Config
from infrastructure.database import init_db, create_all_tables
from presentation.web.controllers import register_blueprints

# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")
app.config["DEBUG"] = Config.DEBUG

init_db(Config.DATABASE_URL)
create_all_tables()

register_blueprints(app)


@app.route("/")
def home():
    return redirect(url_for("projects.index"))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001, debug=Config.DEBUG)
