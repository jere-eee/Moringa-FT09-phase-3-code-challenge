# Phase 3 -WK3 - Code Challenge: Articles - with database by Jeremy Akanle

This repository provides a solution to the **Articles Database Challenge**, which models relationships between Authors, Articles, and Magazines using Python and SQLite.

## Domain Overview

- **Author**: Writes multiple articles.
- **Magazine**: Publishes multiple articles.
- **Article**: Belongs to one author and one magazine.

## Features

### Author
- `articles()`: Lists all articles by the author.
- `magazines()`: Lists magazines where the author’s articles were published.

### Magazine
- `articles()`: Lists all associated articles.
- `contributors()`: Lists all authors.
- `article_titles()`: Lists all article titles for the magazine.
- `contributing_authors()`: Lists authors with more than 2 articles.

### Article
- Retrieves the associated `Author` and `Magazine`.

## Setting Up the Database

To set up the database for this project, follow these steps:

1. Install the required dependencies by running:

    ```bash
    pipenv install
    ```

2. Activate the virtual environment:

    ```bash
    pipenv shell
    ```

3. Create and initialize the database by executing:

    ```bash
    python3 app.py
    ```

## Deliverables

This project involves implementing the following features:

- **CRUD Operations**: Create, read, update, and delete functionality for Authors, Magazines, and Articles.
- **Object Relationships**: Use SQL joins to establish relationships between the models.
- **Validation**: Ensure that all fields adhere to the specified constraints for data integrity.

