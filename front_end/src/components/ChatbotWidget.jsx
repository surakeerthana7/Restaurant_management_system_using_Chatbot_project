import { useState } from "react";
import { fetchAPI } from "../services/api";

function ChatbotWidget() {
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([
        {
            sender: "bot",
            text: "Hello! Welcome to Foodie Restaurant. How can I help you?"
        }
    ]);

    const sendMessage = async (e) => {
        e.preventDefault();

        if (!message.trim()) return;

        const userMessage = message;

        setMessages((prev) => [
            ...prev,
            { sender: "user", text: userMessage }
        ]);

        setMessage("");

        try {
            const data = await fetchAPI("/api/chatbot/", {
                method: "POST",
                body: JSON.stringify({ message: userMessage })
            });

            setMessages((prev) => [
                ...prev,
                {
                    sender: "bot",
                    text: data.response || data.reply || "Sorry, I couldn't understand."
                }
            ]);
        } catch (error) {
            setMessages((prev) => [
                ...prev,
                { sender: "bot", text: error.message }
            ]);
        }
    };

    return (
        <div className="chatbot">
            <h3>Restaurant Assistant</h3>

            <div className="chat-messages">
                {messages.map((msg, index) => (
                    <p key={index} className={msg.sender}>
                        <strong>{msg.sender === "bot" ? "Bot: " : "You: "}</strong>
                        {msg.text}
                    </p>
                ))}
            </div>

            <form onSubmit={sendMessage}>
                <input
                    type="text"
                    placeholder="Ask something..."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                />

                <button type="submit">Send</button>
            </form>
        </div>
    );
}

export default ChatbotWidget;