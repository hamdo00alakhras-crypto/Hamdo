const BASE_URL = "http://localhost:8000";

function getAuthToken() {
    return localStorage.getItem("access_token");
}

function setAuthToken(token) {
    localStorage.setItem("access_token", token);
}

function isLoggedIn() {
    return !!getAuthToken();
}

function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_data");
    window.location.href = "login.html";
}

async function apiRequest(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            "Content-Type": "application/json",
        },
    };

    if (isLoggedIn()) {
        defaultOptions.headers["Authorization"] = `Bearer ${getAuthToken()}`;
    }

    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers,
        },
    };

    if (mergedOptions.body && typeof mergedOptions.body === "object") {
        mergedOptions.body = JSON.stringify(mergedOptions.body);
    }

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, mergedOptions);
        const data = await response.json();

        if (!response.ok) {
            throw { status: response.status, ...data };
        }

        return data;
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
}

async function login(username, password) {
    const response = await fetch(`${BASE_URL}/api/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (!response.ok) {
        throw data;
    }

    setAuthToken(data.access_token);
    return data;
}

async function register(userData) {
    return apiRequest("/api/auth/register", {
        method: "POST",
        body: userData,
    });
}

async function getCurrentUser() {
    return apiRequest("/api/auth/me");
}

async function getProducts(filters = {}) {
    const params = new URLSearchParams();
    if (filters.category_id) params.append("category_id", filters.category_id);
    if (filters.material) params.append("material", filters.material);
    if (filters.min_price) params.append("min_price", filters.min_price);
    if (filters.max_price) params.append("max_price", filters.max_price);
    if (filters.karat) params.append("karat", filters.karat);

    const queryString = params.toString();
    return apiRequest(`/api/products/${queryString ? "?" + queryString : ""}`);
}

async function getProduct(productId) {
    return apiRequest(`/api/products/${productId}`);
}

async function getCategories() {
    return apiRequest("/api/products/categories/");
}

async function getCart() {
    return apiRequest("/api/cart/");
}

async function addToCart(productId, quantity = 1) {
    return apiRequest("/api/cart/add", {
        method: "POST",
        body: { product_id: productId, quantity },
    });
}

async function updateCartItem(itemId, quantity) {
    return apiRequest(`/api/cart/update/${itemId}?quantity=${quantity}`, {
        method: "PUT",
    });
}

async function removeFromCart(itemId) {
    return apiRequest(`/api/cart/remove/${itemId}`, {
        method: "DELETE",
    });
}

async function clearCart() {
    return apiRequest("/api/cart/clear", {
        method: "DELETE",
    });
}

async function getOrders() {
    return apiRequest("/api/orders/");
}

async function checkout(orderData) {
    return apiRequest("/api/orders/checkout", {
        method: "POST",
        body: orderData,
    });
}

async function generateDesign(designData) {
    return apiRequest("/api/ai/generate-design", {
        method: "POST",
        body: designData,
    });
}

async function getMyDesigns() {
    return apiRequest("/api/ai/my-designs");
}

function formatPrice(price) {
    return new Intl.NumberFormat("ar-SA", {
        style: "currency",
        currency: "SAR",
    }).format(price);
}

function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="loading-spinner">جاري التحميل...</div>';
    }
}

function showError(message) {
    alert("خطأ: " + message);
}

function showSuccess(message) {
    alert(message);
}
