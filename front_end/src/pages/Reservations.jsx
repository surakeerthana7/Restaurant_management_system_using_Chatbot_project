import { useState } from "react";
import { fetchAPI } from "../services/api";

function Reservations() {
    const [form, setForm] = useState({
        table_id: "",
        reservation_date: "",
        guest_count: 1
    });

    const [message, setMessage] = useState("");

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleReservation = async (e) => {
        e.preventDefault();

        try {
            await fetchAPI("/api/reservations/", {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`
                },
                body: JSON.stringify({
                    ...form,
                    guest_count: Number(form.guest_count)
                })
            });

            setMessage("Reservation successful!");
        } catch (error) {
            setMessage(error.message);
        }
    };

    return (
        <div className="reservation-page">
            <h1>Table Reservation</h1>

            <form onSubmit={handleReservation}>
                <input
                    name="table_id"
                    placeholder="Enter Table ID"
                    value={form.table_id}
                    onChange={handleChange}
                    required
                />

                <input
                    type="datetime-local"
                    name="reservation_date"
                    value={form.reservation_date}
                    onChange={handleChange}
                    required
                />

                <input
                    type="number"
                    name="guest_count"
                    min="1"
                    value={form.guest_count}
                    onChange={handleChange}
                    required
                />

                <button type="submit">Book Table</button>
            </form>

            <p>{message}</p>
        </div>
    );
}

export default Reservations;