import json
from models.chat_model import Chat
from models.chatHistory_model import ChatHistory
from models.chatMessage_model import ChatMessage
from database import db

class ChatService:

    def get_chat_history(self):
        """
        Obtiene el historial de chats guardados.
        """
        # Consultar el historial de chats con los datos del chat relacionado
        chat_history = db.session.query(ChatHistory, Chat).join(Chat, ChatHistory.chat_id == Chat.chat_id).all()

        # Formatear los resultados en una lista de diccionarios
        history_list = []
        for history, chat in chat_history:
            history_list.append({
                "history_id": history.history_id,
                "chat_id": chat.chat_id,
                "title": chat.title,
                "saved_at": history.saved_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        return history_list
    
    def save_ai_response(self, chat_id, message_text):
        """
        Guarda la respuesta de la IA en la tabla chat_messages.

        :param chat_id: ID del chat al que pertenece la respuesta.
        :param message_text: Contenido del mensaje generado por la IA (puede ser un diccionario).
        """
        # Convertir el mensaje a una cadena si es un diccionario
        if isinstance(message_text, dict):
            message_text = json.dumps(message_text, ensure_ascii=False)

        # Crear un nuevo mensaje en la tabla chat_messages
        ai_message = ChatMessage(
            chat_id=chat_id,
            sender="IA",  # Indicar que el remitente es la IA
            message_text=message_text
        )

        # Agregar el mensaje a la sesión de la base de datos
        db.session.add(ai_message)

        # Confirmar los cambios en la base de datos
        db.session.commit()

        return {
            "message_id": ai_message.message_id,
            "chat_id": ai_message.chat_id,
            "sender": ai_message.sender,
            "message_text": ai_message.message_text,
            "sent_at": ai_message.sent_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def create_new_chat(self, title):
        """
        Crea un nuevo chat en la tabla chats.

        :param title: Título del nuevo chat.
        :return: Diccionario con los detalles del chat creado.
        """
        # Crear una nueva instancia de Chat
        new_chat = Chat(
            title=title
        )

        # Agregar el nuevo chat a la sesión de la base de datos
        db.session.add(new_chat)

        # Confirmar los cambios en la base de datos
        db.session.commit()

        return {
            "chat_id": new_chat.chat_id,
            "title": new_chat.title,
            "created_at": new_chat.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }