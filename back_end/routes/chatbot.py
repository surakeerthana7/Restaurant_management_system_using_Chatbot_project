
from fastapi import APIRouter, HTTPException
from datetime import datetime

from database import chatbot_collection, menu_collection
from models.chatbot_message import ChatbotMessageCreate

router = APIRouter()


# Get available food items from MongoDB
def get_menu_items():
    return list(menu_collection.find({"available": True}))


# Generate chatbot response
def get_bot_response(message):
    text = message.lower().strip()
    foods = get_menu_items()

    if not text:
        return "Please enter a message so I can help you."

    # Greeting
    if any(word in text for word in ["hello", "hi", "hey", "good morning", "good evening"]):
        return (
            "Hello! Welcome to Foodie Restaurant! 😊\n"
            "I am your restaurant assistant. I can help you explore our menu, "
            "find food by price, recommend dishes, and guide you with orders "
            "and reservations. What would you like?"
        )

    # Show complete menu
    if "menu" in text or "food items" in text or "what do you have" in text:
        if not foods:
            return "Our menu is currently empty. Please check again later."

        reply = "Here are some items available in our restaurant:\n\n"

        for food in foods[:20]:
            reply += (
                f"🍽️ {food.get('name', 'Food')}"
                f" - ₹{food.get('price', 0)}\n"
            )

        if len(foods) > 20:
            reply += "\nVisit the Menu page to see all our food items."

        return reply

    # Food recommendations by budget
    if any(word in text for word in ["under", "below", "budget", "cheap", "affordable"]):
        import re

        numbers = re.findall(r"\d+", text)

        if numbers:
            budget = int(numbers[0])

            matching = [
                food for food in foods
                if float(food.get("price", 0)) <= budget
            ]

            if matching:
                reply = f"Here are some foods available under ₹{budget}:\n\n"

                for food in matching[:10]:
                    reply += (
                        f"🍽️ {food.get('name')} - "
                        f"₹{food.get('price')}\n"
                    )

                return reply

            return f"Sorry, we don't have food items under ₹{budget} right now."

        return "Please tell me your budget. For example: Suggest food under 200."

    # Vegetarian recommendations
    if any(word in text for word in ["vegetarian", "veg food", "veg dishes"]):
        veg_items = [
            food for food in foods
            if any(word in food.get("name", "").lower()
                   for word in ["veg", "paneer", "mushroom", "gobi",
                                "dosa", "idli", "pulao", "chana",
                                "corn", "kofta"])
        ]

        if veg_items:
            return "Here are some vegetarian options:\n\n" + "\n".join(
                f"🥗 {food.get('name')} - ₹{food.get('price')}"
                for food in veg_items[:10]
            )

        return "Please check our Menu page for vegetarian options."

    # Non-vegetarian recommendations
    if any(word in text for word in ["non veg", "non-veg", "chicken", "mutton", "fish", "prawn"]):
        nonveg_items = [
            food for food in foods
            if any(word in food.get("name", "").lower()
                   for word in ["chicken", "mutton", "fish", "prawn", "egg"])
        ]

        if nonveg_items:
            return "Here are our non-vegetarian options:\n\n" + "\n".join(
                f"🍗 {food.get('name')} - ₹{food.get('price')}"
                for food in nonveg_items[:10]
            )

        return "Sorry, no non-vegetarian items are currently available."

    # Search for a particular food item
    for food in foods:
        food_name = food.get("name", "").lower()

        if food_name and food_name in text:
            return (
                f"Yes! We have {food.get('name')}.\n"
                f"Description: {food.get('description', 'Delicious food')}\n"
                f"Price: ₹{food.get('price')}\n"
                "Would you like to order it? You can add it from our Menu page."
            )

    # Category questions
    if "starter" in text:
        category = "Starters"
    elif "biryani" in text:
        category = "Biryani"
    elif "dessert" in text or "sweet" in text:
        category = "Desserts"
    elif "drink" in text or "juice" in text or "beverage" in text:
        category = "Beverages"
    elif "rice" in text or "noodles" in text:
        category = "Rice and Noodles"
    else:
        category = None

    if category:
        items = [
            food for food in foods
            if food.get("category", "").lower() == category.lower()
        ]

        if items:
            return f"Our {category} items are:\n\n" + "\n".join(
                f"🍽️ {food.get('name')} - ₹{food.get('price')}"
                for food in items[:10]
            )

        return f"Sorry, no {category} are currently available."

    # Order assistance
    if "order" in text or "how to buy" in text or "place order" in text:
        return (
            "To place an order:\n"
            "1. Open the Menu page.\n"
            "2. Select your favourite food.\n"
            "3. Add it to your cart.\n"
            "4. Open your cart and continue to checkout.\n\n"
            "I can also help you find food!"
        )

    # Reservation assistance
    if "reservation" in text or "book a table" in text or "table booking" in text:
        return (
            "You can reserve a table through the Reservations page. "
            "Choose your date, time and number of guests."
        )

    # Payment assistance
    if "payment" in text or "pay" in text:
        return (
            "You can check the payment options during checkout. "
            "Please select an available payment method."
        )

    # Delivery assistance
    if "delivery" in text or "deliver" in text:
        return (
            "You can place an order through our Menu and Cart pages. "
            "Delivery details will be shown during checkout."
        )

    # Opening hours
    if "timing" in text or "open" in text or "hours" in text:
        return (
            "Please contact the restaurant for its confirmed opening "
            "and closing hours."
        )

    # Thanks and goodbye
    if "thank" in text:
        return "You're welcome! 😊 Thank you for choosing Foodie Restaurant."

    if "bye" in text:
        return "Goodbye! Have a wonderful day. Visit us again! 😊"

    # Help
    if "help" in text:
        return (
            "I can help you with:\n"
            "🍽️ View menu\n"
            "💰 Find food within your budget\n"
            "🥗 Vegetarian food\n"
            "🍗 Non-vegetarian food\n"
            "📦 Placing orders\n"
            "🪑 Table reservations\n"
            "💳 Payment information\n\n"
            "What would you like to know?"
        )

    return (
        "I'm here to help! 😊 You can ask me questions like:\n\n"
        "• Show me the menu\n"
        "• Suggest food under 200\n"
        "• What vegetarian food do you have?\n"
        "• Show me biryani items\n"
        "• What is the price of Chicken Biryani?\n"
        "• How can I place an order?"
    )


# Send message to chatbot
@router.post("/")
@router.post("/message")
def chat_with_bot(chat: ChatbotMessageCreate):

    if not chat.message or not chat.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    bot_reply = get_bot_response(chat.message)

    chat_data = {
        "user_id": None,
        "session_id": getattr(chat, "session_id", None),
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


# Get chat history
@router.get("/history/{session_id}")
def get_chat_history(session_id: str):

    messages = []

    for chat in chatbot_collection.find(
        {"session_id": session_id}
    ).sort("created_at", 1):

        messages.append({
            "message": chat.get("message", ""),
            "response": chat.get("response", ""),
            "created_at": chat.get("created_at")
        })

    return messages

