import { useState } from "react";
import { fetchAPI } from "../services/api";

function OrderTracking() {
    const [orderId, setOrderId] = useState("");
    const [order, setOrder] = useState(null);
    const [message, setMessage] = useState("");

    const trackOrder = async (e) => {
        e.preventDefault();

        try {
            const data = await fetchAPI(`/api/orders/${orderId}`);
            setOrder(data);
            setMessage("");
        } catch (error) {
            setOrder(null);
            setMessage(error.message);
        }
    };

    return (
        <div className="tracking-page">
            <h1>Track Your Order</h1>

            <form onSubmit={trackOrder}>
                <input
                    type="text"
                    placeholder="Enter Order ID"
                    value={orderId}
                    onChange={(e) => setOrderId(e.target.value)}
                    required
                />

                <button type="submit">Track Order</button>
            </form>

            {order && (
                <div className="order-card">
                    <h3>Order Details</h3>
                    <p>Order ID: {order._id}</p>
                    <p>Status: {order.status}</p>
                    <p>Total: ₹{order.total_amount}</p>
                </div>
            )}

            {message && <p>{message}</p>}
        </div>
    );
}

export default OrderTracking;