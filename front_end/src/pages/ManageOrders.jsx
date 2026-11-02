
import { useEffect, useState } from "react";
import { fetchAPI } from "../services/api";

function ManageOrders() {
    const [orders, setOrders] = useState([]);
    const [message, setMessage] = useState("");

    const loadOrders = async () => {
        try {
            const data = await fetchAPI("/api/orders/");
            setOrders(Array.isArray(data) ? data : []);
            setMessage("");
        } catch (error) {
            setMessage(error.message);
        }
    };

    useEffect(() => {
        loadOrders();
    }, []);

    const updateStatus = async (id, status) => {
        try {
            await fetchAPI(`/api/orders/${id}`, {
                method: "PUT",
                body: JSON.stringify({ status })
            });

            setMessage("Order status updated successfully!");
            loadOrders();
        } catch (error) {
            setMessage(error.message);
        }
    };

    const deleteOrder = async (id) => {
        if (!window.confirm("Are you sure you want to delete this order?")) {
            return;
        }

        try {
            await fetchAPI(`/api/orders/${id}`, {
                method: "DELETE"
            });

            setMessage("Order deleted successfully!");
            loadOrders();
        } catch (error) {
            setMessage(error.message);
        }
    };

    return (
        <div className="page-container">
            <h1>Manage Orders</h1>
            <p>View and manage customer orders.</p>

            {message && <p>{message}</p>}

            <h2>Total Orders: {orders.length}</h2>

            <div style={{ overflowX: "auto" }}>
                <table>
                    <thead>
                        <tr>
                            <th>Order ID</th>
                            <th>Customer</th>
                            <th>Total Amount</th>
                            <th>Status</th>
                            <th>Update Status</th>
                            <th>Action</th>
                        </tr>
                    </thead>

                    <tbody>
                        {orders.map((order) => (
                            <tr key={order.id || order._id}>
                                <td>{order.id || order._id}</td>
                                <td>{order.customer_name || order.user_id || "Customer"}</td>
                                <td>₹{order.total_amount || order.total || 0}</td>
                                <td>{order.status || "Pending"}</td>
                                <td>
                                    <select
                                        value={order.status || "Pending"}
                                        onChange={(e) =>
                                            updateStatus(
                                                order.id || order._id,
                                                e.target.value
                                            )
                                        }
                                    >
                                        <option value="Pending">Pending</option>
                                        <option value="Confirmed">Confirmed</option>
                                        <option value="Preparing">Preparing</option>
                                        <option value="Ready">Ready</option>
                                        <option value="Delivered">Delivered</option>
                                        <option value="Cancelled">Cancelled</option>
                                    </select>
                                </td>
                                <td>
                                    <button
                                        onClick={() =>
                                            deleteOrder(order.id || order._id)
                                        }
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {orders.length === 0 && !message && (
                <p>No orders available.</p>
            )}
        </div>
    );
}

export default ManageOrders;
