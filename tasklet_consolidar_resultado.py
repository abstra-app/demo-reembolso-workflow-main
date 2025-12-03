from abstra.tasks import get_trigger_task, get_tasks, send_task
import json

print("=== Iniciando Consolidação de Resultado ===")

# Recebe a task que disparou este tasklet (vem do Component 2)
task_trigger = get_trigger_task()

print(f"Task recebida: {task_trigger.id}")
print(f"Task type: {task_trigger.type}")

# O payload da task do Component 2 contém apenas o plano e resposta
plano_e_resposta = task_trigger.payload

print("\n--- Plano e Resposta (Component 2) ---")
print(json.dumps(plano_e_resposta, indent=2, ensure_ascii=False))

# O Component 2 JÁ ENVIA os dados completos no payload!
# Vamos extrair diretamente do payload recebido
print("\n🔍 Extraindo dados do payload recebido...")
print(f"Chaves no payload: {list(plano_e_resposta.keys())}")

# Extrai input_original e decisao_politica que já vêm no payload
input_original = plano_e_resposta.get("input_original", {})
decisao_politica = plano_e_resposta.get("decisao_politica", {})

print(f"\n✅ Input original encontrado: {bool(input_original)}")
if input_original:
    print(f"   Campos: {list(input_original.keys())}")
    print(f"   Booking ID: {input_original.get('booking_id', 'N/A')}")
    print(f"   Cenário: {input_original.get('cenario_teste', 'N/A')}")

print(f"\n✅ Decisão política encontrada: {bool(decisao_politica)}")
if decisao_politica:
    print(f"   Campos: {list(decisao_politica.keys())}")
    print(f"   Tipo: {decisao_politica.get('TIPO_SOLICITACAO', 'N/A')}")
    print(f"   Elegível: {decisao_politica.get('ELEGIVEL', False)}")

# Se não encontrou os dados, cria estrutura vazia
if not input_original:
    print("\n⚠️ Input original não encontrado no payload")
    input_original = {
        "cenario_teste": "DESCONHECIDO",
        "booking_id": "N/A",
        "canal_venda": "N/A",
        "data_viagem": "N/A",
        "data_solicitacao": "N/A",
        "valor_pago": 0,
        "texto_solicitacao": "N/A"
    }

if not decisao_politica:
    print("\n⚠️ Decisão de política não encontrada no payload")
    decisao_politica = {
        "TIPO_SOLICITACAO": "N/A",
        "MOTIVO": "N/A",
        "ELEGIVEL": False,
        "VALOR_REEMBOLSO": 0,
        "CODIGO_REGRA_APLICADA": "N/A",
        "RESTRICOES": None
    }

# Monta o objeto consolidado
resultado_consolidado = {
    "cenario_teste": input_original.get("cenario_teste", "DESCONHECIDO") if input_original else "DESCONHECIDO",
    "input_original": input_original if input_original else {},
    "decisao_politica": decisao_politica if decisao_politica else {},
    "plano_e_resposta": {
        "ACOES": plano_e_resposta.get("ACOES", []),
        "RESPOSTA_SUGERIDA": plano_e_resposta.get("RESPOSTA_SUGERIDA", ""),
        "ESCALAR_SUPERVISOR": plano_e_resposta.get("ESCALAR_SUPERVISOR", False)
    }
}

# Exibe o resultado consolidado de forma formatada
print("\n" + "=" * 80)
print("RESULTADO CONSOLIDADO - DEMO PÓS-VENDA")
print("=" * 80)

print(f"\n📋 CENÁRIO: {resultado_consolidado['cenario_teste']}")

print("\n" + "-" * 80)
print("1️⃣  INPUT ORIGINAL (Solicitação do Cliente)")
print("-" * 80)
if resultado_consolidado['input_original']:
    print(f"Booking ID: {resultado_consolidado['input_original'].get('booking_id', 'N/A')}")
    print(f"Canal de Venda: {resultado_consolidado['input_original'].get('canal_venda', 'N/A')}")
    print(f"Data Viagem: {resultado_consolidado['input_original'].get('data_viagem', 'N/A')}")
    print(f"Data Solicitação: {resultado_consolidado['input_original'].get('data_solicitacao', 'N/A')}")
    valor_pago = resultado_consolidado['input_original'].get('valor_pago', 0)
    print(f"Valor Pago: R$ {valor_pago if valor_pago else 0:.2f}")
    print(f"\nTexto da Solicitação:")
    print(f'"{resultado_consolidado["input_original"].get("texto_solicitacao", "N/A")}"')
else:
    print("⚠️  Dados não encontrados")

print("\n" + "-" * 80)
print("2️⃣  DECISÃO DE POLÍTICA (Component 1 - Motor de Políticas)")
print("-" * 80)
if resultado_consolidado['decisao_politica']:
    print(f"Tipo de Solicitação: {resultado_consolidado['decisao_politica'].get('TIPO_SOLICITACAO', 'N/A')}")
    print(f"Motivo: {resultado_consolidado['decisao_politica'].get('MOTIVO', 'N/A')}")
    print(f"Elegível: {'✅ SIM' if resultado_consolidado['decisao_politica'].get('ELEGIVEL') else '❌ NÃO'}")
    valor_reembolso = resultado_consolidado['decisao_politica'].get('VALOR_REEMBOLSO', 0)
    print(f"Valor Reembolso: R$ {valor_reembolso if valor_reembolso else 0:.2f}")
    print(f"Código Regra Aplicada: {resultado_consolidado['decisao_politica'].get('CODIGO_REGRA_APLICADA', 'N/A')}")
    restricoes = resultado_consolidado['decisao_politica'].get('RESTRICOES')
    print(f"Restrições: {restricoes if restricoes else 'Nenhuma'}")
else:
    print("⚠️  Dados não encontrados")

print("\n" + "-" * 80)
print("3️⃣  PLANO E RESPOSTA (Component 2 - Agente de Resolução)")
print("-" * 80)

acoes = resultado_consolidado['plano_e_resposta']['ACOES']
print(f"\n📌 AÇÕES PLANEJADAS ({len(acoes)} ações):")
for i, acao in enumerate(acoes, 1):
    print(f"\n  Ação {i}:")
    print(f"    Tipo: {acao.get('tipo', 'N/A')}")
    if 'valor' in acao:
        print(f"    Valor: R$ {acao['valor']:.2f}")
    if 'motivo' in acao:
        print(f"    Motivo: {acao['motivo']}")
    if 'tag' in acao:
        print(f"    Tag: {acao['tag']}")
    if 'nova_data' in acao:
        print(f"    Nova Data: {acao['nova_data']}")
    if 'canal' in acao:
        print(f"    Canal: {acao['canal']}")

print(f"\n💬 RESPOSTA SUGERIDA:")
print(f'"{resultado_consolidado["plano_e_resposta"]["RESPOSTA_SUGERIDA"]}"')

escalar = resultado_consolidado['plano_e_resposta']['ESCALAR_SUPERVISOR']
print(f"\n🚨 ESCALAR PARA SUPERVISOR: {'✅ SIM' if escalar else '❌ NÃO'}")

print("\n" + "=" * 80)
print("FIM DO RESULTADO CONSOLIDADO")
print("=" * 80)

# Também salva o JSON completo para referência
print("\n📄 JSON COMPLETO:")
print(json.dumps(resultado_consolidado, indent=2, ensure_ascii=False))

# Envia task para análise do caso
print("\n📤 Enviando task para análise do caso...")

send_task(
    "analisar_caso",
    resultado_consolidado
)

print("✅ Task de análise enviada com sucesso!")

# Completa a task
task_trigger.complete()

print("\n=== Consolidação Finalizada ===")
