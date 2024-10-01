import psycopg2
from psycopg2 import Error

# Database connection parameters
database = "postgres"
user = "postgres"
password = "Emilia2022"
host = "localhost"
port = "5432"

def create_connection():
    """Create a database connection to the PostgreSQL database."""
    conn = None
    try:
        conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        print("Connection to database successful.")
    except Error as e:
        print(f"Error connecting to the database: {e}")
    return conn

def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_sql)
            conn.commit()
            print("Table created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")

if __name__ == "__main__":
    sql_create_status_table = """
    CREATE TABLE IF NOT EXISTS status (
      id SERIAL PRIMARY KEY,
      name VARCHAR(50) UNIQUE NOT NULL CHECK (name IN ('new', 'in progress', 'completed')),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      fullname VARCHAR(100),
      email VARCHAR(100) UNIQUE,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
      id SERIAL PRIMARY KEY,
      title VARCHAR(100),
      description TEXT,
      status_id INT,
      user_id INT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (status_id) REFERENCES status (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
      FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    );
    """

    with create_connection() as conn:
        if conn is not None:
            # Create status table
            create_table(conn, sql_create_status_table)
            # Create users table
            create_table(conn, sql_create_users_table)
            # Create tasks table
            create_table(conn, sql_create_tasks_table)
        else:
            print("Error! Cannot create the database connection.")
