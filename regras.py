from decimal import Decimal

from extracao import extrair_fatura
from validacao import validar_faturas


def aplicacao_de_regra(faturas):

    concessonarias = ["CIA LUZ DO VALE", "COMPANHIA ELETRICA SUDESTE"]

    for fatura in faturas:
        consumo_kwh = fatura["consumo_kwh"]

        if fatura["distribuidora"] in concessonarias:
            perda_kwh = consumo_kwh * Decimal("0.01")
            consumo_ajustado_kwh = consumo_kwh + perda_kwh

            fatura["perda_kwh"] = perda_kwh
            fatura["consumo_ajustado_kwh"] = consumo_ajustado_kwh

        else:
            fatura["perda_kwh"] = Decimal("0.00")
            fatura["consumo_ajustado_kwh"] = Decimal(str(consumo_kwh))

    return faturas


res1 = extrair_fatura()
res2, _ = validar_faturas(res1)
res3 = aplicacao_de_regra(res2)

print(f"""
Distribuidora: {res3[0]["distribuidora"]}
Valor total: R$ {res3[0]["valor_total"]:.2f}
Perda: {res3[0]["perda_kwh"]} kWh
Consumo ajustado: R$ {res3[0]["consumo_ajustado_kwh"]} kWh
""")

print(f"""
Distribuidora: {res3[1]["distribuidora"]}
Valor total: R$ {res3[1]["valor_total"]:.2f}
Perda: {res3[1]["perda_kwh"]} kWh
Consumo ajustado: R$ {res3[1]["consumo_ajustado_kwh"]} kWh
""")

print(f"""
Distribuidora: {res3[2]["distribuidora"]}
Valor total: R$ {res3[2]["valor_total"]:.2f}
Perda: {res3[2]["perda_kwh"]} kWh
Consumo ajustado: R$ {res3[2]["consumo_ajustado_kwh"]} kWh
""")
