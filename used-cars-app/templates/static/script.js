document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('car-form');
    const resultsTable = document.getElementById('results-table');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {
            brand: formData.get('brand'),
            model: formData.get('model'),
            fuelType: formData.get('fuelType'),
            color: formData.get('color')
        };

        fetch('/filter-cars', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(cars => {
            resultsTable.innerHTML = '';
            if (cars.length > 0) {
                cars.forEach(car => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${car.brand}</td>
                        <td>${car.model}</td>
                        <td>${car.fuelType}</td>
                        <td>${car.color}</td>
                        <td><img src="${car.imageUrl}" alt="${car.brand} ${car.model}" width="100"></td>
                    `;
                    resultsTable.appendChild(row);
                });
            } else {
                resultsTable.innerHTML = '<tr><td colspan="5">No cars found</td></tr>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});