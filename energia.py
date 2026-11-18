"""GS2026.2 SERS: consumo de iluminação, LED e energia solar."""
import json
from dataclasses import dataclass
from math import isfinite
from pathlib import Path

CAMINHO_DADOS = Path(__file__).resolve().parent / "data" / "energia_sers.json"


@dataclass(frozen=True)
class Cenario:
    pontos: int
    horas_dia: float
    dias: int
    w_fluorescente: float
    w_led: float
    fluxo_lm: int
    tarifa: float
    investimento_led: float
    solar_kwp: float
    irradiacao: float
    desempenho: float
    coincidencia: float
    investimento_solar: float


@dataclass(frozen=True)
class Resultado:
    consumo_original: float
    consumo_led: float
    geracao_potencial: float
    solar_usada: float
    rede_com_solar: float
    gasto_original: float
    gasto_led: float
    gasto_solar: float
    retorno_led: float | None
    retorno_solar_incremental: float | None


def carregar_cenario():
    dados = json.loads(CAMINHO_DADOS.read_text(encoding="utf-8-sig"))
    return Cenario(**dados["cenario"])


def calcular(c: Cenario) -> Resultado:
    original = c.pontos * c.w_fluorescente * c.horas_dia * c.dias / 1000
    led = c.pontos * c.w_led * c.horas_dia * c.dias / 1000
    geracao = c.solar_kwp * c.irradiacao * c.desempenho * c.dias
    solar = min(geracao, led * c.coincidencia)
    rede = led - solar
    economia_led = (original - led) * c.tarifa
    economia_solar = solar * c.tarifa
    retorno_led = c.investimento_led / economia_led if economia_led > 0 else None
    retorno_solar = c.investimento_solar / economia_solar if economia_solar > 0 else None
    return Resultado(original, led, geracao, solar, rede, original * c.tarifa,
                     led * c.tarifa, rede * c.tarifa, retorno_led, retorno_solar)


def n(valor):
    return f"{valor:.2f}".replace(".", ",")


def brl(valor):
    return f"R$ {n(valor)}"


def retorno(meses, divisor=1, unidade="meses"):
    if meses is None:
        return "sem retorno calculável nesse cenário"
    return f"{n(meses / divisor)} {unidade}"


def orientar(c: Cenario) -> str:
    r = calcular(c)
    linhas = [
        f"ILUMINAÇÃO | {c.pontos} pontos de cerca de {c.fluxo_lm} lm por lâmpada",
        f"Período de {c.dias} dias, {n(c.horas_dia)} h/dia, tarifa de {brl(c.tarifa)}/kWh.",
        "",
        "Cenário de referência | fluorescente na rede",
        f"  Consumo: {n(r.consumo_original)} kWh | Custo variável: {brl(r.gasto_original)}",
        "Opção A | LED na rede",
        f"  Consumo: {n(r.consumo_led)} kWh | Custo variável: {brl(r.gasto_led)}",
        f"  Investimento: {brl(c.investimento_led)} | Economia frente à referência: "
        f"{brl(r.gasto_original - r.gasto_led)}/período",
        f"  Retorno simples do LED: {retorno(r.retorno_led)}",
        "Opção B | Mesmo LED com apoio solar fotovoltaico",
        f"  Consumo: {n(r.consumo_led)} kWh | Energia comprada: {n(r.rede_com_solar)} kWh",
        f"  Geração potencial: {n(r.geracao_potencial)} kWh | Uso direto no recorte: "
        f"{n(r.solar_usada)} kWh ({n(c.coincidencia * 100)}% de coincidência assumida)",
        f"  Custo variável: {brl(r.gasto_solar)} | Investimento adicional solar: "
        f"{brl(c.investimento_solar)}",
        f"  Economia adicional frente ao LED: {brl(r.gasto_led - r.gasto_solar)}/período",
        f"  Retorno simples apenas desse investimento adicional: "
        f"{retorno(r.retorno_solar_incremental, 12, 'anos')}",
        "",
        "Recomendação: avalie primeiro o LED com fluxo luminoso equivalente.",
        "Considere aproveitar geração solar já disponível em horário de uso. Para um novo",
        "sistema, avalie a carga total do imóvel e obtenha orçamento profissional.",
        "Destine fluorescentes a um ponto de coleta do sistema de logística reversa.",
        "",
        "Estimativa didática. Custos e coincidência não foram medidos. A geração é potencial.",
        "O cálculo exclui créditos por excedentes, custos fixos, manutenção e financiamento.",
        "Não é projeto elétrico nem previsão de redução da fatura.",
        "Fontes e premissas: docs/ENERGIA_SERS.md (INPE, Inmetro, ANEEL e SINIR).",
    ]
    return "\n".join(linhas)


def ler_decimal(rotulo, padrao, minimo, maximo):
    while True:
        valor = input(f"{rotulo} [{n(padrao)}]: ").strip()
        if not valor:
            return padrao
        try:
            numero = float(valor.replace(",", "."))
            if isfinite(numero) and minimo <= numero <= maximo:
                return numero
        except ValueError:
            pass
        print(f"Informe um número entre {n(minimo)} e {n(maximo)}.")


def menu_energia():
    from dataclasses import replace
    from assistente import ler_opcao

    cenario = carregar_cenario()
    print("\nCitizen Assist AI | Energia, GS2026.2 SERS")
    print("1. Ver cenário de exemplo\n2. Ajustar cenário\n0. Voltar")
    opcao = ler_opcao("Escolha energética: ", 0, 2)
    if opcao == 0:
        return
    if opcao == 2:
        horas = ler_decimal("Horas de uso por dia", cenario.horas_dia, 0, 24)
        tarifa = ler_decimal("Custo variável em R$/kWh", cenario.tarifa, 0, 5)
        coincidencia = ler_decimal("Uso de LED que coincide com geração solar (%)",
                                  cenario.coincidencia * 100, 0, 100)
        cenario = replace(cenario, horas_dia=horas, tarifa=tarifa,
                          coincidencia=coincidencia / 100)
    print("\n" + orientar(cenario))

