from flask import Blueprint, jsonify
from api.services.history_service import get_history_data, get_all_symbols_data

history_bp = Blueprint("history", __name__)

@history_bp.route("/history/<symbol>", methods=["GET"])
def get_history(symbol):
    df = get_history_data(symbol)
    if df.empty:
        return jsonify({"status": "error", "message": f"No data found for {symbol.upper()}"}), 404
    return jsonify(df.to_dict(orient="records"))

@history_bp.route("/symbols", methods=["GET"])
def get_symbols():
    return jsonify({"symbols": get_all_symbols_data()})

@history_bp.route("/history/all", methods=["GET"])
def get_all_history():
    from utils.db import get_collection
    collection = get_collection()
    data = list(collection.find({}, {'_id': 0}))
    return jsonify(data)
