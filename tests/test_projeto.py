"""Testes técnicos isolados: não representam testes com pessoas reais."""
import contextlib
import csv
import io
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch
from base_conhecimento import BaseConhecimento, normalizar
from assistente import Assistente, contem_dados_pessoais, ler_opcao

ROOT = Path(__file__).resolve().parents[1]


class ProjetoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='teste_', dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        self.base = BaseConhecimento(ROOT / 'data/base_conhecimento.json')
        self.assertTrue(self.base.carregar())
        self.assistente = Assistente('Teste', self.base, self.dir)
        self.output = io.StringIO()
        self.capture = contextlib.redirect_stdout(self.output)
        self.capture.__enter__()
        self.addCleanup(self.capture.__exit__, None, None, None)

    def test_base_completa(self):
        self.assertGreaterEqual(len(self.base.orientacoes), 10)
        self.assertEqual(len(self.base.categorias()), 3)

    def test_normalizacao(self):
        self.assertEqual(normalizar('  SITUAÇÃO—CPF?! '), ' situacao cpf ')

    def test_busca_pontuacao_conhecida(self):
        pontos, orientacao = self.base.buscar('Como obter carteira de trabalho digital?')[0]
        self.assertEqual((pontos, orientacao.id), (7, 4))

    def test_limite_medio(self):
        self.assertEqual(self.base.buscar('ctps digital')[0][0], 4)

    def test_palavra_inteira(self):
        self.assertEqual(self.base.buscar('sinergia')[0][0], 0)

    def test_repeticao_nao_infla_score(self):
        self.assertEqual(self.base.buscar('ctps digital')[0][0], self.base.buscar('ctps digital ctps digital')[0][0])

    def test_ordem_e_tuplas(self):
        resultados = self.base.buscar('carteira trabalho')
        self.assertIsInstance(resultados[0], tuple)
        self.assertEqual([p for p, _ in resultados], sorted([p for p, _ in resultados], reverse=True))

    def test_limites_privacidade(self):
        self.assertFalse(contem_dados_pessoais('1234567'))
        self.assertTrue(contem_dados_pessoais('12.34 56-78'))
        self.assertTrue(contem_dados_pessoais('teste@exemplo'))

    def test_bloqueio_nao_registra(self):
        with patch('builtins.input', side_effect=['123.456.789-00', 'teste@exemplo', '0']):
            self.assistente.perguntar()
        self.assertEqual(self.assistente.historico, [])
        self.assertFalse((self.dir / 'historico.json').exists())

    def test_registro_tambem_bloqueia(self):
        self.assertFalse(self.assistente.registrar('pergunta', '12345678', None, False, 1, time.time()))
        self.assertEqual(self.assistente.historico, [])

    def test_entrada_invalida(self):
        with patch('builtins.input', side_effect=['abc', '', '99', '-1', '2']):
            self.assertEqual(ler_opcao('Opção: ', 0, 5), 2)

    def test_fluxo_encontrado_feedback_invalido(self):
        with patch('builtins.input', side_effect=['', 'ctps digital', 'talvez', 's', '0']):
            self.assistente.perguntar()
        r = self.assistente.historico[0]
        self.assertTrue(r['encontrou'])
        self.assertTrue(r['ajudou'])
        self.assertEqual(r['tentativas'], 2)

    def test_nao_encontrado(self):
        with patch('builtins.input', side_effect=['astronomia', '0']):
            self.assistente.perguntar()
        self.assertFalse(self.assistente.historico[0]['encontrou'])

    def test_categoria(self):
        with patch('builtins.input', side_effect=['1', '1', 's', '0', '0']):
            self.assistente.navegar()
        self.assertEqual(self.assistente.historico[0]['origem'], 'categoria')

    def test_indicadores_persistencia_csv(self):
        agora = time.time()
        self.assistente.registrar('pergunta', 'ctps digital', self.base.orientacoes[3], True, 1, agora - 10)
        self.assistente.registrar('pergunta', '=astronomia', None, False, 2, agora - 20)
        with patch('builtins.input', side_effect=['5']):
            self.assistente.avaliar()
        a = Assistente('Reaberto', self.base, self.dir)
        indicadores = a.indicadores()
        self.assertEqual(indicadores['resposta_encontrada_pct'], 50)
        self.assertEqual(indicadores['ajudou_pct'], 50)
        self.assertEqual(indicadores['facilidade_media_1_a_5'], 5)
        self.assertEqual(indicadores['tentativas_por_atendimento'], 1.5)
        self.assertAlmostEqual(indicadores['tempo_medio_para_encontrar_segundos'], 10, delta=0.2)
        self.assertTrue(a.exportar_csv())
        with (self.dir / 'atendimentos.csv').open(encoding='utf-8-sig', newline='') as f:
            linhas = list(csv.DictReader(f))
        self.assertEqual(len(linhas), 2)
        self.assertEqual(linhas[1]['pergunta'], "'=astronomia")

    def test_zero_atendimentos(self):
        self.assertEqual(self.assistente.indicadores()['atendimentos'], 0)
        self.assertIsNone(self.assistente.indicadores()['facilidade_media_1_a_5'])

    def test_json_ausente_corrompido_esquema(self):
        b = BaseConhecimento(self.dir / 'base.json')
        self.assertFalse(b.carregar())
        for texto in ('{', '{}', '[1]', 'null'):
            b.caminho.write_text(texto, encoding='utf-8')
            self.assertFalse(b.carregar())

    def test_preserva_base_valida_se_reload_falha(self):
        self.base.caminho = self.dir / 'ausente.json'
        self.assertFalse(self.base.carregar())
        self.assertEqual(self.base.buscar('ctps digital')[0][1].id, 4)

    def test_historico_corrompido_preservado(self):
        (self.dir / 'historico.json').write_text('{', encoding='utf-8')
        a = Assistente('Teste', self.base, self.dir)
        self.assertEqual(a.historico, [])
        self.assertEqual(len(list(self.dir.glob('*.bak'))), 1)

    def test_alteracao_ao_vivo(self):
        pergunta = 'livrinho azul'
        self.assertLess(self.base.buscar(pergunta)[0][0], 3)
        dados = json.loads(self.base.caminho.read_text(encoding='utf-8'))
        dados[3]['palavras_chave'].append(pergunta)
        self.base.caminho = self.dir / 'base.json'
        self.base.caminho.write_text(json.dumps(dados), encoding='utf-8')
        self.assertTrue(self.base.carregar())
        self.assertEqual(self.base.buscar(pergunta)[0][1].id, 4)
        self.assertEqual(self.base.buscar(pergunta)[0][0], 3)


if __name__ == '__main__':
    unittest.main()
