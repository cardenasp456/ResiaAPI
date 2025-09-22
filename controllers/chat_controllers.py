from flask import Blueprint, jsonify
from services.chat_service import ChatService
import json

chat_blueprint = Blueprint('chat', __name__)
chat_service = ChatService()

@chat_blueprint.route('/chat/history', methods=['GET'])
def get_chat_history():
    history = chat_service.get_chat_history()
    return jsonify(history), 200

@chat_blueprint.route('/api/chat/<int:chat_id>/messages', methods=['GET'])
def get_chat_messages(chat_id):
    chat_service = ChatService()
    messages = chat_service.get_chat_messages(chat_id)

    if not messages:
        return jsonify({"message": "No se encontraron mensajes para este chat"}), 404

    # Asegura que no escape acentos (config global recomendada)
    # current_app.config["JSON_AS_ASCII"] = False

    parsed_list = []
    for m in messages:
        raw = (m.get("message_text") or "").strip()
        if (raw.startswith("{") and raw.endswith("}")) or (raw.startswith("[") and raw.endswith("]")):
            try:
                obj = json.loads(raw)
                parsed_list.append(obj)
            except json.JSONDecodeError:
                continue

    if not parsed_list:
        return jsonify({"message": "No hay mensajes con JSON válido"}), 404

    # Si solo hay uno, devuelve el objeto directamente (no lista)
    if len(parsed_list) == 1:
        # Nota: usamos jsonify para respetar headers/UTF-8
        return jsonify(parsed_list[0]), 200

    # Si hay varios, devuelve la lista de JSONs
    return jsonify(parsed_list), 200