# Import Flask modules
from flask import Flask, jsonify, request
 
# Import JSON module for reading/writing JSON files
import json
 
# Import OS module to check whether files exist
import os
 
# Import sentiment analysis function from ai_module.py
from ai_module import analyze_feedback
 
 
# Create Flask application
app = Flask(__name__)
 
# Inventory database file
DB_FILE = "inventory.json"
 
 
# Create inventory.json if it does not exist
def init_db():
 
    # Check whether the file exists
    if not os.path.exists(DB_FILE):
 
        # Create new file
        with open(DB_FILE, "w", encoding="utf-8") as f:
 
            # Store empty list inside file
            json.dump([], f)
 
 
# Run database initialization
init_db()
 
 
# Home API
@app.route("/")
def home():
 
    # Return welcome message
    return {"message": "Smart Inventory API is running!"}
 
 
# Get all inventory items
@app.route("/inventory", methods=["GET"])
def get_inventory():
 
    # Open inventory file
    with open(DB_FILE, "r", encoding="utf-8") as f:
 
        # Return all inventory data
        return jsonify(json.load(f))
 
 
# Add new inventory item
@app.route("/add", methods=["POST"])
def add_item():
 
    # Read JSON request body
    item = request.get_json()
 
    # Validate request body
    if not isinstance(item, dict):
 
        return jsonify({
            "success": False,
            "message": "Please provide a valid JSON object."
        }), 400
 
    # Load existing inventory data
    with open(DB_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
 
    # Add new item
    data.append(item)
 
    # Save updated inventory data
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
 
    # Return success response
    return jsonify({
        "success": True,
        "message": "Item added!",
        "item": item
    }), 201
 
 
# Sample inventory data stored in memory
inventory_data = [
    {
        "ProductID": "P001",
        "ProductName": "Copper Rod",
        "Stock": 120,
        "Price": 500.0
    },
    {
        "ProductID": "P002",
        "ProductName": "Aluminium Sheet",
        "Stock": 80,
        "Price": 800.0
    }
]
 
 
# API to return sample inventory
@app.route('/sampleinventory', methods=['GET'])
def inventory():
 
    return jsonify(inventory_data)
 
 
# Feedback Sentiment Analysis API
@app.route("/feedback", methods=["POST"])
def feedback():
 
    # Read JSON request body safely
    data = request.get_json(silent=True)
 
    # Check whether valid JSON was provided
    if not isinstance(data, dict):
 
        return jsonify({
            "error": "Provide valid JSON"
        }), 400
 
    # Get feedback text from JSON
    feedback_text = data.get("feedback", "")
 
    # Validate feedback text
    if not isinstance(feedback_text, str) or not feedback_text.strip():
 
        return jsonify({
            "error": "Feedback text is required"
        }), 400
 
    # Analyze sentiment using TextBlob
    sentiment = analyze_feedback(feedback_text)
 
    # Return feedback and sentiment score
    return jsonify({
        "feedback": feedback_text,
        "sentiment_score": sentiment
    })
 
 
# Start Flask server
if __name__ == "__main__":
 
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False
    )