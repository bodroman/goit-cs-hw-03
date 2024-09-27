from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Налаштування бази даних
client = MongoClient(
    'mongodb+srv://romangalay7:4FfLhHg1QotsRgBB@cluster0.bkzwh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0',
    server_api=ServerApi('1'))

db = client["cat_database"]
collection = db["cats"]


def create_cat(name, age, features):
    """Створює нового кота в базі даних."""
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    collection.insert_one(cat)
    print(f"Кіт {name} успішно доданий.")


def read_all_cats():
    """Виводить усі записи котів із колекції."""
    cats = collection.find()
    for cat in cats:
        print(cat)


def read_cat_by_name(name):
    """Виводить інформацію про кота за його ім'ям."""
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"Кота з ім'ям {name} не знайдено.")


def update_cat_age(name, new_age):
    """Оновлює вік кота за його ім'ям."""
    result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.modified_count > 0:
        print(f"Вік кота {name} успішно оновлено на {new_age}.")
    else:
        print(f"Кота з ім'ям {name} не знайдено.")


def add_feature_to_cat(name, feature):
    """Додає нову характеристику до списку features кота за ім'ям."""
    result = collection.update_one({"name": name}, {"$addToSet": {"features": feature}})
    if result.modified_count > 0:
        print(f"Характеристика '{feature}' успішно додана до кота {name}.")
    else:
        print(f"Кота з ім'ям {name} не знайдено.")


def delete_cat_by_name(name):
    """Видаляє запис кота з колекції за ім'ям."""
    result = collection.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Кіт {name} успішно видалений.")
    else:
        print(f"Кота з ім'ям {name} не знайдено.")


def delete_all_cats():
    """Видаляє всі записи з колекції."""
    collection.delete_many({})
    print("Усі коти успішно видалені.")


# Приклади використання функцій
if __name__ == "__main__":
    # Додавання котів (для прикладу)
    create_cat("Barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    create_cat("Murzik", 5, ["любить м'ячики", "дослідник"])

    # Читання всіх котів
    print("Усі коти:")
    read_all_cats()

    # Читання кота за ім'ям
    print("\nДеталі кота з ім'ям Barsik:")
    read_cat_by_name("Barsik")

    # Оновлення віку кота
    update_cat_age("Barsik", 4)

    # Додавання характеристики
    add_feature_to_cat("Barsik", "любить молоко")

    # Видалення кота
    delete_cat_by_name("Murzik")

    # Видалення всіх котів
    delete_all_cats()
