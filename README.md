# 📈 Painel Interativo - Cotações & Previsão do Tempo

Aplicação web desenvolvida em Python para acompanhamento em tempo real de cotações financeiras (USD, EUR, BTC) e dados de previsão meteorológica por geolocalização.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Interface Web:** Streamlit
- **Análise & Manipulação de Dados:** Pandas / OpenPyXL
- **Consumo de APIs:** Requests
- **Deploy:** Streamlit Community Cloud

## ⚡ Funcionalidades

- **Cotações Financeiras:** Consulta via API REST com suporte a cabeçalhos customizados (*User-Agent*) e gestão de resiliência (*Rate Limit HTTP 429*).
- **Geolocalização & Clima:** Consulta meteorológica com base em coordenadas de latitude e longitude.
- **Persistência Local:** Atualização automatizada de métricas e histórico em planilha Excel.
- **UI Customizada:** Design modular responsivo com injeção de CSS customizado.

## 📂 Estrutura do Repositório

```text
├── app.py                # Código principal da aplicação
├── Cotações.xlsx         # Ficheiro de persistência de dados
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação do projeto
