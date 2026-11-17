# Relatório da atividade com LLMs

Substituam os campos entre colchetes. Preservem os títulos, os nomes dos perfis e as colunas. Usem `ND` para dado indisponível, com justificativa, e `0` para contagem efetivamente igual a zero.

## Identificação e ambiente

- Integrantes: [nomes completos da dupla ou trio]
- artifactId: [valor no pom.xml]
- Java: [versão]
- Maven: [versão]
- Sistema operacional: [nome e versão]

## Reprodução das consultas por API

- Configuração oficial: Groq Free, `openai/gpt-oss-120b`
- Python: [versão]
- Plano congelado: [manifesto](plano-llm/manifesto.json)
- Ordem, tentativas e metadados: [log da API](evidencias/eventos.jsonl)
- Comando utilizado: `python3 scripts/gerar_testes_llm.py gerar`
- Instruções de acesso, validação e reprodução: [guia do projeto](docs/consulta-llm.md)
- Incidentes e desvios observados: [perfis afetados e descrição, ou nenhum]

## Análises anteriores às consultas

Preencham os arquivos abaixo antes da geração. Registrem as classes de equivalência, os valores-limite, as tabelas de decisão e as obrigações de cobertura aplicáveis. Justifiquem critérios dispensados quando necessário. Os casos concretos e seus oráculos serão projetados pela LLM e discutidos após a geração.

- [Aluguel](analises/aluguel.md)
- [Pôquer](analises/poquer.md)
- [Acadêmico](analises/academico.md)

## Execuções e evidências

| Perfil | Comando executado | Resultado da execução e justificativa, se necessário | Registro |
|---|---|---|---|
| aluguel-completa | [comando] | [resultado] | [registro](evidencias/aluguel-completa/registro.md) |
| aluguel-sem-codigo | [comando] | [resultado] | [registro](evidencias/aluguel-sem-codigo/registro.md) |
| aluguel-sem-especificacao | [comando] | [resultado] | [registro](evidencias/aluguel-sem-especificacao/registro.md) |
| aluguel-sem-analise | [comando] | [resultado] | [registro](evidencias/aluguel-sem-analise/registro.md) |
| poquer-completa | [comando] | [resultado] | [registro](evidencias/poquer-completa/registro.md) |
| poquer-sem-codigo | [comando] | [resultado] | [registro](evidencias/poquer-sem-codigo/registro.md) |
| poquer-sem-especificacao | [comando] | [resultado] | [registro](evidencias/poquer-sem-especificacao/registro.md) |
| poquer-sem-analise | [comando] | [resultado] | [registro](evidencias/poquer-sem-analise/registro.md) |
| academico-completa | [comando] | [resultado] | [registro](evidencias/academico-completa/registro.md) |
| academico-sem-codigo | [comando] | [resultado] | [registro](evidencias/academico-sem-codigo/registro.md) |
| academico-sem-especificacao | [comando] | [resultado] | [registro](evidencias/academico-sem-especificacao/registro.md) |
| academico-sem-analise | [comando] | [resultado] | [registro](evidencias/academico-sem-analise/registro.md) |

## Métricas por perfil

Em testes executados, registrem o total do Surefire e informem falhas, erros e ignorados nas colunas próprias. Em exclusões, contem os testes removidos antes da execução. Para linhas e ramos, usem o contador da classe principal no XML JaCoCo. Para mutação, contem apenas `KILLED` como mortos e incluam todos os mutantes reportados no denominador. Em outros estados, discriminem os nomes e as contagens.

| Perfil | Testes no Surefire | Falhas | Erros | Ignorados | Exclusões | Linhas cobertas/total | Ramos cobertos/total | KILLED/total | SURVIVED | NO_COVERAGE | TIMED_OUT | Outros estados |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aluguel-completa | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] |
| aluguel-sem-codigo | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] |
| aluguel-sem-especificacao | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] |
| aluguel-sem-analise | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] |
| poquer-completa | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] |
| poquer-sem-codigo | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] |
| poquer-sem-especificacao | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] |
| poquer-sem-analise | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] |
| academico-completa | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] |
| academico-sem-codigo | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] |
| academico-sem-especificacao | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] |
| academico-sem-analise | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] | [valor] |

## Test smells por perfil

Usem o `summary.json` do tsDetect para registrar os métodos reconhecidos e as contagens. Listem os tipos com ocorrência positiva e indiquem a evidência. Se a medição estiver indisponível, usem `ND` e expliquem o motivo.

| Perfil | Métodos reconhecidos | Total de ocorrências | Tipos e contagens | Evidência ou justificativa de ND |
|---|---|---|---|---|
| aluguel-completa | [valor] | [valor] | [tipos e contagens] | [link ou motivo] |
| aluguel-sem-codigo | [valor] | [valor] | [tipos e contagens] | [link ou motivo] |
| aluguel-sem-especificacao | [valor] | [valor] | [tipos e contagens] | [link ou motivo] |
| aluguel-sem-analise | [valor] | [valor] | [tipos e contagens] | [link ou motivo] |
| poquer-completa | [valor] | [valor] | [tipos e contagens] | [link ou motivo] |
| poquer-sem-codigo | [valor] | [valor] | [tipos e contagens] | [link ou motivo] |
| poquer-sem-especificacao | [valor] | [valor] | [tipos e contagens] | [link ou motivo] |
| poquer-sem-analise | [valor] | [valor] | [tipos e contagens] | [link ou motivo] |
| academico-completa | [valor] | [valor] | [tipos e contagens] | [link ou motivo] |
| academico-sem-codigo | [valor] | [valor] | [tipos e contagens] | [link ou motivo] |
| academico-sem-especificacao | [valor] | [valor] | [tipos e contagens] | [link ou motivo] |
| academico-sem-analise | [valor] | [valor] | [tipos e contagens] | [link ou motivo] |

## Comparação entre condições

Calculem Completa menos cada ablação a partir das frações e arredondem apenas o resultado. Justifiquem `ND` quando a comparação estiver indisponível.

| Funcionalidade | Comparação | Δ linhas (pp) | Δ ramos (pp) | Δ mutação (pp) | Justificativa para ND |
|---|---|---|---|---|---|
| aluguel | Completa − Sem código | [valor] | [valor] | [valor] | [motivo ou não se aplica] |
| aluguel | Completa − Sem especificação | [valor] | [valor] | [valor] | [motivo ou não se aplica] |
| aluguel | Completa − Sem análise | [valor] | [valor] | [valor] | [motivo ou não se aplica] |
| poquer | Completa − Sem código | [valor] | [valor] | [valor] | [motivo ou não se aplica] |
| poquer | Completa − Sem especificação | [valor] | [valor] | [valor] | [motivo ou não se aplica] |
| poquer | Completa − Sem análise | [valor] | [valor] | [valor] | [motivo ou não se aplica] |
| academico | Completa − Sem código | [valor] | [valor] | [valor] | [motivo ou não se aplica] |
| academico | Completa − Sem especificação | [valor] | [valor] | [valor] | [motivo ou não se aplica] |
| academico | Completa − Sem análise | [valor] | [valor] | [valor] | [motivo ou não se aplica] |

## Referência externa com EvoSuite

| Funcionalidade | Linhas cobertas/total | Ramos cobertos/total | KILLED/total | Evidência ou motivo de ND | Comparação com a LLM |
|---|---|---|---|---|---|
| aluguel | [valor] | [valor] | [valor] | [referência] | [análise] |
| poquer | [valor] | [valor] | [valor] | [referência] | [análise] |
| academico | [valor] | [valor] | [valor] | [referência] | [análise] |

## Discussão

Para cada funcionalidade, citem IDs dos casos, métodos JUnit ou trechos das evidências. Comparem as quatro suítes lado a lado e expliquem as diferenças e o efeito da análise do grupo. Expliquem os test smells mais relevantes com exemplos das suítes. Identifiquem regras omitidas, redundâncias ou oráculos fracos quando observados e indiquem como revisariam os testes.

- aluguel: [análise]
- poquer: [análise]
- academico: [análise]
