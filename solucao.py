import json
from pathlib import Path

from extracao import extrair_fatura
from regras import aplicacao_de_regra
from validacao import validar_faturas

DIRETORIO_ATUAL = Path(__file__).resolve().parent


def processar_faturas():
    faturas = extrair_fatura()
    _, inconsistencias = validar_faturas(faturas)
    faturas = aplicacao_de_regra(faturas)

    for fatura in faturas:
        fatura["inconsistencias"] = []

        for problema in inconsistencias:
            if problema["arquivo"] == fatura["arquivo"]:
                fatura["inconsistencias"].append(problema["motivo"])

        if fatura["inconsistencias"]:
            fatura["status"] = "INCONSISTENTE"
        else:
            fatura["status"] = "VALIDADA"

    for fatura in faturas:
        print(f"\n- {fatura['arquivo']} -")
        print(f"Distribuidora: {fatura['distribuidora']}")
        print(f"Cliente: {fatura['cliente']}")
        print(f"Consumo: {fatura['consumo_kwh']} kWh")
        print(f"Status: {fatura['status']}")

        if "perda_kwh" in fatura:
            if fatura["perda_kwh"] is None:
                print("Perda: não calculada (consumo ausente)")
                print("Consumo ajustado: não calculado")
            else:
                print(f"Perda: {fatura['perda_kwh']} kWh")
                print(f"Consumo ajustado: {fatura['consumo_ajustado_kwh']} kWh")

        print(f"Total: R$ {fatura['valor_total']}")

    print("\n-- INCONSISTÊNCIAS ENCONTRADAS")

    if inconsistencias:
        for problema in inconsistencias:
            print(f"\nFatura: {problema['arquivo']}")
            print(f"Problema: {problema['motivo']}")
    else:
        print("Nenhuma inconsistência encontrada.")

    arquivo_saida = DIRETORIO_ATUAL / "resultado.json"

    with arquivo_saida.open("w", encoding="utf-8") as arquivo:
        json.dump(faturas, arquivo, ensure_ascii=False, indent=4, default=str)

    print(f"\nArquivo gerado: {arquivo_saida}")


if __name__ == "__main__":
    processar_faturas()
