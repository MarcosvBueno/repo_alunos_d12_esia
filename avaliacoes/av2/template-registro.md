# Registro individual — AV2

**Limite: duas páginas de análise + anexo técnico curto.** Estudante: Marcos Vinicius Bueno Estevam — Data: 23/10/2026 — Caminho: B (MiniLoja)

**Escopo (seis campos):** objetivo: extrair a soma do subtotal para `_calcular_subtotal`; pode tocar: `caso/miniloja/calculo.py`, novo `caso/testes_existentes/test_calculo_av2.py` e este registro; não pode tocar: assinatura, outros módulos, testes preexistentes, contrato ou golden master; invariantes: ordem subtotal → desconto → frete → taxa, flag NATAL, `float`/`round` e igualdade exata nos 10 casos do golden; pronto quando: diff restrito, golden e testes de cálculo passam e as mutações relevantes falham; pare e pergunte se a proposta mudar saídas, assinatura, tipo numérico ou arquivos fora do escopo.

**Plano do agente: o que cortei ou corrigi:** limitei a mudança à extração do loop. Cortei a correção de `> 200` para `>= 200` e qualquer troca de arredondamento, pois alterariam comportamento. Mantive as variáveis locais `preco` e `qtd` para a mutação da multiplicação prevista no script ser aplicável.

**Comportamento preservado:** método: comparação exata com o golden master; entradas: 10 cenários com cupons, UFs e flag NATAL; resultado: `python3 caso/validar_golden_master.py` → `OK: 10 casos iguais ao golden master.` (antes e depois da refatoração).

| Teste (derivado de qual regra do contrato)                     | Como provei que falharia (sabotagem, mutação ou diferencial) | Resultado |
| -------------------------------------------------------------- | ------------------------------------------------------------ | --------- |
| `test_subtotal_soma_preco_vezes_quantidade` — R1.1             | `preco * qtd` → `preco + qtd`; falhou: 95,45 ≠ 118,55.       | Morto     |
| `test_promo10_em_sp_aplica_desconto_antes_da_taxa` — R1.2/R1.4 | 10% → 9%; falhou: 99,19 ≠ 98,33.                             | Morto     |
| `test_frete_e_taxa_de_rj_abaixo_do_limite` — R1.3/R1.4         | Frete RJ 21,50 → 22,50; falhou: 66,25 ≠ 65,19.               | Morto     |
| `test_natal_ativo_aplica_desconto_de_vinte_por_cento` — R1.2   | Com flag ativa, 20% → 21%; falhou: 248,85 ≠ 252,00.          | Morto     |

**Mutantes sobreviventes e tratamento(ou equivalentes justificados):** no arquivo `calculo.py`, 18 mutantes: 17 mortos e 1 sobrevivente (94%). O sobrevivente troca `desconto_aplicado = True` por `False`; a variável só controla um `pass`, então é equivalente para a saída observável de `calcular_total`. A primeira mutação de NATAL que tentei não atingiu a linha pretendida; corrigi a seleção e a prova isolada acima matou o mutante.

**Documentação (contrato e motivo) ou ADR:** docstring de `calcular_total` registra a ordem de R1 e que a extração mantém resultados legados; a divergência de limite do frete e arredondamento deve ser tratada em mudança comportamental separada.
**O que a IA errou (o quê, onde, como detectei):** na primeira configuração do mutador, omiti `PYTHONPATH=caso`; o subprocesso não localizou `miniloja` e a ferramenta reportou que a linha de base já falhava. Detectei comparando com o comando de cálculo, incluí o caminho e repeti a mutação. Na primeira sabotagem de NATAL, usei um trecho que também era prefixo do multiplicador VIP15 (`0.85`); conferi o código mutado, corrigi para casar a linha completa de NATAL e executei a prova isolada.
**Limite da verificação e condição para rever:** o golden cobre 10 entradas e os testes de cálculo, 13 casos; não prova todas as combinações. R1 diverge do legado em subtotal de R$ 200,00 (PE: contrato R$ 210,00; código R$ 223,55) e no exemplo de R$ 2,00 em PE (contrato R$ 15,65; código R$ 15,64); não corrigi esses pontos. A suíte completa roda 30 testes e mantém duas falhas preexistentes de cadastro, também presentes antes da mudança. Rever em mudança separada aprovada para alinhar o comportamento a R1.

**Procedência/IA:** ferramenta e modelo visíveis: Claude / Sonnet 5.5; **tarefa delegada e contexto:** apoio técnico no caminho B, incluindo a refatoração de `calcular_total`, a elaboração do helper, dos testes e da docstring; **trecho aproveitado:** helper, testes e docstring; **minha verificação/intervenção:** revisei a refatoração de `calcular_total`, conferi os 13 testes específicos e comparei os resultados com o golden master. O raciocínio e a decisão registrados são meus.

**Anexo:** diff: `calculo.py` extrai `_calcular_subtotal` e documenta o motivo; novo `test_calculo_av2.py` contém quatro testes; testes antigos e golden master não foram editados. `python3 -m unittest discover -s testes_existentes -p 'test_calculo*.py'` → 13 testes OK. A suíte completa reporta duas falhas de cadastro já existentes na linha de base: resposta 422 vs 400 e 422 vs 201.

**Revisão:** [x] escopo; [x] comportamento; [x] testes com prova; [x] documentação; [x] erros da IA; [x] limite.

## Anexo técnico — código para análise

O código abaixo reproduz os arquivos entregues. Em `calculo.py`, a única mudança funcional de estrutura é a extração do subtotal; as outras funções auxiliares já existiam e foram mantidas. O arquivo de testes é novo.

### `caso/miniloja/calculo.py`

```python
"""Cálculo de totais de pedido."""
from miniloja import flags

FRETE_POR_UF = {"PE": 12.9, "SP": 19.9, "RJ": 21.5}
TAXA_POR_UF = {"PE": 0.05, "SP": 0.07, "RJ": 0.06}


def _aplicar_desconto(total, cupom):
    """Aplica o cupom ao total; devolve (total, desconto_aplicado)."""
    desconto_aplicado = False
    if cupom is not None:
        if cupom == "PROMO10":
            total = total * 0.9
            desconto_aplicado = True
        elif cupom == "VIP15":
            total = total * 0.85
            desconto_aplicado = True
        elif cupom == "FRETEGRATIS":
            # tratado em _calcular_frete
            desconto_aplicado = False
        elif cupom == "NATAL":
            # campanha antiga; só vale se a flag estiver ligada
            if flags.promo_natal_ativa():
                total = total * 0.8
                desconto_aplicado = True
            else:
                desconto_aplicado = False
        else:
            # cupom desconhecido é ignorado
            desconto_aplicado = False
    return total, desconto_aplicado


def _calcular_frete(total, cupom, uf):
    """Frete do pedido, dado o total já com desconto."""
    frete = 0
    if cupom == "FRETEGRATIS":
        frete = 0
    else:
        if total > 200:
            frete = 0
        else:
            if uf == "PE":
                frete = 12.9
            elif uf == "SP":
                frete = 19.9
            elif uf == "RJ":
                frete = 21.5
            else:
                frete = 29.9
    return frete


def _taxa_servico(uf):
    """Alíquota da taxa de serviço por UF."""
    if uf == "PE":
        taxa = 0.05
    elif uf == "SP":
        taxa = 0.07
    elif uf == "RJ":
        taxa = 0.06
    else:
        taxa = 0.08
    return taxa


def _calcular_subtotal(itens):
    """Soma preço vezes quantidade, preservando a ordem recebida dos itens."""
    subtotal = 0
    for item in itens:
        preco = item["preco"]
        qtd = item["qtd"]
        subtotal = subtotal + preco * qtd
    return subtotal


def calcular_total(itens, cupom=None, uf="PE"):
    """Calcula na ordem subtotal, desconto, frete e taxa definida por R1.

    A extração do subtotal mantém as saídas float/round dos chamadores atuais;
    divergências legadas no limite do frete e no arredondamento são mudanças
    comportamentais e devem ser tratadas separadamente.
    """
    total = _calcular_subtotal(itens)
    # total = round(total, 2)  # tentamos arredondar aqui em 2023, desfeito

    # desconto
    total, desconto_aplicado = _aplicar_desconto(total, cupom)

    # frete
    frete = _calcular_frete(total, cupom, uf)
    total = total + frete

    # taxa de serviço por UF
    taxa = _taxa_servico(uf)
    imposto = total * taxa
    total = total + imposto

    if desconto_aplicado:
        pass  # reservado para relatório de descontos (não implementado)

    return round(total, 2)
```

### `caso/testes_existentes/test_calculo_av2.py`

```python
"""Testes AV2: expectativas calculadas a partir do contrato R1."""
import unittest
from unittest.mock import patch

from miniloja.calculo import calcular_total


class TestCalculoAV2(unittest.TestCase):
    def test_subtotal_soma_preco_vezes_quantidade(self):
        # R1.1: 50*1 + 25*2 = 100; (100 + 12,90) * 1,05 = 118,545.
        # O comportamento float/round atual devolve 118,55.
        itens = [{"preco": 50.0, "qtd": 1}, {"preco": 25.0, "qtd": 2}]
        self.assertEqual(calcular_total(itens, None, "PE"), 118.55)

    def test_promo10_em_sp_aplica_desconto_antes_da_taxa(self):
        # R1.2 e R1.4: (80 - 10%) + 19,90 = 91,90; * 1,07 = 98,333.
        self.assertEqual(calcular_total([{"preco": 80.0, "qtd": 1}], "PROMO10", "SP"), 98.33)

    def test_frete_e_taxa_de_rj_abaixo_do_limite(self):
        # R1.3 e R1.4: (40 + 21,50) * 1,06 = 65,19.
        self.assertEqual(calcular_total([{"preco": 40.0, "qtd": 1}], None, "RJ"), 65.19)

    def test_natal_ativo_aplica_desconto_de_vinte_por_cento(self):
        # R1.2: 300 - 20% = 240; frete grátis (> 200); taxa PE 5% = 252.
        with patch.dict("os.environ", {"MINILOJA_PROMO_NATAL": "1"}):
            total = calcular_total([{"preco": 300.0, "qtd": 1}], "NATAL", "PE")
        self.assertEqual(total, 252.0)


if __name__ == "__main__":
    unittest.main()
```

### Comandos e resultados

Executados na raiz do repositório:

```text
python3 caso/validar_golden_master.py
OK: 10 casos iguais ao golden master.
```

Executado dentro de `caso/`:

```text
python3 -m unittest discover -s testes_existentes -p 'test_calculo*.py'
Ran 13 tests
OK
```

Mutação focada nos testes de cálculo, executada na raiz:

```text
PYTHONPATH=caso MINILOJA_TEST_CMD='python3 -B -m unittest discover -s caso/testes_existentes -p "test_calculo*.py"' python3 -B testes/mutacao_manual.py calculo.py
Mutantes: 18 | mortos: 17 | sobreviventes: 1 | escore: 94%
SOBREVIVEU calculo.py: variável sem efeito (mutante equivalente)
```

Na suíte completa, antes e depois da mudança, os dois testes de cadastro que falham são `test_cadastro_sem_nome_e_rejeitado` (espera 400, recebe 422) e `test_cadastro_valido` (espera 201, recebe 422). Eles não exercitam `calcular_total`.
