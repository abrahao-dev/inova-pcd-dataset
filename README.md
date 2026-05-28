# 📊 Inova.PCD — Dataset de Iniciativa de Inclusão

Dataset oficial do **Projeto Final da Formação Full Stack** do programa **Inova.PCD da Telos**.

Conjunto de dados curado para simular uma **iniciativa corporativa real de inclusão de pessoas com deficiência (PCD)** em uma empresa de tecnologia. Pensado para popular um sistema de gestão de atividades, alimentar dashboards e servir de entrada para análises em Python.

> 📚 **Tudo neste README amarra ao que vocês já viram no curso.** Especificamente nos **Níveis 7 e 8** (Node + Express + Mongoose + MongoDB Atlas) e no **Nível 5** (Pandas pra análise). Se travar, voltem nas aulas — não é matéria nova.

---

## 🎯 Para que serve

Este dataset apoia o projeto final em 3 fases (uma por semana):

| Semana | Uso |
|---|---|
| **Semana 1** — Back-end | Popular MongoDB Atlas via **Compass Import** (mesmo fluxo da **Aula 09 · Nível 8**) — 65 tarefas prontas |
| **Semana 2** — Front-end | Alimentar dashboard com dados reais (não lista vazia) |
| **Semana 3** — Python | Entrada para análise, métricas e visualizações |

O schema foi desenhado para **bater diretamente** com a model `Task` esperada no back-end (Node.js + Mongoose):

| Coluna do CSV | Campo da Task (exemplo) |
|---|---|
| `titulo` | `title` |
| `descricao` | `desc` |
| `status` | `status` (enum: `pendente`/`andamento`/`concluida`) |
| `prioridade` | `prio` (enum: `alta`/`media`/`baixa`) |
| `categoria` | `story` |
| `data_criacao` | `created` |

> Campos extras (`responsavel`, `publico_alvo`, `estimativa_horas`, `horas_gastas`, `data_conclusao`) **não exigem mudança no schema** — servem para análise.

> 💡 **Atalho recomendado:** deixem o schema da Task com os nomes em **português** (`titulo`, `descricao`, `prioridade`, ...). Assim os documentos importados via Compass batem direto com o schema, sem precisar renomear campo nenhum. Só mantenham o mesmo padrão no front e na API.

---

## 📁 Arquivos

```
data/
├── atividades.csv           65 linhas  | dataset principal
├── responsaveis.csv          8 linhas  | pessoas (para JOIN)
└── status_historico.csv    138 linhas  | transições de status no tempo
```

### `atividades.csv` — Dataset principal

A "fonte da verdade". Use para popular o banco e fazer análises base.

**Colunas (13)**:
| Coluna | Tipo | Exemplo |
|---|---|---|
| `id` | int | `1` |
| `titulo` | string | `Auditar contraste de cores no portal RH` |
| `descricao` | string | `Validar WCAG AA nos textos e botoes principais` |
| `categoria` | string | `Acessibilidade Digital` |
| `status` | enum | `pendente` / `andamento` / `concluida` |
| `prioridade` | enum | `alta` / `media` / `baixa` |
| `responsavel` | string | `Ana Ribeiro` |
| `papel_responsavel` | string | `Dev Front` |
| `publico_alvo` | string | `Visual` / `Auditiva` / `Motora` / `Intelectual` / `Geral` |
| `estimativa_horas` | int | `8` |
| `horas_gastas` | int | `9` |
| `data_criacao` | date `YYYY-MM-DD` | `2025-11-15` |
| `data_conclusao` | date ou vazio | `2026-01-08` |

**Categorias (7 eixos da iniciativa)**:
- `Acessibilidade Digital` — WCAG, ARIA, leitores de tela
- `Inclusao na Empregabilidade` — Lei 8.213/91, processo seletivo
- `Tecnologia Assistiva` — Hardware/software adaptados
- `Comunicacao Inclusiva` — Libras, audiodescrição, linguagem acessível
- `Capacitacao de Equipes` — Treinamentos, sensibilização
- `Adaptacao de Ambiente Fisico` — Rampas, banheiros, sinalização tátil
- `Plataforma Interna` — Ferramentas, dashboards, automações

**Distribuição**:
```
Status:        46% concluída  |  34% pendente   |  20% andamento
Prioridade:    49% média      |  29% baixa      |  22% alta
Público-alvo:  43% Geral      |  23% Auditiva   |  14% Motora  |  12% Visual  |  8% Intelectual
Período:       novembro/2025 a maio/2026
```

### `responsaveis.csv` — Para exercitar JOIN

Informações complementares dos 8 colaboradores responsáveis. Coluna `nome` é chave de junção com `atividades.responsavel`.

| Coluna | Descrição |
|---|---|
| `nome` | Nome completo (chave) |
| `papel` | Cargo |
| `departamento` | Tecnologia, Produto, Pessoas e Cultura, Marketing |
| `anos_empresa` | Tempo de casa |
| `formacao_acessibilidade` | `sim` / `nao` |

### `status_historico.csv` — Linha do tempo das tarefas

Log de cada transição de status (`pendente → andamento → concluida`) com timestamp. Útil para análise de séries temporais.

| Coluna | Descrição |
|---|---|
| `task_id` | ID da tarefa (FK com `atividades.id`) |
| `status_anterior` | Status antes da mudança (vazio na criação) |
| `status_novo` | Novo status |
| `data_mudanca` | Quando ocorreu (`YYYY-MM-DD`) |

---

## 🚀 Como usar

### Importar no MongoDB Atlas (via Compass) — método da Aula 09 · Nível 8

> ⚠️ **Único método ensinado no curso.** Sem `mongoimport` CLI, sem script Node/Mongoose extra. É o mesmo passo a passo da **Aula 09 — Nível 8 (MongoDB Atlas)**.

1. **Criar cluster** no [MongoDB Atlas](https://www.mongodb.com/atlas) (free tier M0 — basta e-mail)
2. **Database Access** → criar usuário com senha (anota a senha)
3. **Network Access** → liberar IP (em sala: `0.0.0.0/0` pra todo mundo conseguir conectar)
4. **Connect → Compass** → copia a connection string (`mongodb+srv://...`)
5. Abre o **MongoDB Compass**, cola a string, conecta
6. Cria o banco (ex: nome da squad) e a collection `tasks`
7. Na collection → **ADD DATA → Import JSON or CSV file**
8. Seleciona `data/atividades.csv`, marca **CSV** com **First row is header**, confirma

Pronto — 65 documentos importados, mesmo fluxo da aula.

> 💡 A mesma connection string vai no `.env` do back-end como `MONGO_URI` (igual ao que vocês fizeram na **Aula 04 — Nível 8** com `.env` e na **Aula 07 — Nível 8** ao conectar via Mongoose).

> ⚠️ **Squad decide os nomes.** Nome do banco, nome dos campos no schema da Task — escolhas da squad. Os nomes neste README são só exemplos.

### Carregar em Python (Sprint 3)

```python
import pandas as pd

ativ = pd.read_csv('data/atividades.csv')
resp = pd.read_csv('data/responsaveis.csv')

print(ativ.head())
print(ativ['status'].value_counts())
```

### Carregar no navegador (Pyodide — opcional)

```python
import pandas as pd
import io
from pyodide.http import pyfetch

resp = await pyfetch('/data/atividades.csv')
df = pd.read_csv(io.StringIO(await resp.string()))
```

### Carregar no JavaScript (front-end — opcional)

```js
const resp = await fetch('/data/atividades.csv');
const texto = await resp.text();
// Parser CSV: PapaParse ou split simples respeitando aspas
```

### Abrir em Excel / Numbers / Google Sheets

- Excel/Numbers: duplo clique no `.csv`
- Google Sheets: `Arquivo > Importar > Upload`
- Encoding: UTF-8 (padrão)

---

## 🔧 Setup do back-end (cola pra Sprint 1)

> 📚 **Vocês já estudaram tudo isso no curso.** Esta seção só amarra o dataset ao que vocês fizeram nas aulas:
>
> | Aula | Pra que serve aqui |
> |---|---|
> | **Nível 7 · Aulas 12–14** | Estruturando uma API: rotas, CRUD de usuários, organização da aplicação |
> | **Nível 8 · Aulas 02, 03** | Login + JWT |
> | **Nível 8 · Aula 04** | Variáveis de ambiente (`.env`) |
> | **Nível 8 · Aulas 07, 10, 11** | Mongoose: conexão, CRUD, hooks |
> | **Nível 8 · Aula 09** | MongoDB Atlas (cluster + Compass) |
> | **Nível 8 · Aula 12** | CRUD de Filmes — o gabarito mais próximo: troquem **Filme → Task** |

### 1. Mapeamento CSV → schema Mongoose

O CSV vem em português. Quando vocês modelarem o schema da `Task` (igual fizeram com o de Filmes na **Aula 12 N8**), o caminho mais simples é manter os nomes em português pra bater direto com o CSV importado:

```
titulo       → titulo
descricao    → descricao
status       → status
prioridade   → prioridade
categoria    → categoria
data_criacao → data_criacao
```

Se a squad preferir nomes em inglês (`title`, `desc`, `prio`, `story`, `created`), também funciona — só lembrem que os documentos importados via Compass virão com os nomes do CSV, então vocês precisarão renomear (pelo Compass campo a campo, ou via `updateMany` no `mongosh`). Discutam em squad qual caminho preferem.

> 💡 **Atalho recomendado:** schema em português = zero conversão. Só mantenham o mesmo padrão no front e na API.

### 2. Estrutura de pastas recomendada (back-end)

Mesma convenção que vocês usaram no **CRUD de Filmes (Aula 12 N8)** — só trocando "Filme" por "Task":

```
backend/
├── server.js                  # Entrypoint: cria o Express, conecta no Mongo, escuta a porta
├── config/
│   └── db.js                  # Função connectDB() — encapsula mongoose.connect()
├── models/
│   ├── User.js                # Schema do usuário (name, email, password)
│   └── Task.js                # Schema da tarefa (titulo, descricao, status, prioridade, categoria, user)
├── routes/
│   ├── authRoutes.js          # POST /register, POST /login (públicas)
│   └── taskRoutes.js          # GET, POST, PUT, DELETE /tasks (protegidas por JWT)
├── controllers/
│   ├── authController.js      # Lógica de register e login (bcrypt + JWT) — Aula 02/03 N8
│   └── taskController.js      # Lógica do CRUD de tarefas — Aula 12 N8 (CRUD Filmes)
└── middlewares/
    └── auth.js                # Valida o JWT do header e anexa req.user
```

**Princípio** (igual à **Aula 14 N7 — Organizando aplicação**):
- `routes/` só **define URLs** e aponta para o controller (zero lógica de negócio)
- `controllers/` tem a **lógica de negócio** (regras, validações, chamadas ao banco)
- `models/` define a **forma dos dados** (schema Mongoose)
- `middlewares/` faz **validação ANTES da rota** (ex: checar JWT)
- `config/` isola **configurações** (conexão DB, variáveis de ambiente)

### 3. `.env` mínimo (Aula 04 · Nível 8)

```env
MONGO_URI=mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/<nome-do-banco>?retryWrites=true&w=majority
JWT_SECRET=troque-isso-por-uma-string-longa-e-aleatoria
PORT=3000
```

> ⚠️ Nunca commite o `.env`. Adicione `.env` no `.gitignore`.

### 4. Fluxo JWT em uma frase

> **Usuário loga → backend valida senha → gera token → cliente guarda → manda token em toda request → middleware decodifica ANTES de chegar no controller.**

Diagrama mental:

```
1) POST /login                            2) Toda request protegida
   email + senha                             Header: x-auth-token: <jwt>
        │                                            │
        ▼                                            ▼
   bcrypt.compare()                             middleware/auth.js
        │                                            │
        ▼                                            ▼
   jwt.sign({user:{id}}, SECRET)                jwt.verify(token, SECRET)
        │                                            │
        ▼                                            ▼
   Retorna { token }                            req.user = decoded.user
                                                     │
                                                     ▼
                                               controller executa
```

**Pontos-chave**:
- O token é **assinado** com `JWT_SECRET` (variável de ambiente) — qualquer alteração no token invalida a assinatura
- O token **não é criptografado**, é apenas codificado em base64. **Nunca coloque senha no payload**
- Padrão de payload: `{ user: { id: <ObjectId> } }`, expiração `1h`
- Sem token ou token inválido → o middleware retorna `401` e o controller nem é chamado

---

## 🎯 10 análises sugeridas (Sprint 3 — Nível 5)

### Estatística descritiva (fácil)
1. Distribuição por status
2. Distribuição por categoria
3. Distribuição por público-alvo

### Agregações com `groupby` (médio)
4. Taxa de conclusão por categoria
5. Horas estimadas vs reais (gap de estimativa)
6. Carga de trabalho por responsável

### JOIN entre arquivos (médio)
7. Departamentos que mais entregam
8. Formação em acessibilidade × velocidade de entrega

### Séries temporais (avançado — usa `status_historico.csv`)
9. Lead time médio mensal
10. Tarefas "presas" em andamento por muito tempo

### Exemplos rápidos

```python
# Taxa de conclusão por categoria
ativ.groupby('categoria')['status'].apply(
    lambda s: (s == 'concluida').mean() * 100
).round(1).sort_values(ascending=False)

# JOIN: formação × lead time
ativ = pd.read_csv('data/atividades.csv')
resp = pd.read_csv('data/responsaveis.csv')
df = ativ.merge(resp, left_on='responsavel', right_on='nome')
c = df[df['status'] == 'concluida'].copy()
c['data_criacao']   = pd.to_datetime(c['data_criacao'])
c['data_conclusao'] = pd.to_datetime(c['data_conclusao'])
c['lead_time']      = (c['data_conclusao'] - c['data_criacao']).dt.days
c.groupby('formacao_acessibilidade')['lead_time'].mean()
```

---

## ✅ Aderência ao escopo oficial

O dataset foi desenhado para casar diretamente com os requisitos do **Projeto Final da Formação Full Stack — Inova.PCD**.

### Atende ao documento oficial do projeto

| Requisito do documento | Como o dataset atende |
|---|---|
| Cenário de "tarefas" (um dos 3 sugeridos) | Tarefas reais de iniciativa de inclusão PCD |
| Atributos: identificação do item | Coluna `id` |
| Atributos: categoria/tipo | Coluna `categoria` (7 eixos) |
| Atributos: valores numéricos | `estimativa_horas`, `horas_gastas` |
| Atributos: datas (criação, atualização, conclusão) | `data_criacao`, `data_conclusao` + `status_historico.csv` (linha do tempo de atualizações) |
| Atributos: status | Coluna `status` (enum) |
| "Base personalizada visando adaptar ao contexto" | Tema alinhado ao propósito do programa Inova.PCD |
| "Base pode ser populada ainda mais pelos colaboradores" | Schema documentado, fácil de estender |

### Atende às análises sugeridas para a Semana 3

| Análise sugerida no documento | Onde está no dataset |
|---|---|
| "Média de tarefas concluídas" | `(df['status'] == 'concluida').mean()` aplicado a `atividades.csv` |
| "Visualização básica" | 10 análises sugeridas no README + estrutura compatível com Chart.js e Matplotlib |

### Alinhamento com o Trello do projeto

O dataset apoia diretamente vários cards do Trello do projeto (tanto na versão **sequencial** quanto na **em paralelo**):

| Card do Trello | Como o dataset apoia |
|---|---|
| `Modelar Banco de Dados (Users e Tasks)` | Schema das colunas valida a model `Task` escolhida — o import via Compass (Aula 09 N8) carrega o CSV direto na collection |
| `Implementar CRUD de Tarefas` | 65 tarefas reais como volume de teste para o CRUD |
| `Implementar Script de Análise de Dados em Python` | Entrada direta do script — sem precisar criar dados de teste |
| `Gerar Primeiras Métricas de Produtividade` | Métricas naturais: taxa de conclusão, lead time, sobrecarga por responsável |
| `Criar Visualizações de Dados da Plataforma` | 10 análises sugeridas no README cobrem distribuições, agregações e séries temporais |
| `Testar API Completa no Postman/Insomnia` | Dataset populado ajuda nos testes de `GET /tasks` (lista não-vazia, filtros) |

> 💡 **Importante**: o Trello organiza o backlog **da squad** (tarefas de desenvolvimento). O dataset entrega os **dados de domínio** que vão ser geridos pela aplicação. São camadas diferentes — e por isso se complementam sem sobreposição.

---

## ⚠️ Limitações e premissas

- **Dataset sintético plausível**: tarefas fictícias baseadas em práticas reais de iniciativas de inclusão em empresas brasileiras de tecnologia. Não representam empresa específica.
- **Período curto** (~6 meses): suficiente para análise descritiva, limitado para tendências de longo prazo.
- **Nomes de responsáveis são fictícios**: não são pessoas reais.

---

## 📚 Referências contextuais

- **Lei Brasileira de Inclusão (LBI)** — Lei 13.146/2015
- **Lei de Cotas** — Lei 8.213/91, Art. 93
- **WCAG 2.1** — Web Content Accessibility Guidelines (W3C)
- **eMAG** — Modelo de Acessibilidade em Governo Eletrônico

---

## 📄 Licença

Dataset distribuído sob licença **MIT** — uso livre para fins educacionais e comerciais, mantida atribuição.

---

**Mantido por**: Telos — Programa Inova.PCD
**Versão**: 1.0 (maio/2026)
