from openai import OpenAI

modelos = ["openai/gpt-oss-20b:groq"]
client = OpenAI(base_url="https://router.huggingface.co/v1", api_key="")

def avaliar_vaga_IA(curriculo, vaga):
      prompt = f"""
      SUA FUNÇÃO:
      - Levantar todos os requisitos da vaga.
      - Comparar o currículo com os requisitos levantados.

      VAGA:
      - Título: {vaga.titulo}
      - Descrição: {vaga.descricao}

      CURRÍCULO:
      - {curriculo}

      O QUE VOCÊ PRECISA RESPONDER:
      - Decidir se o candidato é "APTO" ou "NÃO APTO".
      - Identificar se a vaga é "PJ", "CLT" ou "NÃO IDENTIFICADO".
      - Classificar o candidato como "FORTE", "MÉDIO" ou "FRACO".

      VOCÊ DEVE RESPONDER OBRIGATORIAMENTE E SOMENTE NO FORMATO ABAIXO:
      - Compatibilidade: SIM/NÃO
      - Classificação: FORTE/MÉDIO/FRACO
      - Aplicabilidade: APLICAR/NÃO APLICAR
      - Motivo para não aplicar: DESCREVER EM ATÉ 30 CARACTERES
      - Tipo de contrato: PJ/CLT/NÃO IDENTIFICADO
      """

      for modelo in modelos:
            try:
                  resposta = client.chat.completions.create(model = modelo, temperature = 0.2, messages=[{"role": "user", "content": prompt}])      
                  print(resposta.choices[0].message.content)
                  return resposta.choices[0].message.content
            except Exception as erro:
                  print(f"Créditos insuficientes:", erro)
                  continue

      return None
