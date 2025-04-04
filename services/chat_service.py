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
        Guarda la respuesta de la IA en la tabla chat_messages y actualiza el historial.

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
        db.session.add(ai_message)

        # Verificar si el chat ya está en el historial
        chat_history = ChatHistory.query.filter_by(chat_id=chat_id).first()
        if not chat_history:
            # Si no está en el historial, agregarlo
            new_history = ChatHistory(chat_id=chat_id)
            db.session.add(new_history)

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
        Crea un nuevo chat en la tabla chats y lo registra en el historial.

        :param title: Título del nuevo chat.
        :return: Diccionario con los detalles del chat creado.
        """
        # Crear una nueva instancia de Chat
        new_chat = Chat(
            title=title
        )

        # Agregar el nuevo chat a la sesión de la base de datos
        db.session.add(new_chat)
        db.session.commit()  # Confirmar para obtener el chat_id

        # Crear una entrada en el historial para el nuevo chat
        new_history = ChatHistory(
            chat_id=new_chat.chat_id
        )
        db.session.add(new_history)
        db.session.commit()

        return {
            "chat_id": new_chat.chat_id,
            "title": new_chat.title,
            "created_at": new_chat.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_chat_messages(self, chat_id):
        """
        Obtiene los mensajes de un chat específico.

        :param chat_id: ID del chat cuyos mensajes se desean obtener.
        :return: Lista de diccionarios con los mensajes del chat.
        """
        # Consultar los mensajes del chat
        messages = ChatMessage.query.filter_by(chat_id=chat_id).order_by(ChatMessage.sent_at).all()

        # Formatear los resultados en una lista de diccionarios
        message_list = []
        for message in messages:
            message_list.append({
                "message_id": message.message_id,
                "chat_id": message.chat_id,
                "sender": message.sender,
                "message_text": message.message_text,
                "sent_at": message.sent_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        return message_list