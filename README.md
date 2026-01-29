# 🚧 Work In Progress: School Registry API

This is a Django REST API project designed to manage student absences. It allows for user authentication, student management, and tracking functionality for student absences.

## Features

*   **User Authentication**: Secure registration and login using JWT (JSON Web Tokens).
*   **Student Management**: View detailed information about students.
*   **Absence Tracking**: Create, view, and manage absence records for students.
*   **Permissions**: Protected endpoints ensuring only authenticated users can access data.

## key Technologies

*   **Python**: Core programming language.
*   **Django**: High-level Python web framework.
*   **Django REST Framework**: Toolkit for building Web APIs.
*   **SimpleJWT**: JSON Web Token authentication for Django REST Framework.
*   **SQLite**: Default database for development.
*   **PyCharm**: IDE used for development.

## Prerequisites

*   Python 3.8+ installed.
*   `pip` (Python package installer).

## Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd registro_assenze
    ```

2.  **Create and activate a virtual environment:**

    *   **macOS/Linux:**
        ```bash
        python -m venv .venv
        source .venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        python -m venv .venv
        .\.venv\Scripts\activate
        ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run database migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Start the development server:**

    ```bash
    python manage.py runserver
    ```

    The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

Here are the main API endpoints available:

### CRUD

| Endpoint | Description |
| :--- | :--- |
| `admin/` | Django Admin interface |

### Authentication

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login to get access and refresh tokens |
| POST | `/api/auth/token/refresh/` | Refresh the access token |
| POST | `/api/auth/password-change/` | Change the authenticated user's password |

### Students

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/api/students/` | List all students |
| POST | `/api/students/` | Create a new student |
| GET | `/api/students/<id>/` | Retrieve details of a specific student |

### Absences

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/api/absences/` | List all absences |
| POST | `/api/absences/` | Create a new absence record |
| GET | `/api/absences/<id>/` | Retrieve details of a specific absence |
| PUT/PATCH | `/api/absences/<id>/` | Update a specific absence |
| DELETE | `/api/absences/<id>/` | Delete a specific absence |

## Project Structure

*   `config/`: Project main configuration, settings, and URL routing.
*   `core/`: Core functionality, including absence management and user-related views.
*   `students/`: Student management application.
