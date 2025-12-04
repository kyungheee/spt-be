from fastapi import FastAPI
from typing import Union

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10): 
   return fake_items_db[skip : skip + limit] # 경로 매개변수의 일부가 아닌 다른 함수의 매개변수를 선언하면 쿼리 매개변수로 자동 해석

@app.get("/items/{item_id}")
async def read_item_2(item_id: str, q: Union[str, None] = None): # 기본값을 None으로 설정하여 선택적으로 매개변수를 선언
   if q:
      return {"item_id": item_id, "q": q}
   return {"item_id": item_id}

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
   user_id: int, item_id: str, q: Union[str, None]= None, short: bool = False
):
   item = {"item_id": item_id, "owner_id": user_id}
   if q:
      item.update({"q": q})   
   if not short:
      item.update(
         {"description": "This is an amazing item that has a long description"}
      )
   return item