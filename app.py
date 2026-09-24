from flask import Flask, request, jsonify
from database import init_db
from routes import api
from logger import setup_logger

app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api")
logger = setup_logger()

@app.route("/")
def home():
    return jsonify({
        "application": "Python Expense Tracker",
        "status": "running",
        "message": "Expense Tracker API is running"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    init_db()
    logger.info("Expense Tracker started")
    app.run(debug=True)
