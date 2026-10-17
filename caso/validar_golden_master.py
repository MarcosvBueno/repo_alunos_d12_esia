"""Compara calcular_total com o snapshot salvo em dados/golden_master_calculo.json."""
import json
import os
from pathlib import Path

from miniloja.calculo import calcular_total


ARQUIVO_GOLDEN = Path(__file__).parent / "dados" / "golden_master_calculo.json"
VARIAVEL_NATAL = "MINILOJA_PROMO_NATAL"


def main():
    golden = json.loads(ARQUIVO_GOLDEN.read_text(encoding="utf-8"))
    divergencias = []
    variavel_anterior = os.environ.get(VARIAVEL_NATAL)

    try:
        for caso in golden["cases"]:
            entrada = caso["input"]
            os.environ[VARIAVEL_NATAL] = "1" if entrada["promo_natal"] else "0"
            atual = calcular_total(
                entrada["itens"], entrada["cupom"], entrada["uf"]
            )
            if atual != caso["expected"]:
                divergencias.append((caso["id"], caso["expected"], atual))
    finally:
        if variavel_anterior is None:
            os.environ.pop(VARIAVEL_NATAL, None)
        else:
            os.environ[VARIAVEL_NATAL] = variavel_anterior

    if divergencias:
        for identificador, esperado, atual in divergencias:
            print(
                f"DIVERGÊNCIA {identificador}: esperado={esperado!r}, "
                f"atual={atual!r}"
            )
        print(f"{len(divergencias)} de {len(golden['cases'])} casos divergiram.")
        return 1

    print(f"OK: {len(golden['cases'])} casos iguais ao golden master.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
