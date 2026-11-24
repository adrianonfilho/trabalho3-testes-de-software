# Critérios de teste — aluguel

Esta análise registra critérios e obrigações de cobertura. As entradas concretas, os resultados esperados de cada caso e as asserções JUnit serão projetados pela LLM.

### Análise caixa-preta do grupo

Fonte: [especificação de aluguel](../docs/aluguel/especificacao.md).

Nas regras abaixo, `D` representa as diárias, `K` a quilometragem rodada, `H` as horas de atraso e `E = K - 100 × D` o excedente de quilômetros. As regras de cálculo pressupõem argumentos válidos.

#### Classes de equivalência

| Parâmetro ou regra | Classe de equivalência | Domínio ou condição |
|---|---|---|
| Categoria | CE-01 — econômica, válida | `ECONOMICO`, com diária de R$ 120. |
| Categoria | CE-02 — intermediária, válida | `INTERMEDIARIO`, com diária de R$ 180. |
| Categoria | CE-03 — SUV, válida | `SUV`, com diária de R$ 280. |
| Categoria | CE-04 — nula, inválida | Ausência da categoria. |
| Nível | CE-05 — comum, válido | `COMUM`, sem desconto de fidelidade. |
| Nível | CE-06 — prata, válido | `PRATA`, com benefício condicionado à duração e ao histórico. |
| Nível | CE-07 — ouro, válido | `OURO`, com benefício condicionado à duração e ao histórico. |
| Nível | CE-08 — nulo, inválido | Ausência do nível do cliente. |
| Diárias | CE-09 — não positivas, inválidas | `D <= 0`. |
| Diárias | CE-10 — duração curta, válida | `1 <= D <= 2`, sem desconto por duração. |
| Diárias | CE-11 — primeira faixa, válida | `3 <= D <= 6`, com desconto de 5%. |
| Diárias | CE-12 — segunda faixa, válida | `7 <= D <= 14`, com desconto de 10%. |
| Diárias | CE-13 — duração longa, válida | `D >= 15`, até o máximo representável em `int`, com desconto de 15%. |
| Quilometragem | CE-14 — negativa, inválida | `K < 0`. |
| Quilometragem válida | CE-15 — dentro da franquia | `K >= 0` e `E <= 0`, sem cobrança adicional. |
| Quilometragem válida | CE-16 — excedente baixo | `1 <= E <= 100`, todo o excedente a R$ 0,80/km. |
| Quilometragem válida | CE-17 — excedente intermediário | `101 <= E <= 300`, todo o excedente a R$ 1,00/km. |
| Quilometragem válida | CE-18 — excedente alto | `E >= 301`, todo o excedente a R$ 1,50/km. |
| Atraso | CE-19 — negativo, inválido | `H < 0`. |
| Atraso | CE-20 — tolerado, válido | `0 <= H <= 1`, isento. |
| Atraso | CE-21 — cobrança por hora, válido | `2 <= H <= 3`, com 20% da diária sem desconto por hora. |
| Atraso | CE-22 — cobrança fixa, válido | `H >= 4`, com cobrança de uma diária sem desconto. |
| Seguro | CE-23 — sem seguro, válido | `SEM_SEGURO`, sem adicional de seguro. |
| Seguro | CE-24 — básico, válido | `BASICO`, com R$ 25 por diária. |
| Seguro | CE-25 — completo, válido | `COMPLETO`, com R$ 45 por diária. |
| Seguro | CE-26 — nulo, inválido | Ausência do argumento; diferente da opção válida `SEM_SEGURO`. |
| Histórico | CE-27 — sem atraso anterior | Valor falso, permitindo fidelidade se os outros requisitos forem satisfeitos. |
| Histórico | CE-28 — com atraso anterior | Valor verdadeiro, impedindo fidelidade independentemente da duração. |
| Fidelidade prata | CE-29 — elegível | `PRATA`, `D >= 7` e sem atraso anterior. |
| Fidelidade prata | CE-30 — não elegível | `PRATA` com `D < 7` ou com atraso anterior. |
| Fidelidade ouro | CE-31 — elegível | `OURO`, `D >= 5` e sem atraso anterior. |
| Fidelidade ouro | CE-32 — não elegível | `OURO` com `D < 5` ou com atraso anterior. |

#### Valores-limite

| Parâmetro ou regra | Valor-limite | Classes separadas e inclusão do limite |
|---|---|---|
| Validade das diárias | 1 | Abaixo de 1 é inválido; 1 já é válido. Considerar os inteiros vizinhos e o limite. |
| Desconto por duração | 2/3 | 2 ainda não recebe desconto; 3 já recebe 5%. |
| Desconto por duração | 6/7 | 6 recebe 5%; 7 já recebe 10%. |
| Desconto por duração | 14/15 | 14 recebe 10%; 15 já recebe 15%. |
| Fidelidade prata | 7 diárias | Sem atraso anterior, abaixo de 7 não há benefício; 7 já habilita 5%. Considerar o limite e os vizinhos. |
| Fidelidade ouro | 5 diárias | Sem atraso anterior, abaixo de 5 não há benefício; 5 já habilita 10%. Considerar o limite e os vizinhos. |
| Validade da quilometragem | 0 | Negativos são inválidos; zero pertence ao domínio válido. |
| Franquia | `K = 100 × D`, ou `E = 0` | No limite e abaixo dele não há adicional; o primeiro quilômetro excedente já é cobrado. Considerar os lados alcançáveis no domínio de `K`. |
| Tarifa do excedente | `E = 100/101` | 100 ainda usa R$ 0,80/km; 101 muda a tarifa de todo o excedente para R$ 1,00/km. |
| Tarifa do excedente | `E = 300/301` | 300 ainda usa R$ 1,00/km; 301 muda a tarifa de todo o excedente para R$ 1,50/km. |
| Validade do atraso | 0 | Negativos são inválidos; zero pertence ao domínio válido. |
| Tolerância de atraso | 1/2 horas | 1 é isento; 2 cobra 20% da diária por cada hora de atraso, incluindo ambas as horas. |
| Cobrança fixa de atraso | 3/4 horas | 3 ainda usa cobrança por hora; 4 já cobra uma diária inteira sem desconto. |
| Representação numérica | Máximo de `int` | É limite do tipo, sem nova restrição de negócio. Considerar valores altos de diárias, quilômetros e horas, sem exigir entradas fora do tipo. |

#### Tabela de decisão

| Regra | Combinação de condições | Ação prevista na especificação |
|---|---|---|
| RD-01 | Categoria, nível ou seguro nulo | Lançar `NullPointerException`; verificar cada argumento isoladamente. |
| RD-02 | Enums presentes e alguma entrada numérica inválida: `D <= 0`, `K < 0` ou `H < 0` | Lançar `IllegalArgumentException`; verificar cada invalidade isoladamente. |
| RD-03 | Categoria `ECONOMICO` | Usar diária de R$ 120. |
| RD-04 | Categoria `INTERMEDIARIO` | Usar diária de R$ 180. |
| RD-05 | Categoria `SUV` | Usar diária de R$ 280. |
| RD-06 | `1 <= D <= 2` | Aplicar 0% de desconto por duração sobre as diárias brutas. |
| RD-07 | `3 <= D <= 6` | Aplicar 5% de desconto por duração sobre as diárias brutas. |
| RD-08 | `7 <= D <= 14` | Aplicar 10% de desconto por duração sobre as diárias brutas. |
| RD-09 | `D >= 15` | Aplicar 15% de desconto por duração sobre as diárias brutas. |
| RD-10 | Nível `COMUM`; duração e histórico indiferentes | Não aplicar desconto de fidelidade. |
| RD-11 | Nível `PRATA` ou `OURO`, com atraso anterior; duração indiferente | Não aplicar desconto de fidelidade. |
| RD-12 | `PRATA`, sem atraso anterior e `D < 7` | Não aplicar desconto de fidelidade. |
| RD-13 | `PRATA`, sem atraso anterior e `D >= 7` | Aplicar 5% sobre as diárias após o desconto por duração. |
| RD-14 | `OURO`, sem atraso anterior e `D < 5` | Não aplicar desconto de fidelidade. |
| RD-15 | `OURO`, sem atraso anterior e `D >= 5` | Aplicar 10% sobre as diárias após o desconto por duração. |
| RD-16 | `E <= 0` | Não cobrar quilometragem adicional. |
| RD-17 | `1 <= E <= 100` | Cobrar todo o excedente a R$ 0,80/km. |
| RD-18 | `101 <= E <= 300` | Cobrar todo o excedente a R$ 1,00/km, sem cálculo progressivo. |
| RD-19 | `E >= 301` | Cobrar todo o excedente a R$ 1,50/km, sem cálculo progressivo. |
| RD-20 | Seguro `SEM_SEGURO` | Não acrescentar seguro. |
| RD-21 | Seguro `BASICO` | Acrescentar R$ 25 por diária. |
| RD-22 | Seguro `COMPLETO` | Acrescentar R$ 45 por diária. |
| RD-23 | `0 <= H <= 1` | Não cobrar atraso. |
| RD-24 | `2 <= H <= 3` | Cobrar 20% da diária sem desconto multiplicados por `H`. |
| RD-25 | `H >= 4` | Cobrar uma diária sem desconto. |
| RD-26 | Todos os argumentos válidos | Somar diárias após descontos sucessivos, quilometragem, seguro e atraso; retornar `BigDecimal` com duas casas decimais e `HALF_UP`. Os adicionais não recebem os descontos das diárias. |

### Análise caixa-branca do grupo

Fonte: [CalculadoraCustoLocacao.java](../src/main/java/br/com/aluguelcarros/CalculadoraCustoLocacao.java).

| Método ou trecho | Decisão, condição ou caminho | Obrigação de cobertura |
|---|---|---|
| CB-01 — `calcularCustoLocacao`, validação de nulidade | A disjunção (OU) só avalia o nível quando a categoria está presente e só avalia o seguro quando ambos estão presentes. | Cobrir categoria nula; categoria presente e nível nulo; categoria e nível presentes e seguro nulo; todos presentes. Cobrir exceção e continuidade. |
| CB-02 — `numeroDiarias <= 0` | Após validar os enums, rejeita diárias não positivas. | Cobrir verdadeiro e falso, incluindo a fronteira entre zero e uma diária. |
| CB-03 — `quilometrosRodados < 0` | Só é alcançada após validar diárias. | Cobrir verdadeiro e falso com argumentos anteriores válidos, incluindo zero no caminho válido. |
| CB-04 — `horasAtraso < 0` | Só é alcançada após as demais validações. | Cobrir verdadeiro e falso com argumentos anteriores válidos, incluindo zero no caminho válido. |
| CB-05 — escolha de `valorDiaria` | Distingue econômico, intermediário e, no ramo final, SUV. | Cobrir os três caminhos e ambos os resultados das comparações alcançadas. Não pressupor outro valor não nulo do enum. |
| CB-06 — escolha de `taxaDescontoDuracao` | Compara a duração a 2, 6 e 14 em sequência; cada comparação posterior exige as anteriores falsas. | Cobrir os quatro caminhos e ambos os resultados de cada decisão alcançada, incluindo as transições de faixa. |
| CB-07 — fidelidade `PRATA` | A conjunção (E) só avalia duração para prata; só avalia histórico para prata com pelo menos sete diárias. | Cobrir nível diferente de prata; prata com duração insuficiente; prata com duração suficiente e histórico impeditivo; prata com todos os requisitos satisfeitos. Cada condição avaliada deve poder impedir o benefício. |
| CB-08 — fidelidade `OURO` | Só é alcançada após a expressão de prata resultar falsa. Duração e histórico também usam curto-circuito. | Cobrir nível diferente de ouro ao alcançar a decisão; ouro com duração insuficiente; ouro com duração suficiente e histórico impeditivo; ouro com todos os requisitos satisfeitos. Cobrir também o ramo final sem fidelidade. |
| CB-09 — cálculo dos descontos | Duração incide sobre o bruto; fidelidade incide sobre o saldo após duração. | Exercitar nenhum desconto, apenas duração e os dois descontos. Distinguir aplicação sucessiva de soma de percentuais ou aplicação ao total com adicionais. |
| CB-10 — `100L * numeroDiarias` e subtração do excedente | Calcula a franquia em `long` e converte quilômetros antes de subtrair. | Considerar diárias cuja franquia ultrapasse o máximo de `int`, com parâmetros representáveis. Uma franquia maior que a quilometragem não deve gerar cobrança por estouro. |
| CB-11 — `quilometrosExcedentes <= 0` | Se verdadeiro, zera o adicional e não examina tarifas; caso contrário, entra na cobrança. | Cobrir excedente negativo, zero e positivo; só exigir decisões de tarifa no ramo positivo. |
| CB-12 — tarifas do excedente | No ramo positivo, compara excedente a 100 e depois a 300, escolhendo uma tarifa única. | Cobrir as três tarifas e ambos os resultados das decisões alcançadas. Distinguir cobrança integral pela tarifa escolhida de cobrança progressiva por faixas. |
| CB-13 — escolha de seguro e multiplicação por diárias | Distingue sem seguro, básico e completo; multiplica o valor escolhido por toda a duração. | Cobrir os três caminhos e duração que torne observável a multiplicação. Combinar seguro e descontos para verificar que o seguro fica fora da base descontada. |
| CB-14 — decisões de atraso | Compara horas a 1 e, fora da tolerância, a 3; usa diária bruta tanto na cobrança por hora como na fixa. | Cobrir isenção, ambas as durações do ramo por hora e cobrança fixa a partir de quatro horas, inclusive acima da fronteira. Considerar descontos ativos para verificar a base bruta e a cobrança fixa independente das horas adicionais. |
| CB-15 — soma final e `setScale(2, HALF_UP)` | Soma quatro componentes e normaliza a escala monetária. | Cobrir componentes isoláveis e composição com todos positivos, verificando valor e escala de duas casas. Com as constantes e entradas atuais, os totais já são múltiplos de centavo; não exigir empate de meio centavo inalcançável para distinguir modos de arredondamento. |
