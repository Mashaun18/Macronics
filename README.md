**Macronics Project**
======================

**Overview**
------------

This is a Django-based e-commerce project for managing customers, vendors, products, orders, and payments.

**Features**
------------

* User authentication and authorization using Django's built-in auth system and Simple JWT
* Customer, vendor, product, order, and payment management
* RESTful API using Django Rest Framework

**Requirements**
---------------

* Python 3.8+
* Django 5.1+
* Django Rest Framework 3.12+
* Simple JWT 5.2+

**Installation**
---------------

1. Clone the repository: `git clone https://github.com/Mashaun18/Macronics.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (on Linux/Mac) or `venv\Scripts\activate` (on Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Set environment variables: `DATABASE_URL` (see `settings.py` for more information)
6. Run migrations: `python manage.py migrate`
7. Start the development server: `python manage.py runserver`

**API Documentation**
--------------------

API documentation is available at `POSTMAN` (e.g., 'https://interstellar-space-896126.postman.co/workspace/New-Team-Workspace~d1d8f4ad-846b-422e-b179-650b6e9415e1/collection/31299998-4b2b54f3-0a95-48b6-8f00-1aa0ae56f9a9?action=share&creator=31299998`).

**Contributing**
---------------

Contributions are welcome! Please submit a pull request with your changes.

**License**
----------

This project is licensed under the MIT License. See `LICENSE` for more information.
