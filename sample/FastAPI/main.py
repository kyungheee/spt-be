from fastapi import FastAPI
from enum import Enum # 열거형

class ModelName(str, Enum): # 열거형 클래스를 사용하는 타입 어노테이션으로 경로 매개변수를 생성
   alexnet = 'alexnet'      
   resnet = 'resnet'
   lenet = 'lenet'
   
app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
   if model_name is ModelName.alexnet: # 경로 매개변수의 값은 열거형 멤버가 된다
      return {"model_name": model_name, "message": "Deep Learning FTW!"}
   
   if model_name.value == "lenet": # 열거형 값 가져오기
      return {"model_name": model_name, "message": "LeCNN all the images"}
   
   return {"model_name": model_name, "message": "Have som residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str): # 매개변수 이름은 file_path이며, :path는 매개변수가 경로와 일치해야 함을 명시
   return {"file_path": file_path}