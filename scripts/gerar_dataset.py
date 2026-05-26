"""
Gerador reproduzivel do dataset Inova.PCD.

Gera 4 arquivos em data/:
- atividades.csv        (65 linhas, limpo)
- responsaveis.csv      (8 linhas)
- atividades_sujo.csv   (100 linhas, 35 com problemas)
- status_historico.csv  (138 transicoes)

Uso:
    python3 scripts/gerar_dataset.py

Dependencias:
    pip install pandas

Seeds:
    random.seed(42) - dataset principal
    random.seed(43) - versao suja + historico
"""
import csv
import random
import datetime
import os
import pandas as pd

random.seed(42)

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# DADOS BASE
# ============================================================
catalogo = {
    'Acessibilidade Digital': [
        ('Auditar contraste de cores no portal RH', 'Validar WCAG AA nos textos e botoes principais'),
        ('Implementar navegacao por teclado no sistema de chamados', 'Permitir uso completo sem mouse'),
        ('Adicionar atributos ARIA nos formularios institucionais', 'Labels, roles e descricoes para leitores de tela'),
        ('Testar leitor de tela NVDA na intranet', 'Cobertura das 10 paginas mais acessadas'),
        ('Configurar texto alternativo em imagens do site', 'Padronizar uso de alt em CMS'),
        ('Revisar estrutura semantica HTML do blog', 'Corrigir hierarquia de headings h1-h6'),
        ('Implementar modo alto contraste no dashboard', 'Botao de alternancia + persistencia da escolha'),
        ('Ajustar tempo de sessao para usuarios com necessidades cognitivas', 'Estender timeout configurave'),
        ('Adicionar legenda automatica em videos do canal interno', 'Integrar API de transcricao'),
        ('Documentar guia de acessibilidade para devs', 'Checklist WCAG aplicado ao stack interno'),
        ('Implementar atalhos de teclado no sistema de aprovacao', 'Mapear atalhos para acoes frequentes'),
        ('Corrigir foco visivel em elementos interativos', 'Outline customizado e visivel'),
        ('Validar zoom 200% sem perda de funcionalidade', 'Testar 5 telas criticas'),
        ('Auditar PDFs do RH com leitor de tela', 'Marcar PDFs nao acessiveis para refazer'),
    ],
    'Inclusao na Empregabilidade': [
        ('Mapear vagas abertas elegiveis para Lei de Cotas', 'Levantamento por departamento e nivel'),
        ('Estabelecer parceria com Instituto Caminhar', 'Reuniao com diretoria e contrato'),
        ('Adaptar processo seletivo com videos em Libras', 'Aplicar em 3 vagas piloto'),
        ('Treinar gestores sobre Lei 8.213/91', 'Workshop 2h com case real'),
        ('Revisar descricoes de vagas para linguagem inclusiva', 'Remover termos capacitistas'),
        ('Criar canal anonimo para feedback de candidatos PcD', 'Form + tratamento de dados'),
        ('Implementar etapa de entrevista com interprete', 'Disponivel sob demanda'),
        ('Estudar caso de empresa benchmark em inclusao', 'Documento com aprendizados aplicaveis'),
        ('Definir KPIs trimestrais de contratacao PcD', 'Meta por trimestre + responsaveis'),
        ('Avaliar adequacao do teste tecnico para candidatos com deficiencia visual', 'Adaptar para CLI ou leitor de tela'),
        ('Implementar acompanhamento dos primeiros 90 dias', 'Checkpoint quinzenal com novos colaboradores PcD'),
    ],
    'Tecnologia Assistiva': [
        ('Adquirir 5 teclados ergonomicos', 'Aprovacao + compra + distribuicao'),
        ('Avaliar softwares de transcricao automatica', 'Comparar 3 opcoes (Otter, Whisper, Verbit)'),
        ('Implantar legenda automatica nas reunioes Teams', 'Ativar globalmente + treinar usuarios'),
        ('Testar mouse adaptado para colaborador com mobilidade reduzida', 'Solicitar 2 modelos para teste'),
        ('Avaliar lupa eletronica para colaborador com baixa visao', 'Especificar modelo e fornecedor'),
        ('Configurar narrador do Windows nos PCs do laboratorio', 'Atalhos e perfis salvos'),
        ('Adquirir cadeira ergonomica adaptada', 'Pedido para 2 colaboradores'),
        ('Pesquisar headset com cancelamento de ruido para colaborador autista', 'Comparar 3 modelos'),
    ],
    'Comunicacao Inclusiva': [
        ('Contratar interprete de Libras part-time', 'Disponivel terca e quinta para reunioes'),
        ('Adicionar audiodescricao nos videos institucionais', 'Pipeline de pos-producao'),
        ('Criar guia de linguagem inclusiva', 'Documento publicado na wiki'),
        ('Adaptar comunicados internos para leitura facil', 'Versao simplificada paralela'),
        ('Implementar tag de acessibilidade nos posts internos', 'Sinaliza versao em Libras / leitura facil'),
        ('Revisar manual do colaborador com foco em clareza', 'Reduzir jargao e siglas'),
        ('Gravar versao em Libras das politicas internas', 'Top 5 documentos mais lidos'),
        ('Padronizar uso de emoji descritivo em comunicacoes', 'Evitar emoji sem contexto'),
    ],
    'Capacitacao de Equipes': [
        ('Workshop sobre etiqueta na convivencia com PcD', '2h presencial + online'),
        ('Treinamento Libras Basico para gestores', 'Curso 20h em 5 semanas'),
        ('Capacitacao em comunicacao inclusiva', 'Modulo de 4h para todos os times'),
        ('Treinar squad de produto em design inclusivo', 'Workshop pratico de 3h'),
        ('Sensibilizacao sobre deficiencias invisiveis', 'Painel com colaboradores PcD'),
        ('Capacitacao de RH em recrutamento inclusivo', 'Curso especifico de 8h'),
        ('Treinar lideres em adaptacao razoavel', 'Conceito e casos praticos'),
        ('Workshop com instituicao parceira sobre TEA', 'Convidar especialista externo'),
    ],
    'Adaptacao de Ambiente Fisico': [
        ('Instalar rampa de acesso no estacionamento', 'Lateral norte com aprovacao do sindico'),
        ('Adequar banheiros (PNE) no andar 3', 'Barras de apoio e largura de porta'),
        ('Implantar sinalizacao tatil nos corredores', 'Piso podo-tatil andares 1-5'),
        ('Avaliar acessibilidade da copa', 'Altura de pia e bebedouro'),
        ('Reservar vagas PcD no estacionamento', 'Pintura + placa + fiscalizacao'),
        ('Instalar piso podo-tatil na recepcao', 'Direcional e alerta'),
        ('Revisar iluminacao para colaboradores com baixa visao', 'Areas comuns e estacoes de trabalho'),
        ('Configurar elevador com voz e Braille', 'Validar instalacao + treino do porteiro'),
    ],
    'Plataforma Interna': [
        ('Implementar dashboard de metricas PcD', 'Vagas, contratacoes, retencao por trimestre'),
        ('Sistema interno de gestao de adaptacoes', 'Workflow de solicitacao e aprovacao'),
        ('Integrar API de traducao para Libras', 'Avaliar VLibras e Hand Talk'),
        ('Criar formulario de adaptacao razoavel', 'Padrao corporativo + fluxo de aprovacao'),
        ('Publicar relatorio anual de diversidade', 'Dados consolidados + comparativo anual'),
        ('Implementar onboarding diferenciado para PcD', 'Material em multiplos formatos'),
        ('Backup e versionamento das politicas de inclusao', 'Repositorio interno indexado'),
        ('Painel interno de tarefas com filtro por acessibilidade', 'Marca tarefas com requisitos especiais'),
    ],
}

responsaveis = [
    ('Ana Ribeiro', 'Dev Front', 'Tecnologia', 3, 'sim'),
    ('Bruno Costa', 'Designer UX', 'Produto', 5, 'sim'),
    ('Camila Lopes', 'Product Manager', 'Produto', 4, 'nao'),
    ('Diego Martins', 'Dev Back', 'Tecnologia', 2, 'nao'),
    ('Eduarda Souza', 'Especialista Acessibilidade', 'Pessoas e Cultura', 7, 'sim'),
    ('Felipe Andrade', 'QA', 'Tecnologia', 3, 'sim'),
    ('Gabriela Pinto', 'Dev Full', 'Tecnologia', 1, 'nao'),
    ('Henrique Alves', 'Analista Comunicacao', 'Marketing', 4, 'sim'),
]

publico_alvo_pool = ['Visual', 'Auditiva', 'Motora', 'Intelectual', 'Geral', 'Geral', 'Geral']
status_pool = ['concluida'] * 40 + ['andamento'] * 30 + ['pendente'] * 30
prioridade_pool = ['alta'] * 25 + ['media'] * 50 + ['baixa'] * 25

# Janela temporal
data_inicial = datetime.date(2025, 11, 1)
data_final = datetime.date(2026, 5, 25)
delta_dias = (data_final - data_inicial).days

# ============================================================
# 1) ATIVIDADES.CSV
# ============================================================
linhas = []
task_id = 1
for categoria, lista in catalogo.items():
    for titulo, desc in lista:
        status = random.choice(status_pool)
        prio = random.choice(prioridade_pool)
        resp = random.choice(responsaveis)
        publico = random.choice(publico_alvo_pool)
        estimativa = random.choice([2, 4, 8, 16, 24, 40, 60, 80])

        if status == 'pendente':
            horas_gastas = 0
        elif status == 'andamento':
            horas_gastas = random.randint(1, max(1, estimativa - 1))
        else:
            horas_gastas = int(estimativa * random.uniform(0.7, 1.4))

        dias_offset = random.randint(0, delta_dias - 1)
        data_criacao = data_inicial + datetime.timedelta(days=dias_offset)
        if status == 'concluida':
            dias_ate_conc = random.randint(2, 60)
            data_conclusao = data_criacao + datetime.timedelta(days=dias_ate_conc)
            if data_conclusao > data_final:
                data_conclusao = data_final
            data_conclusao_str = data_conclusao.isoformat()
        else:
            data_conclusao_str = ''

        linhas.append({
            'id': task_id,
            'titulo': titulo,
            'descricao': desc,
            'categoria': categoria,
            'status': status,
            'prioridade': prio,
            'responsavel': resp[0],
            'papel_responsavel': resp[1],
            'publico_alvo': publico,
            'estimativa_horas': estimativa,
            'horas_gastas': horas_gastas,
            'data_criacao': data_criacao.isoformat(),
            'data_conclusao': data_conclusao_str,
        })
        task_id += 1

random.shuffle(linhas)
for i, l in enumerate(linhas, 1):
    l['id'] = i

campos = ['id','titulo','descricao','categoria','status','prioridade',
          'responsavel','papel_responsavel','publico_alvo','estimativa_horas',
          'horas_gastas','data_criacao','data_conclusao']

with open(os.path.join(OUT_DIR, 'atividades.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=campos)
    w.writeheader()
    w.writerows(linhas)
print(f'OK atividades.csv ({len(linhas)} linhas)')

# ============================================================
# 2) RESPONSAVEIS.CSV
# ============================================================
with open(os.path.join(OUT_DIR, 'responsaveis.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['nome', 'papel', 'departamento', 'anos_empresa', 'formacao_acessibilidade'])
    w.writerows(responsaveis)
print(f'OK responsaveis.csv ({len(responsaveis)} linhas)')

# ============================================================
# 3) STATUS_HISTORICO.CSV
# ============================================================
random.seed(43)
ativ = pd.read_csv(os.path.join(OUT_DIR, 'atividades.csv'))
historico = []
for _, row in ativ.iterrows():
    tid = int(row['id'])
    criacao = pd.to_datetime(row['data_criacao']).date()
    status = row['status']

    historico.append({
        'task_id': tid, 'status_anterior': '', 'status_novo': 'pendente',
        'data_mudanca': criacao.isoformat()
    })

    if status in ('andamento', 'concluida'):
        dias = random.randint(1, 15)
        data_and = criacao + datetime.timedelta(days=dias)
        historico.append({
            'task_id': tid, 'status_anterior': 'pendente', 'status_novo': 'andamento',
            'data_mudanca': data_and.isoformat()
        })

    if status == 'concluida':
        data_conc = pd.to_datetime(row['data_conclusao']).date()
        historico.append({
            'task_id': tid, 'status_anterior': 'andamento', 'status_novo': 'concluida',
            'data_mudanca': data_conc.isoformat()
        })

with open(os.path.join(OUT_DIR, 'status_historico.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['task_id','status_anterior','status_novo','data_mudanca'])
    w.writeheader()
    w.writerows(historico)
print(f'OK status_historico.csv ({len(historico)} transicoes)')

# ============================================================
# 4) ATIVIDADES_SUJO.CSV
# ============================================================
sujas = []
proximo_id = len(ativ) + 1

# (a) 5 duplicatas exatas
for _ in range(5):
    base = ativ.sample(1).iloc[0].to_dict()
    base['id'] = proximo_id
    sujas.append(base)
    proximo_id += 1

# (b) 5 datas invalidas
for d in ['2026-02-30', '2025-13-15', '31/04/2026', 'abril 2026', '']:
    base = ativ.sample(1).iloc[0].to_dict()
    base['id'] = proximo_id
    base['data_criacao'] = d
    sujas.append(base)
    proximo_id += 1

# (c) 5 valores faltantes
for _ in range(5):
    base = ativ.sample(1).iloc[0].to_dict()
    base['id'] = proximo_id
    campo = random.choice(['titulo', 'responsavel', 'categoria'])
    base[campo] = ''
    sujas.append(base)
    proximo_id += 1

# (d) 5 enums com ruido
for s in [' concluida', 'Pendente', 'ANDAMENTO', 'concluída', 'concluida ']:
    base = ativ.sample(1).iloc[0].to_dict()
    base['id'] = proximo_id
    base['status'] = s
    sujas.append(base)
    proximo_id += 1

# (e) 5 inconsistencias logicas
for _ in range(5):
    base = ativ.sample(1).iloc[0].to_dict()
    base['id'] = proximo_id
    erro = random.choice(['conc_sem_data', 'pend_com_horas', 'data_invertida'])
    if erro == 'conc_sem_data':
        base['status'] = 'concluida'
        base['data_conclusao'] = ''
    elif erro == 'pend_com_horas':
        base['status'] = 'pendente'
        base['horas_gastas'] = random.randint(5, 30)
    elif erro == 'data_invertida':
        base['data_conclusao'] = '2025-01-15'
    sujas.append(base)
    proximo_id += 1

# (f) 10 outliers numericos
for _ in range(10):
    base = ativ.sample(1).iloc[0].to_dict()
    base['id'] = proximo_id
    erro = random.choice(['hr_negativa', 'hr_absurda', 'estim_zero'])
    if erro == 'hr_negativa':
        base['horas_gastas'] = -5
    elif erro == 'hr_absurda':
        base['horas_gastas'] = 9999
    elif erro == 'estim_zero':
        base['estimativa_horas'] = 0
    sujas.append(base)
    proximo_id += 1

df_sujo = pd.concat([ativ, pd.DataFrame(sujas)], ignore_index=True)
df_sujo.to_csv(os.path.join(OUT_DIR, 'atividades_sujo.csv'), index=False)
print(f'OK atividades_sujo.csv ({len(df_sujo)} linhas, {len(sujas)} com problemas)')

print()
print('Dataset gerado em', OUT_DIR)
