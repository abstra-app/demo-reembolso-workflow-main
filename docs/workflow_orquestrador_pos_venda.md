# Workflow Pai – `OrquestradorPosVenda`

Workflow responsável por **disparar cenários de teste de pós-venda**, chamar dois **Components** em sequência e exibir o resultado final consolidado.

No contexto deste projeto:

- **Component 1 (Workflow Filho 1):** `MotorPoliticasPosVenda`
- **Component 2 (Workflow Filho 2):** `AgentePlanoResolucao`

Ambos são workflows filhos que serão **adicionados ao projeto como Components** e reutilizados pelo workflow pai.

Fluxo macro:

1. Formulário inicial: escolha de **1 entre 5 cenários de teste**.  
2. Construção de um payload de solicitação a partir do cenário escolhido.  
3. Chamada do **Component `MotorPoliticasPosVenda`**.  
4. Chamada do **Component `AgentePlanoResolucao`**.  
5. Tasklet final que imprime o resultado consolidado para uso na demo.

---

## 1. Formulário inicial

### 1.1. Campo do formulário

O workflow pai inicia com um form contendo:

- Campo: `cenario_teste`  
  - Tipo: seleção (enum)  
  - Opções:
    - `CASE_1_CANCELAMENTO_ANTECIPADO`
    - `CASE_2_ATRASO_OPERACIONAL_GRAVE`
    - `CASE_3_NO_SHOW_TARIFA_RESTRITA`
    - `CASE_4_REMARCACAO`
    - `CASE_5_RECLAMACAO_SERVICO_ATENDIMENTO`

`cenario_teste` é o único input explícito do workflow pai na interface.

---

## 2. Construção do payload de solicitação

Após o form, um step de código (por exemplo, `montar_payload_cenario`) converte o valor de `cenario_teste` em um **payload de solicitação** com o seguinte formato genérico:

```json
{
  "booking_id": "string",
  "canal_venda": "string",
  "data_viagem": "string",
  "data_solicitacao": "string",
  "valor_pago": 0,
  "texto_solicitacao": "string"
}
```

Este payload será enviado como input para o Component `MotorPoliticasPosVenda`.

### 2.1. `CASE_1_CANCELAMENTO_ANTECIPADO`

Descrição: cancelamento antecipado, tom neutro/cordial.

```json
{
  "booking_id": "CB-20251220-001",
  "canal_venda": "app",
  "data_viagem": "2025-12-20",
  "data_solicitacao": "2025-12-18",
  "valor_pago": 199.90,
  "texto_solicitacao": "Oi, tive um imprevisto e não vou mais conseguir viajar. Queria cancelar e, se possível, receber o reembolso do valor da passagem. Obrigada!"
}
```

### 2.2. `CASE_2_ATRASO_OPERACIONAL_GRAVE`

Descrição: atraso operacional grave, cliente insatisfeito, risco alto.

```json
{
  "booking_id": "CB-20251205-045",
  "canal_venda": "web",
  "data_viagem": "2025-12-05",
  "data_solicitacao": "2025-12-06",
  "valor_pago": 259.50,
  "texto_solicitacao": "O ônibus atrasou mais de 3 horas, perdi um compromisso importante e ninguém deu informação nenhuma. É a segunda vez que isso acontece com vocês. Quero meu dinheiro de volta e sinceramente não sei se volto a comprar."
}
```

### 2.3. `CASE_3_NO_SHOW_TARIFA_RESTRITA`

Descrição: no-show por erro do cliente, tarifa restrita, pedido de exceção.

```json
{
  "booking_id": "CB-20251210-077",
  "canal_venda": "parceiro",
  "data_viagem": "2025-12-10",
  "data_solicitacao": "2025-12-11",
  "valor_pago": 180.00,
  "texto_solicitacao": "Comprei a passagem errada no horário e acabei perdendo o ônibus. Foi culpa minha, mas queria ver se é possível algum tipo de reembolso ou crédito."
}
```

### 2.4. `CASE_4_REMARCACAO`

Descrição: pedido de remarcação simples, tom colaborativo.

```json
{
  "booking_id": "CB-20251222-090",
  "canal_venda": "app",
  "data_viagem": "2025-12-22",
  "data_solicitacao": "2025-12-20",
  "valor_pago": 210.00,
  "texto_solicitacao": "Oi, tive uma mudança de planos e queria apenas remarcar minha viagem para o dia seguinte, se possível. Não preciso de reembolso, só trocar o horário."
}
```

### 2.5. `CASE_5_RECLAMACAO_SERVICO_ATENDIMENTO`

Descrição: reclamação de atendimento, sem pedido de reembolso explícito.

```json
{
  "booking_id": "CB-20251215-120",
  "canal_venda": "web",
  "data_viagem": "2025-12-15",
  "data_solicitacao": "2025-12-16",
  "valor_pago": 150.00,
  "texto_solicitacao": "A viagem até que correu bem, mas o atendimento no guichê foi péssimo, a atendente foi grossa e me deixou bem desconfortável. Não estou pedindo reembolso, só gostaria que registrassem a reclamação."
}
```

---

## 3. Relação com o Component `MotorPoliticasPosVenda` (Workflow Filho 1)

O **`MotorPoliticasPosVenda`** é um workflow filho que será **adicionado ao projeto como um Component** e reutilizado pelo `OrquestradorPosVenda` e por outros workflows.

### 3.1. O que o Component faz (do ponto de vista do workflow pai)

Do ponto de vista do workflow pai, o Component `MotorPoliticasPosVenda`:

- Recebe o payload da solicitação.  
- Aplica regras determinísticas de política de pós-venda.  
- Retorna uma **decisão de política estruturada**.

### 3.2. Input enviado ao Component `MotorPoliticasPosVenda`

Para qualquer cenário, o workflow pai envia ao Component:

```json
{
  "booking_id": "string",
  "canal_venda": "string",
  "data_viagem": "string",
  "data_solicitacao": "string",
  "valor_pago": 0,
  "texto_solicitacao": "string"
}
```

Mapeamento:

- `booking_id` → do payload do cenário  
- `canal_venda` → do payload do cenário  
- `data_viagem` → do payload do cenário  
- `data_solicitacao` → do payload do cenário  
- `valor_pago` → do payload do cenário  
- `texto_solicitacao` → do payload do cenário  

### 3.3. Output recebido do Component `MotorPoliticasPosVenda`

O workflow pai recebe do Component a decisão de política neste formato:

```json
{
  "TIPO_SOLICITACAO": "string",
  "MOTIVO": "string",
  "ELEGIVEL": true,
  "VALOR_REEMBOLSO": 0,
  "CODIGO_REGRA_APLICADA": "string",
  "RESTRICOES": "string or null"
}
```

Campos disponíveis no contexto do pai:

- `TIPO_SOLICITACAO`  
- `MOTIVO`  
- `ELEGIVEL`  
- `VALOR_REEMBOLSO`  
- `CODIGO_REGRA_APLICADA`  
- `RESTRICOES`

O workflow pai não altera esses valores; apenas os reutiliza como input do próximo Component.

---

## 4. Relação com o Component `AgentePlanoResolucao` (Workflow Filho 2)

O **`AgentePlanoResolucao`** é outro workflow filho que será **adicionado ao projeto como Component**. Ele consome a decisão de política do primeiro Component e gera plano + resposta usando IA.

### 4.1. O que o Component faz (do ponto de vista do workflow pai)

Do ponto de vista do workflow pai, o Component `AgentePlanoResolucao`:

- Recebe:
  - o texto da solicitação do cliente, e  
  - a decisão de política retornada pelo `MotorPoliticasPosVenda`.  
- Gera um **plano de ações estruturado** (`ACOES`).  
- Gera uma **resposta sugerida** para o cliente (`RESPOSTA_SUGERIDA`).  
- Indica se o caso deve ser **escalado para um supervisor** (`ESCALAR_SUPERVISOR`).

### 4.2. Input enviado ao Component `AgentePlanoResolucao`

O workflow pai monta o input combinando texto original + decisão de política:

```json
{
  "texto_solicitacao": "string",
  "TIPO_SOLICITACAO": "string",
  "MOTIVO": "string",
  "ELEGIVEL": true,
  "VALOR_REEMBOLSO": 0,
  "CODIGO_REGRA_APLICADA": "string",
  "RESTRICOES": "string or null"
}
```

Mapeamento:

- `texto_solicitacao` → texto original do payload do cenário  
- `TIPO_SOLICITACAO` → do Component `MotorPoliticasPosVenda`  
- `MOTIVO` → do Component `MotorPoliticasPosVenda`  
- `ELEGIVEL` → do Component `MotorPoliticasPosVenda`  
- `VALOR_REEMBOLSO` → do Component `MotorPoliticasPosVenda`  
- `CODIGO_REGRA_APLICADA` → do Component `MotorPoliticasPosVenda`  
- `RESTRICOES` → do Component `MotorPoliticasPosVenda`  

### 4.3. Output recebido do Component `AgentePlanoResolucao`

O workflow pai recebe do Component:

```json
{
  "ACOES": [
    {
      "tipo": "string",
      "valor": 0,
      "motivo": "string opcional",
      "tag": "string opcional",
      "nova_data": "string opcional",
      "canal": "string opcional"
    }
  ],
  "RESPOSTA_SUGERIDA": "string",
  "ESCALAR_SUPERVISOR": false
}
```

Variáveis disponíveis no contexto do pai:

- `ACOES`  
- `RESPOSTA_SUGERIDA`  
- `ESCALAR_SUPERVISOR`

---

## 5. Tasklet final – impressão do resultado consolidado

Após a execução dos dois Components, o workflow pai executa um step final (por exemplo, `imprimir_resultado`) que:

1. Consolida:  
   - cenário selecionado,  
   - input original,  
   - decisão de política (Component 1),  
   - plano e resposta (Component 2).  
2. Imprime/loga esse objeto para ser visualizado na demo.

### 5.1. Estrutura sugerida do objeto consolidado

```json
{
  "cenario_teste": "CASE_X_...",
  "input_original": {
    "booking_id": "string",
    "canal_venda": "string",
    "data_viagem": "string",
    "data_solicitacao": "string",
    "valor_pago": 0,
    "texto_solicitacao": "string"
  },
  "decisao_politica": {
    "TIPO_SOLICITACAO": "string",
    "MOTIVO": "string",
    "ELEGIVEL": true,
    "VALOR_REEMBOLSO": 0,
    "CODIGO_REGRA_APLICADA": "string",
    "RESTRICOES": "string or null"
  },
  "plano_e_resposta": {
    "ACOES": [
      {
        "tipo": "string",
        "valor": 0,
        "motivo": "string opcional",
        "tag": "string opcional",
        "nova_data": "string opcional",
        "canal": "string opcional"
      }
    ],
    "RESPOSTA_SUGERIDA": "string",
    "ESCALAR_SUPERVISOR": false
  }
}
```

Esse objeto pode ser:

- impresso em log,  
- exibido em painel de debug/output,  
- ou usado em qualquer visualização adicional.

---

## 6. Sequência de execução do Workflow Pai

Ordem dos steps do `OrquestradorPosVenda`:

1. `form_inicio`  
   - Campo: `cenario_teste`.

2. `montar_payload_cenario`  
   - Constrói `input_original` com base no cenário selecionado.

3. `chamar_MotorPoliticasPosVenda` (Component)  
   - Input: `input_original`.  
   - Output: `decisao_politica`.

4. `chamar_AgentePlanoResolucao` (Component)  
   - Input: `texto_solicitacao` (de `input_original`) + `decisao_politica`.  
   - Output: `plano_e_resposta`.

5. `imprimir_resultado`  
   - Monta objeto consolidado com:
     - `cenario_teste`  
     - `input_original`  
     - `decisao_politica`  
     - `plano_e_resposta`  
   - Imprime/loga para ser utilizado na demonstração.
