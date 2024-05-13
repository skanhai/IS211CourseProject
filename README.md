# IS211CourseProject
Final Project Book Catalogue


Book Catalogue Web Application

Overview

The Book Catalogue Web Application is built using Flask, a Python web framework, and SQLite for database management. The core functionality revolves around user authentication, book management, and integration with the Google Books API for book search. The app.py file defines routes for user login, registration, dashboard access, book search, saving, and deletion. Upon user registration, the provided username and password are stored securely in the SQLite database. The dashboard route fetches and displays the user's saved books from the database, allowing them to view, delete, and search for new books. The search() route handles searches by ISBN or title, utilizing the Google Books API to fetch book data based on the user's query. Search results are then rendered in the search_results.html template, where users can select books to save to their catalogue. The application's structure and clear routing ensure smooth navigation and interaction for users managing their book collections. Additionally, the style.css file enhances the user interface with custom styling, providing a visually appealing experience.


This Flask-based web application allows users to manage their personal book catalogues. Users can register with a username and password, then log in to access their dashboard. From the dashboard, users can search for books by ISBN or title using the Google Books API. Search results display book details, and users can save and delete books on their catalogues. The application also features a logout option to securely end sessions.

Model Details

The relational model of the Book Catalogue Web Application is structured around two main tables: "users" and "books." The "users" table stores user data, including unique IDs, usernames, and hashed passwords for secure authentication. Each user can have multiple books associated with them, which are stored in the "books" table. This table contains book details such as titles, authors, page counts, average ratings, and thumbnail URLs. A foreign key constraint links each book entry to its respective user, ensuring data integrity and allowing for efficient retrieval of user-specific book collections. This relational model enables users to manage their personalized book catalogues seamlessly, with each book entry tied to the user who added it.


Hosting
The application is hosted on PythonAnywhere, providing a live environment for users to access their book catalogues from anywhere with an internet connection. The link is https://skanhai96.pythonanywhere.com/
