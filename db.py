from fastapi import Body
import psycopg2 as p2
import json

def connect_db():
    global connect, cursor
    connect = p2.connect(dbname = "postgres", user="postgres", password="postgres", host="127.0.0.1")
    cursor = connect.cursor()
    # cursor.execute("CREATE DATABASE recipes_db")
    cursor.execute(
"CREATE TABLE IF NOT EXISTS recipes (id TEXT PRIMARY KEY, name TEXT, description TEXT, ingredients TEXT, steps TEXT)")
    cursor.execute(
"CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, login TEXT, password TEXT)")
    connect.commit()
    print('Подключился к базе')


#INSERT

def db_create_recipe(recipe):
    cursor.execute(
        "INSERT INTO recipes (id, name, description, ingredients, steps) VALUES(%s, %s, %s, %s, %s)",
        (recipe.id, recipe.name, recipe.description, recipe.ingredients, json.dumps(recipe.steps)))

def db_create_user(user):
    cursor.execute(
        "INSERT INTO users (id, login, password) VALUES(%s, %s, %s, %s, %s)",
        (user.id, user.login, user.password))


#SELECT

def db_get_recipes():
    recipes = cursor.execute("SELECT * FROM recipes")
    recipes = cursor.fetchall()
    return recipes

def db_get_recipes_id(recipe_id):
    cursor.execute("SELECT * FROM recipes WHERE id=%s", (recipe_id,))
    recipe = cursor.fetchall()
    return recipe

def db_get_user_ex(user_id):
    cursor.execute("SELECT * FROM recipes WHERE id=%s", (user_id,))
    user = cursor.fetchall()
    if user:
        return True
    else:
        return False

#UPDATE

def db_edit_recipe(data = Body()):
    cursor.execute(
            "UPDATE recipes SET name=%s WHERE id=%s", (data["name"], data["id"]))
    cursor.execute(
        "UPDATE recipes SET description=%s WHERE id=%s", (data["description"], data["id"]))
    cursor.execute(
        "UPDATE recipes SET ingredients=%s WHERE id=%s", (data["ingredients"], data["id"]))
    cursor.execute(
        "UPDATE recipes SET steps=%s WHERE id=%s",(json.dumps(data["steps"]), data["id"]))

#DЕLETE

def db_delete_recipe(id):
    cursor.execute("DELETE FROM recipes WHERE id=%s", (id,))