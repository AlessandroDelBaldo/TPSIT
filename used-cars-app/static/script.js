document.addEventListener('DOMContentLoaded', function() {
    const tbody = document.querySelector('#cars-table tbody');

    fetch('/api/cars', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ brand: '', model: '', fuel_type: '', color: '' })
    })
    .then(response => response.json())
    .then(cars => {
        if (cars.length > 0) {
            cars.forEach(car => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${car.brand}</td>
                    <td>${car.model}</td>
                    <td>${car.fuel_type}</td>
                    <td>${car.color}</td>
                    <td><img src="${car.image_url}" alt="${car.brand} ${car.model}" width="100"></td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="5">No cars found</td></tr>';
        }
    })
    .catch(error => console.error('Error:', error));
});
