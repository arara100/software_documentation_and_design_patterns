import sys
import os

# Ensure project root is on the path when running this file directly.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask
from flask_restx import Api

from infrastructure.config import Config
from infrastructure.database import init_db, create_all_tables
from presentation.api.routes import register_namespaces

# ---------------------------------------------------------------------------
# App & Swagger setup
# ---------------------------------------------------------------------------

app = Flask(__name__)
app.config["DEBUG"] = Config.DEBUG

api = Api(
    app,
    version="1.0",
    title="Project Planning API",
    description=(
        "Three-tier REST API for the Project Planning System.\n\n"
        "**Architecture**\n"
        "- Data Access Layer: SQLAlchemy ORM + CSV reader\n"
        "- Business Logic Layer: services depend on DAL *interfaces* (IoC / DI)\n"
        "- Presentation Layer: Flask-RESTX endpoints (controllers defined via interfaces)"
    ),
    doc="/swagger",
)

init_db(Config.DATABASE_URL)
create_all_tables()

register_namespaces(api)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=Config.DEBUG)
