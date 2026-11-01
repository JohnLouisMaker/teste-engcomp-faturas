import re
from decimal import Decimal
from pathlib import Path

diretorio_atual = Path(__file__).resolve().parent
diretorio_dados = diretorio_atual / "dados"

PADRAO_CPF = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
PADRAO_CNPJ = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"
PADRAO_CAMPO = r":\s*(.+)"
PADRAO_KWH = r"(\d[\d.]*)\s*KWH"
PADRAO_MOEDA = r"\d[\d.]*,\d{2}"

MESES = {
    "JANEIRO": "01",
    "FEVEREIRO": "02",
    "MARÇO": "03",
    "MARCO": "03",
    "ABRIL": "04",
    "MAIO": "05",
    "JUNHO": "06",
    "JULHO": "07",
    "AGOSTO": "08",
    "SETEMBRO": "09",
    "OUTUBRO": "10",
    "NOVEMBRO": "11",
    "DEZEMBRO": "12",
}


def extrair_fatura():
    fatura_formatada = []
    arquivos_faturas = sorted(diretorio_dados.glob("*.txt"))

    for arquivo in arquivos_faturas:
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
            "itens": [],
            "valor_total": None,
        }

        arquivo_lido = arquivo.read_text(encoding="utf-8")
        arquivo_formatado = arquivo_lido.splitlines()

        dentro_de_faturamento = False

        if arquivo_formatado:
            fatura["distribuidora"] = arquivo_formatado[0].strip().upper()
            fatura["distribuidora"] = fatura["distribuidora"].replace("*", "").strip()
            fatura["distribuidora"] = fatura["distribuidora"].replace(" - DISTRIBUIDORA DE ENERGIA", "").strip()

        for linha in arquivo_formatado:
            linha_formatada = linha.strip().upper()

            if linha_formatada.startswith(("NOME", "CLIENTE", "TITULAR")):
                resultado_regex = re.search(PADRAO_CAMPO, linha_formatada)
                if resultado_regex:
                    fatura["cliente"] = resultado_regex.group(1).strip()

            if linha_formatada.startswith(("CPF/CNPJ", "CNPJ/CPF", "DOCUMENTO")):
                resultado_regex = re.search(rf"{PADRAO_CNPJ}|{PADRAO_CPF}", linha_formatada)
                if resultado_regex:
                    fatura["documento"] = resultado_regex.group()

            if linha_formatada.startswith(("UNIDADE CONSUMIDORA", "INSTALACAO", "NO DA INSTALACAO")):
                resultado_regex = re.search(PADRAO_CAMPO, linha_formatada)
                if resultado_regex:
                    fatura["unidade_consumidora"] = resultado_regex.group(1).strip()

            if linha_formatada.startswith(
                (
                    "MES DE REFERENCIA",
                    "MÊS DE REFERENCIA",
                    "MES DE REFERÊNCIA",
                    "MÊS DE REFERÊNCIA",
                    "REFERENCIA",
                    "REFERÊNCIA",
                    "MES/ANO",
                    "MÊS/ANO",
                )
            ):
                resultado_regex = re.search(PADRAO_CAMPO, linha_formatada)
                if resultado_regex:
                    mes, ano = resultado_regex.group(1).strip().split("/")
                    mes_formatado = MESES.get(mes, mes)
                    fatura["referencia"] = f"{ano}-{mes_formatado}"

            if linha_formatada.startswith(("DATA DE VENCIMENTO", "DATA VENCIMENTO", "VENCIMENTO")):
                resultado_regex = re.search(PADRAO_CAMPO, linha_formatada)
                if resultado_regex:
                    dia, mes, ano = resultado_regex.group(1).strip().split("/")
                    mes_formatado = MESES.get(mes, mes)
                    fatura["vencimento"] = f"{ano}-{mes_formatado}-{dia}"

            if linha_formatada.startswith(("LEITURA ANTERIOR", "ANTERIOR", "DATA ANTERIOR")):
                resultado_regex = re.search(PADRAO_KWH, linha_formatada)
                if resultado_regex:
                    fatura["leitura_anterior"] = int(resultado_regex.group(1).replace(".", ""))

            if linha_formatada.startswith(("LEITURA ATUAL", "ATUAL", "DATA ATUAL")):
                resultado_regex = re.search(PADRAO_KWH, linha_formatada)
                if resultado_regex:
                    fatura["leitura_atual"] = int(resultado_regex.group(1).replace(".", ""))

            if linha_formatada.startswith(("CONSUMO FATURADO", "CONSUMO.:", "CONSUMO DO MES")):
                resultado_regex = re.search(PADRAO_KWH, linha_formatada)
                if resultado_regex:
                    fatura["consumo_kwh"] = int(resultado_regex.group(1).replace(".", ""))

            if linha_formatada.startswith(
                (
                    "FATURAMENTO",
                    "COMPOSICAO DA FATURA",
                    "DESCRICAO DOS ITENS FATURADOS",
                )
            ):
                dentro_de_faturamento = True
                continue

            if dentro_de_faturamento:
                if linha_formatada.startswith(("TOTAL A PAGAR", "TOTAL DA FATURA", "VALOR TOTAL DA FATURA")):
                    resultado_regex = re.search(PADRAO_MOEDA, linha_formatada)
                    if resultado_regex:
                        valor_formatado = resultado_regex.group()
                        fatura["valor_total"] = Decimal(valor_formatado.replace(".", "").replace(",", "."))

                    dentro_de_faturamento = False
                    continue

                valores_encontrados = re.findall(PADRAO_MOEDA, linha_formatada)
                if valores_encontrados:
                    valor_formatado = valores_encontrados[-1]
                    valor_decimal = Decimal(valor_formatado.replace(".", "").replace(",", "."))
                    fatura["itens"].append(valor_decimal)

            if linha_formatada.startswith(("BANDEIRA TARIFARIA", "BANDEIRA:")):
                resultado_regex = re.search(PADRAO_CAMPO, linha_formatada)
                if resultado_regex:
                    fatura["bandeira"] = resultado_regex.group(1).strip()

        fatura_formatada.append(fatura)

    return fatura_formatada


print(extrair_fatura())
