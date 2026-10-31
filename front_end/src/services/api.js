const API_URL = "http://127.0.0.1:8000";

export async function fetchAPI(endpoint, options = {}) {
    const response = await fetch(`${API_URL}${endpoint}`, {
        headers: {
            "Content-Type": "application/json",
            ...options.headers
        },
        ...options
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Something went wrong");
    }

    return data;
}