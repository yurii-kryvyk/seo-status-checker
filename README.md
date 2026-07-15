# SEO Status Checker

A web application for checking HTTP status codes of multiple URLs.

Built with **FastAPI**, **httpx**, **HTML**, **CSS**, and **JavaScript**.

## Features

- Check multiple URLs at once
- Asynchronous HTTP requests
- URL normalization
- Remove duplicate URLs
- HTTP status code detection
- Response time measurement
- Search results
- Table sorting
- Status counters
- Color-coded status highlighting
- Swagger API documentation

## Technologies

- Python 3.11+
- FastAPI
- Uvicorn
- httpx
- Jinja2
- HTML
- CSS
- JavaScript

## Project Structure

```
seo-status-checker/
│
├── main.py
│
├── schemas/
│   ├── __init__.py
│   └── url.py
│
├── services/
│   ├── __init__.py
│   └── checker.py
│
├── static/
│
├── templates/
│
├── README.md
├── requirements.txt
└── LICENSE
```

## Installation

Clone the repository

```bash
git clone https://github.com/yurii-kryvyk/seo-status-checker.git
```

Open the project

```bash
cd seo-status-checker
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
uvicorn main:app --reload
```

Open your browser

```
http://127.0.0.1:8000
```

Swagger documentation

```
http://127.0.0.1:8000/docs
```

## License

This project is licensed under the MIT License.