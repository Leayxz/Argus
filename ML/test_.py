from learning import MachineLearning, ModeloPersistido

class Mock(ModeloPersistido):
      def persistir_modelo_treinado(self, *args, **kwargs):
            pass
      def carregar_modelo_treinado(self, *args, **kwargs):
            pass

class TestMachineLearning:

      def test_unitario_avaliar_vaga(self):

            # TESTE MODELO NAO CARREGADO
            ml = MachineLearning(Mock())
            teste1 = ml.avaliar_vaga("Teste modelo não carregado.")
            assert teste1.status_code == 400

            # TESTE MODELO CARREGADO E COMPARACAO FEITA
            ml.treinar_modelo("Teste A", 0)
            ml.treinar_modelo("Teste B", 1)
            teste2 = ml.avaliar_vaga("Teste modelo carregado.")
            assert teste2.status_code == 200

      def test_unitario_treinar_modelo(self):

            # TESTE MODELO COM LABELS INSUFICIENTES
            ml = MachineLearning(Mock())
            resposta1 = ml.treinar_modelo("Teste A", 0)
            assert resposta1.status_code == 400

            # TESTE MODELO COM LABELS SUFICIENTES
            ml.treinar_modelo("Teste B", 0)
            resposta2 = ml.treinar_modelo("Teste C", 1)
            assert resposta2.status_code == 201

"""
Testes cobrindo caminho correto, alternativo e errado.
Testar endpoints sem precisar subir o servidor é algo interessante.
"""
