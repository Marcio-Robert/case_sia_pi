# Bibliotecas
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import re

print("Iniciando a coleta de notícias...")

# Definindo a URL do feed RSS do Google Notícias com a query de busca "Inteligência Artificial Piauí"
url = "https://news.google.com/rss/search?q=Intelig%C3%AAncia+Artificial+Piau%C3%AD&hl=pt-BR&gl=BR&ceid=BR:pt-419"

# Fazendo a requisição HTTP para pegar o conteúdo do feed
try:
    response = requests.get(url)
    response.raise_for_status()  # status 404
    print("Feed RSS acessado com sucesso!")
except requests.exceptions.RequestException as e:
    print(f"Erro ao acessar o feed RSS: {e}")
    exit()

# Processando (parse) o XML recebido
root = ET.fromstring(response.content)

# Criar uma lista para armazenar notícias
noticias_lista = []

# Iterando no XML e extraindo as informações (de cada notícia)
for item in root.findall('.//item'):
    titulo = item.find('title').text
    link = item.find('link').text

    # Limpando descrição
    descricao_html = item.find('description').text
    descricao_limpa = re.sub(
        '<.*?>', '', descricao_html) if descricao_html else "Descrição não disponível"

    noticia = {
        'titulo': titulo,
        'link': link,
        'descricao': descricao_limpa
    }
    noticias_lista.append(noticia)

# Verificando se foram coletadas notícias
if not noticias_lista:
    print("Nenhuma notícia encontrada para os termos de busca. O script será encerrado.")
    exit()

print(f"{len(noticias_lista)} notícias encontradas.")

# Usando a biblioteca Pandas para criar DataFrame
df = pd.DataFrame(noticias_lista)

# Salvando o DataFrame em um arquivo CSV
# O index=False remove a coluna de índice do CSV
df.to_csv('noticias.csv', index=False, encoding='utf-8-sig')

print("Dados coletados e salvos com sucesso no arquivo 'noticias.csv'!")
