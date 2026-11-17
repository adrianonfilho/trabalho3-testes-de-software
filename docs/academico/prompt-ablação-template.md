Você é especialista em testes unitários Java com JUnit 5. Use o material fornecido para projetar os casos de teste, escolher as entradas e determinar os resultados ou exceções esperados. Responda somente com o código Java completo da suíte JUnit 5, incluindo o pacote e os imports necessários. Entregue o código em texto puro, sem cercas de Markdown nem explicações.

# Consolidação parcial acadêmica

## API pública

Classe `ConsolidacaoParcial` no pacote `br.com.academico`.

```java
public static SituacaoAcademica consolidarParcialmente(
    Float nota1, Float nota2, Float nota3, Integer frequencia)
```

O enum de retorno `SituacaoAcademica` contém `REMF`, `REPF`, `REP`, `APR`, `APRN` e `REC`.

## Código

`src/main/java/br/com/academico/ConsolidacaoParcial.java`

```java
package br.com.academico;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Objects;

public class ConsolidacaoParcial {
    public static SituacaoAcademica consolidarParcialmente(
            Float nota1, Float nota2, Float nota3, Integer frequencia) {
        Objects.requireNonNull(frequencia, "frequencia");
        if (frequencia < 0 || frequencia > 100) {
            throw new IllegalArgumentException("Frequência deve estar entre 0 e 100");
        }

        BigDecimal primeira = arredondarNota(nota1);
        BigDecimal segunda = arredondarNota(nota2);
        BigDecimal terceira = arredondarNota(nota3);
        BigDecimal media = primeira.add(segunda).add(terceira)
                .divide(BigDecimal.valueOf(3), 1, RoundingMode.HALF_UP);

        if (media.compareTo(BigDecimal.valueOf(3)) < 0) {
            return frequencia < 75 ? SituacaoAcademica.REMF : SituacaoAcademica.REP;
        }
        if (frequencia < 75) {
            return SituacaoAcademica.REPF;
        }
        if (media.compareTo(BigDecimal.valueOf(7)) >= 0) {
            return SituacaoAcademica.APR;
        }
        BigDecimal menorNota = primeira.min(segunda).min(terceira);
        if (media.compareTo(BigDecimal.valueOf(5)) >= 0 && menorNota.compareTo(BigDecimal.valueOf(3)) >= 0) {
            return SituacaoAcademica.APRN;
        }
        return SituacaoAcademica.REC;
    }

    private static BigDecimal arredondarNota(Float nota) {
        Objects.requireNonNull(nota, "nota");
        if (!Float.isFinite(nota) || nota < 0 || nota > 10) {
            throw new IllegalArgumentException("Nota deve ser finita e estar entre 0 e 10");
        }
        return new BigDecimal(nota.toString()).setScale(1, RoundingMode.HALF_UP);
    }
}
```

`src/main/java/br/com/academico/SituacaoAcademica.java`

```java
package br.com.academico;

public enum SituacaoAcademica {
    REPF, REP, REC, APR, APRN, REMF
}
```

## Especificação

### Entradas válidas

As três notas devem ser finitas e pertencer a [0, 10]. A frequência, em porcentagem inteira já calculada sobre a base aplicável, deve pertencer a [0, 100].

### Resultados e exceções

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

## Análise

# Critérios de teste — academico

> Orientação: Substituam todos os campos entre colchetes. Acrescentem uma linha por classe, fronteira, regra ou obrigação de cobertura. Se um critério não se aplicar, substituam sua tabela por uma justificativa breve.

> Orientação: Registrem somente os critérios e seus resultados de análise. A LLM escolhe os valores de entrada para cada caso, determina o resultado esperado e escreve os testes JUnit.

### Análise caixa-preta do grupo

> Orientação: Usem a especificação como fonte. Considerem notas, frequência, arredondamento e as regras de classificação da situação acadêmica.

#### Classes de equivalência

> Orientação: Informem o parâmetro ou regra, deem um nome à classe e descrevam a faixa ou propriedade que inclui seus membros. Registrem classes válidas e inválidas quando previstas.

| Parâmetro ou regra | Classe de equivalência | Domínio ou condição |
|---|---|---|
| [parâmetro ou regra] | [nome e validade da classe] | [faixa ou propriedade que define a classe] |

#### Valores-limite

> Orientação: Indiquem o valor onde muda a validade ou o comportamento e descrevam as classes que ele separa. Esclareçam a qual classe pertence o próprio limite.

| Parâmetro ou regra | Valor-limite | Classes separadas e inclusão do limite |
|---|---|---|
| [parâmetro ou regra] | [valor da fronteira] | [classes de cada lado e classe do limite] |

#### Tabela de decisão

> Orientação: Uma linha descreve uma combinação geral de condições e a ação que a especificação prevê. Usem estados ou categorias, como condição satisfeita, condição insatisfeita ou indiferente, quando couber.

| Regra | Combinação de condições | Ação prevista na especificação |
|---|---|---|
| [identificador da regra] | [condições e estados aplicáveis] | [ação geral] |

### Análise caixa-branca do grupo

> Orientação: Usem o código de produção. Na primeira coluna, indiquem o método e o trecho ou a decisão. Na segunda, descrevam em linguagem natural como a decisão, condição ou caminho funciona. Na terceira, indiquem quais resultados de decisão, ramos ou caminhos a suíte deve exercitar. Se houver curto-circuito, indiquem quando uma condição posterior chega a ser avaliada.

| Método ou trecho | Decisão, condição ou caminho | Obrigação de cobertura |
|---|---|---|
| [método ou referência ao trecho] | [descrição estrutural] | [resultados, ramos ou caminhos a exercitar] |
