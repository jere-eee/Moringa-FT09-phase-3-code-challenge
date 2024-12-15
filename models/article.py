from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

conn = get_db_connection()
cursor = conn.cursor()

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        try:
            if isinstance(title, str) and 5 <= len(title) <= 50:
                self._title = title
            else:
                raise ValueError("Title must be a string between 5-50 characters.")

            self._content = content
            self._author_id = author_id
            self._magazine_id = magazine_id
            self._id = id

            cursor.execute("""
                           INSERT INTO articles (title, content, author_id, magazine_id)
                           VALUES (?, ?, ?, ?)
                           """, 
                           (self._title, self._content, self._author_id,self._magazine_id))
            conn.commit()
            self._id = cursor.lastrowid
        except Exception as e:
            print(f"Error creating article: {e}")
    @property
    def title(self):
        cursor.execute('SELECT title FROM articles WHERE id = ?', (self._id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise ValueError("Article not in database.")

    @title.setter
    def title(self, title):
        raise AttributeError("Title cannot be changed after creation.")

    @property
    def author(self):
        return Author.get(self._author_id)

    @property
    def magazine(self):
        return Magazine.get(self._magazine_id)
    
    def __repr__(self):
        return f'<Article {self.title}>'
