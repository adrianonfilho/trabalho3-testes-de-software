# Consolidação parcial acadêmica

## API pública

Classe `ConsolidacaoParcial` no pacote `br.com.academico`.

```java
public static SituacaoAcademica consolidarParcialmente(
    Float nota1, Float nota2, Float nota3, Integer frequencia)
```

O enum de retorno `SituacaoAcademica` contém `REMF`, `REPF`, `REP`, `APR`, `APRN` e `REC`.

## Entradas válidas

As três notas devem ser finitas e pertencer a [0, 10]. A frequência, em porcentagem inteira já calculada sobre a base aplicável, deve pertencer a [0, 100].

## Resultados e exceções

Cada nota é arredondada para uma casa decimal com `HALF_UP`. A média aritmética dessas três notas também é arredondada para uma casa decimal com `HALF_UP`. As decisões usam os valores arredondados.

| Condição | `SituacaoAcademica` |
|---|---|
| Frequência abaixo de 75% e média menor que 3 | `REMF` — reprovado por média e faltas |
| Frequência abaixo de 75% e média de pelo menos 3 | `REPF` — reprovado por faltas |
| Frequência de pelo menos 75% e média menor que 3 | `REP` — reprovado por média |
| Frequência de pelo menos 75% e média de pelo menos 7 | `APR` — aprovado por média |
| Frequência de pelo menos 75%, média de 5 até abaixo de 7 e todas as notas de pelo menos 3 | `APRN` — aprovado por notas |
| Frequência de pelo menos 75% e demais casos com média de pelo menos 3 | `REC` — em recuperação |

Para entradas com um único argumento inválido, nulos provocam `NullPointerException` e valores fora do domínio, incluindo notas não finitas, provocam `IllegalArgumentException`.
