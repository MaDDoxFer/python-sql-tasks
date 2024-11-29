import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def create_post(conn, post):
    query = """
    INSERT INTO posts (title, content, author_id)
    VALUES (%s, %s, %s)
    RETURNING id;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (post['title'], post['content'], post['author_id']))
        conn.commit()
        return cursor.fetchone()[0]


def add_comment(conn, comment):
    query = """
    INSERT INTO comments (post_id, author_id, content)
    VALUES (%s, %s, %s)
    RETURNING id;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (comment['post_id'], comment['author_id'], comment['content']))
        conn.commit()
        return cursor.fetchone()[0]


def get_latest_posts(conn, n):
    posts_query = """
    SELECT id, title, content, author_id, created_at
    FROM posts
    ORDER BY created_at DESC
    LIMIT %s;
    """
    comments_query = """
    SELECT id, post_id, author_id, content, created_at
    FROM comments
    WHERE post_id = %s
    ORDER BY created_at;
    """
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute(posts_query, (n,))
        posts = cursor.fetchall()

        result = []
        for post in posts:
            cursor.execute(comments_query, (post['id'],))
            comments = cursor.fetchall()
            result.append({
                'id': post['id'],
                'title': post['title'],
                'content': post['content'],
                'author_id': post['author_id'],
                'created_at': post['created_at'],
                'comments': [
                    {
                        'id': comment['id'],
                        'author_id': comment['author_id'],
                        'content': comment['content'],
                        'created_at': comment['created_at']
                    }
                    for comment in comments
                ]
            })
        return result
# END
