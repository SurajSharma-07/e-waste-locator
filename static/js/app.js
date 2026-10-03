let map;
let markers = [];
let userMarker = null;
let userLocation = null;
let facilities = [];

const $ = (id) => document.getElementById(id);

document.addEventListener("DOMContentLoaded", async () => {
    initMap();
    await loadCategories();
    await searchFacilities();

    $("searchBtn").addEventListener("click", searchFacilities);
    $("categorySelect").addEventListener("change", searchFacilities);
    $("radiusSelect").addEventListener("change", searchFacilities);
    $("searchInput").addEventListener("keydown", (e) => {
        if (e.key === "Enter") searchFacilities();
    });
    $("locateBtn").addEventListener("click", useMyLocation);
    $("closeDetail").addEventListener("click", () => $("detailPanel").classList.add("hidden"));
});

function initMap() {
    // Mumbai is used only as the initial map view; it is not the user's location.
    map = L.map("map").setView([19.0760, 72.8777], 11);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
}

async function loadCategories() {
    try {
        const res = await fetch("/api/categories");
        const categories = await res.json();
        for (const category of categories) {
            const option = document.createElement("option");
            option.value = category;
            option.textContent = category;
            $("categorySelect").appendChild(option);
        }
    } catch (error) {
        console.error(error);
    }
}

function useMyLocation() {
    if (!navigator.geolocation) {
        setStatus("Geolocation is not supported by this browser.");
        return;
    }

    setStatus("Requesting your location...");

    navigator.geolocation.getCurrentPosition(
        (position) => {
            userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            if (userMarker) map.removeLayer(userMarker);

            userMarker = L.marker([userLocation.lat, userLocation.lng])
                .addTo(map)
                .bindPopup("Your current location")
                .openPopup();

            map.setView([userLocation.lat, userLocation.lng], 13);
            searchFacilities();
        },
        (error) => {
            setStatus("Location permission was not available. You can still search manually.");
            console.warn(error);
        },
        { enableHighAccuracy: true, timeout: 10000 }
    );
}

async function searchFacilities() {
    const params = new URLSearchParams();

    const q = $("searchInput").value.trim();
    const category = $("categorySelect").value;
    const radius = $("radiusSelect").value;

    if (q) params.set("q", q);
    if (category) params.set("category", category);
    if (userLocation) {
        params.set("lat", userLocation.lat);
        params.set("lng", userLocation.lng);
        params.set("radius", radius);
    }

    setStatus("Loading facilities...");

    try {
        const res = await fetch(`/api/facilities?${params.toString()}`);
        if (!res.ok) throw new Error("Unable to load facilities");
        facilities = await res.json();

        renderFacilities();
        renderMarkers();

        $("facilityCount").textContent = facilities.length;
        $("resultSubtitle").textContent = userLocation
            ? `Within ${radius} km of your location`
            : "Showing verified facilities";

        setStatus(`${facilities.length} verified facility record(s) found.`);
    } catch (error) {
        console.error(error);
        setStatus("Could not load facilities. Check that Flask and MySQL are running.");
    }
}

function renderFacilities() {
    const list = $("facilityList");
    list.innerHTML = "";

    if (!facilities.length) {
        list.innerHTML = `
            <div class="empty">
                <strong>No verified facilities found.</strong>
                <p>The database currently contains no verified records matching your search.</p>
            </div>
        `;
        return;
    }

    for (const facility of facilities) {
        const item = document.createElement("article");
        item.className = "facility";
        item.innerHTML = `
            <h4>${escapeHtml(facility.name)}
                ${facility.distance_km !== null
                    ? `<span class="distance">${facility.distance_km} km</span>` : ""}
            </h4>
            <p>${escapeHtml(facility.address)}, ${escapeHtml(facility.city)}</p>
            <p>${escapeHtml(facility.operating_hours || "Hours not provided")}</p>
            <span class="badge">✓ Verified</span>
        `;

        item.addEventListener("click", () => {
            map.setView([facility.latitude, facility.longitude], 15);
            showDetail(facility);
        });

        list.appendChild(item);
    }
}

function renderMarkers() {
    for (const marker of markers) map.removeLayer(marker);
    markers = [];

    for (const facility of facilities) {
        const marker = L.marker([facility.latitude, facility.longitude])
            .addTo(map)
            .bindPopup(`<strong>${escapeHtml(facility.name)}</strong><br>Verified facility`);

        marker.on("click", () => showDetail(facility));
        markers.push(marker);
    }

    if (facilities.length && !userLocation) {
        const bounds = L.latLngBounds(facilities.map(f => [f.latitude, f.longitude]));
        map.fitBounds(bounds.pad(0.15));
    }
}

function showDetail(facility) {
    const directionUrl =
        `https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route=` +
        `${facility.latitude}%2C${facility.longitude}`;

    $("detailContent").innerHTML = `
        <span class="badge">✓ Verified</span>
        <h2>${escapeHtml(facility.name)}</h2>

        <div class="detail-grid">
            <div class="detail-item">
                <strong>Address</strong>
                <span>${escapeHtml(facility.address)}, ${escapeHtml(facility.city)},
                ${escapeHtml(facility.state)} ${escapeHtml(facility.pincode || "")}</span>
            </div>
            <div class="detail-item">
                <strong>Contact</strong>
                <span>${escapeHtml(facility.contact || "Not provided")}</span>
            </div>
            <div class="detail-item">
                <strong>Operating Hours</strong>
                <span>${escapeHtml(facility.operating_hours || "Not provided")}</span>
            </div>
            <div class="detail-item">
                <strong>Verification</strong>
                <span>${escapeHtml(facility.verification_source || "Source not listed")}</span>
            </div>
            <div class="detail-item">
                <strong>Last Verified</strong>
                <span>${escapeHtml(facility.last_verified || "Not provided")}</span>
            </div>
            <div class="detail-item">
                <strong>Email</strong>
                <span>${escapeHtml(facility.email || "Not provided")}</span>
            </div>
        </div>

        <h3>Accepted e-waste</h3>
        <div class="tags">
            ${facility.accepted_categories.map(c => `<span class="tag">${escapeHtml(c)}</span>`).join("")}
        </div>

        ${facility.notes ? `<p>${escapeHtml(facility.notes)}</p>` : ""}

        <div class="detail-actions">
            <a href="${directionUrl}" target="_blank" rel="noopener">Get Directions</a>
            ${facility.website
                ? `<a href="${escapeAttr(facility.website)}" target="_blank" rel="noopener">Website</a>`
                : ""}
        </div>
    `;

    $("detailPanel").classList.remove("hidden");
    $("detailPanel").scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function setStatus(message) {
    $("status").textContent = message;
}

function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (char) => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
    }[char]));
}

function escapeAttr(value) {
    return escapeHtml(value);
}
