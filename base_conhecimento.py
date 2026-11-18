"""Carregamento validado e busca determinística, sem API externa."""
import json
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from orientacao import Orientacao


def normalizar(texto):
    texto = unicodedata.normalize('NFD', texto.lower())
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = ''.join(c if c.isalnum() else ' ' for c in texto)
    return ' ' + ' '.join(texto.split()) + ' '


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.orientacoes = []

    def carregar(self):
        try:
            dados = json.loads(self.caminho.read_text(encoding='utf-8-sig'))
            if not isinstance(dados, list) or len(dados) < 10:
                raise ValueError('A base precisa de pelo menos 10 orientações.')
            ids = set()
            novas = []
            for item in dados:
                if not isinstance(item, dict) or not all(c in item for c in Orientacao.CAMPOS):
                    raise ValueError('Registro incompleto.')
                if type(item['id']) is not int or item['id'] in ids:
                    raise ValueError('ID inválido ou repetido.')
                ids.add(item['id'])
                for campo in ('categoria', 'titulo', 'resposta', 'onde', 'fonte', 'verificado_em'):
                    if not isinstance(item[campo], str) or not item[campo].strip():
                        raise ValueError('Campo textual inválido: ' + campo)
                for campo in ('palavras_chave', 'documentos'):
                    if not isinstance(item[campo], list) or not item[campo] or not all(isinstance(x, str) and x.strip() for x in item[campo]):
                        raise ValueError('Lista inválida: ' + campo)
                if len(set(normalizar(x) for x in item['palavras_chave'])) < 3:
                    raise ValueError('São necessárias 3 palavras-chave distintas.')
                url = urlparse(item['fonte'])
                if url.scheme != 'https' or not (url.hostname or '').endswith('.gov.br'):
                    raise ValueError('Use uma fonte oficial HTTPS gov.br.')
                date.fromisoformat(item['verificado_em'])
                novas.append(Orientacao(item))
            if len({o.categoria for o in novas}) < 3:
                raise ValueError('São necessárias 3 categorias.')
            self.orientacoes = novas
            return True
        except (OSError, ValueError, TypeError) as erro:
            print(f'Não foi possível carregar a base: {erro}')
            print('Corrija data/base_conhecimento.json e escolha recarregar.')
            return False

    def categorias(self):
        return sorted({o.categoria for o in self.orientacoes})

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        pergunta = normalizar(pergunta)
        titulo = normalizar(orientacao.titulo)
        chaves = {normalizar(p) for p in orientacao.palavras_chave}
        pontos = sum(3 for chave in chaves if chave in pergunta)
        pontos += sum(1 for palavra in set(pergunta.split())
                      if len(palavra) >= 4 and f' {palavra} ' in titulo)
        return pontos

    def buscar(self, pergunta):
        resultados = [(self.pontuar(pergunta, o), o) for o in self.orientacoes]
        return sorted(resultados, key=lambda par: (-par[0], par[1].id))

