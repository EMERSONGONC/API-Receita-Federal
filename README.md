# 🔍 Consulta CNPJ - Receita Federal (Interface Flet)

Este projeto realiza a consulta de múltiplos CNPJs pela ReceitaWS via API e exporta os resultados para um arquivo Excel.

## ⚙️ Funcionalidades

- Leitura de um arquivo `.xlsx` com CNPJs
- Consulta automática via API (autenticada)
- Exportação dos dados consultados para Excel
- Interface gráfica com **Flet**

## 📦 Requisitos

- Python 3.9+
- Chave da API ReceitaWS 
- Instalar dependências:

```bash
pip install -r requirements.txt
```

## 📁 Formato do Excel de entrada

A aba deve se chamar `Input_CNPJ` e conter uma coluna chamada `CNPJ`.

## 🛡 Segurança

A chave da API fica no arquivo `.env`, que **não é enviado ao GitHub**.

