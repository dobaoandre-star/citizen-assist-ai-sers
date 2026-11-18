"""Uma orientação verificada da base de conhecimento."""

class Orientacao:
    CAMPOS = ('id', 'categoria', 'titulo', 'palavras_chave', 'resposta',
              'documentos', 'onde', 'fonte', 'verificado_em')

    def __init__(self, dados):
        for campo in self.CAMPOS:
            setattr(self, campo, dados[campo])

    def exibir(self):
        print(f'\n>> {self.titulo} [{self.categoria}]')
        print(self.resposta)
        print('Documentos / requisitos (somente no canal oficial):')
        for documento in self.documentos:
            print(f'  - {documento}')
        print(f'Onde: {self.onde}')
        print(f'Fonte: {self.fonte}')
        print(f'Verificado em: {self.verificado_em}')
        print('Aviso: este assistente não é canal oficial.')

