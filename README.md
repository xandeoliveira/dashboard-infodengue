# 📊 Dashboard InfoDengue

Este projeto é um dashboard desenvolvido em Python com Streamlit para visualização interativa de dados sobre casos de dengue, utilizando informações da API do InfoDengue e dados do IBGE. Pode ser acessado em [https://dashboard-infodengue.streamlit.app/](https://dashboard-infodengue.streamlit.app/).

## 📁 Estrutura do Projeto

```
dashboard-infodengue/
├── datasets/           # Dados locais em CSV para análise
├── notebooks/          # Notebooks de exploração e pré-processamento
├── ibge.py             # Funções auxiliares relacionadas ao IBGE
├── infodengue.py       # Funções para consumo e tratamento dos dados do InfoDengue
├── main.py             # App principal Streamlit
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação do projeto
```

## 🚀 Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/xandeoliveira/dashboard-infodengue.git
   cd dashboard-infodengue
   ```

2. (Opcional) Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate no Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o app:
   ```bash
   streamlit run main.py
   ```

## 🧠 Tecnologias e Bibliotecas

- Python 3.x
- Streamlit
- Pandas
- Matplotlib (via Jupyter)
- API InfoDengue

## 🛠️ Desenvolvimento

- `infodengue.py`: coleta e tratamento dos dados de casos de dengue via API pública.
- `ibge.py`: contém funções para obter informações os códigos municipais.
- `main.py`: interface visual do dashboard via Streamlit.

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais detalhes.