# Roteiro técnico — alvo de 7 minutos e 30 segundos

Este roteiro é apoio de estudo. Fale com a própria voz e explique o código que realmente compreendeu. Não use narração de IA. Se houver dupla ou trio, todos devem falar e explicar uma parte técnica. Câmera opcional; código e terminal precisam ficar legíveis.

**Grave só após fazer os testes reais e preencher o README.** Os campos entre colchetes devem ser substituídos por resultados verdadeiros. Faça um ensaio com cronômetro; a duração depende da fala e das demonstrações. Tudo depois de 8 minutos não será avaliado.

## 0:00–0:25 — equipe, público e problema

Tela: README.

“Olá, sou Yihang Xu, RM 571720, da turma 1CCPY. Este é o Citizen Assist AI — Primeiro Emprego. O público são jovens que precisam acessar serviços como a Carteira de Trabalho Digital e a conta gov.br. A ideia é reunir orientações simples, com fonte oficial, em um programa de terminal.”

## 0:25–1:10 — JSON, dicionários e tuplas

Tela: registro de ID 4 em `data/base_conhecimento.json`; depois `buscar()`.

“A base contém onze orientações e três categorias. Cada orientação é um dicionário, com ID, categoria, título, palavras-chave, resposta, documentos, local, fonte e data de verificação. A lista de palavras-chave ajuda a relacionar formas diferentes de perguntar. O programa só responde com conteúdo desta base. Na busca, uso tuplas com dois elementos: a pontuação e o objeto de orientação. Isso permite ordenar os resultados sem separar a resposta do seu score.”

Mostre os campos e abra uma fonte oficial, sem entrar em uma conta pessoal. Explique que a equipe conferiu as fontes antes da entrega apenas se tiver feito essa conferência.

## 1:10–2:00 — classes e composição

Tela: construtores nas três classes e inicialização em `main.py`.

“Dividi as responsabilidades em três classes. Orientacao guarda os dados e exibe a resposta. BaseConhecimento carrega o JSON, lista categorias e executa a busca. Assistente controla a conversa e os registros. O self representa o objeto atual: self.historico, por exemplo, é o histórico deste assistente. A composição aparece porque o assistente possui uma base, e a base possui uma lista de orientações. Não precisei usar herança para representar essa relação.”

Mostre `base.carregar()`, a criação do assistente, `orientacao.exibir()` e um método de cada classe.

## 2:00–2:45 — normalização e conta dos pontos

Tela: `normalizar()` e `pontuar()`.

“Primeiro removo acentos, transformo pontuação em espaços e converto para minúsculas. A busca compara palavras completas. Cada palavra-chave encontrada vale três pontos. Cada palavra distinta da pergunta, com quatro ou mais caracteres, presente no título vale um. Na pergunta ‘Como obter carteira de trabalho digital?’, a frase-chave vale três pontos; obter, carteira, trabalho e digital somam quatro. O resultado é sete pontos, confiança alta. De três a cinco é média; abaixo de três não há resposta. Confiança aqui significa correspondência textual, não garantia sobre o serviço.”

Mostre também a ordenação das tuplas e o desempate por ID.

## 2:45–4:10 — execução e validações

Tela: terminal. Execute `python main.py` (ou `python3 main.py`).

1. No menu, digite `abc`: deve mostrar erro e permitir tentar novamente.
2. Escolha `1`, pergunte `Como obter carteira de trabalho digital?`: mostre os 7 pontos, materiais, fonte, data e aviso. Responda `s`.
3. Digite `astronomia`: não encontrado.
4. Digite `123.456.789-00`, número fictício apenas para testar a regra: bloqueado.
5. Digite `teste@exemplo`: bloqueado.
6. Digite `0`, entre em `2`, escolha uma categoria e uma orientação. Responda `s` e use os retornos por `0` até o menu.

“Entradas inválidas não encerram o programa. Se a pergunta contém arroba ou pelo menos oito dígitos, ela é recusada antes da busca e não vai para o histórico. Os documentos mostrados são para o canal oficial: o assistente não solicita que a pessoa digite esses dados.”

## 4:10–5:20 — alteração ao vivo obrigatória

Prepare apenas o editor aberto. A modificação precisa acontecer durante a gravação.

1. Na opção `1`, pergunte `livrinho azul`: deve dar não encontrado.
2. Digite `0` para retornar ao menu.
3. Abra `data/base_conhecimento.json`. No registro **ID 4**, acrescente `"livrinho azul"` à lista `palavras_chave`, com a vírgula correta. Salve.
4. No menu, escolha `5` para recarregar.
5. Escolha `1` e repita `livrinho azul`: agora encontra ID 4 com **3 pontos, confiança MÉDIA**.
6. Responda e volte ao menu.

“Acabei de alterar o vocabulário no JSON sem modificar a regra de busca. A recarga valida o arquivo e cria os objetos novamente. Essa expressão é um exemplo controlado para mostrar o mecanismo. Ela não é uma denominação oficial da carteira digital.”

Após o ensaio, remova a expressão antes da gravação definitiva, para que a primeira tentativa volte a falhar. No produto final, prefira manter somente sinônimos úteis e realmente adequados ao público. Uma dúvida genérica pode ter outros sentidos; explique essa limitação.

## 5:20–6:25 — histórico, CSV e testes reais

Tela: opção `3`, depois `4`, os arquivos JSON/CSV e a seção preenchida do README.

“Cada atendimento registra data, origem, pergunta, orientação, se encontrou, se ajudou, tentativas e tempo. A diferença entre time.time no início e no final mede o atendimento, incluindo a leitura e o feedback. Uso csv.DictWriter para exportar campos com cabeçalho. As avaliações ficam em outro JSON e são usadas para a média de facilidade.”

“O teste foi feito com [quantidade real] pessoas de fora da equipe, em [quantidade real] atendimentos. O resultado foi [percentual real] de respostas encontradas e [percentual real] de ajuda. A dificuldade observada foi [fato real]. A melhoria que fiz foi [alteração real], e depois [resultado real].”

Mostre que as perguntas bloqueadas não aparecem no histórico. Diferencie os números coletados antes da gravação dos atendimentos adicionados na demonstração. Não atribua os testes automatizados às pessoas.

## 6:25–7:10 — decisão técnica e limitações

Tela: tratamento de erros em `carregar()`, depois README.

“Escolhi regras locais porque consigo explicar exatamente por que uma resposta foi encontrada. O projeto funciona sem API externa e não gera informações fora da base. A validação do JSON evita travamento quando o arquivo está ausente ou incorreto; numa recarga com erro, a base anterior continua disponível. Uma limitação é que palavras-chave não entendem todo o contexto e podem não reconhecer uma forma diferente de perguntar. As fontes também precisam de revisão periódica. A proteção de dados segue uma regra simples e não identifica nomes escritos por extenso.”

## 7:10–7:30 — encerramento

Tela: repositório público e README com links reais.

“O código está dividido nos quatro arquivos principais. O README explica execução, pontuação, fontes, indicadores e limitações. Ao sair, a pessoa dá uma nota de facilidade e o programa exporta o CSV. Obrigado.”

Saia do programa e mostre a nota 1–5 e a exportação. Não deixe credenciais ou informações de contas pessoais visíveis.

## Conferência antes de publicar

- Duração entre 5 e 8 minutos.
- Código legível e som compreensível.
- Todos os integrantes falam; sem voz sintética.
- JSON, dicionários, tuplas, classes, self, composição e cálculo de score explicados.
- Encontrado, não encontrado, inválido, privacidade, categoria e alteração ao vivo demonstrados.
- Histórico, CSV e indicadores reais mostrados.
- Uma decisão e uma limitação explicadas.
- YouTube “Não listado”; link acessível sem autorização especial.
