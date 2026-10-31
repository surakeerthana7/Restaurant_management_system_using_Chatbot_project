import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { fetchAPI } from "../services/api";

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const data = await fetchAPI("/api/auth/login", {
                method: "POST",
                body: JSON.stringify({ email, password })
            });

            localStorage.setItem("token", data.access_token);
            setMessage("Login successful!");
            navigate("/menu");
        } catch (error) {
            setMessage(error.message);
        }
    };

    return (
        <div className="auth-page">
            <form className="auth-form" onSubmit={handleLogin}>
                <h2>Login</h2>

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

                <button type="submit">Login</button>

                <p>{message}</p>

                <p>
                    Don't have an account? <Link to="/register">Register</Link>
                </p>
            </form>
        </div>
    );
}

export default Login;