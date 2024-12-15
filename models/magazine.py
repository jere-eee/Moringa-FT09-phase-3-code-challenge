from database.connection import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

class Magazine:
    def __init__(self, id, name, category):
        if isinstance(name, str) and 2 <= len(name) <= 16:
            self._name = name
        else:
            raise ValueError("Name must be string between 2-16 characters.")
        if isinstance(category, str) and len(category) > 0:
            self._category = category
        else:
            raise ValueError("Category must be non-empty string.")
        self._id = id
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self._name, self._category))
        conn.commit()
        self._id = cursor.lastrowid
        
    @property
    def name(self):
        cursor.execute('SELECT name FROM magazines WHERE id = ?', (self._id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise ValueError("Magazine not in database.")
        
    @name.setter
    def name(self, name):
        if isinstance(name, str) and 2 <= len(name) <= 16:
            cursor.execute('UPDATE magazines SET name = ? WHERE id = ?', (name, self._id))
            conn.commit()
        else:
            raise ValueError("Name must be string between 2-16 characters.")

    @property
    def category(self):
        cursor.execute('SELECT category FROM magazines WHERE id = ?', (self._id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise ValueError("Magazine not in database.")
        
    @category.setter
    def category(self, category):
        if isinstance(category, str) and len(category) > 0:
            cursor.execute('UPDATE magazines SET category = ? WHERE id = ?', (category, self._id))
            conn.commit()
        else:
            raise ValueError("Category must be non-empty string.")

    @classmethod
    def get(cls, magazine_id):
        cursor.execute('SELECT name FROM magazines WHERE id = ?', (magazine_id,))
        result = cursor.fetchone()
        if result:
            return result[0]  
        else:
            raise ValueError(f"Magazine with id {magazine_id} not found.")
    
    def articles(self):
        cursor.execute("""
            SELECT articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles 
            WHERE articles.magazine_id = ?               
        """, (self._id,))
        return cursor.fetchall()
    
    def contributors(self):
        try:
            cursor.execute("""
                SELECT DISTINCT authors.name
                FROM authors
                INNER JOIN articles ON articles.author_id = authors.id
                WHERE articles.magazine_id = ?
            """, (self._id,))
            results = cursor.fetchall()
            from models.author import Author
            return [Author(result[0]) for result in results]
        except Exception as e:
            print(f"Error fetching contributors for magazine {self._id}: {e}")
            return []
    
    def article_titles(self):
        if self.articles:
            [result[0] for result in Magazine.articles()]   
        else:
            return None
        
    def contributing_authors(self):
        all_contributors = self.contributors()

        contributing_authors = []
        for author in all_contributors:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM articles 
                WHERE author_id = ? AND magazine_id = ?
            """, (author.id, self._id))
            article_count = cursor.fetchone()[0]

            if article_count > 2:
                contributing_authors.append(author)

        return contributing_authors if contributing_authors else None
    def __repr__(self):
        return f'<Magazine {self.name} of category {self.category}>'
