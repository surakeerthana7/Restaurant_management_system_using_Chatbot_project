import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { fetchAPI } from "../services/api";

function Register() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();

        try {
            await fetchAPI("/api/auth/register", {
                method: "POST",
                body: JSON.stringify({
                    name,
                    email,
                    password,
                    role: "customer"
                })
            });

            setMessage("Registration successful!");
            navigate("/login");
        } catch (error) {
            setMessage(error.message);
        }
    };

    return (
        <div className="auth-page">
            <form className="auth-form" onSubmit={handleRegister}>
                <h2>Create Account</h2>

                <input
                    type="text"
                    placeholder="Enter Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />

                <input
                    type="email"
                    placeholder="Enter Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />

                <input
                    type="password"
                    placeholder="Enter Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <button type="submit">Register</button>

                <p>{message}</p>

                <p>
                    Already have an account? <Link to="/login">Login</Link>
                </p>
            </form>
        </div>
    );
}

export default Register;