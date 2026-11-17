Você é especialista em testes unitários Java com JUnit 5. Use o material fornecido para projetar os casos de teste, escolher as entradas e determinar os resultados ou exceções esperados. Responda somente com o código Java completo da suíte JUnit 5, incluindo o pacote e os imports necessários. Entregue o código em texto puro, sem cercas de Markdown nem explicações.

# Custo de locação de carro

## API pública

Classe `CalculadoraCustoLocacao` no pacote `br.com.aluguelcarros`. O tipo `BigDecimal` é de `java.math`.

```java
public CalculadoraCustoLocacao()
public BigDecimal calcularCustoLocacao(CategoriaVeiculo categoria, NivelCliente nivelCliente,
    int numeroDiarias, int quilometrosRodados, int horasAtraso, TipoSeguro seguro,
    boolean possuiAtrasoAnterior)
```

- `CategoriaVeiculo` — `ECONOMICO`, `INTERMEDIARIO`, `SUV`.
- `NivelCliente` — `COMUM`, `PRATA`, `OURO`.
- `TipoSeguro` — `SEM_SEGURO`, `BASICO`, `COMPLETO`.

## Código

`src/main/java/br/com/aluguelcarros/CalculadoraCustoLocacao.java`

```java
package br.com.aluguelcarros;

import java.math.BigDecimal;
import java.math.RoundingMode;

public class CalculadoraCustoLocacao
{
    public BigDecimal calcularCustoLocacao(CategoriaVeiculo categoria, NivelCliente nivelCliente, int numeroDiarias, int quilometrosRodados, int horasAtraso, TipoSeguro seguro, boolean possuiAtrasoAnterior)
    {
        if (categoria == null || nivelCliente == null || seguro == null)
        {
            throw new NullPointerException("Argumentos não podem ser nulos");
        }

        if (numeroDiarias <= 0)
        {
            throw new IllegalArgumentException("Número de diárias deve ser maior que zero");
        }

        if (quilometrosRodados < 0)
        {
            throw new IllegalArgumentException("Quilometragem rodada não pode ser negativa");
        }

        if (horasAtraso < 0)
        {
            throw new IllegalArgumentException("Horas de atraso não podem ser negativas");
        }

        BigDecimal valorDiaria;
        if (categoria == CategoriaVeiculo.ECONOMICO)
        {
            valorDiaria = new BigDecimal("120.00");
        }
        else if (categoria == CategoriaVeiculo.INTERMEDIARIO)
        {
            valorDiaria = new BigDecimal("180.00");
        }
        else
        {
            valorDiaria = new BigDecimal("280.00");
        }

        BigDecimal taxaDescontoDuracao;
        if (numeroDiarias <= 2)
        {
            taxaDescontoDuracao = BigDecimal.ZERO;
        }
        else if (numeroDiarias <= 6)
        {
            taxaDescontoDuracao = new BigDecimal("0.05");
        }
        else if (numeroDiarias <= 14)
        {
            taxaDescontoDuracao = new BigDecimal("0.10");
        }
        else
        {
            taxaDescontoDuracao = new BigDecimal("0.15");
        }

        BigDecimal valorBrutoDiarias = valorDiaria.multiply(BigDecimal.valueOf(numeroDiarias));
        BigDecimal descontoDuracao = valorBrutoDiarias.multiply(taxaDescontoDuracao);
        BigDecimal valorDiariasComDesconto = valorBrutoDiarias.subtract(descontoDuracao);

        // Cada condição representa um requisito independente para o benefício.
        BigDecimal taxaDescontoFidelidade;
        if (nivelCliente == NivelCliente.PRATA && numeroDiarias >= 7 && !possuiAtrasoAnterior)
        {
            taxaDescontoFidelidade = new BigDecimal("0.05");
        }
        else if (nivelCliente == NivelCliente.OURO && numeroDiarias >= 5 && !possuiAtrasoAnterior)
        {
            taxaDescontoFidelidade = new BigDecimal("0.10");
        }
        else
        {
            taxaDescontoFidelidade = BigDecimal.ZERO;
        }

        BigDecimal descontoFidelidade = valorDiariasComDesconto.multiply(taxaDescontoFidelidade);
        BigDecimal valorFinalDiarias = valorDiariasComDesconto.subtract(descontoFidelidade);

        // O uso de long evita estouro ao multiplicar uma quantidade grande de diárias.
        long franquiaQuilometros = 100L * numeroDiarias;
        long quilometrosExcedentes = (long) quilometrosRodados - franquiaQuilometros;
        BigDecimal custoQuilometragem;
        if (quilometrosExcedentes <= 0)
        {
            custoQuilometragem = BigDecimal.ZERO;
        }
        else
        {
            BigDecimal tarifaQuilometrica;
            if (quilometrosExcedentes <= 100)
            {
                tarifaQuilometrica = new BigDecimal("0.80");
            }
            else if (quilometrosExcedentes <= 300)
            {
                tarifaQuilometrica = new BigDecimal("1.00");
            }
            else
            {
                tarifaQuilometrica = new BigDecimal("1.50");
            }
            custoQuilometragem = BigDecimal.valueOf(quilometrosExcedentes).multiply(tarifaQuilometrica);
        }

        BigDecimal valorSeguroDiaria;
        if (seguro == TipoSeguro.SEM_SEGURO)
        {
            valorSeguroDiaria = BigDecimal.ZERO;
        }
        else if (seguro == TipoSeguro.BASICO)
        {
            valorSeguroDiaria = new BigDecimal("25.00");
        }
        else
        {
            valorSeguroDiaria = new BigDecimal("45.00");
        }
        BigDecimal custoSeguro = valorSeguroDiaria.multiply(BigDecimal.valueOf(numeroDiarias));

        BigDecimal custoAtraso;
        if (horasAtraso <= 1)
        {
            custoAtraso = BigDecimal.ZERO;
        }
        else if (horasAtraso <= 3)
        {
            custoAtraso = valorDiaria.multiply(new BigDecimal("0.20")).multiply(BigDecimal.valueOf(horasAtraso));
        }
        else
        {
            custoAtraso = valorDiaria;
        }

        BigDecimal total = valorFinalDiarias.add(custoQuilometragem).add(custoSeguro).add(custoAtraso);
        return total.setScale(2, RoundingMode.HALF_UP);
    }
}
```

`src/main/java/br/com/aluguelcarros/CategoriaVeiculo.java`

```java
package br.com.aluguelcarros;

public enum CategoriaVeiculo
{
    ECONOMICO,
    INTERMEDIARIO,
    SUV
}
```

`src/main/java/br/com/aluguelcarros/NivelCliente.java`

```java
package br.com.aluguelcarros;

public enum NivelCliente
{
    COMUM,
    PRATA,
    OURO
}
```

`src/main/java/br/com/aluguelcarros/TipoSeguro.java`

```java
package br.com.aluguelcarros;

public enum TipoSeguro
{
    SEM_SEGURO,
    BASICO,
    COMPLETO
}
```

## Especificação

### Entradas válidas

Informe categoria, nível e seguro. O número de diárias deve ser positivo. Quilometragem rodada e horas de atraso devem ser inteiros não negativos. `possuiAtrasoAnterior` indica se o cliente tem registro de atraso anterior.

### Resultados e exceções

O total em reais soma diárias após descontos, quilometragem excedente, seguro e atraso. O retorno é um `BigDecimal` com duas casas decimais e arredondamento `HALF_UP`.

| Componente | Regra |
|---|---|
| Diária | `ECONOMICO` R$ 120, `INTERMEDIARIO` R$ 180, `SUV` R$ 280. |
| Desconto por duração | Sobre as diárias brutas: 1–2 → 0%, 3–6 → 5%, 7–14 → 10%, 15 ou mais → 15%. |
| Fidelidade | Sobre as diárias após o desconto por duração: `PRATA` 5% a partir de 7 diárias, `OURO` 10% a partir de 5. `COMUM` ou cliente com atraso anterior recebe 0%. |
| Quilometragem | Franquia de 100 km por diária. Cobra-se todo o excedente a uma única tarifa: até 100 km → R$ 0,80/km, 101–300 km → R$ 1,00/km, acima de 300 km → R$ 1,50/km. |
| Seguro por diária | `SEM_SEGURO` R$ 0, `BASICO` R$ 25, `COMPLETO` R$ 45. |
| Atraso | 0–1 h → isento, 2–3 h → 20% da diária sem desconto por hora, 4 h ou mais → uma diária sem desconto. |

Categoria, nível ou seguro nulo geram `NullPointerException`. Com esses argumentos presentes, menos de uma diária, quilometragem negativa ou atraso negativo geram `IllegalArgumentException`.

## Análise

# Critérios de teste — aluguel

> Orientação: Substituam todos os campos entre colchetes. Acrescentem uma linha por classe, fronteira, regra ou obrigação de cobertura. Se um critério não se aplicar, substituam sua tabela por uma justificativa breve.

> Orientação: Registrem somente os critérios e seus resultados de análise. A LLM escolhe os valores de entrada para cada caso, determina o resultado esperado e escreve os testes JUnit.

### Análise caixa-preta do grupo

> Orientação: Usem a especificação como fonte. Considerem as faixas de diárias, quilometragem e atraso e as regras de fidelidade.

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
