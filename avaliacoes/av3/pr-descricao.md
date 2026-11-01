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

## Como foi verificado

Execuções em Python 3.14.7, na raiz do repositório, salvo indicação.

```text
$ python3 -B testes/test_miniloja.py --codigo caso
Ran 11 tests ... OK

$ python3 caso/validar_golden_master.py
OK: 10 casos iguais ao golden master.

$ python3 -B testes/test_miniloja.py --codigo caso --existentes
Ran 34 tests ... FAILED (failures=2)
FAIL: test_cadastro_sem_nome_e_rejeitado
FAIL: test_cadastro_valido

$ cd caso && python3 -B -m unittest testes_existentes.test_acesso_av3
Ran 4 tests ... OK
```

As 2 falhas de `test_cadastro.py` já existem na `main` (30 testes, as mesmas 2 falhas) e ficaram fora do escopo. Os 4 testes a mais são os deste PR.

Barreira de escopo, que não deve imprimir nada:

```bash
git diff --name-only main...av3 | grep -v -x -E 'caso/miniloja/handlers\.py|caso/testes_existentes/test_acesso_av3\.py|avaliacoes/av3/(template-registro|pr-descricao)\.md'
```

## Teste que falharia sem a mudança

`test_usuario_nao_ve_pedido_de_outro_usuario` e `test_pedido_de_outro_responde_igual_a_pedido_inexistente`, em `caso/testes_existentes/test_acesso_av3.py`. Para repetir pelo histórico:

```bash
git checkout d606929   # teste sem a correção: FAILED (failures=2), 200 != 404
(cd caso && python3 -B -m unittest testes_existentes.test_acesso_av3)
git checkout aa55ae1   # mesmo teste com a correção: OK
(cd caso && python3 -B -m unittest testes_existentes.test_acesso_av3)
git checkout av3
```

Os 4 testes finais contra o `handlers.py` da `main` dão `FAILED (failures=5)`: um teste de resposta igual e os 4 intrusos (202, 50, 0 e `None`).

## Mutação de `get_pedido`

Executada em cópia descartável, com `test_acesso_av3` e `test_handlers`. A ferramenta `testes/mutacao_manual.py` não foi usada porque não tem mutantes dessa função e `testes/` não pode ser alterada.

| Mutante | Primeira versão (`aa55ae1`) | Versão final (`177b13e`) |
| --- | --- | --- |
| Sem a checagem de dono | morto | morto |
| `!=` vira `==` | morto | morto |
| `!=` vira `<` | **sobreviveu** | morto |
| `!=` vira `>` | morto | morto |
| `!=` vira `is not` | **sobreviveu** | morto |
| `or` vira `and` | morto | morto |
| Compara `pedido["id"]` | morto | morto |
| `usuario_id` vazio pula a checagem | **sobreviveu** | morto |
| `403` para pedido de outro | morto | morto |
| `404` com corpo diferente para pedido de outro | morto | morto |
| `404` devolvendo o pedido no corpo | morto | morto |

Para repetir um mutante: troque `!=` por `<` em `caso/miniloja/handlers.py:38`, rode o comando de acesso acima e desfaça com `git checkout caso/miniloja/handlers.py`.

## Dependências novas

Nenhuma.

## O que a IA errou

Os erros, a detecção e as correções estão em `avaliacoes/av3/template-registro.md`. Os sobreviventes acima são o principal deles, corrigidos no commit `177b13e`.
