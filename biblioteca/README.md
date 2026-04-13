# 📚 BibliotecaBot – Chatbot de Busca de Livros

Chatbot desenvolvido com **Rasa Open Source** integrado à **Open Library API** para busca de livros por título, autor ou assunto — sem necessidade de chave de API.

---

## 📁 Estrutura do Projeto

```
biblioteca_bot/
├── actions/
│   └── actions.py        # 3 actions: buscar por título, autor e assunto
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
| `buscar livro Dom Casmurro` | Resultados por título |
| `livros do autor Machado de Assis` | Obras do autor |
| `livros sobre filosofia` | Livros por assunto |
| `procurar Harry Potter` | Resultados por título |
| `tchau` | Despedida |

---

## 🧩 Componentes principais

| Componente | Nome | Descrição |
|---|---|---|
| Entity | `titulo` | Captura o título do livro |
| Entity | `autor` | Captura o nome do autor |
| Entity | `assunto` | Captura o assunto/tema |
| Slot | `titulo / autor / assunto` | Armazenam os dados para as actions |
| Action | `action_buscar_titulo` | Busca por título na Open Library |
| Action | `action_buscar_autor` | Busca por autor na Open Library |
| Action | `action_buscar_assunto` | Busca por assunto na Open Library |

---

## 🌐 API Utilizada

**Open Library API** — https://openlibrary.org/developers/api

- ✅ Gratuita e sem necessidade de chave de API
- Busca por título, autor, ISBN e assunto
- Retorna metadados, edições e links para leitura online
