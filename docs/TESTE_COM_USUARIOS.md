# Teste com pessoas reais

**Situação: ainda não realizado.** Este é um protocolo, não um relatório de resultados.

## Antes do teste

1. Convide pelo menos três pessoas que não fazem parte da equipe. Não registre nomes, idade, CPF, telefone ou e-mail.
2. Explique: “Este é um protótipo escolar, não é canal oficial. Faça perguntas genéricas sobre serviços públicos, sem dados pessoais. As perguntas e avaliações ficam salvas localmente.”
3. Use uma cópia separada do projeto para ensaios. Na pasta destinada ao teste real, comece com `historico.json` e `avaliacoes.json` contendo `[]` e CSV somente com cabeçalho.
4. Cada pessoa utiliza uma execução própria do programa e dá a sua nota ao sair. A contagem de três pessoas é confirmada presencialmente pela equipe, sem identificá-las no programa.

## Distribuição sugerida — mínimo 10 atendimentos

| Pessoa anônima | Quantidade | Tarefas sugeridas |
|---|---:|---|
| A | 4 | Obter carteira digital; criar conta; recuperar senha; uma pergunta com palavras próprias |
| B | 3 | Procurar vagas; consultar CPF; abrir uma orientação por categoria |
| C | 3 | Consultar contratos; descobrir se carteira tem custo; pergunta livre |

Peça que formulem as próprias dúvidas. Não dite todas as palavras-chave: o objetivo é observar dificuldades reais. Perguntas bloqueadas, telas abertas e entradas vazias não contam como atendimentos concluídos. Confira o total na opção 3.

## Durante e depois

- Deixe a pessoa ler a orientação e responder `s` ou `n` de forma independente.
- Não prometa benefício ou atendimento real: o programa apenas orienta.
- Ao sair, peça a nota pessoal de facilidade de 1 a 5.
- Após os três participantes, consulte indicadores e exporte CSV.
- Registre no README a quantidade de pessoas, o total de atendimentos, os indicadores e as dúvidas não resolvidas.
- Escolha uma dificuldade efetivamente observada e faça uma melhoria. Exemplo possível: adicionar um sinônimo que uma pessoa usou. Não invente que esse caso aconteceu.
- Teste novamente a pergunta depois da alteração e descreva antes/depois. Se não houver falha de busca, use uma dificuldade de compreensão ou navegação relatada e registre a mudança correspondente.
- Revise as perguntas manualmente antes de publicar; retire dados pessoais que a regra simples não detecte. Mantenha JSON e CSV consistentes, exportando novamente após qualquer revisão.

## Registro para copiar ao README

```text
Data do teste: [preencher]
Pessoas externas: [quantidade, sem nomes]
Atendimentos antes da melhoria: [quantidade]
Resposta encontrada: [%]
Ajudou: [%]
Tempo médio para encontrar: [segundos]
Tentativas por atendimento: [média]
Facilidade: [média de 1 a 5]
Dúvidas sem solução: [perguntas genéricas]
Dificuldade observada: [fato]
Melhoria implementada: [mudança concreta]
Resultado do novo teste: [fato, sem inventar]
```

Os 20 testes automatizados são uma verificação técnica separada e não substituem esta etapa.
