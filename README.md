# FastAPI Products & Users API

\*by Andrii Sernovskyi

Backend REST API built with FastAPI, PostgreSQL, and SQLAlchemy — implementing user authentication, product/category management, and full test coverage.

## Features

- JWT-based authentication (register, login, protected routes)
- Ownership-based access control (users can only edit/delete their own products)
- Full CRUD for Products and Categories
- Pagination, sorting, and search on product listing
- Custom exception handling
- Automated tests with pytest (isolated test database)
- Database migrations with Alembic
- Dockerized for easy setup

## Tech Stack

- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **Pydantic** — data validation
- **JWT (python-jose)** + **passlib/bcrypt** — authentication
- **pytest** — testing
- **Docker** — containerization

## Getting Started

### Local Setup

1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies:
