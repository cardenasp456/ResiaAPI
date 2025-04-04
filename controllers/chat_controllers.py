from flask import Blueprint, jsonify
from services.chat_service import ChatService

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

    return jsonify(messages), 200