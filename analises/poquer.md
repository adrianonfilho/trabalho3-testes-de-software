# Critérios de teste — poquer

Esta análise registra critérios e obrigações de cobertura. As entradas concretas, os resultados esperados de cada caso e as asserções JUnit serão projetados pela LLM.

### Análise caixa-preta do grupo

Fonte: [especificação de pôquer](../docs/poquer/especificacao.md).

Cada carta é o par formado pelos elementos de mesmo índice das listas de valores e naipes. As regras de classificação pressupõem cinco cartas válidas e distintas. Uma sequência exige cinco valores distintos e consecutivos, com ás apenas na ponta inferior ou superior.

#### Classes de equivalência

| Parâmetro ou regra | Classe de equivalência | Domínio ou condição |
|---|---|---|
| Lista de valores | CE-01 — nula, inválida | Referência da lista nula. |
| Lista de naipes | CE-02 — nula, inválida | Referência da lista nula. |
| Elementos de valores | CE-03 — nulo, inválido | Pelo menos um elemento nulo na lista de valores. |
| Elementos de naipes | CE-04 — nulo, inválido | Pelo menos um elemento nulo na lista de naipes. |
| Tamanho de cada lista | CE-05 — insuficiente, inválido | Menos de cinco elementos, incluindo lista vazia. |
| Tamanho de cada lista | CE-06 — exato, válido | Exatamente cinco elementos. Ambas as listas devem satisfazer esta condição. |
| Tamanho de cada lista | CE-07 — excedente, inválido | Mais de cinco elementos. |
| Identidade das cartas | CE-08 — duplicação, inválida | O mesmo par valor/naipe ocorre mais de uma vez, adjacente ou não. |
| Identidade das cartas | CE-09 — cartas distintas, válida | Cinco pares distintos. Mesmo valor com naipes diferentes e mesmo naipe com valores diferentes são permitidos. |
| Multiplicidade dos valores | CE-10 — todos distintos | Distribuição de frequências `1+1+1+1+1`. |
| Multiplicidade dos valores | CE-11 — um par | Distribuição `2+1+1+1`. |
| Multiplicidade dos valores | CE-12 — dois pares | Distribuição `2+2+1`. |
| Multiplicidade dos valores | CE-13 — trinca sem par | Distribuição `3+1+1`. |
| Multiplicidade dos valores | CE-14 — trinca com par | Distribuição `3+2`. |
| Multiplicidade dos valores | CE-15 — quadra | Distribuição `4+1`. |
| Naipes | CE-16 — uniforme | Todas as cartas do mesmo naipe. |
| Naipes | CE-17 — mistos | Pelo menos dois naipes diferentes, inclusive quando apenas uma carta difere. |
| Sequência de valores distintos | CE-18 — sem ás | Cinco valores consecutivos sem envolver ás. |
| Sequência de valores distintos | CE-19 — ás baixo | Ás seguido dos quatro menores valores seguintes. |
| Sequência de valores distintos | CE-20 — ás alto | Os quatro maiores valores não ás seguidos do ás. |
| Ausência de sequência | CE-21 — lacuna | Cinco valores distintos não consecutivos, inclusive os que estão próximos de uma sequência. |
| Ausência de sequência | CE-22 — passagem circular indevida | Só haveria continuidade atravessando de rei para ás em posição interna, o que não é permitido. |
| Ordem das cartas | CE-23 — permutação válida | Reordenação conjunta das listas preservando os pares valor/naipe; deve manter a classificação. |

#### Valores-limite

| Parâmetro ou regra | Valor-limite | Classes separadas e inclusão do limite |
|---|---|---|
| Tamanho de cada lista | 5 | Abaixo e acima de cinco é inválido; cinco é o único tamanho válido. Considerar o limite e tamanhos vizinhos, variando as listas independentemente. |
| Quantidade de cartas distintas | 5 | Com cinco posições, menos de cinco pares distintos indica duplicação; cinco é válido. |
| Valores distintos em sequência | 5 | Cinco valores distintos são necessários; quatro valores distintos com repetição não formam sequência, mesmo que a distância entre extremos seja quatro. |
| Maior frequência de um valor | 2, 3 e 4 | Duas ocorrências caracterizam par; três, trinca; quatro, quadra. Com maior frequência 2, observar a quantidade de pares; com frequência 3, observar a existência de um par. |
| Quantidade de pares | 0, 1 e 2 | Distingue ausência de pares, um par e dois pares. Um par com trinca recebe classificação superior. Três pares são impossíveis em cinco cartas. |
| Uniformidade de naipes | 5 cartas do mesmo naipe | Cinco é uniforme; quatro do mesmo naipe e uma diferente já pertencem à classe mista. |
| Sequências com ás | Extremidades inferior e superior | Ás é permitido apenas nas duas pontas previstas; a passagem de rei para ás em posição interna não cria sequência. |
| Continuidade dos valores | Ausência de lacunas | Uma lacuna rompe a sequência. Com cinco valores distintos em ordem linear, a diferença entre extremos deve ser quatro, ressalvada a sequência alta com ás. |

#### Tabela de decisão

| Regra | Combinação de condições | Ação prevista na especificação |
|---|---|---|
| RD-01 | Uma das listas nula; outra válida | Lançar `NullPointerException`. |
| RD-02 | Elemento nulo em uma das listas; demais elementos e tamanhos válidos | Lançar `NullPointerException`. |
| RD-03 | Alguma lista com tamanho diferente de cinco, sem nulos | Lançar `IllegalArgumentException`. |
| RD-04 | Listas com cinco elementos não nulos, mas par valor/naipe repetido | Lançar `IllegalArgumentException`. |
| RD-05 | Sequência alta com ás e naipe uniforme | Retornar `SEQUENCIA_REAL_DO_MESMO_NAIPE`, com prioridade sobre as demais classificações aplicáveis. |
| RD-06 | Sequência com naipe uniforme, sem ser a real | Retornar `SEQUENCIA_DO_MESMO_NAIPE`, incluindo ás baixo. |
| RD-07 | Quatro cartas de um valor e uma de outro | Retornar `QUADRA`. |
| RD-08 | Três cartas de um valor e duas de outro | Retornar `TRINCA_E_PAR`, com prioridade sobre trinca e um par. |
| RD-09 | Naipe uniforme, sem sequência | Retornar `CINCO_DO_MESMO_NAIPE`. |
| RD-10 | Sequência com naipes mistos | Retornar `SEQUENCIA`, incluindo ambas as posições permitidas do ás. |
| RD-11 | Três cartas de um valor e duas de valores diferentes entre si e da trinca | Retornar `TRINCA`. |
| RD-12 | Dois pares de valores distintos e uma carta de outro valor | Retornar `DOIS_PARES`, com prioridade sobre um par. |
| RD-13 | Um par e três cartas de valores distintos entre si e do par | Retornar `UM_PAR`. |
| RD-14 | Cinco valores distintos, sem sequência e com naipes mistos | Retornar `CARTA_ALTA`. |
| RD-15 | Permutação conjunta das posições de uma mão válida | Preservar a classificação; manter cada valor associado ao respectivo naipe. |


### Análise caixa-branca do grupo

Fonte: [Mao.java](../src/main/java/br/com/poquer/Mao.java).

| Método ou trecho | Decisão, condição ou caminho | Obrigação de cobertura |
|---|---|---|
| CB-01 — construtor, `List.copyOf` | Copia primeiro valores e depois naipes. Lista ou elemento nulo lança exceção antes da validação explícita de tamanho. | Cobrir lista nula e elemento nulo em cada argumento, isoladamente, além da criação válida. Considerar nulos em posições diferentes e aceitar listas válidas mutáveis e imutáveis. |
| CB-02 — construtor, validação dos tamanhos | A disjunção (OU) só avalia tamanho dos naipes quando o tamanho de valores é cinco. | Cobrir primeira condição verdadeira; primeira falsa e segunda verdadeira; ambas falsas. Para cada lista, considerar tamanhos inferiores e superiores ao exigido, sem nulos. |
| CB-03 — construtor, laço sobre as cartas | Para tamanhos válidos, percorre cinco posições e insere pares no conjunto. | Cobrir execução completa e término normal com cartas distintas. A primeira inserção é necessariamente inédita; não exigir zero iterações em uma construção válida. |
| CB-04 — construtor, negação de `cartasDistintas.add` | Inserção inédita permite continuar; inserção repetida provoca exceção. | Cobrir ambos os caminhos, com duplicata adjacente e não adjacente, em posições iniciais e finais possíveis. Distinguir repetição do par de repetição apenas do valor ou do naipe. |
| CB-05 — `classificar`, mapeamento, `distinct` e `sorted` | Converte valores em números, remove repetições e ordena antes de detectar sequência. | Exercitar mãos fora de ordem e todas as multiplicidades válidas; observar invariância da classificação sob permutação conjunta e redução da lista distinta quando há valores repetidos. |
| CB-06 — `sequenciaAltaComAs` | Reconhece exclusivamente a lista ordenada dos cinco valores da sequência alta com ás. | Cobrir verdadeiro e falso, com naipes uniformes e mistos. Distinguir ás alto, ás baixo e passagem circular indevida. |
| CB-07 — cálculo de `sequencia` | Ás alto torna a disjunção verdadeira sem avaliar a conjunção restante. Caso contrário, só compara extremos quando há cinco valores distintos. | Cobrir sequência alta com curto-circuito; não alta com menos de cinco distintos; cinco distintos com diferença entre extremos igual a quatro; e cinco distintos com diferença diferente de quatro. Não exigir acesso ao último índice no caminho com menos de cinco distintos. |
| CB-08 — `mesmoNaipe` com `allMatch` | Compara cada naipe ao primeiro e interrompe ao encontrar diferença; a primeira comparação é sempre verdadeira. | Cobrir todos iguais e diferença em posições posteriores, inclusive perto do fim. Considerar os quatro naipes como referência. Não exigir stream vazio, impedido pelo construtor. |
| CB-09 — laço sobre `valores` e vetor `frequencias` | Incrementa o vetor pelo número de cada valor. | Cobrir extremos do enum, incluindo ás e rei, e maiores frequências 1, 2, 3 e 4. O laço sempre percorre cinco cartas; frequência 5 para um valor é inalcançável em mão válida. |
| CB-10 — laço sobre frequências, contagem de pares e `Math.max` | Percorre as 14 posições, conta frequências iguais a 2 e encontra a maior frequência. O índice zero não representa carta. | Cobrir decisão de par verdadeira e falsa, com zero, um e dois pares. Percorrer frequências 0, 1, 3 e 4; observar maior frequência independentemente da posição numérica do valor repetido. O vetor é sempre percorrido integralmente. |
| CB-11 — decisão de sequência real | A conjunção só examina sequência alta se o naipe for uniforme; ambas verdadeiras causam retorno imediato. | Cobrir naipe misto com segunda condição não avaliada; uniforme sem sequência alta; uniforme com sequência alta. Verificar prioridade da classificação real. |
| CB-12 — decisão de sequência do mesmo naipe | Só é alcançada após descartar a real; só examina sequência se o naipe for uniforme. | Cobrir naipe misto com curto-circuito; uniforme sem sequência; uniforme com sequência não real, incluindo ás baixo. Não exigir real neste retorno, pois já retornaria antes. |
| CB-13 — `maiorFrequencia == 4` | Após descartar as duas classificações anteriores, retorna quadra. | Cobrir verdadeiro e falso, garantindo que a carta isolada não impeça reconhecer a quadra. |
| CB-14 — trinca com par | A conjunção só avalia `pares == 1` quando a maior frequência é três. | Cobrir ausência de trinca com curto-circuito; trinca sem par; trinca com par. O caso sem par deve prosseguir à classificação posterior. |
| CB-15 — decisão isolada de mesmo naipe | Só é alcançada após descartar sequência do mesmo naipe, quadra e trinca com par. | Cobrir uniforme sem sequência, retornando cinco do mesmo naipe, e misto, prosseguindo. Não exigir uniforme com par, combinação rejeitada como duplicata no construtor. |
| CB-16 — decisão isolada de sequência | Neste ponto, sequências alcançáveis têm naipes mistos, pois as uniformes já retornaram. | Cobrir verdadeiro e falso; no verdadeiro, contemplar sequência ordinária, ás baixo e ás alto. |
| CB-17 — decisão isolada de trinca | Trinca com par já foi tratada; a trinca restante tem distribuição `3+1+1`. | Cobrir verdadeiro para trinca sem par e falso para os caminhos seguintes. |
| CB-18 — decisões de dois pares e um par | Dois pares retornam antes da comparação de um par. | Cobrir verdadeiro e falso em cada decisão alcançada: dois pares, um par e nenhum par. Não exigir a segunda comparação após o retorno de dois pares. |
| CB-19 — retorno final e conjunto das saídas | A ausência das classificações anteriores resulta em carta alta. | Alcançar o retorno final com cinco valores distintos, não consecutivos e naipes mistos; alcançar também os outros nove retornos e as exceções do construtor. |
