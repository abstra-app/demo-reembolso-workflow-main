"""
STEP 5: Montar Output Final

Responsabilidades:
- Receber os dados validados e avaliados do tasklet anterior
- Consolidar no formato final esperado
- Logar o resultado final
- Completar a task original
"""

from abstra.tasks import get_trigger_task
import json

print("=== STEP 5: Montar Output Final ===")

# Recebe a task do step anterior
task = get_trigger_task()
payload = task.payload

print(f"\nTask recebida: {task.id}")
print(f"Tipo da task: {task.type}")

# Extrai os dados finais
acoes_validadas = payload.get("acoes_validadas", [])
resposta_final = payload.get("resposta_final", "")
escalar_supervisor = payload.get("escalar_supervisor", False)
violacoes = payload.get("violacoes", [])
avaliacao_qualidade = payload.get("avaliacao_qualidade", {})

# ✅ IMPORTANTE: Extrai os dados da decisao de politica (Component 1)
contexto_original = payload.get("contexto_original", {})
decisao_politica = {
    "TIPO_SOLICITACAO": contexto_original.get("tipo_solicitacao", ""),
    "MOTIVO": contexto_original.get("motivo", ""),
    "ELEGIVEL": contexto_original.get("elegivel", False),
    "VALOR_REEMBOLSO": contexto_original.get("valor_reembolso", 0.0),
    "CODIGO_REGRA_APLICADA": contexto_original.get("codigo_regra_aplicada", ""),
    "RESTRICOES": contexto_original.get("restricoes", None)
}

# ✅ NOVO: Extrai o input_original completo (todos os dados que vieram no Step 1)
input_original = payload.get("input_original", {})

print(f"\n[CONSOLIDACAO] Montando output final...")

# Monta o output final no formato especificado
output_final = {
    "ACOES": acoes_validadas,
    "RESPOSTA_SUGERIDA": resposta_final,
    "ESCALAR_SUPERVISOR": escalar_supervisor,
    
    # ✅ ADICIONA: Dados da decisao de politica (Component 1)
    "decisao_politica": decisao_politica,
    
    # ✅ ADICIONA: Input original completo (todos os dados recebidos no Step 1)
    "input_original": input_original
}

print(f"\n{'='*60}")
print("OUTPUT FINAL DO WORKFLOW")
print(f"{'='*60}")
print(json.dumps(output_final, indent=2, ensure_ascii=False))
print(f"{'='*60}")

# Log de metricas
print(f"\n[METRICAS]")
print(f"  - Total de acoes: {len(acoes_validadas)}")
print(f"  - Tipos de acoes: {', '.join([a.get('tipo', 'N/A') for a in acoes_validadas])}")
print(f"  - Escalar supervisor: {escalar_supervisor}")
print(f"  - Violacoes detectadas: {len(violacoes)}")
if avaliacao_qualidade:
    print(f"  - Qualidade geral: {avaliacao_qualidade.get('qualidade_geral', 'N/A')}/10")
    print(f"  - Clareza: {avaliacao_qualidade.get('clareza', 'N/A')}/10")
    print(f"  - Empatia: {avaliacao_qualidade.get('empatia', 'N/A')}/10")

# Se houve violacoes, loga detalhes
if violacoes:
    print(f"\n[VIOLACOES DETECTADAS]")
    for i, v in enumerate(violacoes):
        print(f"  {i+1}. {v}")

# Se escalou para supervisor, loga motivo
if escalar_supervisor:
    print(f"\n[ALERTA] Caso escalado para supervisor")
    motivos = []
    if violacoes:
        motivos.append(f"{len(violacoes)} violacao(oes) de politica")
    if avaliacao_qualidade.get('qualidade_geral', 10) < 6:
        motivos.append("qualidade baixa da resposta")
    if motivos:
        print(f"  Motivos: {', '.join(motivos)}")

print("\n=== STEP 5 Concluido ===")
print("=== Workflow AgentePlanoResolucao Finalizado ===")

# Envia task com o output final no formato especificado
from abstra.tasks import send_task

print("\n[ENVIANDO TASK] Enviando output final para o workflow pai...")

send_task(
    type="plano_resolucao_completo",
    payload=output_final
)

print("✅ Task enviada com sucesso!")
print(f"   Tipo: plano_resolucao_completo")
print(f"   Payload: {len(acoes_validadas)} acoes, escalar={escalar_supervisor}")
print(f"   Decisao politica incluida: elegivel={decisao_politica.get('ELEGIVEL', False)}, valor=R$ {decisao_politica.get('VALOR_REEMBOLSO', 0):.2f}")
print(f"   Input original incluido: {len(input_original)} campos")

# Completa a task
task.complete()
