from decimal import Decimal

from extracao import extrair_fatura


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
            resultado_campo = fatura.get(campo)

            if resultado_campo is None or resultado_campo == "":
                inconsistencias.append(f"CAMPO FALTANDO: {campo} no {fatura['arquivo']}")
                fatura_valida = False

        if fatura.get("valor_total") is not None and fatura.get("itens") is not None:
            soma_itens = sum(fatura["itens"])

            if abs(soma_itens - fatura["valor_total"]) > Decimal("0.01"):
                inconsistencias.append(f"INCONSISTÊNCIA NO CÁLCULO: {fatura['arquivo']}")
                fatura_valida = False

        if (
            fatura.get("leitura_atual") is not None
            and fatura.get("leitura_anterior") is not None
            and fatura.get("consumo_kwh") is not None
        ):
            calculo_consumo = fatura["leitura_atual"] - fatura["leitura_anterior"]

            if calculo_consumo != fatura["consumo_kwh"]:
                inconsistencias.append(f"INCONSISTÊNCIA NA LEITURA: {fatura['arquivo']}")
                fatura_valida = False

        if fatura_valida:
            validadas.append(fatura)

    return validadas, inconsistencias


resultado = extrair_fatura()
resultado_formatado = validar_faturas(resultado)
print(resultado_formatado)
