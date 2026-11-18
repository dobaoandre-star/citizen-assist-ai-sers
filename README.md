# Citizen Assist AI — Primeiro Emprego

GS2026.2 · Pensamento Computacional e Automação com Python · FIAP · 1CCPY

**Nome:Yihang Xu— RM：571720(individual)

## GS2026.2 | Soluções em Energias Renováveis e Sustentáveis

Yihang Xu · RM 571720 · 1CCPY · Trabalho individual.

Escolha **6. Energia e iluminação** no menu para comparar LED na rede com LED apoiado por energia solar. A simulação usa dados de irradiação do INPE e premissas de uso e custo identificadas. Consulte [análise e referências](docs/ENERGIA_SERS.md) e [roteiro de testes com usuários](docs/TESTES_USUARIOS_SERS.md).

## Proposta

O assistente orienta jovens que estão se preparando para o primeiro emprego no Brasil. Reúne instruções sobre conta gov.br, Carteira de Trabalho Digital, procura de vagas e CPF. O problema é a informação espalhada em vários serviços oficiais. O programa apresenta orientações simples e informa onde conferir cada uma.

Relação proposta com os ODS: **8**, acesso ao trabalho; **10**, redução de barreiras de acesso à informação; **16**, acesso a informações de serviços públicos. O projeto não mede impacto social real nestes ODS.

## Estado da entrega

- Implementação e base inicial: prontas para revisão e estudo.
- Testes técnicos: execute o comando abaixo; relatório em `docs/VALIDACAO_TECNICA.md`.
- **Teste com pelo menos 3 pessoas externas e 10 atendimentos: PENDENTE.**
- **Melhoria baseada no teste real: PENDENTE.**
- **Repositório público:** https://github.com/dobaoandre-star/citizen-assist-ai
- **Vídeo próprio no YouTube, não listado: PENDENTE — inserir URL.**

Não apresentar testes automatizados como participação de usuários. O histórico distribuído está vazio de propósito. Antes de entregar, substituir as pendências pelos dados e links reais.

## Como executar

Requer Python 3.10 ou superior, sem bibliotecas externas. Extraia o ZIP e abra o terminal na pasta que contém `main.py`.

```bash
python main.py
```

No macOS, se necessário, use `python3 main.py`. Os caminhos de dados são relativos ao arquivo principal, portanto o programa também pode ser iniciado por um caminho absoluto.

Menu: 1 perguntar; 2 navegar por categorias; 3 indicadores; 4 exportar CSV; 5 recarregar JSON; 0 sair. Ao sair, informe a facilidade de 1 a 5. Na avaliação, 0 retorna ao menu sem encerrar. Todas as seleções têm retorno por 0. Ctrl+C/EOF encerra com exportação dos atendimentos concluídos.

## Organização e orientação a objetos

| Arquivo / classe | Responsabilidade |
|---|---|
| `main.py` | Inicialização e menu |
| `orientacao.py` / `Orientacao` | Atributos do registro JSON e método `exibir()` |
| `base_conhecimento.py` / `BaseConhecimento` | `carregar`, `categorias`, `por_categoria`, `pontuar`, `buscar` |
| `assistente.py` / `Assistente` | `perguntar`, `navegar`, `registrar`, `indicadores`, `exportar_csv` |
| `data/base_conhecimento.json` | 11 orientações em 3 categorias |
| `data/historico.json` | Lista de dicionários de atendimentos reais |
| `data/avaliacoes.json` | Notas anônimas por sessão |
| `data/atendimentos.csv` | Exportação tabular dos atendimentos |
| `tests/test_projeto.py` | Testes automatizados, com arquivos temporários |

Composição: um `Assistente` possui uma `BaseConhecimento`; a base possui uma lista de objetos `Orientacao`. `self` referencia o objeto que executa o método. Cada registro JSON é um dicionário. A busca produz uma lista de tuplas `(pontos, orientacao)`.

## Busca por pontuação

1. Normalização Unicode remove acentos, troca pontuação por espaços, converte para minúsculas e junta espaços repetidos.
2. Cada palavra-chave distinta presente como palavra ou frase inteira vale **3 pontos**.
3. Cada palavra distinta da pergunta, com pelo menos 4 caracteres, presente como palavra inteira no título vale **1 ponto**.
4. Ordenação decrescente pela pontuação; empates são resolvidos pelo menor ID.
5. **6 ou mais: ALTA; 3 a 5: MÉDIA; abaixo de 3: não encontrado**.
6. Exibe o melhor resultado e até duas alternativas com pelo menos 3 pontos. O usuário pode abrir uma alternativa; o registro guarda a orientação efetivamente exibida por último.

Exemplo: `Como obter carteira de trabalho digital?` → registro 4: frase `carteira de trabalho` = 3; palavras `obter`, `carteira`, `trabalho`, `digital` no título = 4; total **7, ALTA**. Repetir uma palavra não aumenta pontos. Frases sobrepostas diferentes podem pontuar, conforme a regra do enunciado.

O score mede semelhança textual, não probabilidade de verdade nem direito a um serviço. Não há IA generativa, API paga, inferência jurídica ou busca online durante a execução. Não foram integradas outras disciplinas.

## Regras, privacidade e arquivos

Perguntas com `@` ou pelo menos 8 dígitos no total, mesmo separados por pontuação, são recusadas antes da busca e não são gravadas. O registro também valida a mesma regra como segunda barreira. O programa não pede nome, CPF, telefone ou e-mail. Documentos citados na resposta devem ser apresentados apenas ao serviço oficial.

Essa regra não detecta todos os dados pessoais: nomes e endereços escritos por extenso podem passar. Oriente os participantes a usar perguntas genéricas e revise o histórico antes de publicar no GitHub. Não envie cópias de segurança `.bak`, que podem conter registros antigos.

JSON da base ausente, corrompido ou fora do esquema gera aviso sem encerrar. Se a recarga falhar depois de uma leitura válida, conserva a base anterior em memória. Histórico inválido é preservado em `.bak` antes de começar uma lista nova; se isso falhar, o salvamento desse arquivo é desativado. Escritas JSON usam arquivo temporário e substituição. Erros de exportação exibem aviso. CSV usa `csv.DictWriter`, UTF-8 com BOM e proteção contra fórmulas em perguntas.

## Definição dos indicadores

Um atendimento corresponde a uma pergunta válida enviada ou a uma orientação aberta por categoria. Perguntas não encontradas também contam. Uma nova pergunta é um novo atendimento. Entradas vazias antes da pergunta contam como tentativas; entradas bloqueadas por privacidade e retornos por 0 não são atendimentos. Na navegação, cada orientação aberta corresponde a uma tentativa.

- Resposta encontrada: atendimentos com orientação / todos os atendimentos × 100.
- Ajudou: feedback `s` / todos os atendimentos × 100. Sem feedback não conta como sucesso.
- Tempo: `time.time()` no início até o feedback, arredondado para uma casa. Inclui leitura e resposta do usuário. A média de tempo para encontrar usa somente atendimentos com orientação.
- Tentativas: média do campo `tentativas` em todos os atendimentos.
- Facilidade: média das notas 1–5, uma por saída normal da sessão. Sem notas, mostra `null` (não medido).
- Sem solução: perguntas sem orientação ou com feedback `n`, sem repetição. Feedback omitido aparece em um contador separado.

O tempo e as tentativas são medidas operacionais deste protótipo; não representam tempo total de resolução de uma solicitação no governo.

## Teste com usuários — preencher após realizar

Siga `docs/TESTE_COM_USUARIOS.md`. Cada pessoa deve usar uma sessão separada e dar sua própria nota ao sair. Não registrar nomes ou contatos.

| Medida | Resultado real |
|---|---|
| Pessoas externas à equipe | PENDENTE (mínimo 3) |
| Atendimentos | PENDENTE (mínimo 10) |
| Resposta encontrada | PENDENTE |
| Ajudou | PENDENTE |
| Tempo médio | PENDENTE |
| Tentativas por atendimento | PENDENTE |
| Facilidade média | PENDENTE |
| Dúvidas sem solução | PENDENTE |

**Melhoria motivada pelo teste:** PENDENTE. Registrar a dificuldade realmente observada, a mudança e o resultado da nova tentativa. A expressão de demonstração do vídeo é apenas um ensaio, não evidência de melhoria com pessoas reais.

## Validação técnica

```bash
python -m unittest discover -s tests -v
```

Os testes usam diretórios temporários e não preenchem `data/historico.json`. Cobrem pontuação, busca, fronteiras de palavras, acentos, privacidade, entradas inválidas, navegação, persistência, indicadores, CSV, JSON inválido e recarga após inclusão de palavra-chave.

## Fontes oficiais

Consulta de referência realizada em **16/11/2026**. Cada registro contém a fonte correspondente e `verificado_em`. Antes da entrega, a equipe deve abrir as fontes e confirmar o conteúdo; ao revisar, atualizar a data. Documentos adicionais podem variar por situação e canal.

- https://www.gov.br/pt-br/servicos/criar-sua-conta-gov.br
- https://www.gov.br/governodigital/pt-br/acessibilidade-e-usuario/atendimento-gov.br/duvidas-na-conta-gov.br/recuperar-senha-da-conta-gov.br
- https://www.gov.br/pt-br/servicos/obter-a-carteira-de-trabalho
- https://www.gov.br/trabalho-e-emprego/pt-br/servicos/trabalhador/carteira-de-trabalho/perguntas-frequentes-carteira-de-trabalho-digital
- https://www.gov.br/pt-br/servicos/acessar-portal-emprega-brasil-2013-trabalhador
- https://www.gov.br/pt-br/servicos/inscrever-no-cpf
- https://www.gov.br/pt-br/servicos/consultar-cadastro-de-pessoas-fisicas
- https://www.gov.br/pt-br/servicos/atualizar-cadastro-de-pessoas-fisicas
