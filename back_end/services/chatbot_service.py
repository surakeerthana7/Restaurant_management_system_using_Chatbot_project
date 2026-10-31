
# Restaurant Chatbot Service

def generate_response(message: str):

    message = message.lower().strip()

    # Greeting
    if any(word in message for word in ["hello", "hi", "hey"]):
        return "Hello! Welcome to our restaurant. How can I help you?"

    # Menu Questions
    elif "menu" in message or "food" in message:
        return "You can explore our restaurant menu to see all available food items."

    # Price Questions
    elif "price" in message or "cost" in message:
        return "Please check the menu section to see the prices of our food items."

    # Order Questions
    elif "order" in message:
        return "You can place your food order through our online ordering system."

    # Reservation Questions
    elif "reservation" in message or "table" in message:
        return "You can reserve a restaurant table through the Reservations section."

    # Payment Questions
    elif "payment" in message or "pay" in message:
        return "We support Cash, UPI, and Card payment options."

    # Delivery Questions
    elif "delivery" in message:
        return "You can select the delivery option while placing your order."

    # Feedback Questions
    elif "feedback" in message or "review" in message:
        return "You can share your experience through our Feedback section."

    # Opening Hours
    elif "timing" in message or "hours" in message:
        return "Please contact our restaurant for the latest opening hours."

    # Thank You
    elif "thank" in message:
        return "You're welcome! Thank you for choosing our restaurant."

    # Goodbye
    elif "bye" in message:
        return "Goodbye! We hope to see you again."

    # Default Response
    else:
        return (
            "Sorry, I couldn't understand your question. "
            "You can ask me about food, menu, orders, "
            "reservations, payments, or delivery."
        )
