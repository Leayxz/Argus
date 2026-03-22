from fastapi import FastAPI
from pydantic import BaseModel
from modelos import avaliar_vaga_IA

app = FastAPI()
curriculo = """"""

class VagaRequest(BaseModel):
      titulo: str
      descricao: str

@app.post("/analisar-vaga")
def analisar_vaga(vaga: VagaRequest):
      resposta = avaliar_vaga_IA(curriculo, vaga)
      if not resposta: return {"resposta": "Nenhum provedor respondeu."}
      return {"resposta": resposta}
