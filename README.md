
# Django Customized Admin Panel

This project demonstrates a Django application with a customized admin panel and APIs for managing records, agents, and reasons. It uses Django REST Framework for serialization and API handling.

## Overview

The project includes three main models:

1. **Agent**: Represents an agent with a user and an assigned phone number.
2. **Reason**: Represents reasons for specific actions or records.
3. **Record**: Stores records with details like an agent, phone number, delay, and associated reason.


### Features

- **Admin Panel**: Customizable admin interface for managing agents, reasons, and records.
- **REST API**: Provides endpoints for creating, reading, updating, and deleting agents, reasons, and records.
- **Authentication**: Simple login feature for user authentication.

### Setup Instructions

1. Clone the repository and navigate to the project directory.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations to set up the database:
   ```bash
   python manage.py migrate
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```
5. Access the admin panel at `http://127.0.0.1:8000/admin` to manage data.

### API Endpoints

- `POST /api/login/`: Authenticate a user with a username and password.
- `GET /api/agents/`: List all agents.
- `GET /api/reasons/`: List all reasons.
- `GET /api/records/`: List all records.

This setup provides a foundation for managing and tracking records efficiently through a customized Django admin panel and REST APIs.
