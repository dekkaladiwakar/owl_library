# Owl Library

## Overview
Owl Library is a Django-based library management system, allowing users to manage books, authors, and lending records. 

## Technical Stack
- Django
- Django Rest Framework (DRF)
- PostgreSQL

## Installation
Clone the repository:
```bash
git clone https://github.com/dekkaladiwakar/owl_library.git
```
Follow the installation instructions for Django and PostgreSQL.

## Models
- User
- Author
- Book
- Lending

## API Endpoints
- Users CRUD: `/user/`
- Authors CRUD: `/author/`
- Books CRUD: `/book/`
- View available books: `GET /book/available/` ___(Assignment)___
- View books by author: `GET /book/author/<author-name>` ___(Assignment)___
- Check borrowing eligibility: `GET /act/eligible/book/<book-owl-id>/user/<user-name>` ___(Assignment)___

- Borrow Book: `POST /act/borrow/` ___(Assignment)___

  - Request Body (JSON):
    - `owl_id` (string): Unique ID of the book
    - `user_id` (number): Unique ID of the user

- Return Book: `POST /act/return/` ___(Assignment)___
  - Request Body (JSON):
    - `owl_id` (string): Unique ID of the book
    - `user_id` (number): Unique ID of the user
- View all borrowings by user: `GET /act/borrow/user/<user-id>/all`
- View active borrowings by user: `GET /act/borrow/user/<user-id>/active`

## Future Implementations
- Implement authentication.
- Notification system for due returns.
- Auto-return feature for digital books.
