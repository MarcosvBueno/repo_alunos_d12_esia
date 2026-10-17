# Registro individual — AV1.3

**Limite: uma página, incluindo evidências essenciais.** Estudante: Marcos Vinicius Bueno Estevam — Data: 17/10/2026
Origem: `caso/testes_existentes/` e `caso/regras.md` fictícios; modalidade: execução própria / transcrição (marque): execução assistida por IA, com comandos executados pelo assistente.

| Teste suspeito                                 | Tipo de tautologia                             | Sabotagem que apliquei (ou raciocínio) | Continuou verde?                  |
| ---------------------------------------------- | ---------------------------------------------- | -------------------------------------- | --------------------------------- |
| `test_calculo::test_cupom_natal_com_flag`      | Asserção fraca: só exige resultado não nulo    | NATAL 20% → 21%                        | Sim; mutante sobreviveu.          |
| `test_pedidos::test_fluxo_chama_colaboradores` | Super-mock; só verifica chamadas               | `total_fmt` sempre zero                | Sim; mutante sobreviveu.          |
| `test_relatorios::test_simular_desconto`       | Asserção superficial: confere só o prefixo`R$` | Somar R&#36; 1 ao valor                | Sim; 26 testes passaram na cópia. |

| Mutante sobrevivente   | Por que sobreviveu                             | Teste que o mataria (ou "equivalente", com justificativa)                                                     |
| ---------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| NATAL 20% → 21%        | O teste só exige resultado não nulo.           | Com a campanha ativa:`self.assertEqual(calcular_total([{"preco": 1000.0, "qtd": 1}], "NATAL", "PE"), 840.0)`. |
| Frete RJ 21,50 → 22,50 | Falta pedido comum abaixo de R&#36; 200 em RJ. | `self.assertEqual(calcular_total([{"preco": 40.0, "qtd": 1}], None, "RJ"), 65.19)`.                           |

| Caso derivado do contrato (entrada) | Esperado (cálculo à mão)                     | Observado no código | Decisão                                                     |
| ----------------------------------- | -------------------------------------------- | ------------------- | ----------------------------------------------------------- |
| R&#36; 200, sem cupom, PE           | `200 × 1,05` = R&#36; 210,00 (frete grátis)  | R&#36; 223,55       | Diverge: o código usa`> 200`; R1 exige `>= 200`.            |
| R&#36; 2, sem cupom, PE             | `(2 + 12,90) × 1,05` = 15,645 → R&#36; 15,65 | R&#36; 15,64        | Diverge:`float` + `round` não dá meio para cima neste caso. |
| R&#36; 100, `PROMO10`, SP           | `(90 + 19,90) × 1,07` = R&#36; 117,59        | R&#36; 117,59       | Conforme R1.                                                |

**ADR curto:** contexto: R1 exige frete grátis a partir de R&#36; 200 e arredondamento meio para cima, mas o código diverge; decisão: R1 prevalece e as divergências devem ser registradas, sem alterar código/testes nesta atividade; consequências: o teste existente fixa R&#36; 223,55 e falha se o limite for corrigido; alternativa descartada: ajustar o esperado ao código, pois esconderia a divergência.

**Trecho essencial de evidência:** `python3 -m unittest discover -s testes_existentes`: 26 testes, OK; na cópia temporária, mutação: 31, 23 mortos, 8 sobreviventes, escore 74%; a sabotagem do relatório também deixou os 26 testes verdes. **Limite do que a suíte garante e condição para rever a decisão:** os 8 sobreviventes incluem um mutante equivalente; suíte verde não prova todo R1/R2. Rever se R1 mudar ou após correção explícita. `caso/validar_golden_master.py` não existe nesta cópia; testes não foram alterados e mutações foram restauradas.

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code (Sonnet 5.5); variante não informada); tarefa delegada e contexto: análise da AV1.3, cálculos e execução dos comandos com apoio de IA; trecho aproveitado: classificações, testes propostos e cálculos; minha verificação/intervenção: pedi ao assistente que executasse os comandos e revisei os resultados com R1 antes de entregar. Use "não informado" para metadados indisponíveis. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] três testes; [x] dois mutantes; [x] três casos do contrato; [x] ADR; [x] até uma página.
