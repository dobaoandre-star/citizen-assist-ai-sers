"""Execute: python main.py (Python 3.10 ou superior)."""
import json
from pathlib import Path
from base_conhecimento import BaseConhecimento
from assistente import Assistente, ler_opcao
from energia import menu_energia


def main():
    base = BaseConhecimento(Path(__file__).resolve().parent / 'data' / 'base_conhecimento.json')
    base.carregar()
    assistente = Assistente('Citizen Assist AI — Primeiro Emprego', base)
    print('\n' + assistente.nome)
    print('Este assistente não é canal oficial. Não informe nomes, CPF, telefone ou e-mail.')
    print('Dúvidas e avaliações são guardadas localmente, sem identificação de pessoas.')
    try:
        while True:
            print('\n1. Perguntar\n2. Categorias\n3. Indicadores\n4. Exportar CSV\n5. Recarregar base\n6. Energia e iluminação\n0. Sair')
            opcao = ler_opcao('Escolha: ', 0, 6)
            if opcao == 1:
                assistente.perguntar()
            elif opcao == 2:
                assistente.navegar()
            elif opcao == 3:
                print(json.dumps(assistente.indicadores(), ensure_ascii=False, indent=2))
            elif opcao == 4:
                assistente.exportar_csv()
            elif opcao == 5:
                if base.carregar():
                    print('Base atualizada.')
            elif opcao == 6:
                menu_energia()
            elif assistente.avaliar():
                assistente.exportar_csv()
                print('Obrigado!')
                break
    except (EOFError, KeyboardInterrupt):
        print('\nSessão interrompida. Atendimentos concluídos já foram salvos.')
        assistente.exportar_csv()


if __name__ == '__main__':
    main()
