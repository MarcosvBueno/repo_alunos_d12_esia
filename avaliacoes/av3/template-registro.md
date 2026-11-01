# Registro individual — AV3

**Limite: três páginas + até duas de evidências.** Estudante: Marcos Vinicius Bueno Estevam — Data: 01/11/2026 — Caminho: A (meu código) / **B (MiniLoja: B1**, B2 ou B3)

**Modo de interação usado e por quê (raio de impacto, oráculo, familiaridade):** ___ **Alternativa comparada:** ___

**Escopo declarado antes (seis campos):** objetivo: `get_pedido` só entrega o pedido ao dono (R4.1), com teste negativo; pode tocar: `caso/miniloja/handlers.py` (somente `get_pedido`), novo `caso/testes_existentes/test_acesso_av3.py`, `avaliacoes/av3/template-registro.md` e `avaliacoes/av3/pr-descricao.md`; não pode tocar: `caso/regras.md`, `testes/`, testes já existentes, golden master, `repositorio.py`, `pedidos.py`, assinatura de `get_pedido` e dependências; invariantes: o dono continua recebendo 200 com o pedido, pedido inexistente continua 404 com `{"erro": "não encontrado"}`, as 11 verificações e o golden master continuam iguais e a suíte existente não ganha falha além das 2 já presentes em `test_cadastro.py`; pronto quando: o teste negativo falha no commit do teste e passa no commit da correção, as mutações de `get_pedido` são mortas e a barreira de escopo sai vazia; pare e pergunte se a correção exigir mudar assinatura, repositório ou contrato, ou se aparecer falha fora das 2 conhecidas. **Cumprido? Como verifiquei (comando ou barreira):** ___

**Verificação:** teste que falharia sem a mudança ___; prova (execução antes e depois, sabotagem ou mutação) ___

| O que a IA errou (o quê, onde) | Como detectei | O que corrigi e por quê (causa e impacto) |
| --- | --- | --- |
| ___ |  |  |
| ___ |  |  |
| ___ |  |  |

**Dependências novas (se houver) e checagem:** ___

| Medição do meu time | Meu desenho |
| --- | --- |
| Pergunta e decisão | ___ |
| Métrica primária e guardrail | ___ |
| Baseline, período e método | ___ |
| Risco de manipulação e contramedida | ___ |
| Tarefa recorrente a automatizar e verificação exigida | ___ |

**Limites e condição para rever:** ___

**Procedência/IA:** não utilizada / ferramenta e modelo visíveis: ___; tarefa delegada e contexto: ___; trecho aproveitado: ___; minha verificação/intervenção: ___. O raciocínio e a decisão registrados são meus.

**Revisão:** [ ] modo; [ ] escopo; [ ] verificação; [ ] erros da IA; [ ] medição e automação; [ ] procedência.
