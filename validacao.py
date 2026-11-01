from decimal import Decimal


def validar_faturas(faturas):
    inconsistencias = []
    validadas = []

    campos_obrigatorios = [
        "arquivo",
        "distribuidora",
        "cliente",
        "documento",
        "unidade_consumidora",
        "referencia",
        "vencimento",
        "leitura_anterior",
        "leitura_atual",
        "consumo_kwh",
        "valor_total",
    ]

    for fatura in faturas:
        fatura_valida = True

        for campo in campos_obrigatorios:
            valor_campo = fatura.get(campo)

            if valor_campo is None or valor_campo == "":
                inconsistencias.append(
                    {"arquivo": fatura.get("arquivo"), "motivo": f"Campo obrigatório ausente: {campo}"}
                )
                fatura_valida = False

        if fatura.get("valor_total") is not None and fatura.get("itens") is not None:
            soma_itens = sum(fatura["itens"])
            diferenca = fatura["valor_total"] - soma_itens

            if abs(diferenca) > Decimal("0.01"):
                inconsistencias.append(
                    {
                        "arquivo": fatura.get("arquivo"),
                        "motivo": (
                            f"Divergência de R$ {abs(diferenca):.2f} entre a soma dos itens e o total declarado."
                            f"\nSoma dos itens: R$ {soma_itens:.2f}"
                            f"\nTotal declarado: R$ {fatura['valor_total']:.2f}"
                        ),
                    }
                )
                fatura_valida = False

        if (
            fatura.get("leitura_atual") is not None
            and fatura.get("leitura_anterior") is not None
            and fatura.get("consumo_kwh") is not None
        ):
            calculo_consumo = fatura["leitura_atual"] - fatura["leitura_anterior"]

            if calculo_consumo != fatura["consumo_kwh"]:
                inconsistencias.append(
                    {
                        "arquivo": fatura.get("arquivo"),
                        "motivo": (
                            f"Consumo informado ({fatura['consumo_kwh']} kWh) é diferente do cálculo realizado."
                            f"\nleitura atual - anterior ({calculo_consumo} kWh)"
                        ),
                    }
                )
                fatura_valida = False

        if fatura_valida:
            validadas.append(fatura)

    return validadas, inconsistencias
