# B1 — Bloquear o acesso a pedidos de outro usuário (R4)

## Intenção

`get_pedido` devolve qualquer pedido a qualquer usuário, o que viola R4.1 ("um usuário só pode ver os próprios pedidos"). O defeito foi apontado na revisão da AV1.5 como anterior àquele PR e pendente de correção à parte. Este PR corrige só isso, com teste negativo.

Reprodução na `main` (`db9512c`):

```text
criado por 1: 201 1 1
lido por 2: (200, {'usuario_id': 1, 'itens': [...], 'total': 66.05, ..., 'id': 1})
inexistente: (404, {'erro': 'não encontrado'})
```

## Escopo (declarado antes da mudança)

- **Objetivo:** `get_pedido` só entrega o pedido ao dono (R4.1), com teste negativo.
- **Pode tocar:** `caso/miniloja/handlers.py` (somente `get_pedido`); novo `caso/testes_existentes/test_acesso_av3.py`; `avaliacoes/av3/template-registro.md`; `avaliacoes/av3/pr-descricao.md`.
- **Não pode tocar:** `caso/regras.md`; `testes/`; testes já existentes; golden master; `repositorio.py`; `pedidos.py`; assinatura de `get_pedido`; dependências.
- **Invariantes:** o dono continua recebendo 200 com o pedido; pedido inexistente continua 404 com `{"erro": "não encontrado"}`; as 11 verificações e o golden master continuam iguais; a suíte existente não ganha falha nova além das 2 já presentes em `test_cadastro.py`.
- **Pronto quando:** o teste negativo falha no commit do teste e passa no commit da correção; as mutações de `get_pedido` são mortas; a barreira de escopo sai vazia.
- **Pare e pergunte se:** a correção exigir mudar assinatura, repositório ou contrato, ou se aparecer falha fora das 2 conhecidas.

## Plano

1. Commit do teste negativo, vermelho, sem tocar no código.
2. Commit da correção mínima em `get_pedido`, verde.
3. Provar pelo histórico (vermelho e verde) e por mutações de `get_pedido` em cópia descartável.
4. Rodar a barreira de escopo sobre o diff contra a `main`.
5. Fechar a descrição e o registro.

**Cortes do plano:**

- Filtrar dentro de `RepositorioPedidos.obter`: muda a assinatura e passa a regra de acesso para a persistência.
- Corrigir as 2 falhas de `test_cadastro.py`: são anteriores e não têm relação com R4.
- Adicionar mutantes em `testes/mutacao_manual.py`: a pasta não pode ser alterada.

**Decisão de contrato:** R4 não define o status. Uso `404` com o mesmo corpo de pedido inexistente, e não `403`, porque os ids são sequenciais e `403` confirmaria quais pedidos existem.

## Modo de interação

Agente de codificação com escopo declarado (Claude Code, Claude Opus 5.5).

- **Raio de impacto:** baixo. Uma função de um caso fictício, em branch própria, com reversão por git.
- **Oráculo:** forte. R4.1 define o esperado, sem depender do código atual.
- **Familiaridade:** alta. O defeito já estava localizado e reproduzido desde a AV1.5.
- **Alternativa comparada:** editar com escopo, em conversa. A correção é pequena e esse modo bastaria para o código. Escolhi o agente porque a parte cara aqui é a prova: separar vermelho e verde no histórico e rodar mutações em cópia.
