
import { useEffect, useState } from "react";
import { fetchAPI } from "../services/api";

function ManageReservations() {
    const [reservations, setReservations] = useState([]);
    const [message, setMessage] = useState("");

    const loadReservations = async () => {
        try {
            const data = await fetchAPI("/api/reservations/");
            setReservations(Array.isArray(data) ? data : []);
            setMessage("");
        } catch (error) {
            setMessage(error.message);
        }
    };

    useEffect(() => {
        loadReservations();
    }, []);

    const updateStatus = async (id, status) => {
        try {
            await fetchAPI(`/api/reservations/${id}`, {
                method: "PUT",
                body: JSON.stringify({ status })
            });

            setMessage("Reservation status updated successfully!");
            loadReservations();
        } catch (error) {
            setMessage(error.message);
        }
    };

    const deleteReservation = async (id) => {
        if (!window.confirm("Are you sure you want to delete this reservation?")) {
            return;
        }

        try {
            await fetchAPI(`/api/reservations/${id}`, {
                method: "DELETE"
            });

            setMessage("Reservation deleted successfully!");
            loadReservations();
        } catch (error) {
            setMessage(error.message);
        }
    };

    return (
        <div className="page-container">
            <h1>Manage Reservations</h1>
            <p>View and manage customer table reservations.</p>

            {message && <p>{message}</p>}

            <h2>Total Reservations: {reservations.length}</h2>

            <div style={{ overflowX: "auto" }}>
                <table>
                    <thead>
                        <tr>
                            <th>Reservation ID</th>
                            <th>Customer</th>
                            <th>Date</th>
                            <th>Time</th>
                            <th>Guests</th>
                            <th>Status</th>
                            <th>Update Status</th>
                            <th>Action</th>
                        </tr>
                    </thead>

                    <tbody>
                        {reservations.map((reservation) => {
                            const id = reservation.id || reservation._id;

                            return (
                                <tr key={id}>
                                    <td>{id}</td>
                                    <td>{reservation.customer_name || reservation.user_id || "Customer"}</td>
                                    <td>{reservation.date || "N/A"}</td>
                                    <td>{reservation.time || "N/A"}</td>
                                    <td>{reservation.guests || reservation.number_of_guests || 0}</td>
                                    <td>{reservation.status || "Pending"}</td>
                                    <td>
                                        <select
                                            value={reservation.status || "Pending"}
                                            onChange={(e) =>
                                                updateStatus(id, e.target.value)
                                            }
                                        >
                                            <option value="Pending">Pending</option>
                                            <option value="Confirmed">Confirmed</option>
                                            <option value="Completed">Completed</option>
                                            <option value="Cancelled">Cancelled</option>
                                        </select>
                                    </td>
                                    <td>
                                        <button onClick={() => deleteReservation(id)}>
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>

            {reservations.length === 0 && !message && (
                <p>No reservations available.</p>
            )}
        </div>
    );
}

export default ManageReservations;
