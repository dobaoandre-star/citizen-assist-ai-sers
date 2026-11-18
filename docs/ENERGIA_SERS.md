# GS2026.2 | Soluções em Energias Renováveis e Sustentáveis
**Yihang Xu · RM 571720 · 1CCPY · Trabalho individual**

## Público e necessidade

Jovens no primeiro emprego e suas famílias podem precisar reduzir gastos em casa sem diminuir a iluminação usada para estudar ou trabalhar. A comparação usa uma residência hipotética em São Paulo, quatro pontos de luz com cerca de 800 lm por lâmpada, cinco horas de uso diário e um período padrão de 30 dias. A equivalência é de fluxo nominal. Distribuição da luz, luminária e iluminância do ambiente devem ser verificadas separadamente.

## Dados e premissas

| Variável | Valor | Origem |
|---|---:|---|
| Pontos, uso e período | 4, 5 h/dia, 30 dias | Cenário ilustrativo |
| Fluorescente e LED | 15 W e 9 W, cerca de 800 lm cada | Modelos nocionais. Conferir etiqueta do produto |
| Tarifa variável | R$ 1,00/kWh | Hipótese didática. Usar custo marginal da conta |
| Troca das 4 lâmpadas | R$ 40,00 | Hipótese didática, R$ 10 por lâmpada |
| Potência solar e fator de desempenho | 0,15 kWp e 0,75 | Hipóteses de cálculo, sem dimensionamento de instalação |
| Irradiação global horizontal média | 4,434 kWh/m²/dia | INPE, Atlas 2ª ed. (2017), registro 5622, lon −46,6490, lat −23,6005 |
| Coincidência da iluminação com geração | 40% da carga LED | Hipótese, sem bateria. Alterável no menu |
| Investimento adicional solar | R$ 3.000,00 | Hipótese ilustrativa, sem cotação. Não representa um kit específico |

O centro de São Paulo foi representado pelas coordenadas aproximadas −23,5505 e −46,6333. Selecionou-se a célula mais próxima do arquivo GLOBAL_HORIZONTAL, ponderando a distância longitudinal pelo cosseno da latitude. O campo ANNUAL é 4434 Wh/m²/dia. Após dividir por 1000, usa-se esse valor como aproximação de 4,434 horas de sol pleno por dia. É uma média de longo prazo, sem garantia para o telhado ou o mês do usuário. Dados e premissas usados pelo programa estão em [energia_sers.json](../data/energia_sers.json).

## Método

- Consumo em kWh = pontos × potência em W × horas/dia × dias ÷ 1000.
- Geração fotovoltaica potencial = potência em kWp × horas de sol pleno × fator de desempenho × dias. A aproximação usa irradiação horizontal e um fator sintético de perdas.
- Uso direto de energia solar = menor valor entre a geração potencial e a carga LED que coincide com a geração. O teto mensal é uma simplificação de balanço, sem simulação horária.
- Energia comprada = consumo LED menos uso solar. Custo variável = energia comprada × tarifa. Energia excedente fica fora do recorte.
- Retorno simples = investimento dividido pela economia estimada no período. Para o solar, usa-se seu investimento adicional e a economia adicional sobre LED. Para expressar anos, usam-se 12 períodos de 30 dias.

## Resultados para a mesma iluminação e o mesmo período

| Indicador | Fluorescente na rede (referência) | LED na rede (A) | LED com apoio solar (B) |
|---|---:|---:|---:|
| Potência total | 60 W | 36 W | 36 W |
| Consumo da iluminação | 9,00 kWh | 5,40 kWh | 5,40 kWh |
| Geração solar potencial | — | — | 14,96 kWh |
| Solar usada pela iluminação | 0,00 kWh | 0,00 kWh | 2,16 kWh |
| Energia comprada | 9,00 kWh | 5,40 kWh | 3,24 kWh |
| Custo variável | R$ 9,00 | R$ 5,40 | R$ 3,24 |
| Investimento inicial suposto | — | R$ 40,00 | R$ 3.040,00 |
| Economia frente à referência | — | R$ 3,60 | R$ 5,76 |

A reduz o consumo em 40% e tem retorno simples de **11,11 períodos**. B mantém o consumo em 5,40 kWh e reduz a energia comprada em outros 2,16 kWh no cenário de exemplo. A economia adicional de B, frente a A, é de R$ 2,16 por período. O investimento adicional teria retorno teórico de **115,74 anos** nesse recorte. Esse valor serve para mostrar que a iluminação isolada não justifica a instalação nova sob as hipóteses usadas. Com coincidência de 0%, a economia adicional é zero. Com coincidência de 100% e geração suficiente, o teto é R$ 5,40 por período.

## Recomendação, ambiente e limites

Priorize LED de fluxo luminoso equivalente. A menor demanda reduz a energia comprada em qualquer horário de uso. Encaminhe as fluorescentes retiradas para pontos de logística reversa. Se já existe geração fotovoltaica, verifique a coincidência com o uso, sem pressupor que a energia produzida de dia seja usada à noite. Uma nova instalação exige avaliação da carga total, telhado, sombreamento, orientação, equipamentos, orçamento e regras locais por profissional habilitado.

O modelo trabalha apenas com energia e custo marginal. Não estima a fatura completa, créditos por excedente, manutenção, perdas de capacidade, financiamento, custo de disponibilidade ou retorno de um sistema para toda a residência. O LED reduz a demanda física. A geração solar altera a origem de parte da energia e traz impactos próprios de fabricação e descarte. Não foi calculado CO₂ evitado nem feito estudo de ciclo de vida.

## Integração e evidências

Abra `python main.py`. No menu principal, escolha **6. Energia e iluminação**, depois **1. Ver cenário de exemplo** ou **2. Ajustar cenário**. O ajuste pede horas, tarifa e coincidência solar. A opção de energia não grava entradas nem pede informações pessoais.

A verificação automatizada cobre o cenário padrão, horário sem coincidência, geração abaixo da demanda e tarifa zero. O roteiro independente de teste com usuários está em [TESTES_USUARIOS_SERS.md](TESTES_USUARIOS_SERS.md). Os relatos de usuários estão pendentes.

## Referências

- INPE, [Atlas Brasileiro de Energia Solar, 2ª edição](https://labren.ccst.inpe.br/atlas_2017.html). Origem da irradiação.
- Inmetro, [Programa Brasileiro de Etiquetagem, lâmpadas](https://www.gov.br/inmetro/pt-br/assuntos/regulamentacao/avaliacao-da-conformidade/programa-brasileiro-de-etiquetagem/tabelas-de-eficiencia-energetica/lampadas/). Verificação de eficiência e características do produto.
- ANEEL, [Micro e Minigeração Distribuída](https://www.gov.br/aneel/pt-br/assuntos/geracao/geracao-distribuida). Contexto tarifário e de viabilidade.
- ANEEL, [Tarifas de aplicação das distribuidoras](https://dadosabertos.aneel.gov.br/pt_BR/dataset/tarifas-distribuidoras-energia-eletrica). Consulta de tarifas reais por distribuidora.
- SINIR, [Logística reversa de lâmpadas fluorescentes](https://www.sinir.gov.br/perfis/logistica-reversa/logistica-reversa/lampadas-fluorescentes-de-vapor-de-sodio-e-mercurio-e-de-luz-mista/). Destinação das fluorescentes.

