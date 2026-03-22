from fastapi import FastAPI
from fastapi.responses import JSONResponse
from learning import ModeloPersistido, MachineLearning
from pydantic import BaseModel
from typing import Literal
from middleware import exception_middleware

app = FastAPI()
app.middleware("http")(exception_middleware)

class Avaliacoes(BaseModel):
      texto_vaga: str

class Treinamentos(BaseModel):
      texto_vaga: str
      label: Literal[0,1]

ml = MachineLearning(ModeloPersistido())
ml.carregar_modelo_existente()

@app.post("/avaliacoes")
def avaliar_vaga_endpoint(vaga: Avaliacoes):
      resposta = ml.avaliar_vaga(vaga.texto_vaga)
      return JSONResponse(status_code = resposta.status_code, content={"msg": resposta.msg})

@app.post("/treinamentos")
def treinar_modelo_endpoint(vaga: Treinamentos):
      resposta = ml.treinar_modelo(vaga.texto_vaga, vaga.label)
      return JSONResponse(status_code = resposta.status_code, content={"msg": resposta.msg})

"""
Estudar race conditions e implementar controle de concorrência na escrita no treinamento do modelo.
Estudar versionamento do modelo.
"""
