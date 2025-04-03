from flask import Blueprint, jsonify
from services.chat_service import ChatService

chat_blueprint = Blueprint('chat', __name__)
chat_service = ChatService()

@chat_blueprint.route('/chat/history', methods=['GET'])
def get_chat_history():
    history = chat_service.get_chat_history()
    return jsonify(history), 200