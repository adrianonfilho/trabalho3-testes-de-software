# Consultas auditáveis à API da Groq

O projeto usa o GPT-OSS 120B (`openai/gpt-oss-120b`) via Chat Completions da GroqCloud. Use uma conta no plano Free, sem ativar faturamento, e uma chave por grupo. Consulte a [criação de chaves](https://console.groq.com/keys), os [limites vigentes](https://console.groq.com/docs/rate-limits) e a [referência da API](https://console.groq.com/docs/api-reference). A cota é por organização e pode variar. O maior prompt completo deve ser conferido em um piloto docente antes de distribuir a atividade.

Use Python 3.9 ou superior, sem dependências adicionais. O script resolve caminhos relativos a partir da raiz do projeto e informa no terminal onde grava as evidências. Na raiz do projeto, copie o modelo e preencha `GROQ_API_KEY` no arquivo `.env` com a chave da Groq.

```sh
cp .env.example .env
```

No PowerShell, use `Copy-Item .env.example .env`. O Git ignora o `.env` local, e o `.env.example` fica no projeto como modelo vazio. Se `GROQ_API_KEY` já estiver definida no ambiente do terminal, ela tem prioridade.

### Testar o acesso e preparar os prompts

Preencham os modelos de [aluguel](../analises/aluguel.md), [pôquer](../analises/poquer.md) e [acadêmico](../analises/academico.md). As orientações acima das tabelas descrevem o que colocar em cada coluna e são removidas na montagem do prompt. Os modelos oficiais já trazem os blocos Código e Especificação. O script confere se o bloco Código corresponde aos arquivos Java de produção sem Javadoc e com linhas em branco consecutivas reduzidas e usa o mesmo bloco em todas as condições que o incluem. Assim, Sem especificação omite o bloco Especificação e mantém o mesmo bloco Código da condição Completa.

Por exemplo, uma linha de caixa-branca pode identificar a decisão de fidelidade `PRATA` em `calcularCustoLocacao`, descrever a avaliação em curto-circuito e pedir cobertura da concessão e da rejeição em cada condição avaliada. A linha fica no nível da decisão e da cobertura. A LLM escolhe os argumentos, calcula os totais esperados e escreve as asserções.

```sh
python3 scripts/gerar_testes_llm.py piloto --saida evidencias-piloto
python3 scripts/gerar_testes_llm.py preparar
python3 scripts/gerar_testes_llm.py verificar
```

O piloto envia somente um exemplo alheio à atividade e salva a evidência em `evidencias-piloto/`. A preparação funciona sem credenciais e cria `plano-llm/`, com os doze prompts, uma cópia das análises usadas e o manifesto. Versionem ou entreguem o manifesto com os prompts antes de gerar as suítes oficiais.

### Executar as consultas oficiais

```sh
python3 scripts/gerar_testes_llm.py gerar
```

A ordem padrão é aluguel, pôquer e acadêmico. Em cada funcionalidade, a sequência é Completa, Sem código, Sem especificação e Sem análise. Cada requisição contém uma mensagem de usuário e os parâmetros fixos, com temperatura 0, esforço de raciocínio baixo e teto de 4.096 tokens de conclusão. A execução usa chamadas sequenciais, sem histórico e sem ferramentas. A temperatura 0 pode reduzir a variabilidade, e novas chamadas ainda podem produzir outras respostas.

Se houver erro de cota ou de serviço, o script registra a tentativa e aguarda o intervalo de `Retry-After` quando fornecido, com até três tentativas por perfil naquela execução. Se persistir um erro HTTP ou de transporte, a execução para e pode ser retomada com o mesmo comando após resolver a causa. Perfis com HTTP 200 arquivado são preservados, inclusive respostas truncadas ou incompletas. Registrem essas limitações no relatório. Se uma interrupção deixar uma tentativa sem metadados, preservem a saída e registrem a reprodução em outro diretório.

Para reproduzir uma consulta sem substituir a evidência oficial:

```sh
python3 scripts/gerar_testes_llm.py gerar --perfil aluguel-completa --saida target/reproducao-aluguel
```

### Evidências produzidas

| Arquivo ou diretório | Conteúdo |
|---|---|
| `plano-llm/manifesto.json` | Ordem prevista, endpoint, parâmetros e SHA-256 do script, das fontes e dos prompts |
| `plano-llm/analises/` | Arquivos de análise usados na montagem dos prompts |
| `evidencias/plano.json` | Cópia do manifesto efetivamente usado |
| `evidencias/eventos.jsonl` | Ordem efetiva, horários UTC, duração, status, limites e espera quando disponíveis |
| `evidencias/resumo.json` | Último estado observado de cada perfil executado |
| `evidencias/<perfil>/prompt.md` e `requisicao.json` | Prompt e bytes do corpo enviado |
| `evidencias/<perfil>/tentativas/NNN/` | Resposta bruta, texto extraído quando disponível e metadados com ID, modelo retornado, motivo de término e uso de tokens |

O cabeçalho de autenticação fica fora dos arquivos. Se a API ecoar a chave no corpo, o script a oculta e marca a ocorrência nos metadados. O manifesto permite detectar alterações nos arquivos congelados. A versão entregue antes da geração registra quais prompts foram apresentados.

Completem as evidências com `registro.md`, o log Maven e os relatórios Surefire, JaCoCo, PIT e tsDetect, seguindo o modelo do projeto. Para guardar a saída completa do Maven, use o perfil correspondente, como neste exemplo:

```sh
mkdir -p evidencias/aluguel-completa
./mvnw -Paluguel-completa,medir,tsdetect verify > evidencias/aluguel-completa/execucao.log 2>&1
```

### Piloto docente dos doze perfis

Antes de distribuir a atividade, usem uma conta Free para preparar e executar um plano separado com análises de demonstração representativas do tamanho esperado. Usem `--analises` e `--plano` na preparação, e o mesmo `--plano` com uma `--saida` separada na geração. Confiram os doze estados, o uso de tokens, os limites retornados e, em particular, o motivo de término dos prompts completos. Registrem a data e o resultado do piloto com a versão do projeto. Se algum limite exigir alterar os parâmetros, façam isso antes de os alunos congelarem os planos.
