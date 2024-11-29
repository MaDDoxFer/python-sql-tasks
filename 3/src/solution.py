import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def batch_insert(conn, products):
    query = """
    INSERT INTO products (name, price, quantity)
    VALUES %s
    """
    values = [(p['name'], p['price'], p['quantity']) for p in products]
    with conn.cursor() as cursor:
        execute_values(cursor, query, values)
        conn.commit()


def get_all_products(conn):
    query = "SELECT * FROM products ORDER BY price DESC"
    with conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()
# END
