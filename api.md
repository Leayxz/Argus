# 📡 Documentação API

### POST /avaliacoes
- Endpoint para avaliação de compatibilidade da vaga.

### Request
```json
{
      "texto_vaga": "string"
}
```

### Response
#### 200
```json
{
      "msg": "Compatibilidade: ⭐ 0.82\n✅ Aplicar"
}
```
#### 400

### POST /treinamentos
- Endpoint para treinamento do modelo de compatibilidade.
- Label pode conter 0 ou 1, sendo 0 para vagas compatíveis e 1 para vagas não compatíveis.

### Request
```json
{
      "texto_vaga": "string",
      "label": 0
}
```

### Response
#### 201
```json
{
      "msg": "🤖 Modelo treinado com sucesso."
} 
```
#### 400
