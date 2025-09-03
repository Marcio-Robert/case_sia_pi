# Documento de Decisões Técnicas

Este documento explica as principais escolhas feitas durante o desenvolvimento do case "Monitoramento de Percepção Pública sobre IA no Piauí".

### 1. Por que a abordagem de regras para análise de sentimento?

Para este projeto, optei por uma abordagem de análise de sentimento baseada em regras (listas de palavras positivas e negativas) por três motivos principais:

* **Transparência e Interpretabilidade:** Diferente de um modelo complexo de Machine Learning (que pode funcionar como uma "caixa-preta"), a abordagem de regras é 100% transparente. É possível auditar facilmente por que uma notícia foi classificada como "Positiva" ou "Negativa", simplesmente verificando as palavras-chave presentes no título. Isso é crucial para um projeto no setor público, onde a clareza nas decisões é fundamental.
* **Simplicidade e Rapidez de Implementação:** A criação de um classificador por regras é direta e não exige um grande volume de dados rotulados para treinamento, o que seria inviável no tempo disponível para o case. A solução é leve, rápida de executar e atende perfeitamente ao objetivo de um monitoramento simplificado.
* **Controle e Customização:** A abordagem permite um controle granular sobre a análise. Se notarmos que o modelo está classificando algo de forma incorreta, podemos simplesmente ajustar ou expandir as listas de palavras-chave, tornando a manutenção do sistema muito mais ágil.

### 2. Como foram tratados possíveis erros ou a falta de notícias no feed RSS?

O tratamento de erros na coleta de dados foi implementado diretamente no script `coleta_noticias.py` através de duas verificações principais:

1.  **Erro de Requisição HTTP:** O script utiliza um bloco `try...except` para encapsular a requisição à URL do Google Notícias. Caso o serviço esteja indisponível ou a URL esteja incorreta, a biblioteca `requests` levantará uma exceção. O programa irá capturar esse erro, imprimir uma mensagem informativa no console (ex: "Erro ao acessar o feed RSS: 404 Client Error") e encerrar a execução de forma controlada, evitando que o script quebre inesperadamente.
2.  **Feed Vazio (Falta de Notícias):** Após uma requisição bem-sucedida, o script verifica se a lista de notícias extraídas do XML está vazia. Se nenhuma notícia for encontrada para os termos de busca, ele imprime uma mensagem clara no console ("Nenhuma notícia encontrada...") e também encerra a execução. Isso garante que o programa não tente criar um dashboard vazio ou gere erros nas etapas seguintes.