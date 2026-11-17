# Registro de execução

Copiem este modelo como `evidencias/<perfil>/registro.md` para cada perfil. Substituam os campos entre colchetes. Usem `não exposto` para informação que a ferramenta não apresenta e `não se aplica` quando o campo não couber.

- Perfil: [nome do perfil]
- Consulta e tentativas: [links relativos aos metadados em `tentativas/NNN/`]
- Estado final da geração: [estado observado no resumo]
- Ocorrências e decisões do grupo: [descrição, ou nenhuma]

## Arquivos do perfil

| Evidência | Caminho relativo a este registro |
|---|---|
| Prompt enviado | `prompt.md` |
| Corpo completo da requisição enviada, com instruções de sistema quando usadas e sem credenciais | `requisicao.json` |
| Respostas e metadados por tentativa | `tentativas/NNN/` |
| Saída da execução Maven | `execucao.log` |
| Surefire | `surefire/` |
| JaCoCo | `jacoco/` |
| PIT | `pit/` |
| tsDetect | `tsdetect/test-smells.csv` e `tsdetect/summary.json` |

Copiem os relatórios gerados mantendo os nomes originais. Listem abaixo os arquivos ou relatórios indisponíveis e os motivos.

[Arquivos indisponíveis e motivos, ou nenhum.]

## Histórico de ajustes

| Caso ou método | Situação original | Alteração ou exclusão | Motivo e regra da especificação, se aplicável |
|---|---|---|---|
| [identificação] | [o que a IA gerou] | [o que mudou] | [justificativa] |

Se não houve ajustes, escrevam `Nenhum ajuste`.
