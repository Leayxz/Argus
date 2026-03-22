from fastapi import Request
from fastapi.responses import JSONResponse

async def exception_middleware(request: Request, call_next) -> JSONResponse:
      try:
            return await call_next(request)

      except Exception as erro:
            print(erro) # LOG EM PROD
            return JSONResponse(status_code = 500, content = {"status_code": 500, "msg": f"Erro interno do servidor"})

"""
O middleware é registrado na instância do FastAPI no arquivo main.
A função "call_next" executa o resto do pipeline e retorna a resposta ao client, erros caem nos excepts.
"""
