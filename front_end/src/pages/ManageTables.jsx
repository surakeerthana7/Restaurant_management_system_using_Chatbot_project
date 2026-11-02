
import { useEffect, useState } from "react";
import { fetchAPI } from "../services/api";

function ManageTables() {
    const [tables, setTables] = useState([]);
    const [message, setMessage] = useState("");

    const [form, setForm] = useState({
        table_number: "",
        capacity: "",
        status: "Available"
    });

    const loadTables = async () => {
        try {
            const data = await fetchAPI("/api/tables/");
            setTables(Array.isArray(data) ? data : []);
            setMessage("");
        } catch (error) {
            setMessage(error.message);
        }
    };

    useEffect(() => {
        loadTables();
    }, []);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const addTable = async (e) => {
        e.preventDefault();

        try {
            await fetchAPI("/api/tables/", {
                method: "POST",
                body: JSON.stringify({
                    ...form,
                    table_number: Number(form.table_number),
                    capacity: Number(form.capacity)
                })
            });

            setMessage("Table added successfully!");
            setForm({
                table_number: "",
                capacity: "",
                status: "Available"
            });
            loadTables();
        } catch (error) {
            setMessage(error.message);
        }
    };

    const updateStatus = async (id, status) => {
        try {
            await fetchAPI(`/api/tables/${id}`, {
                method: "PUT",
                body: JSON.stringify({ status })
            });

            setMessage("Table status updated!");
            loadTables();
        } catch (error) {
            setMessage(error.message);
        }
    };

    const deleteTable = async (id) => {
        if (!window.confirm("Are you sure you want to delete this table?")) {
            return;
        }

        try {
            await fetchAPI(`/api/tables/${id}`, {
                method: "DELETE"
            });

            setMessage("Table deleted successfully!");
            loadTables();
        } catch (error) {
            setMessage(error.message);
        }
    };

    return (
        <div className="page-container">
            <h1>Manage Restaurant Tables</h1>
            <p>Add tables and manage their availability.</p>

            {message && <p>{message}</p>}

            <h2>Add New Table</h2>

            <form onSubmit={addTable}>
                <input
                    type="number"
                    name="table_number"
                    placeholder="Table Number"
                    value={form.table_number}
                    onChange={handleChange}
                    required
                />

                <input
                    type="number"
                    name="capacity"
                    placeholder="Seating Capacity"
                    value={form.capacity}
                    onChange={handleChange}
                    min="1"
                    required
                />

                <select
                    name="status"
                    value={form.status}
                    onChange={handleChange}
                >
                    <option value="Available">Available</option>
                    <option value="Occupied">Occupied</option>
                    <option value="Reserved">Reserved</option>
                </select>

                <button type="submit">Add Table</button>
            </form>

            <h2>Total Tables: {tables.length}</h2>

            <div style={{ overflowX: "auto" }}>
                <table>
                    <thead>
                        <tr>
                            <th>Table Number</th>
                            <th>Capacity</th>
                            <th>Status</th>
                            <th>Update Status</th>
                            <th>Action</th>
                        </tr>
                    </thead>

                    <tbody>
                        {tables.map((table) => {
                            const id = table.id || table._id;

                            return (
                                <tr key={id}>
                                    <td>{table.table_number}</td>
                                    <td>{table.capacity}</td>
                                    <td>{table.status || "Available"}</td>
                                    <td>
                                        <select
                                            value={table.status || "Available"}
                                            onChange={(e) =>
                                                updateStatus(id, e.target.value)
                                            }
                                        >
                                            <option value="Available">Available</option>
                                            <option value="Occupied">Occupied</option>
                                            <option value="Reserved">Reserved</option>
                                        </select>
                                    </td>
                                    <td>
                                        <button onClick={() => deleteTable(id)}>
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>

            {tables.length === 0 && !message && (
                <p>No tables available.</p>
            )}
        </div>
    );
}

export default ManageTables;

