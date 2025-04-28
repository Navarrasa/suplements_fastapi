from fastapi import FastAPI, HTTPException

app = FastAPI()

suplementos = suplementos = [
    {"id": 1, "nome": "Whey Protein", "categoria": "Proteína", "marca": "Gold Standard", "indicado_para": "Atletas, praticantes de musculação"},
    {"id": 2, "nome": "Creatina", "categoria": "Performance", "marca": "Integral Médica", "indicado_para": "Atletas, praticantes de musculação, esportes de alta intensidade"},
    {"id": 3, "nome": "BCAA", "categoria": "Recuperação", "marca": "New Millen", "indicado_para": "Atletas, praticantes de musculação"},
    {"id": 4, "nome": "L-carnitina", "categoria": "Emagrecimento", "marca": "Max Titanium", "indicado_para": "Indivíduos em processo de emagrecimento, atletas"},
    {"id": 5, "nome": "Multivitamínico", "categoria": "Saúde geral", "marca": "Universal Nutrition", "indicado_para": "Indivíduos com necessidade de reposição de vitaminas e minerais"},
    {"id": 6, "nome": "Ômega 3", "categoria": "Saúde Cardiovascular", "marca": "Optimum Nutrition", "indicado_para": "Indivíduos que buscam melhorar a saúde cardiovascular"},
    {"id": 7, "nome": "Caseína", "categoria": "Proteína", "marca": "Dymatize", "indicado_para": "Atletas, praticantes de musculação"}
]

@app.get("/")
async def main():
    return {"suplementos": suplementos}


@app.get("/suplementos/{id_suplemento}")
async def suplemento(id_suplemento: int):
    # Search for the supplement by id
    suplemento_found = next((suplemento for suplemento in suplementos if suplemento["id"] == id_suplemento), None)
    
    if suplemento_found is None:
        # If the supplement with the given id is not found, raise a 404 HTTP exception
        raise HTTPException(status_code=404, detail="Suplemento não encontrado")
    
    return {"suplemento": suplemento_found}