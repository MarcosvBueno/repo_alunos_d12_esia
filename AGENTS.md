# Orientações para agentes

- O backend fictício MiniLoja está em `caso/miniloja/`.
- Rode a suíte com `cd caso && python3 -m unittest discover -s testes_existentes`.
- Compare o cálculo com `python3 caso/validar_golden_master.py` a partir da raiz.
- Refatorações de `calcular_total` preservam assinatura e comportamento observável.
- O código atual usa `float` e `round`; não troque a regra de arredondamento numa refatoração estrutural.
- R1 exige frete grátis a partir de R$ 200 e arredondamento meio para cima; divergências atuais devem ser relatadas, não corrigidas silenciosamente.
- Não altere testes ou o golden master para acomodar uma implementação refatorada.
