#uvicorn main:app --reload

import uuid
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse, FileResponse

from db import *
 
class Recipe:
    def __init__(self, name, description="Описание", ingredients="ингридиенты", steps={"шаг": 5}):
        self.name = name
        self.description = description
        self.ingredients = ingredients
        self.steps = steps
        self.id = str(uuid.uuid4())


connect_db()

def create_recipe():
    print('тут')
    for _ in range(100):
        recipe = Recipe("name",
                        "description",
                        "ingredients",
                        {"шаг": 5})

        # добавляем объект в таблицу recipes
        db_create_recipe(recipe)
create_recipe()

def get_time_cooking(recipe):
    steps_text = json.loads(recipe[4])
    time = 0
    for step_time in steps_text.values:
        try:
            time+=step_time
        except ValueError:
            continue
    return time

 
app = FastAPI()
 
@app.get("/")
async def main():
    return FileResponse("public/index.html")
 
@app.get("/api/recipes")
def get_recipes():
    return db_get_recipes()

 
@app.get("/api/recipes/{id}")
def get_recipe(id):
    # получаем рецепт по id
    recipe = db_get_recipes_id(id)
    print(recipe)
    # если не найден, отправляем статусный код и сообщение об ошибке
    if recipe == None:  
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={ "message": "Рецепт не найден" }
        )
    #если пользователь найден, отправляем его
    return recipe


@app.get("/api/recipes/filters/{filter}")
def get_recipes_filtered(filter):
    if filter == "min_to_max" or filter == 'max_to_min':
        get_recipes_min_max(filter)
    else:
        get_recipes_by_ingredients(filter)


# Поиск по ингридиентам
def get_recipes_by_ingredients(ingredient):
    recipes = db_get_recipes()
    recipes_with_ingredient=[]
    for recipe in recipes:
        if ingredient in recipe[4]:
            recipes_with_ingredient.append()
    if recipes_with_ingredient == []:  
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={ "message": "Рецепты не найден с таким ингридиентом не найдены" }
        )

# Сортируем по времени готовки
def get_recipes_min_max(filter):
    recipes = db_get_recipes()
    dict_recipes={}
    for recipe in recipes:
        time_cooking = get_time_cooking(recipe)         # Получаем все рецепты
        dict_recipes.update({recipe[0]: time_cooking})  # И добавляем в словарь id: время готовки
    if filter == "min_to_max":
        sorted(dict_recipes, key=dict_recipes.get)  
        return dict_recipes # Возвращаем отсортированый словарь             
    elif filter == "max_to_min":
        sorted(dict_recipes, key=dict_recipes.get, reverse=True)
        return dict_recipes # Возвращаем отсортированый словарь


@app.post("/api/recipes/")



 
@app.post("/api/recipes")
def create_recipe(data  = Body()):
    print('тут')
    recipe = Recipe(data["name"],
                    data["description"],
                    data["ingredients"],
                    data["steps"])

    # добавляем объект в таблицу recipes
    db_create_recipe(recipe)
    return recipe
 
@app.put("/api/recipes")
def edit_recipe(data  = Body()):
  
    # получаем рецепт по id
    recipe = db_get_recipes_id(data["id"])
    # если не найден, отправляем статусный код и сообщение об ошибке
    if recipe == None: 
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={ "message": "Рецепт не найден" }
        )
    else:
        # если рецепт найден, изменяем его данные и отправляем обратно клиенту
        db_edit_recipe(data)
        recipe = db_get_recipes_id(data["id"])
    return recipe
 
 
@app.delete("/api/recipes/{id}")
def delete_recipe(id):
    # получаем пользователя по id
    recipe = db_get_recipes_id(id)
  
    # если не найден, отправляем статусный код и сообщение об ошибке
    if recipe == None:
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={ "message": "Рецепт не найден" }
        )
  
    # если пользователь найден, удаляем его
    db_delete_recipe(id)
    return recipe