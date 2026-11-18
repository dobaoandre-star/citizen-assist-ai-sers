# Validação técnica

Data: 16/11/2026. Ambiente de execução: Windows, Python 3.12.14.

Comando: `python -m unittest discover -s tests -v`.

Resultado observado: **20 testes executados, todos aprovados**. Dados dos testes são criados em diretórios temporários dentro do projeto e removidos ao terminar; o histórico entregue continua vazio.

Cobertura: base mínima, normalização, score conhecido, limite médio, palavras inteiras, repetição de palavras, ordenação e tuplas, fronteira de 8 dígitos e arroba, bloqueio sem gravação, validação no registro, entradas inválidas, fluxo com feedback, pergunta não encontrada, categoria, persistência e CSV, indicadores conhecidos, histórico vazio, JSON ausente/corrompido, preservação da base em recarga inválida, cópia de segurança de histórico inválido e alteração de palavra-chave ao vivo.

Os testes não certificam disponibilidade futura dos serviços públicos e não substituem os testes com três pessoas exigidos pela atividade. Teste de usuários, gravação, publicação e envio ao portal continuam pendentes.
