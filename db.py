import uuid
from fastapi import Body
import psycopg2 as p2

def connect_db():
    global connect, cursor
    connect = p2.connect(dbname = "PostgreSQL 15", host="localhost", user="postgres", password="1767")
    cursor = connect.cursor()
    print('Подключился к базе')


#INSERT

def db_create_recipe(data = Body()):
    with cursor as cur:
        cur.execute(
            "INSERT INTO recipes (id, name, description, ingredients, steps) VALUES(%s, %s, %s, %s, %s)",
            (str(uuid.uuid4()), data["name"],data["description"],data["ingredients"],data["steps"]))


#SELECT

def db_get_recipes():
    with cursor as cur:
        recipes = cur.execute("SELECT * FROM recipes").fetchall()
    return recipes

def db_get_recipes(recipe_id):
    with cursor as cur:
        recipe = cur.execute("SELECT * FROM recipes WHERE id=%s", (recipe_id,)).fetchone()
    return recipe


#UPDATE

def db_edit_recipe(data = Body()):
    with cursor as cur:
        cur.execute(
            "UPDATE recipes SET name=%s WHERE id=%s", (data["name"], data["id"]))
        cur.execute(
            "UPDATE recipes SET description=%s WHERE id=%s", (data["description"], data["id"]))
        cur.execute(
            "UPDATE recipes SET ingredients=%s WHERE id=%s", (data["ingredients"], data["id"]))
        cur.execute(
            "UPDATE recipes SET steps=%s WHERE id=%s",(data["steps"], data["id"]))

#DЕLETE

def db_delete_recipe(id):
    with cursor as cur:
        cur.execute("DELETE FROM recipes WHERE id=%s", (id,))