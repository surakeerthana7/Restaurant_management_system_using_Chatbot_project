import { useEffect, useState } from "react";
import { fetchAPI } from "../services/api";

function MyOrders() {
    const [orders, setOrders] = useState([]);
    const [message, setMessage] = useState("Loading orders...");

    useEffect(() => {
        const loadOrders = async () => {
            try {
                const data = await fetchAPI("/api/orders/");
                setOrders(Array.isArray(data) ? data : []);
                setMessage("");
            } catch (error) {
                setMessage(error.message);
            }
        };

        loadOrders();
    }, []);

    return (
        <div className="orders-page">
            <h1>My Orders</h1>

            {message && <p>{message}</p>}

            {orders.map((order) => (
                <div className="order-card" key={order._id}>
                    <h3>Order ID: {order._id}</h3>
                    <p>Status: {order.status}</p>
                    <p>Total: ₹{order.total_amount}</p>
                </div>
            ))}

            {!message && orders.length === 0 && (
                <p>You have no orders yet.</p>
            )}
        </div>
    );
}

export default MyOrders;