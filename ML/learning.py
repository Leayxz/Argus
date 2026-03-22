import joblib, os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from dataclasses import dataclass

@dataclass
class ModeloResposta:
      status_code: int
      msg: str

class ModeloPersistido:

      def carregar_modelo_treinado(self):
            if os.path.exists("modelo_salvo.pkl"): return joblib.load("modelo_salvo.pkl")

      def persistir_modelo_treinado(self, vetorizar, modelo, dataset):
            joblib.dump({"vetorizar": vetorizar, "modelo": modelo, "dataset": dataset}, "modelo_salvo.pkl")

class MachineLearning:

      def __init__(self, DB:ModeloPersistido):

            # ATRIBUTOS PARA PERSISTIR O MODELO
            self.dataset = {}
            self.modelo_treinado = False

            # INSTANCIAS PARA O ML E DB
            self.vetorizar = TfidfVectorizer()
            self.modelo = LogisticRegression()
            self.DB = DB

      def avaliar_vaga(self, texto_vaga: str) -> ModeloResposta:

            # PROTECAO CONTRA MODELO NAO TREINADO
            if not self.modelo_treinado: return ModeloResposta(400, f"Modelo ainda não treinado.")

            # VETORIZA A VAGA E FAZ O CALCULO
            texto_vetorizado = self.vetorizar.transform([texto_vaga])
            score = self.modelo.predict_proba(texto_vetorizado)[0][0]

            if score > 0.50: return ModeloResposta(200, f"Compatibilidade:⭐ {score:2f}\n✅ Aplicar")
            return ModeloResposta(200, f"Compatibilidade: ⭐{score:2f}\n❌ Não aplicar")

      def treinar_modelo(self, texto_vaga: str, label: int) -> ModeloResposta:

            # NOVA VAGA SALVA
            self.dataset[texto_vaga] = label
            print(f"✅ Nova vaga adicionada com sucesso.\n✅ Todas as vagas até o momento: {len(self.dataset)}") # DEBUG

            # SEPARANDO CADA PALAVRA E LABEL
            textos = [texto for texto in self.dataset.keys()]
            labels = [label for label in self.dataset.values()]

            # PROTECAO CONTRA LABELS < 2
            if len(set(labels)) < 2: return ModeloResposta(400, f"⚠️ Modelo sem dados suficientes para treinamento.")

            # VETORIZANDO TEXTO, TREINAR MODELO
            texto_vetorizado = self.vetorizar.fit_transform(textos)
            self.modelo.fit(texto_vetorizado, labels)

            # PERSISTINDO NOVA VAGA, VETORIZACAO E MODELO
            self.DB.persistir_modelo_treinado(self.vetorizar, self.modelo, self.dataset)
            self.modelo_treinado = True # GARANTE QUE O MODELO FOI TREINADO, EVITANDO ERRO DE NAO INICIALIZACAO
            return ModeloResposta(201, f"🤖 Modelo treinado com sucesso.")

      def carregar_modelo_existente(self) -> None:
            if self.modelo_treinado: return
            dados = self.DB.carregar_modelo_treinado()
            if not dados: return
            self.dataset = dados["dataset"]
            self.vetorizar = dados["vetorizar"]
            self.modelo = dados["modelo"]
            self.modelo_treinado = True

"""
Service conhece status_code, o que !!aparentemente é errado!!, mas não gera acoplamento, então está limpo.
Em python consigo mudar o atributo diretamete, em linguagens como java, seria necessário um método set para alterar.
"""
