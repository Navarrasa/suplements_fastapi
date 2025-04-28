from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

suplementos = [
    {"id": 1, "nome": "Whey Protein", "categoria": "Proteína", "marca": "Gold Standard", "indicado_para": "Atletas, praticantes de musculação"},
    {"id": 2, "nome": "Creatina", "categoria": "Performance", "marca": "Integral Médica", "indicado_para": "Atletas, praticantes de musculação, esportes de alta intensidade"},
    {"id": 3, "nome": "BCAA", "categoria": "Recuperação", "marca": "New Millen", "indicado_para": "Atletas, praticantes de musculação"},
    {"id": 4, "nome": "L-carnitina", "categoria": "Emagrecimento", "marca": "Max Titanium", "indicado_para": "Indivíduos em processo de emagrecimento, atletas"},
    {"id": 5, "nome": "Multivitamínico", "categoria": "Saúde geral", "marca": "Universal Nutrition", "indicado_para": "Indivíduos com necessidade de reposição de vitaminas e minerais"},
    {"id": 6, "nome": "Ômega 3", "categoria": "Saúde Cardiovascular", "marca": "Optimum Nutrition", "indicado_para": "Indivíduos que buscam melhorar a saúde cardiovascular"},
    {"id": 7, "nome": "Caseína", "categoria": "Proteína", "marca": "Dymatize", "indicado_para": "Atletas, praticantes de musculação"}
]

class Suplement(BaseModel):
    item_id: str

class SuplementRequest(BaseModel):
    items: List[Suplement]
    query: Optional[str] = None


@app.get("/")
async def main():
    return {"suplementos": suplementos}




@app.get("/suplements/")
async def read_suplements(q: str | None = None):
    results = ("suplements")