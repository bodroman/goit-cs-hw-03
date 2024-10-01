import random
import psycopg2
from faker import Faker

# Ініціалізація Faker
fake = Faker()

# Параметри підключення до бази даних
DB_HOST = 'localhost'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS = 'Emilia2022'

# Функція для заповнення таблиць
def seed_database():
    # Підключення до бази даних
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    cursor = conn.cursor()

    # Заповнення таблиці status
    statuses = ['new', 'in progress', 'completed']
    for status in statuses:
        cursor.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (status,))
    
    # Заповнення таблиці users
    for _ in range(10):  # Створити 10 користувачів
        fullname = fake.name()
        email = fake.unique.email()
        cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s);", (fullname, email))

    # Заповнення таблиці tasks
    cursor.execute("SELECT id FROM users;")
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM status;")
    status_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(20):  # Створити 20 завдань
        title = fake.sentence(nb_words=6)
        description = fake.text()
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)
        cursor.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);",
            (title, description, status_id, user_id)
        )

    # Зберігання змін і закриття з'єднання
    conn.commit()
    cursor.close()
    conn.close()
    print("Database seeded successfully.")

if __name__ == '__main__':
    seed_database()
