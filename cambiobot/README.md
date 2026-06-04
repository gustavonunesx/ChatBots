# 💱 CambioBot – Assistente de Câmbio em Tempo Real

Chatbot desenvolvido com **Rasa Open Source** para conversão de moedas em tempo real usando a **ExchangeRate-API**.

---

## 📁 Estrutura do Projeto

```
cambiobot/
├── actions/
│   └── actions.py        # action_converter_moeda + action_listar_moedas
├── data/
│   ├── nlu.yml           # Intenções e entidades
│   ├── stories.yml       # Histórias de conversa
│   └── rules.yml         # Regras fixas
├── config.yml            # Pipeline NLU e políticas
├── domain.yml            # Intents, slots, entities, responses, actions
├── endpoints.yml         # Servidor de actions
├── credentials.yml       # Canais de comunicação
└── README.md
```

---

## 🔑 Configurar a API Key

1. Acesse https://www.exchangerate-api.com e crie uma conta gratuita
2. Copie sua API Key
3. Cole no arquivo `actions/actions.py`:
```python
API_KEY = "SUA_API_KEY_AQUI"
```

### Testar via curl:
```bash
curl https://v6.exchangerate-api.com/v6/SUA_API_KEY/pair/USD/BRL/100
```

---

## ⚙️ Como executar

### 1. Ativar o ambiente
```bash
conda activate chatbot
```

### 2. Treinar o modelo
```bash
rasa train
```

### 3. Terminal 1 – Servidor de actions
```bash
rasa run actions
```

### 4. Terminal 2 – Iniciar o chat
```bash
rasa shell --endpoints endpoints.yml
```

---

## 💬 Exemplos de uso

| Mensagem do usuário | Resposta esperada |
|---|---|
| `oi` | Saudação de boas-vindas |
| `Converta 100 dólares para reais` | Conversão com cotação em tempo real |
| `Quanto é 50 euros em dólares?` | Resultado da conversão |
| `1000 reais em libras` | Conversão BRL → GBP |
| `quais moedas você suporta?` | Lista de moedas disponíveis |
| `tchau` | Despedida |

---

## 🧩 Componentes principais

| Componente | Nome | Descrição |
|---|---|---|
| Entity | `moeda_origem` | Moeda de partida |
| Entity | `moeda_destino` | Moeda de destino |
| Entity | `valor` | Quantia a converter |
| Slot | `moeda_origem / moeda_destino / valor` | Armazenam os dados para a action |
| Action | `action_converter_moeda` | Consulta a API e retorna o resultado |
| Action | `action_listar_moedas` | Lista as moedas suportadas |

---

## 🌍 Moedas suportadas

| Código | Moeda |
|---|---|
| BRL | Real Brasileiro |
| USD | Dólar Americano |
| EUR | Euro |
| GBP | Libra Esterlina |
| JPY | Iene Japonês |
| ARS | Peso Argentino |
| MXN | Peso Mexicano |
| CHF | Franco Suíço |
| CAD | Dólar Canadense |
| AUD | Dólar Australiano |
| CNY | Yuan Chinês |
