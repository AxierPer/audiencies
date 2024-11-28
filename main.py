import pandas as pd
import json
from fastapi import FastAPI, Query
from typing import List
from database.querys import BaseModel, insert_data, Item, get_data,  get_total_count
from fastapi.middleware.cors import CORSMiddleware
from config.config import URL_DEVELOPMENT, URL_PRODUCTION

class DataResponse(BaseModel):
    data: List[Item]
    total: int

app = FastAPI()

origins = [
    URL_DEVELOPMENT or "",  # URL de tu frontend de React en desarrollo
    URL_PRODUCTION or "",  # URL de tu frontend de producción (si la tienes)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite estas URLs
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

@app.get("/inser-data")
def insert_data_db():
    excel = pd.read_excel("Corregido.xlsx")

    with open("audiencias.json", "r") as file:
        data_json = json.load(file)

    dict_json = json.loads(data_json)
    df_excel = pd.DataFrame(excel)
    df_excel.rename(columns={"zip":"ZipCode"}, inplace=True)
    df_excel["ZipCode"] = df_excel["ZipCode"].astype(str)
    df_excel["ZipCode"] = df_excel["ZipCode"].map(lambda x : "00" + x if len(x) < 4 else x )
    df_excel["ZipCode"] = df_excel["ZipCode"].map(lambda x : "0" + x if len(x) <=4 else x )
    df_json = pd.DataFrame(dict_json)

    final_data = pd.merge(df_excel,df_json, how="left", on="ZipCode")
    print(final_data)

    for data in final_data.to_dict(orient="records"):
        insert_data(data["ZipCode"],data["lat"],data["lng"],data["city"],data["state_id"],data["state_name"],data["density"],data["county_fips"],data["county_name"],data["timezone"], data["Hispanos"],data["poblacion"])



@app.get("/data", response_model=DataResponse)
async def get_data_db(limit: int = Query(50, le=10000), offset: int = Query(0, ge=0)):
    print(f"Limit: {limit}, Offset: {offset}")
    data = get_data(limit,offset)
    total = get_total_count()
    return {"data":data, "total":total}
