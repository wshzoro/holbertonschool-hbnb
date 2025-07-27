document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname;

  if (path.endsWith('index.html') || path === '/' || path === '') {
    initIndexPage();
  } else if (path.endsWith('place.html')) {
    initPlacePage();
  } else if (path.endsWith('add_review.html')) {
    initAddReviewPage();
  } else if (path.endsWith('login.html')) {
    initLoginPage();
  }
});

function initIndexPage() {
  const places = [
    { id: 1, name: 'Cozy Apartment', price: 80 },
    { id: 2, name: 'Beach House', price: 150 },
    { id: 3, name: 'Mountain Cabin', price: 120 },
  ];

  const placesList = document.getElementById('places-list');
  const priceFilter = document.getElementById('price-filter');

  const prices = [...new Set(places.map(p => p.price))].sort((a, b) => a - b);
  prices.forEach(price => {
    const option = document.createElement('option');
    option.value = price;
    option.textContent = `$${price}`;
    priceFilter.appendChild(option);
  });

  displayPlaces(places, placesList);

  priceFilter.addEventListener('change', () => {
    const maxPrice = Number(priceFilter.value);
    const filtered = places.filter(p => p.price <= maxPrice);
    displayPlaces(filtered, placesList);
  });
}

function displayPlaces(places, container) {
  container.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.style.margin = '20px';
    card.style.padding = '10px';
    card.style.border = '1px solid #ddd';
    card.style.borderRadius = '10px';

    card.innerHTML = `
      <h3>${place.name}</h3>
      <p>Price per night: $${place.price}</p>
      <button class="details-button" data-id="${place.id}">View Details</button>
    `;

    container.appendChild(card);
  });

  container.querySelectorAll('.details-button').forEach(button => {
    button.addEventListener('click', (e) => {
      const placeId = e.target.getAttribute('data-id');
      window.location.href = `place.html?id=${placeId}`;
    });
  });
}

function initPlacePage() {
  const placeDetailsSection = document.getElementById('place-details');
  const reviewsSection = document.getElementById('reviews');
  const addReviewSection = document.getElementById('add-review');

  const placeId = new URLSearchParams(window.location.search).get('id') || 1;
  const place = {
    id: placeId,
    name: 'Cozy Apartment',
    host: 'John Doe',
    price: 80,
    description: 'A nice and cozy apartment in the city center.',
    amenities: ['WiFi', 'Air Conditioning', 'Kitchen'],
  };

  const reviews = [
    { id: 1, user: 'Alice', comment: 'Great place!', rating: 5 },
    { id: 2, user: 'Bob', comment: 'Very comfortable.', rating: 4 },
  ];

  placeDetailsSection.className = 'place-details place-info';
  placeDetailsSection.style.margin = '20px';
  placeDetailsSection.style.padding = '10px';
  placeDetailsSection.style.border = '1px solid #ddd';
  placeDetailsSection.style.borderRadius = '10px';

  placeDetailsSection.innerHTML = `
    <h2>${place.name}</h2>
    <p><strong>Host:</strong> ${place.host}</p>
    <p><strong>Price per night:</strong> $${place.price}</p>
    <p>${place.description}</p>
    <p><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>
  `;

  reviewsSection.innerHTML = '';
  reviews.forEach(review => {
    const card = document.createElement('div');
    card.className = 'review-card';
    card.style.margin = '20px';
    card.style.padding = '10px';
    card.style.border = '1px solid #ddd';
    card.style.borderRadius = '10px';

    card.innerHTML = `
      <p><strong>${review.user}:</strong> ${review.comment}</p>
      <p>Rating: ${review.rating} / 5</p>
    `;

    reviewsSection.appendChild(card);
  });

  const loggedIn = Boolean(localStorage.getItem('userLoggedIn'));

  if (loggedIn) {
    addReviewSection.style.display = 'block';
  } else {
    addReviewSection.style.display = 'none';
  }

  const reviewForm = document.getElementById('review-form');
  if (reviewForm) {
    reviewForm.addEventListener('submit', (e) => {
      e.preventDefault();
      alert('Review submitted! (functionality to be implemented)');
      reviewForm.reset();
    });
  }
}

function initAddReviewPage() {
  const placeId = new URLSearchParams(window.location.search).get('id');
  const loggedIn = Boolean(localStorage.getItem('userLoggedIn'));

  if (!loggedIn) {
    alert('You must be logged in to add a review.');
    window.location.href = 'login.html';
    return;
  }

  const reviewForm = document.getElementById('review-form');
  if (reviewForm) {
    reviewForm.addEventListener('submit', (e) => {
      e.preventDefault();
      alert('Review submitted for place id: ' + placeId);
      reviewForm.reset();
    });
  }
}

function initLoginPage() {
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const email = loginForm.email.value.trim();
      const password = loginForm.password.value.trim();

      if (!email || !password) {
        alert('Please enter email and password.');
        return;
      }

      try {
        const response = await fetch('http://localhost:5000/api/v1/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });

        if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/`;
          localStorage.setItem('userLoggedIn', 'true');
          alert('Login successful!');
          window.location.href = 'index.html';
        } else {
          const error = await response.json();
          alert('Login failed: ' + (error.message || 'Invalid credentials'));
        }
      } catch (error) {
        alert('An error occurred: ' + error.message);
      }
    });
  }
}
