from abstra.forms import (
    MarkdownOutput,
    TextOutput,
    MultipleChoiceInput,
    run
)
from abstra.tasks import get_tasks
import json

print("=== Iniciando Formulário de Análise de Casos ===")

# Busca todas as tasks pendentes de análise
tasks_pendentes = [t for t in get_tasks() if t.type == "analisar_caso"]

print(f"Tasks pendentes de análise: {len(tasks_pendentes)}")

if not tasks_pendentes:
    run([[
        MarkdownOutput("""
# 📋 Análise de Casos Pós-Venda

## Nenhum caso pendente de análise

Todos os casos foram analisados ou não há casos processados ainda.

Execute o **Orquestrador Pós-Venda** para gerar novos casos para análise.
        """)
    ]])
    print("Nenhuma task pendente encontrada. Finalizando.")
    exit()

# Processa cada task pendente
for idx, task in enumerate(tasks_pendentes, 1):
    print(f"\n--- Processando task {idx}/{len(tasks_pendentes)} ---")
    print(f"Task ID: {task.id}")
    
    # Extrai os dados do payload
    caso = task.payload
    
    input_original = caso.get("input_original", {})
    decisao_politica = caso.get("decisao_politica", {})
    plano_e_resposta = caso.get("plano_e_resposta", {})
    
    # Formata as ações planejadas
    acoes = plano_e_resposta.get("ACOES", [])
    acoes_formatadas = ""
    for i, acao in enumerate(acoes, 1):
        acoes_formatadas += f"\n**Ação {i}:** {acao.get('tipo', 'N/A')}"
        if 'valor' in acao:
            acoes_formatadas += f" - R$ {acao['valor']:.2f}"
        if 'motivo' in acao:
            acoes_formatadas += f"\n- Motivo: {acao['motivo']}"
        if 'tag' in acao:
            acoes_formatadas += f"\n- Tag: {acao['tag']}"
        if 'nova_data' in acao:
            acoes_formatadas += f"\n- Nova Data: {acao['nova_data']}"
        if 'canal' in acao:
            acoes_formatadas += f"\n- Canal: {acao['canal']}"
        acoes_formatadas += "\n"
    
    # Monta a página de análise
    pagina_analise = [
        MarkdownOutput(f"""
# 📋 Análise de Caso Pós-Venda

**Caso {idx} de {len(tasks_pendentes)}**

---

## 1️⃣ INPUT ORIGINAL (Solicitação do Cliente)

**Cenário:** {caso.get('cenario_teste', 'N/A')}

**Booking ID:** {input_original.get('booking_id', 'N/A')}

**Canal de Venda:** {input_original.get('canal_venda', 'N/A')}

**Data da Viagem:** {input_original.get('data_viagem', 'N/A')}

**Data da Solicitação:** {input_original.get('data_solicitacao', 'N/A')}

**Valor Pago:** R$ {input_original.get('valor_pago', 0):.2f}

**Texto da Solicitação:**

> "{input_original.get('texto_solicitacao', 'N/A')}"

---

## 2️⃣ OUTPUT DAS REGRAS DE POLÍTICA (Motor de Políticas)

**Tipo de Solicitação:** {decisao_politica.get('TIPO_SOLICITACAO', 'N/A')}

**Motivo:** {decisao_politica.get('MOTIVO', 'N/A')}

**Elegível:** {'✅ SIM' if decisao_politica.get('ELEGIVEL') else '❌ NÃO'}

**Valor de Reembolso:** R$ {decisao_politica.get('VALOR_REEMBOLSO', 0):.2f}

**Código da Regra Aplicada:** {decisao_politica.get('CODIGO_REGRA_APLICADA', 'N/A')}

**Restrições:** {decisao_politica.get('RESTRICOES') or 'Nenhuma'}

---

## 3️⃣ DECISÃO DA IA E FUNDAMENTO (Agente de Resolução)

### 📌 Ações Planejadas:
{acoes_formatadas}

### 💬 Resposta Sugerida ao Cliente:

> "{plano_e_resposta.get('RESPOSTA_SUGERIDA', 'N/A')}"

### 🚨 Escalar para Supervisor:

{'✅ SIM' if plano_e_resposta.get('ESCALAR_SUPERVISOR') else '❌ NÃO'}

---

## 4️⃣ CONCLUSÃO FINAL

O sistema processou este caso através de:
1. **Motor de Políticas** - Aplicou regras determinísticas baseadas em políticas da empresa
2. **Agente de IA** - Gerou um plano de ação personalizado e uma resposta empática

**Status:** Aguardando análise humana
        """),
        MultipleChoiceInput(
            key="acao",
            label="Marcar este caso como:",
            options=[
                {"label": "✅ Analisado", "value": "analisado"},
                {"label": "⏭️ Pular para o próximo", "value": "pular"}
            ],
            required=True
        )
    ]
    
    # Executa a página
    state = run([pagina_analise])
    
    acao = state["acao"]
    
    if acao == "analisado":
        # Completa a task
        task.complete()
        print(f"✅ Task {task.id} marcada como analisada e completada")
        
        # Mostra confirmação
        run([[
            MarkdownOutput(f"""
# ✅ Caso Analisado!

O caso **{input_original.get('booking_id', 'N/A')}** foi marcado como analisado.

{'**Próximo caso em seguida...**' if idx < len(tasks_pendentes) else '**Todos os casos foram analisados!**'}
            """)
        ]])
    else:
        print(f"⏭️ Task {task.id} pulada pelo usuário")
        
        # Mostra mensagem de pulo
        run([[
            MarkdownOutput("""
# ⏭️ Caso Pulado

Este caso permanece pendente de análise.

**Próximo caso em seguida...**
            """)
        ]])

# Mensagem final
print(f"\n=== Análise Finalizada ===")
print(f"Total de tasks processadas: {len(tasks_pendentes)}")

run([[
    MarkdownOutput("""
# 🎉 Análise Concluída!

Você revisou todos os casos disponíveis.

Para analisar novos casos, execute novamente este formulário ou processe mais casos no **Orquestrador Pós-Venda**.
    """)
]])
