# Geração de testes JUnit 5 com LLMs

Nesta atividade, vocês usarão uma LLM para projetar testes unitários e devolver o código Java em **JUnit 5**. Uma LLM é um modelo de linguagem que pode gerar texto e código a partir das informações que recebe. Chamamos de **prompt** o texto enviado ao modelo. Ele inclui o pedido de geração e o material que o modelo pode usar para atender ao pedido.

O grupo prepara parte desse material aplicando técnicas que já conhece. Da análise caixa-preta vêm classes de equivalência, valores-limite e regras em tabelas de decisão. Da análise caixa-branca vêm decisões, condições, ramos ou caminhos que merecem cobertura. A LLM usa as informações disponíveis para **escolher as entradas concretas, determinar os resultados esperados e escrever as asserções JUnit 5**. O grupo executa os testes e verifica se o que foi gerado faz sentido à luz da especificação.

A pergunta da atividade é **como a qualidade das suítes muda quando retiramos um bloco do prompt?** Ao final, vocês vão comparar cobertura, mutação e test smells e examinar os testes gerados para explicar as diferenças.

Trabalhem em **dupla ou trio**. Atualizem o `artifactId` no `pom.xml` para identificar todos os integrantes, sem espaços ou acentos. Um exemplo é `AnaSilva-BrunoLima`. Usem o mesmo identificador na entrega e indiquem os nomes completos no relatório.

| Funcionalidade | Especificação | Modelo de prompt | Pacote Java e prefixo do perfil |
|---|---|---|---|
| Aluguel de carros | [Especificação](docs/aluguel/especificacao.md) | [Modelo de ablação](docs/aluguel/prompt-ablação-template.md) | `br.com.aluguelcarros` / `aluguel` |
| Mão de pôquer | [Especificação](docs/poquer/especificacao.md) | [Modelo de ablação](docs/poquer/prompt-ablação-template.md) | `br.com.poquer` / `poquer` |
| Consolidação parcial acadêmica | [Especificação](docs/academico/especificacao.md) | [Modelo de ablação](docs/academico/prompt-ablação-template.md) | `br.com.academico` / `academico` |

## Como funciona a ablação

Cada prompt começa com o mesmo pedido de geração em JUnit 5 e a mesma descrição da API pública Java, com as assinaturas que a suíte pode chamar. O prompt completo acrescenta três blocos:

- **Código** — a implementação Java da funcionalidade.
- **Especificação** — as regras e os comportamentos esperados.
- **Análise** — as informações que o grupo produz ao aplicar os critérios de teste.

Uma **ablação** é a retirada de um componente para observar o que muda no resultado. Neste projeto, o script monta três versões do prompt completo, cada uma omitindo um único bloco. O restante do texto, o modelo e os parâmetros permanecem iguais.

| Condição | Blocos enviados além do pedido e da API pública Java |
|---|---|
| Completa | Código + Especificação + Análise |
| Sem código | Especificação + Análise |
| Sem especificação | Código + Análise |
| Sem análise | Código + Especificação |

Por exemplo, ao comparar **Completa** com **Sem análise** para aluguel, a LLM recebe o mesmo código e a mesma especificação nas duas chamadas. A diferença é a análise produzida pelo grupo. Essa é a comparação principal para investigar a contribuição do trabalho dos alunos. Como a análise pode descrever regras da especificação ou decisões do código, cada ablação mede o efeito de fornecer aquele bloco diretamente.

São **quatro suítes por funcionalidade, totalizando doze**. Cada prompt gera sua própria suíte em uma chamada independente.

## Como preparar e gerar as suítes

1. **Comecem pela especificação.** Antes de examinar a implementação, registrem a análise caixa-preta das três funcionalidades. Identifiquem classes de equivalência, valores-limite e regras em tabelas de decisão, quando pertinentes. A ação da tabela descreve o comportamento geral previsto para cada combinação de condições.
2. **Leiam a implementação.** Registrem a análise caixa-branca descrevendo decisões, condições, ramos ou caminhos e as respectivas obrigações de cobertura. Preencham os três modelos em `analises/` no nível dos critérios. A LLM vai projetar os casos concretos a partir desse material.
3. **Preparem e confiram os prompts.** O script reúne as análises e os materiais oficiais, monta as quatro versões por funcionalidade e salva os doze prompts e seus hashes em `plano-llm/`. Confiram e congelem o plano antes da primeira consulta oficial. Mantenham testes existentes, saídas de execução e relatórios fora dos prompts.
4. **Enviem os prompts.** O script usa o **GPT-OSS 120B pela API da Groq no plano Free**. Nesse contexto, a API da Groq é o serviço que recebe o prompt pelo script e devolve a resposta do modelo. O script envia um prompt de cada vez, sem histórico de outras chamadas, e guarda a resposta original. Sigam o [guia de consulta e reprodução](docs/consulta-llm.md).
5. **Executem e revisem os testes.** Transcrevam o Java gerado para a classe JUnit 5 do perfil correspondente e rodem o Maven. Registrem os ajustes mínimos de compilação e integração. Confiram os resultados esperados pela especificação e expliquem correções ou exclusões, preservando a resposta original. Apliquem a mesma política nas quatro condições e mantenham fixo o código de produção.

### Experimentar a montagem dos prompts

Os arquivos em `analises/` já vêm com linhas de demonstração sobre um pedido fictício. Para montar e verificar os 12 prompts localmente, usem:

```sh
python3 scripts/gerar_testes_llm.py preparar --plano target/plano-llm-demo
python3 scripts/gerar_testes_llm.py verificar --plano target/plano-llm-demo
```

Esses comandos funcionam sem chave e sem chamada à Groq. Antes da geração oficial, substituam as linhas fictícias pelas análises das três funcionalidades e usem `preparar` sem `--plano` para criar `plano-llm/`.

## Transparência, auditoria e reprodução

LLMs podem produzir respostas diferentes para o mesmo prompt, mesmo com o mesmo modelo e os mesmos parâmetros. A reprodução mínima consiste em repetir o procedimento de consulta e em executar as suítes entregues a partir das evidências originais. Guardem o prompt exato, o corpo completo da requisição enviada à API, a resposta bruta e o registro de cada consulta para que o avaliador possa conferir a origem dos testes e os ajustes realizados.

O uso do script e da API é obrigatório nas quatro condições. O manifesto identifica a configuração e os prompts congelados. O script grava na raiz do projeto, em `evidencias/`, a ordem efetiva, o corpo da requisição, a resposta bruta e as falhas. A consulta de demonstração usa `evidencias-piloto/`. Usem uma saída separada para reproduções.

### Configurar a chave da Groq

1. Criem uma chave no plano Free na [página de chaves da Groq](https://console.groq.com/keys).
2. Na raiz do projeto, copiem o modelo com `cp .env.example .env`. No PowerShell, usem `Copy-Item .env.example .env`.
3. Abram o arquivo `.env` e colem a chave após `GROQ_API_KEY=`, na mesma linha. O Git ignora esse arquivo local.
4. Testem a configuração com `python3 scripts/gerar_testes_llm.py piloto --saida evidencias-piloto`. A mensagem `piloto: ok` confirma que a chamada funcionou.

## Entregas semanais

| Semana | Entrega | Marco a conferir |
|---|---|---|
| 1 — 17/11 | Configuração do acesso à LLM via API | O piloto exibe `piloto: ok` e salva a evidência da consulta em `evidencias-piloto/`. |
| 2 | Informações produzidas pela aplicação dos critérios de teste | As análises caixa-preta e caixa-branca das três funcionalidades registram classes de equivalência, valores-limite, regras de decisão e obrigações de cobertura aplicáveis. |
| 3 | Prompts completos e dados iniciais | O grupo entrega o plano com os 12 prompts de ablação e o manifesto. Os prompts são congelados antes das consultas oficiais. Os dados iniciais incluem as primeiras requisições, respostas e medições disponíveis. |
| 4 | Entrega final | O projeto inclui as 12 suítes, as evidências de execução e o relatório com métricas, comparação com EvoSuite e discussão das ablações. |

Entreguem uma versão cumulativa a cada semana.

## Execução e medição

Usem JDK 17 e Maven ou o wrapper do projeto. O JDK 21 também pode executar a atividade. Cada pacote tem quatro arquivos em `src/test/java`, nos diretórios `br/com/aluguelcarros`, `br/com/poquer` e `br/com/academico`. Em cada diretório, preencham `SuiteCompleta.java`, `SuiteSemCodigo.java`, `SuiteSemEspecificacao.java` e `SuiteSemAnalise.java` com testes JUnit 5. As classes começam vazias. O Maven exige testes executáveis no perfil selecionado.

Para executar apenas uma suíte, por exemplo, usem `./mvnw -Paluguel-completa test`. Para medir as doze, executem os comandos abaixo separadamente, com uma condição por vez. No Windows, usem `mvnw.cmd`.

```sh
./mvnw -Paluguel-completa,medir,tsdetect verify
./mvnw -Paluguel-sem-codigo,medir,tsdetect verify
./mvnw -Paluguel-sem-especificacao,medir,tsdetect verify
./mvnw -Paluguel-sem-analise,medir,tsdetect verify
./mvnw -Ppoquer-completa,medir,tsdetect verify
./mvnw -Ppoquer-sem-codigo,medir,tsdetect verify
./mvnw -Ppoquer-sem-especificacao,medir,tsdetect verify
./mvnw -Ppoquer-sem-analise,medir,tsdetect verify
./mvnw -Pacademico-completa,medir,tsdetect verify
./mvnw -Pacademico-sem-codigo,medir,tsdetect verify
./mvnw -Pacademico-sem-especificacao,medir,tsdetect verify
./mvnw -Pacademico-sem-analise,medir,tsdetect verify
```

Para cada perfil, guardem o relatório Surefire de `target/surefire-reports/<perfil>/`, JaCoCo de `target/site/jacoco/<perfil>/` e PIT de `target/pit-reports/<perfil>/`, incluindo HTML e XML quando gerados. Guardem também `test-smells.csv` e `summary.json` de `target/tsdetect/<perfil>/` em `evidencias/<perfil>/tsdetect/`. Copiem as evidências antes de executar `clean`. O perfil mede a classe principal daquela funcionalidade com a suíte selecionada. Os tipos auxiliares, como os enums, ficam fora desse recorte. O perfil `medir` usa o conjunto padrão de mutadores, sem meta mínima de cobertura ou mutação.

Para cada funcionalidade, apresentem lado a lado o número de testes, falhas e exclusões, linhas e ramos cobertos sobre o total, e mutantes mortos sobre o total. Registrem separadamente os sobreviventes, sem cobertura, timeouts e demais estados do XML. Calculem Completa menos cada ablação em pontos percentuais quando houver denominador válido. Tratem Completa menos Sem análise como a comparação principal para avaliar a contribuição dos alunos. Se a execução falhar ou a métrica não estiver disponível, registrem o motivo. Justifiquem as diferenças com casos concretos, incluindo oráculos fracos, redundâncias ou regras que a IA deixou de cobrir. Discutam como a análise do grupo afetou as suítes e o que vocês mudariam no projeto de testes.

### Análise de test smells

O tsDetect inspeciona o código dos testes em busca de padrões que podem dificultar a leitura, a manutenção ou o diagnóstico de falhas. O perfil `tsdetect` analisa a suíte selecionada e registra a quantidade de ocorrências por tipo. Na primeira execução, a ferramenta é baixada e compilada. Tenham Git, Maven, Java e Python 3.9 ou superior disponíveis no terminal.

Para cada suíte, registrem o número de métodos reconhecidos, o total de ocorrências e os tipos detectados. Na comparação, considerem o tamanho das suítes e expliquem, com um trecho ou método, os achados mais relevantes. Quando o detector não reconhecer os testes ou a medição falhar, registrem `ND` com a justificativa. Preservem os achados da suíte medida e registrem eventuais propostas de melhoria no relatório.

## Referência externa com EvoSuite

A referência externa do EvoSuite será fornecida separadamente pelo docente. Usem os resultados distribuídos para a comparação no relatório. As asserções do EvoSuite registram o comportamento observado e podem ser analisadas frente à especificação.

## Entrega e critérios de correção

- Entreguem o projeto Maven. Preencham o [modelo de relatório](relatorio-llm.md) na raiz do projeto com todas as respostas, análises e justificativas, incluindo identificação, ambiente, comandos, as análises caixa-preta e caixa-branca das três funcionalidades, tabela comparativa e discussão. Mantenham o código das doze suítes em `src/test/java` e referenciem as evidências por links relativos no relatório.
- Em cada pasta `evidencias/<perfil>/`, copiem o [modelo de registro](docs/modelos/registro.md) como `registro.md` e preservem os nomes de arquivos indicados no modelo. Entreguem o manifesto, os arquivos automáticos da API, os relatórios de teste e o histórico de ajustes. Excluam segredos e dados pessoais dos registros.
- Na correção serão considerados a qualidade das análises caixa-preta e caixa-branca, a fidelidade ao protocolo e a rastreabilidade, a correção e execução dos testes e a interpretação das métricas e dos test smells. Demonstrem a contribuição do grupo com a análise produzida antes da IA e a crítica dos testes após a geração.
