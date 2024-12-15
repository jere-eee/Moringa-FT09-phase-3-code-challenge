from database.connection import get_db_connection
from models.magazine import Magazine

conn = get_db_connection()
cursor = conn.cursor()

class Author:
    def __init__(self, id, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("Name must be a string longer than 0 characters.")
        self._id = id
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self._name,))
        conn.commit()
        self._id = cursor.lastrowid
    
    @property
    def name(self):
        cursor.execute('SELECT name FROM authors WHERE id = ?', (self._id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise ValueError("Author not found in database.")
    
    @name.setter
    def name(self, name):
        if hasattr(self, '_name'):
            raise AttributeError('Name cannot be changed')
        elif isinstance(name, str) and len(name) > 0:
            cursor.execute('UPDATE authors SET name = ? WHERE id = ?', (name, self._id))
            conn.commit()
        else:
            raise ValueError("Name must be a string longer than 0 characters.")
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if isinstance(id, int):
            self._id = id
        else:
            raise ValueError('ID must be an integer.')
        
    @classmethod
    def get(cls, author_id):
        cursor.execute('SELECT name FROM authors WHERE id = ?', (author_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise ValueError(f"Author with id {author_id} not found.")
        
    def articles(self):
        try:
            cursor.execute("""
                SELECT articles.title, articles.content, articles.author_id, articles.magazine_id
                FROM articles 
                WHERE articles.author_id = ?               
            """, (self._id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching articles for author {self._id}: {e}")
            return []
    
    def magazines(self):
        try:
            cursor.execute("""
                SELECT DISTINCT magazines.name, magazines.category
                FROM magazines
                INNER JOIN articles ON articles.magazine_id = magazines.id
                WHERE articles.author_id = ?
            """, (self._id,))
            results = cursor.fetchall()
            return [Magazine(result[0], result[1]) for result in results]
        except Exception as e:
            print(f"Error fetching magazines for author {self._id}: {e}")
            return []
    def __repr__(self):
        return f'<Author {self.name}>'
