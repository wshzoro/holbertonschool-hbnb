document.addEventListener('DOMContentLoaded', () => {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');

    if (!placeId) {
        alert('Place ID not found in URL.');
        return;
    }

    if (!token) {
        document.getElementById('add-review').style.display = 'none';
    } else {
        document.getElementById('add-review').style.display = 'block';
    }

    fetchPlaceDetails(token, placeId);
});

/**
 * Extract place ID from URL query parameter.
 */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/**
 * Get cookie value by name
 */
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [cName, cValue] = cookie.trim().split('=');
        if (cName === name) return decodeURIComponent(cValue);
    }
    return null;
}

/**
 * Fetch place details from API and display them
 */
async function fetchPlaceDetails(token, placeId) {
    try {
        const res = await fetch(`http://localhost:8000/api/v1/places/${placeId}`, {
            headers: token ? { 'Authorization': `Bearer ${token}` } : {}
        });

        if (!res.ok) throw new Error('Failed to fetch place details');

        const place = await res.json();
        displayPlaceDetails(place);
        displayReviews(place.reviews);
    } catch (error) {
        console.error(error);
        alert('Could not load place details.');
    }
}

/**
 * Populate place details
 */
function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    container.innerHTML = `
        <div class="place-info">
            <h2>${place.name}</h2>
            <p><strong>Host:</strong> ${place.host}</p>
            <p><strong>Price per night:</strong> $${place.price}</p>
            <p><strong>Description:</strong> ${place.description}</p>
            <p><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>
        </div>
    `;
}

/**
 * Display all reviews
 */
function displayReviews(reviews) {
    const reviewsContainer = document.getElementById('reviews');
    for (const review of reviews) {
        const div = document.createElement('div');
        div.className = 'review-card';
        div.innerHTML = `
            <p>"${review.text}"</p>
            <p><strong>User:</strong> ${review.user}</p>
            <p><strong>Rating:</strong> ${review.rating}/5</p>
        `;
        reviewsContainer.appendChild(div);
    }
}
