import { useState } from "react";
import { fetchAPI } from "../services/api";

function Feedback() {
    const [rating, setRating] = useState(5);
    const [comment, setComment] = useState("");
    const [message, setMessage] = useState("");

    const handleFeedback = async (e) => {
        e.preventDefault();

        try {
            await fetchAPI("/api/feedback/", {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`
                },
                body: JSON.stringify({
                    rating: Number(rating),
                    comment
                })
            });

            setMessage("Thank you for your feedback!");
            setComment("");
        } catch (error) {
            setMessage(error.message);
        }
    };

    return (
        <div className="feedback-page">
            <h1>Share Your Feedback</h1>

            <form onSubmit={handleFeedback}>
                <label>Rating:</label>

                <select
                    value={rating}
                    onChange={(e) => setRating(e.target.value)}
                >
                    <option value="5">5 - Excellent</option>
                    <option value="4">4 - Very Good</option>
                    <option value="3">3 - Good</option>
                    <option value="2">2 - Average</option>
                    <option value="1">1 - Poor</option>
                </select>

                <textarea
                    placeholder="Write your feedback..."
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    required
                />

                <button type="submit">Submit Feedback</button>
            </form>

            <p>{message}</p>
        </div>
    );
}

export default Feedback;