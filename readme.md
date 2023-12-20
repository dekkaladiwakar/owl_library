API List:
Users:
1. Users CRUD: /user/
Authors:
1. Authors CRUD: /author/
Books:
1. Books CRUD: /book/
2. GET /book/available/
3. GET /book/author/<author-name>
Lending: (act- Action)
1. GET /act/eligible/book/<book-owl-id>/user/<user-id>
2. POST /act/borrow/
    Request Body: (JSON)
        a. owl_id (string)
        b. user_id (number)
