# Car Parts Company Backend API Setup Guide

Welcome to the setup guide for the Car Parts Company Backend API. This document provides comprehensive instructions for initializing and running the backend environment of our car parts company project. By following these steps, you will be able to set up the project environment, run the Django application, create a superuser for database administration, and access API documentation through Swagger and Redoc.

## Prerequisites

Before beginning the setup process, ensure you have the following installed on your system:

- **Python 3.9 or higher**: The core programming language used for the project.
- **pip**: The Python package installer, used for managing software packages written in Python.
- **Virtual environment (optional but recommended)**: A tool for creating isolated Python environments, allowing you to manage project dependencies separately.
- **Docker (optional)**: A platform for developing, shipping, and running applications inside lightweight containers. This is optional but recommended for a simplified deployment process.

## Installation Steps

Follow these detailed steps to get your development environment up and running:

### 1. Obtain the Project Files

First, you need to get the source files of the project onto your local machine. If a repository URL is provided, clone the repository using Git:

```bash
git clone <repository-url>
cd autocompany
```

### 2. Set Up a Virtual Environment (Optional)

Creating a virtual environment is recommended to avoid conflicts between project dependencies and system-wide Python packages. To set up a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Required Packages

Install all dependencies listed in the `requirements.txt` file to ensure the project runs correctly:

```bash
pip install -r requirements.txt
```

### 4. Database Setup with Migrations

Run Django migrations to set up your database schema:

```bash
python manage.py makemigrations  # Optional step to create new migrations based on model changes
python manage.py migrate  # Apply migrations to the database
```

### 5. Create a Superuser for Django Admin

Create a superuser account for accessing the Django admin interface. This account allows you to manage the application data:

```bash
python manage.py createsuperuser
```

Follow the command-line prompts to set up your superuser's username, email, and password.

#or 

#you can even use Test admin account with SQLite

Test admin user's  credentials
Admin user's username- admin
password - admin@1A


## Running the Project

### Starting the Django Development Server

Launch the Django development server with the following command:

```bash
python manage.py runserver
```

### Accessing the Django Admin Panel

Visit `http://localhost:8000/admin/` in your web browser and log in using the superuser credentials you created to access the Django admin panel.

## API Documentation

### Swagger UI

For interactive API documentation and testing, navigate to `http://localhost:8000/swagger/`.

### Redoc

For a more detailed API documentation layout, visit `http://localhost:8000/redoc/`.

### User Stories vs Endpoints

As a company, I want all my products in a database, so I can offer them via our new platform to customers - POST Endpoint   /products/

As a client, I want to add a product to my shopping cart, so I can order it at a later stage - POST Endpoint  /add-to-cart/

As a client, I want to remove a product from my shopping cart, so I can tailor the order to what I actually need - /remove-from-cart/

As a client, I want to order the current contents in my shopping cart, so I can receive the products I need to repair my car - POST Endpoint  /create-order/

As a client, I want to select a delivery date and time, so I will be there to receive the order - POST Endpoint /orders/


As a client, I want to see an overview of all the products, so I can choose which product I want - GET Endpoint  /products/

As a client, I want to view the details of a product, so I can see if the product satisfies my needs - /products/{id}/

### Test Data

    Existing Product IDs in SQLite DB - 5,6,7

    Existing Cart IDs in SQLite DB - 1

    Existing User IDs in SQLite DB - 1 

## Running in Docker (Optional)

To containerize and run the application using Docker, follow these instructions:

### Building the Docker Image

```bash
docker build -t autocompany .
```

### Running the Docker Container

```bash
docker run -p 8000:8000 -d autocompany
```

After the container starts, access Swagger documentation at `http://localhost:8000/swagger` to explore the available API endpoints.

