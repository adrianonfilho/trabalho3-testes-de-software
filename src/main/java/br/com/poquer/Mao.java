package br.com.poquer;

import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class Mao {
    private final List<ValorCarta> valores;
    private final List<Naipe> naipes;

    public Mao(List<ValorCarta> valores, List<Naipe> naipes) {
        this.valores = List.copyOf(valores);
        this.naipes = List.copyOf(naipes);
        if (this.valores.size() != 5 || this.naipes.size() != 5) {
            throw new IllegalArgumentException("Uma mão deve conter cinco valores e cinco naipes");
        }

        Set<Map.Entry<ValorCarta, Naipe>> cartasDistintas = new HashSet<>();
        for (int indice = 0; indice < this.valores.size(); indice++) {
            if (!cartasDistintas.add(Map.entry(this.valores.get(indice), this.naipes.get(indice)))) {
                throw new IllegalArgumentException("Uma mão deve conter cinco cartas distintas");
            }
        }
    }

    /**
     * Determina a classificação de maior prioridade para as cinco cartas da mão.
     * A ordem das cartas não altera o resultado. O ás pode iniciar a sequência
     * mais baixa ou terminar a sequência mais alta.
     *
     * @return classificação da mão de pôquer
     */
    public ClassificacaoMao classificar() {
        List<Integer> valoresOrdenados = valores.stream()
                .map(ValorCarta::numero).distinct().sorted().toList();
        boolean sequenciaAltaComAs = valoresOrdenados.equals(List.of(1, 10, 11, 12, 13));
        boolean sequencia = sequenciaAltaComAs
                || (valoresOrdenados.size() == 5 && valoresOrdenados.get(4) - valoresOrdenados.get(0) == 4);
        boolean mesmoNaipe = naipes.stream().allMatch(naipe -> naipe == naipes.get(0));

        int[] frequencias = new int[14];
        for (ValorCarta valor : valores) {
            frequencias[valor.numero()]++;
        }
        int pares = 0;
        int maiorFrequencia = 0;
        for (int frequencia : frequencias) {
            if (frequencia == 2) {
                pares++;
            }
            maiorFrequencia = Math.max(maiorFrequencia, frequencia);
        }

        if (mesmoNaipe && sequenciaAltaComAs) {
            return ClassificacaoMao.SEQUENCIA_REAL_DO_MESMO_NAIPE;
        }
        if (mesmoNaipe && sequencia) {
            return ClassificacaoMao.SEQUENCIA_DO_MESMO_NAIPE;
        }
        if (maiorFrequencia == 4) {
            return ClassificacaoMao.QUADRA;
        }
        if (maiorFrequencia == 3 && pares == 1) {
            return ClassificacaoMao.TRINCA_E_PAR;
        }
        if (mesmoNaipe) {
            return ClassificacaoMao.CINCO_DO_MESMO_NAIPE;
        }
        if (sequencia) {
            return ClassificacaoMao.SEQUENCIA;
        }
        if (maiorFrequencia == 3) {
            return ClassificacaoMao.TRINCA;
        }
        if (pares == 2) {
            return ClassificacaoMao.DOIS_PARES;
        }
        if (pares == 1) {
            return ClassificacaoMao.UM_PAR;
        }
        return ClassificacaoMao.CARTA_ALTA;
    }
}
