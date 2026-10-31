import re
from decimal import Decimal
from pathlib import Path


def extrair_fatura():
    atual = Path(__file__).resolve().parent
    pastas_dados = atual / "dados"
    arquivos = pastas_dados.glob("*.txt")

    CPF = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
    CNPJ = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"

    MESES = {
        "01": "JANEIRO",
        "02": "FEVEREIRO",
        "03": "MARCO",
        "04": "ABRIL",
        "05": "MAIO",
        "06": "JUNHO",
        "07": "JULHO",
        "08": "AGOSTO",
        "09": "SETEMBRO",
        "10": "OUTUBRO",
        "11": "NOVEMBRO",
        "12": "DEZEMBRO",
    }

    faturas = []

    for arquivo in arquivos:
        arquivo_lido = arquivo.read_text(encoding="utf-8")
        arquivo_formatado = arquivo_lido.splitlines()

        fatura = {
            "arquivo": arquivo.name,
            "distribuidora": None,
            "cliente": None,
            "documento": None,
            "unidade_consumidora": None,
            "referencia": None,
            "vencimento": None,
            "leitura_anterior": None,
            "leitura_atual": None,
            "consumo_kwh": None,
            "bandeira": None,
            "valor_total": None,
        }

        if arquivo_formatado:
            fatura["distribuidora"] = arquivo_formatado[0].strip().upper()

        for linha in arquivo_formatado:
            linha_formatada = linha.strip().upper()

            if linha_formatada.startswith(("NOME", "CLIENTE", "TITULAR")):
                res = re.search(r":\s*(.+)", linha_formatada)
                if res:
                    fatura["cliente"] = res.group(1).strip()

            if linha_formatada.startswith(("CPF/CNPJ", "CNPJ/CPF", "DOCUMENTO")):
                res = re.search(rf"{CNPJ}|{CPF}", linha_formatada)
                if res:
                    fatura["documento"] = res.group()

            if linha_formatada.startswith(("UNIDADE CONSUMIDORA", "INSTALACAO", "NO DA INSTALACAO")):
                res = re.search(r":\s*(.+)", linha_formatada)
                if res:
                    fatura["unidade_consumidora"] = res.group(1).strip()

            if linha_formatada.startswith(("MES DE REFERENCIA", "REFERENCIA", "MES/ANO")):
                res = re.search(r":\s*(.+)", linha_formatada)
                if res:
                    mes, ano = res.group(1).strip().split("/")
                    mes_formatado = MESES.get(mes, mes)
                    fatura["referencia"] = f"{ano}-{mes_formatado}"

            if linha_formatada.startswith(("DATA DE VENCIMENTO", "DATA VENCIMENTO", "VENCIMENTO")):
                res = re.search(r":\s*(.+)", linha_formatada)
                if res:
                    dia, mes, ano = res.group(1).strip().split("/")
                    fatura["vencimento"] = f"{ano}-{mes}-{dia}"

            if linha_formatada.startswith(("LEITURA ANTERIOR", "ANTERIOR", "DATA ANTERIOR")):
                res = re.search(r"(\d[\d.]*)\s*KWH", linha_formatada)
                if res:
                    fatura["leitura_anterior"] = int(res.group(1).replace(".", ""))

            if linha_formatada.startswith(("LEITURA ATUAL", "ATUAL", "DATA ATUAL")):
                res = re.search(r"(\d[\d.]*)\s*KWH", linha_formatada)
                if res:
                    fatura["leitura_atual"] = int(res.group(1).replace(".", ""))

            if linha_formatada.startswith(("CONSUMO FATURADO", "CONSUMO.:", "CONSUMO DO MES")):
                res = re.search(r"(\d[\d.]*)\s*KWH", linha_formatada)
                if res:
                    fatura["consumo_kwh"] = int(res.group(1).replace(".", ""))

            if linha_formatada.startswith(("BANDEIRA TARIFARIA", "BANDEIRA:")):
                res = re.search(r":\s*(.+)", linha_formatada)
                if res:
                    fatura["bandeira"] = res.group(1).strip()

            if linha_formatada.startswith(("TOTAL A PAGAR", "TOTAL DA FATURA", "VALOR TOTAL DA FATURA")):
                res = re.search(r"\d[\d.]*,\d{2}", linha_formatada)
                if res:
                    valor_texto = res.group()
                    fatura["valor_total"] = Decimal(valor_texto.replace(".", "").replace(",", "."))

        faturas.append(fatura)

    return faturas

print(extrair_fatura())
