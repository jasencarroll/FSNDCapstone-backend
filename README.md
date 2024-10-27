# Project Name: Casting Agency Flask App

### **README for Testing Framework and Setup**

This project is live at [https://fsndcapstone-backend-66c5827e55b3.herokuapp.com/](https://fsndcapstone-backend-66c5827e55b3.herokuapp.com/)

## **Overview**

This project involves building a backend API for a casting agency to manage movies and actors, with role-based access control (RBAC) implemented through Auth0. We have written comprehensive unit tests to ensure that the functionality of the app is robust and secure.

This README provides detailed reasoning behind the tests we have written, as well as instructions on how to set up the Flask app locally. It includes:

- **Test Reasoning**: Why we wrote the tests we did and the logic behind each test category.
- **Local Setup Instructions**: A step-by-step guide to running the Flask app locally, including required files and structure.

---

## **Table of Contents**

1. [Installation](#installation)
2. [Test Strategy Overview](#test-strategy-overview)
3. [Test Categories](#test-categories)
    - [1. Success Tests for Endpoints](#1-success-tests-for-endpoints)
    - [2. Error Tests for Endpoints](#2-error-tests-for-endpoints)
    - [3. RBAC (Role-Based Access Control) Tests](#3-rbac-tests)
4. [Local Setup for the Flask App](#local-setup-for-the-flask-app)
    - [File Structure](#file-structure)
    - [Installation](#installation)
    - [Running the App Locally](#running-the-app-locally)
5. [Modules Explanation](#modules-explanation)

---

## Installation

Requirements:
- Postgres
- .env file
- pip
- flask db

### Postgres

If you have a user database and permissions to create other databases run `psql` if not run `sudo -u postgres psql` and enter the following:

```
CREATE DATABASE casting;
```

### .env file

Store the following variables in the `.env` file. 

```
FLASK_APP=app.py
FLASK_DEBUG=1
DATABASE_URL='postgresql://postgres:admin@localhost:5432/casting'
AUTH0_DOMAIN = 'dev-8his2amisscpohz8.us.auth0.com'
AUDIENCE = 'https://jcsFSNDCapstone510699.com'
ASSISTANT_TOKEN = ''
CASTING_DIRECTOR_TOKEN = ''
EXECUTIVE_PRODUCER_TOKEN = ''
APP_SECRET_KEY = ''
AUTH0_CLIENT_SECRET = ''
AUTH0_CLIENT_ID = ''
```

### pip

```
pip install -r requirements.txt
```

### flask db

### Running locally
```
flask run
```

## **Test Strategy Overview**

The main goal of the tests is to ensure that all endpoints function as expected under different scenarios and that role-based access control (RBAC) works properly. This includes verifying:

- Successful behavior of each endpoint under normal conditions.
- Error handling and proper status code responses when something goes wrong.
- Access control, ensuring that only authorized roles can access and modify specific resources.

We’ve broken down our test approach into three key categories:

---

## **Test Categories**

### **1. Success Tests for Endpoints**

**Why?**  
Success tests are fundamental to verify that each endpoint behaves as expected when provided with valid inputs and authorized users. Each success test aims to validate that the app can handle core CRUD operations without any issues.

#### **Tests Written:**
- **`GET /movies`**: Ensures that movies can be fetched by authorized users (e.g., Casting Assistants, Casting Directors, and Executive Producers).
- **`GET /actors`**: Similar to movies, we ensure actors can be retrieved.
- **`POST /movies`**: Validates that a movie can be successfully created by authorized roles (e.g., Executive Producers).
- **`POST /actors`**: Verifies that new actors can be added to the database by roles with the correct permissions.
- **`PATCH /movies` and `PATCH /actors`**: Ensures that movies and actors can be updated successfully with valid data.
- **`DELETE /movies` and `DELETE /actors`**: Checks that authorized roles can delete resources.

**Reasoning:**  
We chose these tests because they cover the core CRUD functionality of the API. A properly functioning backend must handle the full lifecycle of data manipulation—creating, retrieving, updating, and deleting.

---

### **2. Error Tests for Endpoints**

**Why?**  
Error handling is crucial in any API to ensure users receive clear feedback when something goes wrong, such as missing or incorrect data. Error tests validate that the app responds with the correct status codes and error messages under problematic scenarios.

#### **Tests Written:**
- **`GET /movies` and `GET /actors` without authorization**: Verifies that a 401 Unauthorized error is returned when trying to access these resources without proper authorization.
- **`POST /movies` and `POST /actors` with incomplete data**: Ensures that the app returns a 422 Unprocessable Entity error when required fields are missing or incorrect.
- **`PATCH /movies` and `PATCH /actors` with non-existent resources**: Checks that the app returns a 404 Not Found error when trying to update resources that don’t exist.
- **`DELETE /movies` and `DELETE /actors` with non-existent resources**: Validates that attempting to delete non-existent resources returns a 404 error.

**Reasoning:**  
These tests were written to ensure the app handles edge cases and improper inputs gracefully, without crashing or returning ambiguous errors. A robust app needs to inform users when their actions cannot be completed due to invalid input or lack of authorization.

---

### **3. RBAC Tests**

**Why?**  
Role-based access control (RBAC) ensures that only users with the appropriate permissions can perform certain actions. These tests ensure that the permissions assigned to each role are enforced correctly.

#### **Tests Written:**
- **Casting Assistant**:
  - Can **view** movies and actors but **cannot delete** or modify resources.
  - We wrote tests to verify they can fetch movies/actors but receive a `403 Forbidden` error when attempting to delete or modify resources.

- **Casting Director**:
  - Can **add, delete, and modify actors** but cannot delete movies.
  - Tests ensure they can add and delete actors but receive `403 Forbidden` when attempting to delete movies.

- **Executive Producer**:
  - Has full permissions: can **add, delete, and modify both actors and movies**.
  - Tests validate that the Executive Producer can perform all actions successfully.

**Reasoning:**  
We specifically chose these tests to ensure the security of the app by enforcing role-based restrictions on actions. RBAC prevents unauthorized users from performing actions that could disrupt the data integrity or security of the system.

---

## **Local Setup for the Flask App**

### **File Structure**

```bash
├── app_list.py        # Contains the endpoints logic.
├── app.py             # Main entry point of the Flask app.
├── auth.py            # Handles authentication, authorization, and token validation.
├── manage.py          # Management commands (e.g., for migrations).
├── models.py          # Defines the database models (Movie, Actor).
├── Procfile           # For deploying the app on platforms like Heroku.
├── README.md          # This file (for project documentation).
├── requirements.txt   # Contains the Python dependencies.
├── runtime.txt        # Specifies the Python version.
├── token_tester.py    # Script for testing token validation.
```

---

### **Installation**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/<your-username>/casting-agency.git
   cd casting-agency
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file and add your Auth0 credentials and JWT tokens for the different roles:

   ```
   FLASK_APP=app.py
   FLASK_DEBUG=1
   DATABASE_URL='postgresql://postgres:admin@localhost:5432/casting'
   AUTH0_DOMAIN=<your-auth0-domain>
   API_AUDIENCE=<your-api-audience>
   ASSISTANT_TOKEN=<assistant-jwt>
   DIRECTOR_TOKEN=<director-jwt>
   PRODUCER_TOKEN=<producer-jwt>
   ```

5. **Run database migrations:**

   ```bash
   flask db upgrade
   ```

---

### **Running the App Locally**

1. **Run the Flask app:**

   ```bash
   flask run
   ```

2. **Access the app:**

   Open your browser and go to `http://localhost:5000`.

---

## **Modules Explanation**

### **1. `app.py`**
   The entry point for the Flask application. It sets up the app configuration, initializes extensions, and registers routes.

### **2. `app_list.py`**
   Contains the endpoint logic for managing movies and actors.

### **3. `auth.py`**
   Handles the authentication and authorization logic using JWT tokens and Auth0. It contains decorators like `requires_auth` to enforce RBAC.

### **4. `manage.py`**
   Contains management commands for running database migrations.

### **5. `models.py`**
   Defines the SQLAlchemy models for `Movie` and `Actor` and manages database operations.

### **6. `Procfile`**
   Used for deploying the app to Heroku, defining how to run the app in production.

### **7. `README.md`**
   This documentation file, explaining the project, its setup, and the tests written.

### **8. `requirements.txt`**
   Lists all the Python dependencies needed to run the project (e.g., Flask, SQLAlchemy, Auth0 libraries).

### **9. `runtime.txt`**
   Specifies the version of Python used for deployment.

### **10. `token_tester.py`**
   A helper script for validating tokens and ensuring they work with the API.

---

By following this README, you should be able to run the app locally, understand the purpose behind the tests, and see how role-based access control is enforced in the API.