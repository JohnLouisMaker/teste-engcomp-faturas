from decimal import ROUND_HALF_UP, Decimal


def arredondar(valor):
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def aplicacao_de_regra(faturas):
    concessionarias = [
        "CIA LUZ DO VALE",
        "COMPANHIA ELETRICA SUDESTE",
    ]

    for fatura in faturas:
        consumo_kwh = fatura.get("consumo_kwh")

        if consumo_kwh is None:
            fatura["perda_kwh"] = None
            fatura["consumo_ajustado_kwh"] = None
            continue

        consumo_kwh = Decimal(consumo_kwh)

        if fatura.get("distribuidora") in concessionarias:
            perda_kwh = arredondar(consumo_kwh * Decimal("0.01"))
            consumo_ajustado_kwh = arredondar(consumo_kwh + perda_kwh)

            fatura["perda_kwh"] = perda_kwh
            fatura["consumo_ajustado_kwh"] = consumo_ajustado_kwh

        else:
            fatura["perda_kwh"] = Decimal("0.00")
            fatura["consumo_ajustado_kwh"] = arredondar(consumo_kwh)

    return faturas
