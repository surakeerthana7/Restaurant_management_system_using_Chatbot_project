import { useEffect, useState } from "react";
import { fetchAPI } from "../services/api";

function Profile() {
    const [profile, setProfile] = useState(null);
    const [message, setMessage] = useState("Loading profile...");

    useEffect(() => {
        const loadProfile = async () => {
            try {
                const data = await fetchAPI("/api/users/me", {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`
                    }
                });

                setProfile(data);
                setMessage("");
            } catch (error) {
                setMessage(error.message);
            }
        };

        loadProfile();
    }, []);

    return (
        <div className="profile-page">
            <h1>My Profile</h1>

            {message && <p>{message}</p>}

            {profile && (
                <div className="profile-card">
                    <h3>{profile.name}</h3>
                    <p>Email: {profile.email}</p>
                    <p>Role: {profile.role}</p>
                </div>
            )}
        </div>
    );
}

export default Profile;