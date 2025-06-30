import socket
import whois
import requests
import pandas as pd


# Ler a lista de domínios de um arquivo TXT
with open('dominios.txt', 'r') as arquivo:
    dominios = [linha.strip() for linha in arquivo.readlines()]

# Criar uma lista para armazenar os resultados
resultados = []

# Função para verificar o status de domínio
def verificar_status(dominio):
    try:
        resultado = socket.gethostbyname(dominio)
        return "Ativo", resultado
    except socket.gaierror:
        return "Inativo", None

# Função para consultar informações WHOIS
def consultar_whois(dominio):
    try:
        info = whois.whois(dominio)
        return info
    except Exception as e:
        return str(e)

# Função para consultar ASN
def consultar_asn(ip):
    try:
        url = f"https://ipinfo.io/{ip}/json?token=52f7413fa5f040" 
        response = requests.get(url)
        data = response.json()
        if 'asn' in data:
            return data['asn']
        return "Não disponível"
    except Exception as e:
        return str(e)

# Função para obter o código de status HTTP
def obter_codigo_status(dominio):
    try:
        response = requests.head(f"http://{dominio}")
        return response.status_code
    except Exception as e:
        return str(e)


# Loop através dos domínios
for dominio in dominios:
    status, ip = verificar_status(dominio)
    info_whois = consultar_whois(dominio)
    codigo_status = obter_codigo_status(dominio)

    asn = ""
    if ip:
        asn = consultar_asn(ip)

    resultado = {
        "Domínio": dominio,
       "Status": f"{status} ({codigo_status})",  # Adicione o código de status ao status
        "IP": ip if ip else "Não disponível",
        " WHOIS": info_whois,
        "ASN": asn
    }
    resultados.append(resultado)

# Converter a lista de resultados em um DataFrame
df = pd.DataFrame(resultados)

# Salvar o DataFrame em um arquivo Excel (XLSX)
df.to_excel('informacoes_dominios.xlsx', index=False)

print("Informações dos domínios foram salvas em 'informacoes_dominios.xlsx'.")
