# 📊 Inova.PCD — Dataset de Iniciativa de Inclusão

Dataset oficial do **Projeto Final da Formação Full Stack** do programa **Inova.PCD da Telos**.

Conjunto de dados curado para simular uma **iniciativa corporativa real de inclusão de pessoas com deficiência (PCD)** em uma empresa de tecnologia. Pensado para popular um sistema de gestão de atividades, alimentar dashboards e servir de entrada para análises em Python.

---

## 🎯 Para que serve

Este dataset apoia o projeto final em 3 fases (uma por semana):

| Semana | Uso |
|---|---|
| **Semana 1** — Back-end | Popular MongoDB via script seed (~65 tarefas prontas) |
| **Semana 2** — Front-end | Alimentar dashboard com dados reais (não lista vazia) |
| **Semana 3** — Python | Entrada para análise, limpeza de dados e visualizações |

O schema foi desenhado para **bater diretamente** com a model `Task` esperada no back-end (Node.js + Mongoose):

| Coluna do CSV | Campo da Task |
|---|---|
| `titulo` | `title` |
| `descricao` | `desc` |
| `status` | `status` (enum: `pendente`/`andamento`/`concluida`) |
| `prioridade` | `prio` (enum: `alta`/`media`/`baixa`) |
| `categoria` | `story` |
| `data_criacao` | `created` |

> Campos extras (`responsavel`, `publico_alvo`, `estimativa_horas`, `horas_gastas`, `data_conclusao`) **não exigem mudança no schema** — servem para análise.

---

## 📁 Arquivos

```
data/
├── atividades.csv           65 linhas  | dataset principal (limpo)
├── atividades_sujo.csv     100 linhas  | versão com 35 erros propositais
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

### `atividades_sujo.csv` — Para exercício de limpeza de dados

Mesma estrutura de `atividades.csv` (100 linhas), mas com **35 problemas propositais**:

| Tipo | Qtd | Exemplo |
|---|---|---|
| Duplicatas exatas | 5 | Mesma tarefa com `id` diferente |
| Datas inválidas | 5 | `2026-02-30`, `31/04/2026`, formato textual |
| Valores faltantes | 5 | `titulo` ou `responsavel` em branco |
| Enums com ruído | 5 | `' concluida'`, `'Pendente'`, `'ANDAMENTO'` |
| Inconsistências lógicas | 5 | `status=concluida` sem `data_conclusao` |
| Outliers numéricos | 10 | `horas_gastas=-5`, `=9999`, `estimativa_horas=0` |

Use para exercitar `drop_duplicates`, `str.strip()`, `pd.to_datetime(errors='coerce')`, validação cross-field.

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

### Carregar em Python (local)

```python
import pandas as pd

ativ = pd.read_csv('data/atividades.csv')
resp = pd.read_csv('data/responsaveis.csv')

print(ativ.head())
print(ativ['status'].value_counts())
```

### Carregar no navegador (Pyodide)

```python
import pandas as pd
import io
from pyodide.http import pyfetch

resp = await pyfetch('/data/atividades.csv')
df = pd.read_csv(io.StringIO(await resp.string()))
```

### Carregar no JavaScript (front-end)

```js
const resp = await fetch('/data/atividades.csv');
const texto = await resp.text();
// recomenda-se PapaParse para parsing robusto
```

### Importar no MongoDB

```bash
# Usar o seed script do projeto referência (backend/scripts/seed.js)
node backend/scripts/seed.js
```

Ou direto com `mongoimport`:

```bash
mongoimport --db taskinsight --collection atividades \
            --type csv --headerline \
            --file data/atividades.csv
```

### Abrir em Excel / Numbers / Google Sheets

- Excel/Numbers: duplo clique no `.csv`
- Google Sheets: `Arquivo > Importar > Upload`
- Encoding: UTF-8 (padrão)

---

## 🎯 12 análises sugeridas

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

### Limpeza de dados (médio — usa `atividades_sujo.csv`)
9. Detectar e remover duplicatas
10. Normalizar enums (`str.strip()`, `str.lower()`)
11. Validar datas (`pd.to_datetime(errors='coerce')`)

### Séries temporais (avançado — usa `status_historico.csv`)
12. Lead time médio mensal

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
c['data_criacao'] = pd.to_datetime(c['data_criacao'])
c['data_conclusao'] = pd.to_datetime(c['data_conclusao'])
c['lead_time'] = (c['data_conclusao'] - c['data_criacao']).dt.days
c.groupby('formacao_acessibilidade')['lead_time'].mean()

# Limpeza
sujo = pd.read_csv('data/atividades_sujo.csv')
sujo['status'] = sujo['status'].str.strip().str.lower()
sujo = sujo[sujo['status'].isin(['pendente', 'andamento', 'concluida'])]
sujo = sujo.drop_duplicates(subset=['titulo', 'responsavel', 'data_criacao'])
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
| "Base pode ser populada ainda mais pelos colaboradores" | Schema documentado, reproduzível, fácil de estender |

### Atende às análises sugeridas para a Semana 3

O documento oficial cita três análises mínimas. Todas têm exemplo pronto no README:

| Análise sugerida no documento | Onde está no dataset |
|---|---|
| "Média de tarefas concluídas" | `(df['status'] == 'concluida').mean()` aplicado a `atividades.csv` |
| "Limpeza de dados duplicados" | `atividades_sujo.csv` traz 5 duplicatas propositais (e mais 30 outros tipos de erro) |
| "Visualização básica" | 12 análises sugeridas no README + estrutura compatível com Chart.js e Matplotlib |

### Alinhamento com o Trello do projeto

O dataset apoia diretamente vários cards do Trello do projeto (tanto na versão **sequencial** quanto na **em paralelo**):

| Card do Trello | Como o dataset apoia |
|---|---|
| `Modelar Banco de Dados (Users e Tasks)` | Schema das colunas valida a model `Task` escolhida — o `seed.js` importa o CSV sem erro se a modelagem estiver correta |
| `Implementar CRUD de Tarefas` | 65 tarefas reais como volume de teste para o CRUD |
| `Implementar Script de Análise de Dados em Python` | Entrada direta do script — sem precisar criar dados de teste |
| `Gerar Primeiras Métricas de Produtividade` | Métricas naturais: taxa de conclusão, lead time, sobrecarga por responsável |
| `Criar Visualizações de Dados da Plataforma` | 12 análises sugeridas no README cobrem distribuições, agregações e séries temporais |
| `Testar API Completa no Postman/Insomnia` | Dataset populado ajuda nos testes de `GET /tasks` (lista não-vazia, filtros) |

> 💡 **Importante**: o Trello organiza o backlog **da squad** (tarefas de desenvolvimento). O dataset entrega os **dados de domínio** que vão ser geridos pela aplicação. São camadas diferentes — e por isso se complementam sem sobreposição.

---

## ⚠️ Limitações e premissas

- **Dataset sintético plausível**: tarefas fictícias baseadas em práticas reais de iniciativas de inclusão em empresas brasileiras de tecnologia. Não representam empresa específica.
- **Período curto** (~6 meses): suficiente para análise descritiva, limitado para tendências de longo prazo.
- **Nomes de responsáveis são fictícios**: não são pessoas reais.
- **Sem ruído na versão limpa**: `atividades.csv` está 100% consistente. Use `atividades_sujo.csv` para exercícios de qualidade de dados.

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
