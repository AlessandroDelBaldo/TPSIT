# Used Cars App

This project is a web application that allows users to request a list of used cars from a dealership based on their preferences. The application includes a form where users can specify the brand, model, fuel type, and color of the cars they are interested in. The results are displayed in a table format after filtering the available cars from a JSON file.

## Project Structure

```
used-cars-app
├── products.json        # Contains an array of objects representing available used cars
├── products.py          # Server-side script to handle AJAX requests and filter cars
├── static
│   └── script.js        # Client-side JavaScript for form submission and result display
├── templates
│   ├── list.html        # HTML form for user input
│   └── products.html    # HTML to display filtered results in a table
├── requirements.txt      # Python dependencies for the project
└── README.md            # Documentation for the project
```

## Setup Instructions

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required Python packages listed in `requirements.txt` using pip:
   ```
   pip install -r requirements.txt
   ```
4. Run the server using the following command:
   ```
   python products.py
   ```
5. Open your web browser and go to `http://localhost:5000` to access the application.

## Usage

1. Fill out the form with your desired car specifications (brand, model, fuel type, color).
2. Click the submit button to send your request.
3. The application will display a table with the filtered list of available used cars based on your input.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is open-source and available under the MIT License.