
import { useEffect, useState } from "react";
import { fetchAPI } from "../services/api";

function ManageUsers() {
    const [users, setUsers] = useState([]);
    const [message, setMessage] = useState("");

    const loadUsers = async () => {
        try {
            const data = await fetchAPI("/api/users/");
            setUsers(Array.isArray(data) ? data : []);
            setMessage("");
        } catch (error) {
            setMessage(error.message);
        }
    };

    useEffect(() => {
        loadUsers();
    }, []);

    const updateRole = async (id, role) => {
        try {
            await fetchAPI(`/api/users/${id}`, {
                method: "PUT",
                body: JSON.stringify({ role })
            });

            setMessage("User role updated successfully!");
            loadUsers();
        } catch (error) {
            setMessage(error.message);
        }
    };

    const deleteUser = async (id) => {
        if (!window.confirm("Are you sure you want to delete this user?")) {
            return;
        }

        try {
            await fetchAPI(`/api/users/${id}`, {
                method: "DELETE"
            });

            setMessage("User deleted successfully!");
            loadUsers();
        } catch (error) {
            setMessage(error.message);
        }
    };

    return (
        <div className="page-container">
            <h1>Manage Users</h1>
            <p>View and manage registered restaurant users.</p>

            {message && <p>{message}</p>}

            <h2>Total Users: {users.length}</h2>

            <div style={{ overflowX: "auto" }}>
                <table>
                    <thead>
                        <tr>
                            <th>User ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Update Role</th>
                            <th>Action</th>
                        </tr>
                    </thead>

                    <tbody>
                        {users.map((user) => {
                            const id = user.id || user._id;

                            return (
                                <tr key={id}>
                                    <td>{id}</td>
                                    <td>{user.name || "N/A"}</td>
                                    <td>{user.email || "N/A"}</td>
                                    <td>{user.role || "customer"}</td>
                                    <td>
                                        <select
                                            value={user.role || "customer"}
                                            onChange={(e) =>
                                                updateRole(id, e.target.value)
                                            }
                                        >
                                            <option value="customer">Customer</option>
                                            <option value="admin">Admin</option>
                                            <option value="staff">Staff</option>
                                        </select>
                                    </td>
                                    <td>
                                        <button onClick={() => deleteUser(id)}>
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>

            {users.length === 0 && !message && (
                <p>No registered users available.</p>
            )}
        </div>
    );
}

export default ManageUsers;
