# used to display information on a website 
# information includes latency test, speed test and traffic monitor
from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__, template_folder="templates")

LOG_FILE = "logs.json"

'''
Function to load the latest log data
@ret: dict containing the most recent network stats
'''
def get_logs():
    try:
        if not os.path.exists(LOG_FILE):
            return {}
        
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)
            if logs:
                # Return latest entry
                return logs[-1]
            
    except Exception as e:
        print(f"[ERROR] Failed to load logs: {e}")
    # Empty data if error
    return {}

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/data")
def get_data():
    return jsonify(get_logs())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
