package br.com.academico;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Objects;

public class ConsolidacaoParcial {
    /**
     * Determina a situação acadêmica parcial com base nas notas e na frequência.
     * As notas e a média são arredondadas para uma casa decimal com arredondamento
     * de metade para cima antes da aplicação das regras de aprovação.
     *
     * @param nota1 nota da primeira unidade, entre 0 e 10
     * @param nota2 nota da segunda unidade, entre 0 e 10
     * @param nota3 nota da terceira unidade, entre 0 e 10
     * @param frequencia frequência percentual inteira, entre 0 e 100
     * @return situação acadêmica após a consolidação parcial
     * @throws NullPointerException se algum argumento for nulo
     * @throws IllegalArgumentException se uma nota for não finita ou algum valor estiver fora da faixa
     */
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
