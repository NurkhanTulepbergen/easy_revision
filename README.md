# easy_revision
Store Management System
This is a store management system designed to manage stores, companies, and admin roles. It allows for the tracking of products, product orders, and financial reports. The system supports different roles such as Admin, Store, and Company, with specific permissions and access levels for each.

Features
Role-based access: Admin, Store, and Company users with different levels of access.
Product management: Manage products in the store, including adding, editing, and deleting products.
Reporting: Generate daily, monthly, and yearly financial reports.
Low-stock notifications: Receive notifications when products are low in stock.
Company integration: Companies process orders and manage their own product assortments.
Cart and order management: Stores manage customer orders and track their status.
Tech Stack
Backend: Django, Django Rest Framework
Frontend: HTML, CSS, Bootstrap
Database: SQLite (or PostgreSQL/MySQL)
Libraries: Chart.js (for visualizing product trends)
Authentication: JWT (JSON Web Tokens) for API security
Testing: Pytest for unit tests and coverage
Requirements
Before running the project, ensure you have the following installed:

Python 3.x
Django
Django Rest Framework
Angular
Node.js and npm (for frontend development)
PostgreSQL or MySQL (optional for production)
Installation
Clone the Repository
bash
git clone https://github.com/yourusername/store-management-system.git
cd store-management-system
Backend Setup
Create and activate a virtual environment:

bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install the required Python packages:

bash
pip install -r requirements.txt
Apply database migrations:

bash
python manage.py migrate
Create a superuser for the Django admin:

bash
python manage.py createsuperuser
Start the Django development server:

bash
python manage.py runserver
Frontend Setup
Navigate to the frontend directory and install dependencies:

bash
cd frontend
npm install
Run the Angular development server:

bash
ng serve
Your frontend will be accessible at http://localhost:4200/.

Usage
Admin Dashboard: Access the Django admin at http://localhost:8000/admin/ and manage users, products, and financial reports.
Store Dashboard: Stores can view products, manage orders, and check reports.
Company Dashboard: Companies can view orders, manage products, and generate their own reports.
API: The backend provides a REST API that can be consumed by the frontend or other clients.
API Documentation
The API is documented using Swagger UI, which is integrated into the project with drf_yasg. To view the API documentation:

Run the server.
Navigate to http://localhost:8000/swagger/ to access the API documentation.
Testing
To run unit tests for the project, use:

bash
pytest
For detailed test coverage, run:

bash
pytest --cov=store_management --cov-report=html
This will generate a coverage report in HTML format.
