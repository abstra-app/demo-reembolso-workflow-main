from abstra.forms import CardsInput, MarkdownOutput, run
from abstra.tasks import send_task

print("=== Iniciando Orquestrador de Pós-Venda ===")

# Dicionário com os 10 cenários de teste variados
cenarios = {
    "CASE_1_CLASSICO_APROVADO": {
        "booking_id": "BR12345",
        "canal_venda": "SITE",
        "data_viagem": "2025-01-15",
        "data_solicitacao": "2024-12-03",
        "valor_pago": 450.0,
        "texto_solicitacao": "Olá, preciso cancelar minha viagem de São Paulo para Rio de Janeiro marcada para 15/01/2025. Tive um imprevisto familiar e não poderei mais viajar. Gostaria de solicitar o reembolso do valor pago (R$ 450,00). Comprei o bilhete pelo site no dia 10/11/2024. Meu booking é BR12345."
    },
    "CASE_2_CLASSICO_NEGADO": {
        "booking_id": "ABC789",
        "canal_venda": "APP",
        "data_viagem": "2024-12-04",
        "data_solicitacao": "2024-12-03",
        "valor_pago": 280.0,
        "texto_solicitacao": "Oi, minha viagem é amanhã mas não vou conseguir ir. Posso pedir reembolso? Booking ABC789."
    },
    "CASE_3_NUANCE_VIP_EMERGENCIA": {
        "booking_id": "VIP789",
        "canal_venda": "APP",
        "data_viagem": "2024-12-04",
        "data_solicitacao": "2024-12-04",
        "valor_pago": 680.0,
        "texto_solicitacao": "Olá, sou cliente há 5 anos e viajo com vocês mensalmente. Infelizmente tive uma emergência médica ontem à noite e não consegui viajar hoje. Sei que estou fora do prazo, mas gostaria de solicitar uma exceção devido à situação. Tenho atestado médico. Booking: VIP789. Valor: R$ 680,00."
    },
    "CASE_4_NUANCE_RECLAMACAO_GRAVE": {
        "booking_id": "ANGRY123",
        "canal_venda": "SITE",
        "data_viagem": "2024-12-02",
        "data_solicitacao": "2024-12-03",
        "valor_pago": 420.0,
        "texto_solicitacao": "Isso é um absurdo! O ônibus atrasou 4 HORAS, não tinha ar condicionado funcionando, e o motorista foi extremamente grosseiro quando reclamei. Perdi uma reunião importantíssima de trabalho. Vou postar isso em todas as redes sociais e no Reclame Aqui se não resolverem! Booking: ANGRY123. Paguei R$ 420,00."
    },
    "CASE_5_NUANCE_LIMITE_24H": {
        "booking_id": "LIMIT456",
        "canal_venda": "SITE",
        "data_viagem": "2024-12-04",
        "data_solicitacao": "2024-12-03",
        "valor_pago": 350.0,
        "texto_solicitacao": "Olá, preciso cancelar minha viagem de amanhã. Estou enviando este email às 14h30 e minha viagem é amanhã às 14h45, então são exatamente 24h e 15 minutos de antecedência. Booking: LIMIT456. Valor: R$ 350,00."
    },
    "CASE_6_CLASSICO_RECLAMACAO": {
        "booking_id": "",
        "canal_venda": "PRESENCIAL",
        "data_viagem": "",
        "data_solicitacao": "2024-12-03",
        "valor_pago": 0.0,
        "texto_solicitacao": "Gostaria de registrar uma reclamação sobre o atendimento no guichê da rodoviária. O funcionário foi extremamente grosseiro e mal educado comigo quando fui tirar uma dúvida sobre horários. Isso é inaceitável!"
    },
    "CASE_7_NUANCE_PRIMEIRA_VIAGEM": {
        "booking_id": "NEWBIE001",
        "canal_venda": "SITE",
        "data_viagem": "2024-12-10",
        "data_solicitacao": "2024-12-03",
        "valor_pago": 85.0,
        "texto_solicitacao": "Olá, é minha primeira vez comprando passagem de ônibus online. Acabei de perceber que comprei a passagem para São Paulo-Campinas mas eu queria Campinas-São Paulo (sentido contrário). Comprei há 10 minutos. Posso cancelar e comprar a correta? Booking: NEWBIE001. Valor: R$ 85,00."
    },
    "CASE_8_NUANCE_IDOSO": {
        "booking_id": "SENIOR123",
        "canal_venda": "PRESENCIAL",
        "data_viagem": "2024-12-04",
        "data_solicitacao": "2024-12-03",
        "valor_pago": 180.0,
        "texto_solicitacao": "Bom dia, sou aposentado de 78 anos e não entendo muito de internet. Meu neto me ajudou a comprar a passagem mas ele viajou e eu não consegui cancelar antes. Tentei ligar várias vezes mas a linha estava sempre ocupada. Minha viagem é amanhã mas não posso mais ir por motivos de saúde. Booking: SENIOR123. Valor: R$ 180,00."
    },
    "CASE_9_CLASSICO_PARCIAL": {
        "booking_id": "PARTIAL789",
        "canal_venda": "APP",
        "data_viagem": "2024-12-13",
        "data_solicitacao": "2024-12-03",
        "valor_pago": 300.0,
        "texto_solicitacao": "Preciso cancelar minha passagem. Comprei pelo app há 2 semanas, a viagem é daqui 10 dias. Booking PARTIAL789. Valor pago foi R$ 300,00."
    },
    "CASE_10_NUANCE_CORPORATIVO": {
        "booking_id": "BR-CORP-001",
        "canal_venda": "SITE",
        "data_viagem": "2025-01-20",
        "data_solicitacao": "2024-12-03",
        "valor_pago": 450.0,
        "texto_solicitacao": "Prezados, somos a empresa XYZ Ltda e compramos 15 passagens para uma viagem corporativa que foi cancelada. Este é apenas um dos bookings (BR-CORP-001), mas temos mais 14 com valores similares. Gostaríamos de negociar o reembolso de todas de uma vez. Valor total: R$ 6.750,00. Este booking: R$ 450,00."
    }
}

# Monta os cards com as informações de cada cenário
cards_options = [
    {
        "title": "CASE_1_CLASSICO_APROVADO",
        "subtitle": "🟢 CLÁSSICO - Reembolso Aprovado",
        "description": f"\"{cenarios['CASE_1_CLASSICO_APROVADO']['texto_solicitacao'][:120]}...\"",
        "topLeftExtra": f"🎫 {cenarios['CASE_1_CLASSICO_APROVADO']['booking_id']}",
        "topRightExtra": f"R$ {cenarios['CASE_1_CLASSICO_APROVADO']['valor_pago']:.2f}"
    },
    {
        "title": "CASE_2_CLASSICO_NEGADO",
        "subtitle": "🔴 CLÁSSICO - Reembolso Negado",
        "description": f"\"{cenarios['CASE_2_CLASSICO_NEGADO']['texto_solicitacao']}\"",
        "topLeftExtra": f"🎫 {cenarios['CASE_2_CLASSICO_NEGADO']['booking_id']}",
        "topRightExtra": f"R$ {cenarios['CASE_2_CLASSICO_NEGADO']['valor_pago']:.2f}"
    },
    {
        "title": "CASE_3_NUANCE_VIP_EMERGENCIA",
        "subtitle": "🟡 NUANCE - Cliente VIP + Emergência",
        "description": f"\"{cenarios['CASE_3_NUANCE_VIP_EMERGENCIA']['texto_solicitacao'][:120]}...\"",
        "topLeftExtra": f"🎫 {cenarios['CASE_3_NUANCE_VIP_EMERGENCIA']['booking_id']}",
        "topRightExtra": f"R$ {cenarios['CASE_3_NUANCE_VIP_EMERGENCIA']['valor_pago']:.2f}"
    },
    {
        "title": "CASE_4_NUANCE_RECLAMACAO_GRAVE",
        "subtitle": "🔥 NUANCE - Reclamação Grave + Risco",
        "description": f"\"{cenarios['CASE_4_NUANCE_RECLAMACAO_GRAVE']['texto_solicitacao'][:120]}...\"",
        "topLeftExtra": f"🎫 {cenarios['CASE_4_NUANCE_RECLAMACAO_GRAVE']['booking_id']}",
        "topRightExtra": f"R$ {cenarios['CASE_4_NUANCE_RECLAMACAO_GRAVE']['valor_pago']:.2f}"
    },
    {
        "title": "CASE_5_NUANCE_LIMITE_24H",
        "subtitle": "🟠 NUANCE - Limite 24h (Zona Cinzenta)",
        "description": f"\"{cenarios['CASE_5_NUANCE_LIMITE_24H']['texto_solicitacao'][:120]}...\"",
        "topLeftExtra": f"🎫 {cenarios['CASE_5_NUANCE_LIMITE_24H']['booking_id']}",
        "topRightExtra": f"R$ {cenarios['CASE_5_NUANCE_LIMITE_24H']['valor_pago']:.2f}"
    },
    {
        "title": "CASE_6_CLASSICO_RECLAMACAO",
        "subtitle": "🟢 CLÁSSICO - Reclamação de Atendimento",
        "description": f"\"{cenarios['CASE_6_CLASSICO_RECLAMACAO']['texto_solicitacao']}\"",
        "topLeftExtra": "🎫 Sem booking",
        "topRightExtra": "R$ 0.00"
    },
    {
        "title": "CASE_7_NUANCE_PRIMEIRA_VIAGEM",
        "subtitle": "💙 NUANCE - Primeira Viagem + Erro Recente",
        "description": f"\"{cenarios['CASE_7_NUANCE_PRIMEIRA_VIAGEM']['texto_solicitacao'][:120]}...\"",
        "topLeftExtra": f"🎫 {cenarios['CASE_7_NUANCE_PRIMEIRA_VIAGEM']['booking_id']}",
        "topRightExtra": f"R$ {cenarios['CASE_7_NUANCE_PRIMEIRA_VIAGEM']['valor_pago']:.2f}"
    },
    {
        "title": "CASE_8_NUANCE_IDOSO",
        "subtitle": "👴 NUANCE - Idoso + Dificuldade Tecnológica",
        "description": f"\"{cenarios['CASE_8_NUANCE_IDOSO']['texto_solicitacao'][:120]}...\"",
        "topLeftExtra": f"🎫 {cenarios['CASE_8_NUANCE_IDOSO']['booking_id']}",
        "topRightExtra": f"R$ {cenarios['CASE_8_NUANCE_IDOSO']['valor_pago']:.2f}"
    },
    {
        "title": "CASE_9_CLASSICO_PARCIAL",
        "subtitle": "🟡 CLÁSSICO - Reembolso Parcial (80%)",
        "description": f"\"{cenarios['CASE_9_CLASSICO_PARCIAL']['texto_solicitacao']}\"",
        "topLeftExtra": f"🎫 {cenarios['CASE_9_CLASSICO_PARCIAL']['booking_id']}",
        "topRightExtra": f"R$ {cenarios['CASE_9_CLASSICO_PARCIAL']['valor_pago']:.2f}"
    },
    {
        "title": "CASE_10_NUANCE_CORPORATIVO",
        "subtitle": "💼 NUANCE - Cliente Corporativo + Alto Valor",
        "description": f"\"{cenarios['CASE_10_NUANCE_CORPORATIVO']['texto_solicitacao'][:120]}...\"",
        "topLeftExtra": f"🎫 {cenarios['CASE_10_NUANCE_CORPORATIVO']['booking_id']}",
        "topRightExtra": f"R$ {cenarios['CASE_10_NUANCE_CORPORATIVO']['valor_pago']:.2f}"
    }
]

# Página de seleção de cenário com cards
page_selecao = [
    MarkdownOutput("""
# Orquestrador de Pós-Venda - Demo

Selecione um dos **10 cenários de teste** para simular o fluxo completo de pós-venda:

**Legenda:**
- 🟢 **CLÁSSICO**: Casos diretos e previsíveis
- 🟡 **NUANCE**: Casos que exigem análise contextual
- 🔥 **CRÍTICO**: Casos com risco reputacional

- **Motor de Políticas** (Component 1): aplica regras determinísticas
- **Agente de Resolução** (Component 2): gera plano de ação e resposta com IA

O resultado consolidado será exibido ao final.
    """),
    CardsInput(
        key="cenario_teste",
        label="Escolha o cenário de teste",
        options=cards_options,
        required=True,
        searchable=True,
        multiple=False
    )
]

# Executa o form
state = run([page_selecao])

# O CardsInput retorna o card selecionado como um dicionário
# Usamos o campo 'title' para identificar qual cenário foi escolhido
card_selecionado = state["cenario_teste"]
cenario_selecionado = card_selecionado["title"]
print(f"Cenário selecionado: {cenario_selecionado}")

# Monta o payload do cenário selecionado
payload = cenarios[cenario_selecionado]

print(f"Payload montado para booking_id: {payload['booking_id']}")
print(f"Texto da solicitação: {payload['texto_solicitacao'][:50]}...")

# Adiciona o cenário ao payload para rastreamento
payload["cenario_teste"] = cenario_selecionado

# Envia task para o Component 1 (MotorPoliticasPosVenda)
send_task(
    "solicitar_politica",
    payload
)

print("Task enviada para o Component 1: MotorPoliticasPosVenda")

# Página de confirmação
page_confirmacao = [
    MarkdownOutput(f"""
# ✅ Cenário Enviado para Processamento

**Cenário:** {cenario_selecionado}

**Booking ID:** {payload['booking_id']}

**Fluxo de execução:**
1. ✅ Payload montado e enviado
2. ⏳ Motor de Políticas processando...
3. ⏳ Agente de Resolução gerando plano...
4. ⏳ Consolidando resultado final...

O resultado consolidado será exibido no próximo stage.
    """)
]

run([page_confirmacao])

print("=== Form Orquestrador Finalizado ===")
