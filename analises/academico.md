# Critérios de teste — academico

Esta análise registra os critérios que devem orientar a geração dos testes. As entradas concretas, os resultados esperados de cada caso e as asserções JUnit serão projetados pela LLM.

### Análise caixa-preta do grupo

Fonte: [especificação acadêmica](../docs/academico/especificacao.md).

Nas regras abaixo, `N1`, `N2` e `N3` representam as notas arredondadas individualmente para uma casa decimal com `HALF_UP`; `M` representa a média dessas notas, também arredondada para uma casa decimal com `HALF_UP`; `F` representa a frequência; e `L` representa a menor das três notas arredondadas. As regras de classificação pressupõem argumentos válidos.

#### Classes de equivalência

| Parâmetro ou regra | Classe de equivalência | Domínio ou condição |
|---|---|---|
| Cada uma de `nota1`, `nota2` e `nota3` | CE-01 — nota válida | Valor finito no intervalo fechado [0, 10], considerando o valor recebido antes do arredondamento. |
| Cada nota | CE-02 — nota nula, inválida | Referência nula. |
| Cada nota | CE-03 — abaixo do domínio, inválida | Valor finito menor que 0. |
| Cada nota | CE-04 — acima do domínio, inválida | Valor finito maior que 10. |
| Cada nota | CE-05 — não numérica, inválida | `Float.NaN`. |
| Cada nota | CE-06 — infinita positiva, inválida | `Float.POSITIVE_INFINITY`. |
| Cada nota | CE-07 — infinita negativa, inválida | `Float.NEGATIVE_INFINITY`. |
| Frequência | CE-08 — frequência válida | Inteiro no intervalo fechado [0, 100]. |
| Frequência | CE-09 — frequência nula, inválida | Referência nula. |
| Frequência | CE-10 — abaixo do domínio, inválida | Inteiro menor que 0. |
| Frequência | CE-11 — acima do domínio, inválida | Inteiro maior que 100. |
| Frequência válida | CE-12 — insuficiente | `0 <= F < 75`. |
| Frequência válida | CE-13 — suficiente | `75 <= F <= 100`. |
| Média arredondada | CE-14 — reprovação por média | `0 <= M < 3`. |
| Média arredondada | CE-15 — faixa inferior de recuperação | `3 <= M < 5`. |
| Média arredondada | CE-16 — faixa condicionada à menor nota | `5 <= M < 7`. |
| Média arredondada | CE-17 — aprovação por média | `7 <= M <= 10`. |
| Menor nota arredondada | CE-18 — requisito de aprovação por notas não satisfeito | `L < 3`; relevante para distinguir recuperação de aprovação por notas quando `F >= 75` e `5 <= M < 7`. |
| Menor nota arredondada | CE-19 — requisito de aprovação por notas satisfeito | `L >= 3`, equivalente a todas as notas arredondadas serem de pelo menos 3. |
| Arredondamento de cada nota válida | CE-20 — parte descartada abaixo da metade | O arredondamento mantém o décimo inferior, incluindo notas já representadas com uma casa decimal. |
| Arredondamento de cada nota válida | CE-21 — parte descartada exatamente na metade | O empate entre dois décimos é resolvido em direção ao décimo superior, pois as notas são não negativas. |
| Arredondamento de cada nota válida | CE-22 — parte descartada acima da metade | O arredondamento resulta no décimo superior. |
| Arredondamento da média das notas arredondadas | CE-23 — aproximação ao décimo inferior ou superior | Médias exatas representáveis pelo processo que arredondam para baixo ou para cima, especialmente quando isso muda a faixa de classificação. |

#### Valores-limite

| Parâmetro ou regra | Valor-limite | Classes separadas e inclusão do limite |
|---|---|---|
| Cada nota recebida | 0 | Valores finitos menores que 0 são inválidos; 0 pertence ao domínio válido. Considerar valores representáveis imediatamente abaixo e acima da fronteira. |
| Cada nota recebida | 10 | 10 pertence ao domínio válido; valores finitos maiores que 10 são inválidos, mesmo que o arredondamento os trouxesse para 10,0. Considerar os dois lados da fronteira. |
| Frequência | 0 | Inteiros menores que 0 são inválidos; 0 é válido e indica frequência insuficiente. |
| Frequência | 100 | 100 é válido; inteiros maiores que 100 são inválidos. |
| Frequência para classificação | 75 | Abaixo de 75 a frequência é insuficiente; 75 já pertence à classe suficiente. Exercitar os inteiros vizinhos e o próprio limite. |
| Média arredondada | 3,0 | Abaixo de 3,0 há reprovação por média; 3,0 já pertence à faixa seguinte. A frequência distingue `REMF` de `REP` abaixo desse limite e `REPF` das situações com frequência suficiente a partir dele. |
| Média arredondada | 5,0 | Com frequência suficiente, abaixo de 5,0 e a partir de 3,0 há recuperação; 5,0 já permite `APRN` se todas as notas arredondadas forem de pelo menos 3. |
| Média arredondada | 7,0 | Com frequência suficiente, 7,0 já resulta em `APR`, independentemente do requisito da menor nota; valores abaixo pertencem às faixas anteriores. |
| Menor nota arredondada | 3,0 | Com frequência suficiente e média de 5,0 até abaixo de 7,0, menor nota abaixo de 3,0 implica `REC`; 3,0 já satisfaz o requisito para `APRN`. |
| Arredondamento individual | Ponto médio entre décimos consecutivos | A fronteira decimal é `d + 0,05`, sendo `d` o décimo inferior. Abaixo dela arredonda para `d`; no empate e acima arredonda para o décimo superior. Considerar especialmente a fronteira 2,95, que permite atingir nota arredondada 3,0. |
| Arredondamento da média | Transições que produzem `M = 3,0`, `M = 5,0` ou `M = 7,0` | Considerar médias exatas alcançáveis dos dois lados do ponto de arredondamento para cada limite. Uma média exata abaixo do limite de classificação pode atingi-lo após arredondar; a decisão deve usar `M`. |

#### Tabela de decisão

| Regra | Combinação de condições | Ação prevista na especificação |
|---|---|---|
| RD-01 | Um único argumento nulo; demais argumentos válidos | Lançar `NullPointerException`. Aplicável a cada nota e à frequência. |
| RD-02 | Uma única nota não finita ou fora de [0, 10]; demais argumentos válidos | Lançar `IllegalArgumentException`. |
| RD-03 | Frequência fora de [0, 100]; três notas válidas | Lançar `IllegalArgumentException`. |
| RD-04 | Argumentos válidos; `F < 75` e `M < 3`; menor nota indiferente | Retornar `REMF`: reprovação por média e faltas. |
| RD-05 | Argumentos válidos; `F < 75` e `M >= 3`; menor nota indiferente | Retornar `REPF`: reprovação por faltas, inclusive nas faixas de média que permitiriam aprovação com frequência suficiente. |
| RD-06 | Argumentos válidos; `F >= 75` e `M < 3`; menor nota indiferente | Retornar `REP`: reprovação por média. |
| RD-07 | Argumentos válidos; `F >= 75` e `3 <= M < 5`; menor nota indiferente | Retornar `REC`: recuperação. |
| RD-08 | Argumentos válidos; `F >= 75`, `5 <= M < 7` e `L < 3` | Retornar `REC`: recuperação por não satisfazer o requisito de todas as notas. |
| RD-09 | Argumentos válidos; `F >= 75`, `5 <= M < 7` e `L >= 3` | Retornar `APRN`: aprovação por notas. |
| RD-10 | Argumentos válidos; `F >= 75` e `M >= 7`; menor nota indiferente | Retornar `APR`: aprovação por média. |

### Análise caixa-branca do grupo

Fonte: [ConsolidacaoParcial.java](../src/main/java/br/com/academico/ConsolidacaoParcial.java). O objetivo é cobrir os resultados das decisões e as condições alcançáveis, considerando as saídas antecipadas e o curto-circuito.

| Método ou trecho | Decisão, condição ou caminho | Obrigação de cobertura |
|---|---|---|
| CB-01 — `consolidarParcialmente`, `Objects.requireNonNull(frequencia)` | A nulidade da frequência é verificada antes das demais validações; frequência nula interrompe o método. | Exercitar a interrupção com frequência nula e a continuidade com frequência presente, mantendo as notas válidas. Não exigir mensagem específica da exceção. |
| CB-02 — `consolidarParcialmente`, `frequencia < 0` ou `frequencia > 100` | A disjunção (OU) avalia o limite superior apenas se o limite inferior não foi violado. | Cobrir frequência abaixo de 0, acima de 100 e dentro do domínio: primeira condição verdadeira; primeira falsa e segunda verdadeira; ambas falsas. Nos casos inválidos, alcançar o lançamento de `IllegalArgumentException`. |
| CB-03 — `consolidarParcialmente`, chamadas a `arredondarNota` | As notas são processadas na ordem primeira, segunda e terceira. Uma exceção impede o processamento das próximas e a classificação. | Cobrir o processamento bem-sucedido das três notas e uma falha isolada em cada posição, com argumentos anteriores válidos. Considerar as classes de erro definidas na análise caixa-preta. |
| CB-04 — `arredondarNota`, `Objects.requireNonNull(nota)` | Uma nota nula interrompe o auxiliar antes da validação numérica. | Cobrir nota nula e nota presente por meio da API pública, sem acesso direto ao método privado e sem exigir mensagem específica. |
| CB-05 — `arredondarNota`, não finita ou menor que 0 ou maior que 10 | A disjunção (OU) avalia `nota < 0` apenas quando a nota é finita e avalia `nota > 10` apenas quando ela também não é negativa. | Cobrir: não finita, com demais condições não avaliadas; finita negativa, com última condição não avaliada; finita acima de 10, alcançando a última condição verdadeira; e finita válida, com todas falsas. Exercitar `NaN` e os dois infinitos, embora compartilhem o primeiro ramo. |
| CB-06 — `arredondarNota`, conversão decimal e `setScale` | A nota válida é convertida por sua representação textual e arredondada para uma casa com `HALF_UP`. | Exercitar manutenção de nota já em décimos e arredondamento abaixo, no empate e acima da metade, inclusive quando o resultado muda o requisito de nota mínima. Observar o efeito pela situação retornada. |
| CB-07 — `consolidarParcialmente`, soma e divisão por 3 | A média usa as notas já arredondadas e é arredondada novamente antes de qualquer classificação. | Exercitar médias alcançáveis que arredondam para baixo e para cima. Incluir situações que distingam esse processamento de usar a média sem arredondar ou de calcular a média das notas originais. |
| CB-08 — `consolidarParcialmente`, `media < 3` | A primeira decisão de classificação separa a reprovação por média e retorna antes das decisões posteriores quando verdadeira. | Cobrir verdadeiro e falso, incluindo o limite de média arredondada igual a 3 no ramo falso. |
| CB-09 — `consolidarParcialmente`, ternário `frequencia < 75` quando `media < 3` | No ramo de média insuficiente, a frequência determina `REMF` ou `REP`. | Alcançar o ternário e cobrir seus dois resultados: frequência insuficiente e suficiente. |
| CB-10 — `consolidarParcialmente`, `frequencia < 75` após descartar média menor que 3 | Apenas médias de pelo menos 3 alcançam esta decisão; frequência insuficiente retorna `REPF`. | Cobrir verdadeiro e falso com essa precondição; no ramo verdadeiro, contemplar também médias que permitiriam aprovação se a frequência fosse suficiente. |
| CB-11 — `consolidarParcialmente`, `media >= 7` | Só é alcançada com média de pelo menos 3 e frequência suficiente; retorna `APR` antes de examinar a menor nota. | Cobrir verdadeiro e falso, incluindo igualdade a 7 no ramo verdadeiro. No ramo de aprovação, considerar menor nota abaixo de 3 para verificar a prioridade desta decisão. |
| CB-12 — `consolidarParcialmente`, `primeira.min(segunda).min(terceira)` | Com frequência suficiente e média de 3 até abaixo de 7, determina a menor nota arredondada independentemente de sua posição. | Fazer a menor nota ocorrer em cada posição e considerar empates, especialmente na distinção entre `APRN` e `REC`. |
| CB-13 — `consolidarParcialmente`, `media >= 5` e `menorNota >= 3` | O `&&` só avalia a comparação da menor nota quando a média é de pelo menos 5; este trecho só é alcançado com frequência suficiente e média abaixo de 7. | Cobrir primeira condição falsa, com segunda não avaliada; primeira verdadeira e segunda falsa; ambas verdadeiras. Incluir igualdades a 5 e a 3. Cobrir o retorno `APRN` e os dois motivos distintos para seguir ao retorno `REC`. |
| CB-14 — `consolidarParcialmente`, saídas do método | Há seis retornos de classificação, além das saídas por exceção nas validações. | Alcançar `REMF`, `REP`, `REPF`, `APR`, `APRN` e `REC` e as exceções previstas, respeitando as precondições de cada caminho. Não combinar ramos incompatíveis nem exigir enumeração de todos os valores de entrada. |
