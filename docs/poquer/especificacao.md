# Classificação de mão de pôquer

## API pública

Classe `Mao` no pacote `br.com.poquer`.

```java
public Mao(java.util.List<ValorCarta> valores, java.util.List<Naipe> naipes)
public ClassificacaoMao classificar() // método de Mao
```

O enum `ValorCarta` contém `AS`, `DOIS`, `TRES`, `QUATRO`, `CINCO`, `SEIS`, `SETE`, `OITO`, `NOVE`, `DEZ`, `VALETE`, `DAMA` e `REI`. O enum `Naipe` contém `COPAS`, `OUROS`, `PAUS` e `ESPADAS`.

## Entradas válidas

Passe duas listas com cinco elementos cada. `valores[i]` e `naipes[i]` formam uma carta. Os cinco pares devem ser distintos. A ordem da mão é livre, desde que valor e naipe de cada carta permaneçam juntos ao reordenar as listas.

## Resultados e exceções

Uma sequência tem cinco valores consecutivos distintos. O ás pode ocupar a primeira posição na sequência mais baixa ou a última na sequência mais alta. Em outras posições, a passagem de rei para ás quebra a sequência.

O método devolve a primeira classificação aplicável, nesta ordem de prioridade:

1. `SEQUENCIA_REAL_DO_MESMO_NAIPE` — 10–J–Q–K–A do mesmo naipe.
2. `SEQUENCIA_DO_MESMO_NAIPE` — sequência do mesmo naipe.
3. `QUADRA` — quatro cartas do mesmo valor.
4. `TRINCA_E_PAR` — três cartas de um valor e duas de outro.
5. `CINCO_DO_MESMO_NAIPE` — cinco cartas do mesmo naipe sem sequência.
6. `SEQUENCIA` — sequência com mais de um naipe.
7. `TRINCA` — três cartas do mesmo valor.
8. `DOIS_PARES` — dois pares de valores distintos.
9. `UM_PAR` — duas cartas do mesmo valor.
10. `CARTA_ALTA` — demais mãos.

Lista nula ou elemento nulo provoca `NullPointerException`. Lista com tamanho diferente de cinco ou par de valor e naipe repetido provoca `IllegalArgumentException`.
