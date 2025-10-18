# Fullstack Application

This project is a fullstack application with a Python Flask backend and a React.js frontend. 

## Project Structure

```
fullstack-app
├── backend
│   ├── app.py
│   ├── models
│   │   └── __init__.py
│   ├── routes
│   │   └── __init__.py
│   ├── utils
│   │   └── __init__.py
│   ├── requirements.txt
│   └── config.py
├── frontend
│   ├── public
│   │   └── index.html
│   ├── src
│   │   ├── components
│   │   │   └── App.js
│   │   ├── pages
│   │   │   └── Home.js
│   │   ├── utils
│   │   │   └── api.js
│   │   └── index.js
│   ├── package.json
│   └── package-lock.json
├── .gitignore
└── README.md
```

## Backend Setup

1. Navigate to the `backend` directory.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```
   python app.py
   ```

## Frontend Setup

1. Navigate to the `frontend` directory.
2. Install the required dependencies:
   ```
   npm install
   ```
3. Start the React application:
   ```
   npm start
   ```

## Usage

- The backend API will be available at `http://localhost:5000`.
- The frontend application will be available at `http://localhost:3000`.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes. 

## License

This project is licensed under the MIT License.