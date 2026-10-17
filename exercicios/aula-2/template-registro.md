# Registro individual — AV1.2

**Limite: uma página, incluindo evidências essenciais.** Estudante: Marcos Vinicius Bueno Estevam — Data: 17/10/2026
Origem: `caso/miniloja/calculo.py` fictício; modalidade: execução própria.

**Golden master:** 10 entradas; gerado por: execução de `calcular_total` antes da refatoração; comparação exata por `python3 caso/validar_golden_master.py`, sem tolerância. Resultado:`OK: 10 casos iguais ao golden master.`

| Medida                                                | Rodada 1 (sem escopo)      | Rodada 2 (com escopo)      |
| ----------------------------------------------------- | -------------------------- | -------------------------- |
| Linhas adicionadas/removidas                          | +39 / -60                  | +33 / -15                  |
| Arquivos alterados (e quais estavam fora do esperado) | `caso/miniloja/calculo.py` | `caso/miniloja/calculo.py` |
| Mudou comportamento? (golden master)                  | Não, se manteve igual      | Não, se manteve igual      |
| Tempo de revisão                                      | 4 min                      | 6 min                      |
| Idas e vindas                                         | 0                          | 0                          |

**Escopo da rodada 2:**
objetivo separar internamente o cálculo de desconto, frete e taxa;
pode tocar: caso/miniloja/calculo.py;
não pode tocar: assinatura pública, outros módulos, testes ou golden master;
invariantes preservar exatamente os resultados atuais, incluindo a flag de NATAL, a ordem das etapas e os casos que divergem do contrato.;
pronto quando o diff estiver dentro do escopo e o comparador e os testes existentes passarem.;
pare e pergunte se a solução exigir mudar comportamento, assinatura ou outros arquivos;
reportar o possível bug sem corrigi-lo..

**Plano do agente: o que eu cortei ou corrigi antes de executar:** Não precisei cortar ou corrigir pois ele planejou tendo todos os casos de uso inclusos no planejamento
**Algo que parecia bug e eu apenas reportei:** O frete usa total > 200, mas R1.3 do regras.md exige >= 200. Com subtotal descontado exatamente igual a R$ 200,00, o código cobra frete e o contrato manda dar frete grátis.
**`AGENTS.md` mínimo:**

- Código: `caso/miniloja/`. Contrato: `caso/regras.md` (vale mais que o código).
- Suíte: `cd caso && python3 -B -m unittest discover -s testes_existentes`
- Comparador: `python3 -B caso/validar_golden_master.py` (a partir da raiz)
- Refatoração preserva assinatura e comportamento observável de `calcular_total`.
- Não trocar float/`round` nem a ordem desconto → frete → taxa numa refatoração.
- Divergências do contrato (ex.: frete `>` 200 vs `>=` 200) são reportadas, não corrigidas.
- Não alterar `testes/`, `regras.md`, testes existentes nem o golden master para acomodar o código.
- Se a mudança exigir outro arquivo, outra assinatura ou outro comportamento: parar e perguntar.

**Trecho essencial de evidência:** `python3 caso/validar_golden_master.py` → OK: 10 casos iguais ao golden master. **Limite e condição para rever o escopo:** golden master cobre 10 entradas e registra o comportamento anterior; passar na comparação mostra que esses resultados foram preservados, não que todo o contrato R1 foi atendido. Eu reveria o escopo se surgisse uma divergência ou se fosse necessário mudar o comportamento, a assinatura ou arquivos fora de calculo.py; nesse caso, pararia antes de fazer a mudança.

**Procedência/IA:** ferramenta e modelo visíveis: **Claude code(Sonnet 5.5); tarefa delegada e contexto: \_** apoio à revisão do registro AV1.2, especialmente os campos de evidência e limite do escopo; **trecho aproveitado**: sugestão para resumir a saída do golden master e explicar quando rever o escopo; **minha verificação/intervenção:** adaptei a redação ao meu registro e confirmei a saída do comparador. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] golden master; [x] duas rodadas com números; [x] seis campos; [x] AGENTS.md; [x] até uma página.
