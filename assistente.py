"""Atendimento, persistência local, indicadores e exportação."""
import csv
import json
import time
from datetime import datetime
from pathlib import Path


def contem_dados_pessoais(texto):
    return '@' in texto or sum(c.isdigit() for c in texto) >= 8


def ler_opcao(mensagem, minimo, maximo):
    while True:
        texto = input(mensagem).strip()
        try:
            numero = int(texto)
            if minimo <= numero <= maximo:
                return numero
        except ValueError:
            pass
        print(f'Opção inválida. Digite um número de {minimo} a {maximo}.')


def ler_sim_nao():
    while True:
        resposta = input('Essa orientação ajudou? (s/n; 0 para voltar): ').strip().lower()
        if resposta in ('s', 'n', '0'):
            return {'s': True, 'n': False, '0': None}[resposta]
        print('Digite s, n ou 0.')


class Assistente:
    CAMPOS = ['data', 'origem', 'pergunta', 'id_orientacao', 'encontrou',
              'ajudou', 'tentativas', 'tempo_segundos']

    def __init__(self, nome, base, diretorio=None):
        self.nome = nome
        self.base = base
        self.diretorio = Path(diretorio) if diretorio else base.caminho.parent
        self.historico = self._ler_lista('historico.json')
        self.avaliacoes = self._ler_lista('avaliacoes.json')

    def _ler_lista(self, nome):
        caminho = self.diretorio / nome
        if not caminho.exists():
            return []
        try:
            dados = json.loads(caminho.read_text(encoding='utf-8-sig'))
            if not isinstance(dados, list):
                raise ValueError('Esperada uma lista.')
            for r in dados:
                if not isinstance(r, dict):
                    raise ValueError('Registro inválido.')
                if nome == 'historico.json':
                    if not all(c in r for c in self.CAMPOS):
                        raise ValueError('Histórico incompleto.')
                    if not isinstance(r['pergunta'], str) or contem_dados_pessoais(r['pergunta']):
                        raise ValueError('Histórico contém pergunta inadequada.')
                    if type(r['encontrou']) is not bool or (r['ajudou'] is not None and type(r['ajudou']) is not bool):
                        raise ValueError('Indicador inválido.')
                    if type(r['tentativas']) is not int or r['tentativas'] < 1:
                        raise ValueError('Tentativas inválidas.')
                    if type(r['tempo_segundos']) not in (int, float) or not 0 <= r['tempo_segundos'] < float('inf'):
                        raise ValueError('Tempo inválido.')
                elif type(r.get('nota')) is not int or not 1 <= r['nota'] <= 5:
                    raise ValueError('Nota inválida.')
            return dados
        except (OSError, ValueError, TypeError) as erro:
            print(f'Aviso: {nome} não pôde ser lido ({erro}).')
            # Preserva o arquivo original antes de iniciar um histórico novo.
            try:
                backup = caminho.with_name(nome + '.' + str(time.time_ns()) + '.bak')
                caminho.rename(backup)
                print('Arquivo anterior preservado em cópia .bak; revise antes de publicar.')
            except OSError:
                print('Não foi possível preservar o arquivo; salvamento desativado.')
                if not hasattr(self, '_bloqueados'):
                    self._bloqueados = set()
                self._bloqueados.add(nome)
            return []

    def _salvar(self, nome, dados):
        if nome in getattr(self, '_bloqueados', set()):
            return False
        try:
            self.diretorio.mkdir(parents=True, exist_ok=True)
            destino = self.diretorio / nome
            temporario = destino.with_suffix('.tmp')
            temporario.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding='utf-8')
            temporario.replace(destino)
            return True
        except OSError as erro:
            print(f'Aviso: não foi possível salvar {nome}: {erro}')
            return False

    def registrar(self, origem, pergunta, orientacao, ajudou, tentativas, inicio):
        if contem_dados_pessoais(pergunta):
            return False
        registro = dict(data=datetime.now().astimezone().isoformat(timespec='seconds'),
                        origem=origem, pergunta=pergunta,
                        id_orientacao=orientacao.id if orientacao else None,
                        encontrou=orientacao is not None, ajudou=ajudou,
                        tentativas=tentativas, tempo_segundos=round(time.time() - inicio, 1))
        self.historico.append(registro)
        return self._salvar('historico.json', self.historico)

    def perguntar(self):
        inicio = time.time()
        tentativas = 0
        while True:
            pergunta = input('\nDigite sua dúvida (0 para voltar): ').strip()
            if pergunta == '0':
                return
            if contem_dados_pessoais(pergunta):
                print('Não digite CPF, telefone ou e-mail. Reescreva. Nada foi registrado.')
                continue
            tentativas += 1
            if not pergunta:
                print('Digite uma pergunta sem dados pessoais.')
                continue
            resultados = [(p, o) for p, o in self.base.buscar(pergunta) if p >= 3]
            if not resultados:
                print('Não encontrei. Tente outras palavras ou consulte as categorias.')
                self.registrar('pergunta', pergunta, None, False, tentativas, inicio)
            else:
                pontos, orientacao = resultados[0]
                confianca = 'ALTA' if pontos >= 6 else 'MÉDIA'
                print(f'Confiança da resposta: {confianca} ({pontos} pontos)')
                print('Confiança representa correspondência textual, não certeza jurídica.')
                orientacao.exibir()
                alternativas = resultados[1:3]
                if alternativas:
                    print('\nAlternativas:')
                    for indice, (p, o) in enumerate(alternativas, 1):
                        print(f'{indice}. {o.titulo} ({p} pontos)')
                    escolha = ler_opcao('Alternativa para exibir (0 para voltar ao resultado principal): ', 0, len(alternativas))
                    if escolha:
                        pontos, orientacao = alternativas[escolha - 1]
                        print(f'Confiança: {"ALTA" if pontos >= 6 else "MÉDIA"} ({pontos} pontos)')
                        orientacao.exibir()
                ajudou = ler_sim_nao()
                self.registrar('pergunta', pergunta, orientacao, ajudou, tentativas, inicio)
            inicio = time.time()
            tentativas = 0

    def navegar(self):
        while True:
            categorias = self.base.categorias()
            if not categorias:
                print('Base indisponível. Corrija o JSON e recarregue no menu.')
                return
            print('\nCategorias:')
            for i, categoria in enumerate(categorias, 1):
                print(f'{i}. {categoria}')
            escolha = ler_opcao('Categoria (0 para voltar): ', 0, len(categorias))
            if escolha == 0:
                return
            orientacoes = self.base.por_categoria(categorias[escolha - 1])
            while True:
                inicio = time.time()
                for i, o in enumerate(orientacoes, 1):
                    print(f'{i}. {o.titulo}')
                opcao = ler_opcao('Orientação (0 para voltar): ', 0, len(orientacoes))
                if opcao == 0:
                    break
                orientacao = orientacoes[opcao - 1]
                orientacao.exibir()
                self.registrar('categoria', orientacao.titulo, orientacao, ler_sim_nao(), 1, inicio)

    def indicadores(self):
        n = len(self.historico)
        media = lambda valores: round(sum(valores) / len(valores), 2) if valores else None
        encontrados = [r for r in self.historico if r['encontrou']]
        return {
            'atendimentos': n,
            'resposta_encontrada_pct': round(100 * len(encontrados) / n, 2) if n else 0,
            'ajudou_pct': round(100 * sum(r['ajudou'] is True for r in self.historico) / n, 2) if n else 0,
            'tempo_medio_para_encontrar_segundos': media([r['tempo_segundos'] for r in encontrados]),
            'tentativas_por_atendimento': media([r['tentativas'] for r in self.historico]),
            'facilidade_media_1_a_5': media([r['nota'] for r in self.avaliacoes]),
            'avaliacoes_recebidas': len(self.avaliacoes),
            'duvidas_sem_solucao': list(dict.fromkeys(r['pergunta'] for r in self.historico
                                          if not r['encontrou'] or r['ajudou'] is False)),
            'feedback_nao_informado': sum(r['ajudou'] is None for r in self.historico)
        }

    def exportar_csv(self):
        try:
            self.diretorio.mkdir(parents=True, exist_ok=True)
            caminho = self.diretorio / 'atendimentos.csv'
            with caminho.open('w', encoding='utf-8-sig', newline='') as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=self.CAMPOS)
                escritor.writeheader()
                for registro in self.historico:
                    linha = {c: registro[c] for c in self.CAMPOS}
                    # Impede interpretação de pergunta como fórmula ao abrir no Excel.
                    if linha['pergunta'].lstrip().startswith(('=', '+', '-', '@')):
                        linha['pergunta'] = "'" + linha['pergunta']
                    escritor.writerow(linha)
            print('CSV exportado: data/atendimentos.csv')
            return True
        except OSError as erro:
            print(f'Não foi possível exportar CSV: {erro}')
            return False

    def avaliar(self):
        nota = ler_opcao('Facilidade de uso de 1 a 5 (0 para voltar): ', 0, 5)
        if nota == 0:
            return False
        self.avaliacoes.append({'data': datetime.now().astimezone().isoformat(timespec='seconds'), 'nota': nota})
        self._salvar('avaliacoes.json', self.avaliacoes)
        return True

