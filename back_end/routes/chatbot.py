
from fastapi import APIRouter, HTTPException
from datetime import datetime

from database import chatbot_collection
from models.chatbot_message import ChatbotMessageCreate

router = APIRouter()


# Basic Chatbot Responses
def get_bot_response(message: str):

    message = message.lower().strip()

    if any(word in message for word in ["hello", "hi", "hey"]):
        return "Hello! Welcome to our restaurant. How can I help you?"

    elif "menu" in message:
        return "You can explore our food menu on the Menu page."

    elif "price" in message or "cost" in message:
        return "You can check food prices in our Menu section."

    elif "order" in message:
        return "You can place your food order through the Orders section."

    elif "reservation" in message or "table" in message:
        return "You can book a table through the Reservations section."

    elif "payment" in message or "pay" in message:
        return "We support Cash, UPI, and Card payment options."

    elif "timing" in message or "hours" in message:
        return "Please contact our restaurant for today's opening hours."

    elif "location" in message or "address" in message:
        return "Please contact our restaurant for the exact address."

    elif "thank" in message:
        return "You're welcome! Thank you for choosing our restaurant."

    elif "bye" in message:
        return "Goodbye! Visit us again."

    else:
        return (
            "Sorry, I couldn't understand your question. "
            "You can ask me about our menu, orders, reservations, or payments."
        )


# Send Message to Chatbot
@router.post("/message")
def chat_with_bot(chat: ChatbotMessageCreate):

    if not chat.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    bot_reply = get_bot_response(chat.message)

    chat_data = {
        "user_id": None,  # Will be replaced with logged-in user ID
        "session_id": chat.session_id,
        "message": chat.message,
        "response": bot_reply,
        "sender": "customer",
        "created_at": datetime.utcnow()
    }

    chatbot_collection.insert_one(chat_data)

    return {
        "message": chat.message,
        "response": bot_reply
    }


# Get Chat History
@router.get("/history/{session_id}")
def get_chat_history(session_id: str):

    messages = []

    for chat in chatbot_collection.find(
        {"session_id": session_id}
    ).sort("created_at", 1):

        messages.append({
            "message": chat["message"],
            "response": chat["response"],
            "created_at": chat["created_at"]
        })

    return messages
