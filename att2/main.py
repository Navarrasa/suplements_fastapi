from fastapi import FastAPI, Path, Query, HTTPException, Body
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Literal, Annotated
import json
import os

app = FastAPI()

# -----------------------------------------------------------------

"""
Ler o arquivo json, bd.json

Funcionalidades:

-> load_suplements: verifica se o arquivo exise e retorna seus dados em formato json
-> save_suplements: abre o arquivo em modo de escrita e salva os dados em formato json

"""
# Caminho para o arquivo JSON
DB_FILE = "../bd.json"

# Função para carregar dados do arquivo JSON
def load_suplements():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            return json.load(file)
    return []

# Função para salvar dados no arquivo JSON
def save_suplements(suplements):
    with open(DB_FILE, "w") as file:
        json.dump(suplements, file, indent=4)

# Carrega os suplementos na inicialização
suplementos = load_suplements()

# -----------------------------------------------------------------

# -----------------------------------------------------------------

"""
Modelos de dados para os suplementos

Funcionalidades:

-> BaseModel: define a estrutura dos dados que serão utilizados na API
-> Suplement: modelo para um suplemento, com campos como id, nome, categoria, marca e indicado_para
-> SuplementRequest: modelo para requisições com múltiplos suplementos, incluindo um campo opcional de query
-> FilterParams: modelo para parâmetros de filtro, incluindo limite, offset, ordenação e tags

"""

# Modelo para um suplemento
class Suplement(BaseModel):
    id: int
    nome: str
    categoria: str
    marca: str
    indicado_para: str

# Modelo para requisições com múltiplos suplementos
class SuplementRequest(BaseModel):
    items: List[Suplement]
    query: Optional[str] = None

# Modelo para parâmetros de filtro
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["id", "nome", "categoria"] = "id"
    tags: list[str] = []  # Para filtrar por palavras-chave em indicado_para

# -----------------------------------------------------------------

# Rota raiz
@app.get("/", summary="Retorna a lista completa de suplementos")
async def main():
    return {"suplementos": suplementos}

# Rota para buscar um suplemento por ID
@app.get("/suplements/{suplement_id}", response_model=Suplement, summary="Busca um suplemento específico pelo ID")
async def read_suplement(suplement_id: Annotated[int, Path(title="The ID of the supplement to get", gt=0)]):
    suplement = next((s for s in suplementos if s["id"] == suplement_id), None)
    if suplement is None:
        raise HTTPException(status_code=404, detail="Suplement not found")
    return suplement

# Rota para buscar suplementos com filtro opcional
@app.get("/suplements/", response_model=List[Suplement], summary="Busca suplementos com filtro por nome ou categoria")
async def read_suplements(q: Optional[str] = Query(None, description="Filtrar por nome ou categoria")):
    if q:
        filtered = [s for s in suplementos if q.lower() in s["nome"].lower() or q.lower() in s["categoria"].lower()]
        return filtered
    return suplementos

# Rota para criar múltiplos suplementos
@app.post("/suplements/", response_model=List[Suplement], summary="Adiciona novos suplementos à lista")
async def create_suplements(request: SuplementRequest):
    new_suplements = request.items
    for suplement in new_suplements:
        if any(s["id"] == suplement.id for s in suplementos):
            raise HTTPException(status_code=400, detail=f"Suplemento com ID {suplement.id} já existe")
        suplementos.append(suplement.model_dump())
    save_suplements(suplementos)
    return new_suplements

# Rota para buscar suplementos com filtros avançados
@app.get("/filter/suplements/", response_model=List[Suplement], summary="Busca suplementos com filtros de limite, offset e tags")
async def filter_suplements(filter_query: Annotated[FilterParams, Query()]):
    # Filtra por tags (busca em indicado_para)
    filtered = suplementos
    if filter_query.tags:
        filtered = [
            s for s in filtered
            if any(tag.lower() in s["indicado_para"].lower() for tag in filter_query.tags)
        ]

    # Ordena com base em order_by
    if filter_query.order_by:
        filtered = sorted(filtered, key=lambda x: x[filter_query.order_by])

    # Aplica offset e limit
    start = filter_query.offset
    end = start + filter_query.limit
    filtered = filtered[start:end]

    return filtered

@app.put("/update/{id}/", response_model=Suplement, summary="Atualize itens da Lista de acordo com seus parâmetros")
async def update_suplements(id: int, item: Suplement):
    try:
        suplementos = load_suplements()

        index = next((i for i, s in enumerate(suplementos) if s["id"] == id), None)

        if index is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        suplementos[index] = item.model_dump()
    
        save_suplements(suplementos)
        
        return suplementos[index]
    except Exception as err:
        print(f"Error: {str(err)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar a requisição: {str(err)}")

@app.delete("/delete/{id}/", response_model=Suplement, summary="Delete Itens que não vai mais precisar!")
async def delete_suplements(id: int):
    suplementos = load_suplements()
    index = next((i for i, s in enumerate(suplementos) if s["id"] == id), None)

    if index is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    item_removido = suplementos.pop(index)
    save_suplements(suplementos)

    return item_removido


class SuplementCardBox(BaseModel):
    items : List[Suplement]
    url : HttpUrl

@app.get("/card_suplement_image/{id}", response_model=SuplementCardBox, summary="Busque produtos e suas imagens")
async def suplement_image(id: int):
    # Buscar o suplemento com o id fornecido
    suplemento = next((s for s in suplementos if s["id"] == id), None)

    if suplemento is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Aqui a URL da imagem seria extraída, no caso da variável 'imagem' no suplemento
    suplement_with_image = SuplementCardBox(
        items=[Suplement(**suplemento)],  # Criando o objeto Suplement a partir dos dados
        url=suplemento["imagem"]         # Passando a URL da imagem
    )

    return suplement_with_image  # Retorna o suplemento com a imagem associada