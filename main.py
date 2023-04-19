import uuid
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse, FileResponse
 
class Recipe:
    def __init__(self, name, description="Описание", ingredients="ингридиенты", steps="шаги"):
        self.name = name
        self.description = description
        self.ingredients = ingredients
        self.steps = steps
        self.id = str(uuid.uuid4())
 
# условная база данных УДАЛИТЬ
recipes = [Recipe("Творожная запеканка с яблоками и морковью"),
        Recipe("Банановое печенье"), 
        Recipe("Манник на кефире, с изюмом")]
 
# для поиска рецепта в списке recipes
def find_recipe(id):
    for recipe in recipes: 
         if recipe.id == id:
            return recipe
    return None
 
app = FastAPI()
 
@app.get("/")
async def main():
    return FileResponse("public/index.html")
 
@app.get("/api/recipes")
def get_recipes():
    return recipes
 
@app.get("/api/recipes/{id}")
def get_recipe(id):
    # получаем рецепт по id
    recipe = find_recipe(id)
    print(recipe)
    # если не найден, отправляем статусный код и сообщение об ошибке
    if recipe == None:  
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={ "message": "Рецепт не найден" }
        )
    #если пользователь найден, отправляем его
    return recipe
 
 
@app.post("/api/recipes")
def create_recipe(data  = Body()):
    recipe = Recipe(data["name"],
                    data["description"],
                    data["ingredients"],
                    data["steps"])

    # добавляем объект в список recipes
    recipes.append(recipe)
    return recipe
 
@app.put("/api/recipes")
def edit_recipe(data  = Body()):
  
    # получаем рецепт по id
    recipe = find_recipe(data["id"])
    # если не найден, отправляем статусный код и сообщение об ошибке
    if recipe == None: 
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={ "message": "Рецепт не найден" }
        )
    # если рецепт найден, изменяем его данные и отправляем обратно клиенту
    recipe.name = data["name"]
    recipe.description = data["description"]
    recipe.ingredients = data["ingredients"]
    recipe.steps = data["steps"]
    return recipe
 
 
@app.delete("/api/recipes/{id}")
def delete_recipe(id):
    # получаем пользователя по id
    recipe = find_recipe(id)
  
    # если не найден, отправляем статусный код и сообщение об ошибке
    if recipe == None:
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={ "message": "Рецепт не найден" }
        )
  
    # если пользователь найден, удаляем его
    recipes.remove(recipe)
    return recipe