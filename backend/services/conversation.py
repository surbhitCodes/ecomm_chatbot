"""
Maintain conversaional view of chats
"""
import uuid

conversations = {}          # could use redis too later


def create_session():
    """
    Creates a new session
    """
    session_id = str(uuid.uuid4())
    conversations[session_id] = []
    return session_id


def add_to_conversation(session_id: str, message: str):
    """
    Adds a message to the conversation
    """
    if session_id not in conversations:
        conversations[session_id] = []
    conversations[session_id].append(message)


def get_conversation(session_id: str):
    """
    Getter for the conversation
    """
    return conversations.get(session_id, [])
