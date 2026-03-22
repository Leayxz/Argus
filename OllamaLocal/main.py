import json, time
from ollama import chat

def analisar_vaga():
      vaga_titulo = ""
      vaga_descricao = """"""
      prompt = f"""
      O QUE VOCÊ FAZ:
      - Analise e extraia informações da vaga de emprego.
      - Extraia todas as tecnologias requeridas pela vaga de emprego.
      - Extraia o tipo de contrato da vaga.

      COMO VOCÊ DEVE RESPONDER:
      - Formato obrigatório em JSON

      {{
      "tecs_obrigatorias": [],
      "tecs_desejaveis": [],
      "formacao_desejavel": [],
      "formacao_obrigatoria": [],
      "idiomas_desejaveis": [],
      "idiomas_obrigatorios": [],
      "exige_experiencia_previa": true ou false,
      "tipo_de_contrato": ""
      }}

      Regras:
      - Se não encontrar informação, retorne a lista vazia.
      - Não invente informação.
      - Não responda além do necessário.
      - Não invente resposta.
      - Não explique nada.
      - Não altere nomes ou chaves.

      VAGA:
      Título: {vaga_titulo}
      Descrição: {vaga_descricao}
      """

      print("✅ Aguardando resposta da vaga...")
      resposta = chat(model = "gemma3:4b", messages = [{"role": "user", "content": prompt}], format = "json")
      print("RESPOSTA JSON:\n", resposta["message"]["content"])
      print("TEMPO TOTAL:", resposta["total_duration"] / 1_000_000_000)
      return json.loads(resposta["message"]["content"])

def analisar_curriculo():
      curriculo = """"""
      prompt = f"""
      O QUE VOCÊ FAZ:
      - Analisa e extrai informações de currículos.
      - Extrai todas as tecnologias de currículos.
      
      COMO VOCÊ DEVE RESPONDER:
      - Formato obrigatório em JSON

      {{
      "tecs": [],
      "formacao": [],
      "idiomas": [],
      "anos_experiencia_estimado": ""
      }}

      Regras:
      - Se não encontrar informação, retorne a lista vazia.
      - Não invente informação.
      - Não responda além do necessário.
      - Não invente resposta.
      - Não explique nada.
      - Não altere nomes ou chaves.

      CURRÍCULO
      - {curriculo}
      """

      print("✅ Aguardando resposta do currículo...")
      resposta = chat(model = "gemma3:4b", messages = [{"role": "user", "content": prompt}], format = "json")
      print("RESPOSTA JSON:\n", resposta["message"]["content"])
      print("TEMPO TOTAL:", resposta["total_duration"] / 1_000_000_000)
      return json.loads(resposta["message"]["content"])

def decidir_vaga():      
      requisitos_vaga = analisar_vaga()
      habilidades_candidato = analisar_curriculo()

      obrigatorias = set(tec.lower() for tec in requisitos_vaga["tecs_obrigatorias"])
      desejaveis = set(tec.lower() for tec in requisitos_vaga["tecs_desejaveis"])
      tecs_candidato = set(tec.lower() for tec in habilidades_candidato["tecs"])

      # REGRA 1: CANDIDATO SEM TEC OBRIGATORIA
      tecs_eliminado = obrigatorias - tecs_candidato
      if tecs_eliminado: return {"decisao": "NÃO APLICAR", "motivo": f"Faltam tecs obrigatórias: {tecs_eliminado}"}

      # REGRA 2: NIVEL DE CANDIDATURA
      tecs_comuns = desejaveis & tecs_candidato
      score = len(tecs_comuns)
      total_desejaveis = len(desejaveis)

      percentual = (score / total_desejaveis * 100) if total_desejaveis > 0 else 100

      if percentual >= 80:
            decisao = "APLICAR"
            nivel = "CANDIDATO FORTE"
      elif percentual >= 50:
            decisao = "APLICAR"
            nivel = "CANDIDATO MÉDIO"
      else:
            decisao = "NÃO APLICAR"
            nivel = "CANDIDATO FRACO"
      
      return {"decisao": decisao, "nivel": nivel, "score": score, "percentual": percentual}

inicio = time.time()
resposta = decidir_vaga()
fim = time.time()
print(resposta)
print(f"Terminou em {inicio - fim} segundos.")

"""
Esse código feio não foi o primeiro que construí, só para ficar claro quando voltar aqui.
"""