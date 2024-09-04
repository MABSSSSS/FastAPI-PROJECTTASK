Project Overview
This project is a web application built with FastAPI, leveraging PostgreSQL as the database backend. The application focuses on creating a secure environment where users can manage products and track sales. It integrates various core functionalities such as user authentication, product management, and sales recording.

Key Concepts and Technologies Used
FastAPI: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.

SQLAlchemy: This is the ORM (Object Relational Mapper) used in the project to handle database operations. SQLAlchemy allows us to interact with the PostgreSQL database using Python objects, providing an abstract layer over SQL.

PostgreSQL: The database system used in this project. PostgreSQL is a powerful, open-source object-relational database system with a strong reputation for reliability, feature robustness, and performance.

Pydantic: Used for data validation and settings management. Pydantic helps ensure that data models conform to the expected types and formats.

JWT (JSON Web Token): JWT is used for securing API endpoints through token-based authentication. This ensures that only authenticated users can access certain parts of the application.

OAuth2: OAuth2 with password flow is implemented to handle the authentication mechanism. This allows users to log in with a username and password, and in return, receive a token that can be used to authenticate further requests.

Core Features
User Management: Users can register and log in to the system. Passwords are securely hashed using the bcrypt algorithm.

Product Management: Authenticated users can create, read, update, and delete (CRUD) products. Each product is associated with a user.

Sales Tracking: The application allows users to track sales related to the products. Each sale record contains information about the product sold and the user who made the sale.

Database Schema
The application uses a relational database schema, where:

Users have a one-to-many relationship with Products (a user can own multiple products).
Products have a one-to-many relationship with Sales (a product can have multiple sales).
Sales are linked to both Products and Users, forming a many-to-one relationship from the perspective of the sale.
Security
The application implements robust security features:

Password Hashing: User passwords are never stored in plain text. They are hashed using bcrypt before being stored in the database.
JWT Authentication: JSON Web Tokens are used to secure API endpoints. Each token contains a payload with user information and an expiration time, ensuring that sessions are both secure and time-bound.
OAuth2 with JWT Bearer Tokens: This is the authentication scheme used, providing a secure way to authenticate users via token exchange.
