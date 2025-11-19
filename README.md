# 🚗 FIPE Automator - Consulta Inteligente de Veículos

> Automação em Python para consultar valores de veículos na Tabela FIPE oficial a partir de planilhas Excel, utilizando lógica *fuzzy* para identificar nomes de carros mesmo com erros de digitação.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data-green.svg)
![Status](https://img.shields.io/badge/Status-Concluído-success.svg)

## 🎯 O Problema
Consultar centenas de carros na Tabela FIPE manualmente é lento e propenso a erros. Além disso, os nomes nas planilhas de entrada (ex: "Fiat Palio 2010") raramente batem com a nomenclatura oficial e extensa da FIPE (ex: "Palio 1.0 ECONOMY Fire Flex 8V 4p").

## 🚀 A Solução
Este script lê um arquivo Excel, utiliza algoritmos de similaridade de texto (**Fuzzy Matching**) para encontrar o modelo correspondente mais provável na API da FIPE e retorna o valor atualizado, tratando automaticamente os limites de requisição da API.

### ✨ Funcionalidades Principais
- **📊 Leitura de Excel:** Processa planilhas `.xlsx` contendo Marca, Modelo e Ano.
- **🧠 Inteligência de Texto (Fuzzy):** Identifica o carro correto mesmo se o nome estiver incompleto ou com erros de digitação (Ex: "Toyta Corola" -> "Toyota Corolla").
- **🛡️ Modo Blindado (Anti-Crash):** Sistema de *retry* automático que lida com erros `429 Too Many Requests` da API, aguardando e tentando novamente sem derrubar o script.
- **⏳ Barra de Progresso:** Visualização em tempo real do processamento via terminal.
- **💾 Relatório Final:** Gera uma nova planilha mantendo os dados originais e adicionando: Nome Oficial FIPE, Código FIPE e Valor Avaliado.

---

## 🛠️ Instalação

1. **Clone o repositório** (ou baixe os arquivos):
   ```bash
   git clone [https://github.com/SEU-USUARIO/fipe-automator.git](https://github.com/SEU-USUARIO/fipe-automator.git)
   cd fipe-automator
````

2.  **Crie um ambiente virtual** (Recomendado):

    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as dependências**:

    ```bash
    pip install pandas requests openpyxl thefuzz tqdm
    ```

-----

## 💻 Como Usar

### 1\. Prepare sua Planilha

Crie um arquivo Excel (ex: `entrada.xlsx`) com as seguintes colunas obrigatórias:

  - `Marca` (Ex: Fiat, Volkswagen, Honda)
  - `Modelo` (Ex: Palio Fire, Gol G5, Civic)
  - `Ano_Modelo` (Ex: 2015, 2020)

### 2\. Execute o Script

No terminal, rode:

```bash
python fipe_bot.py
```

### 3\. Siga as instruções

O script pedirá o nome do arquivo. Digite o nome (ex: `entrada.xlsx`) e aguarde o processamento.
Ao final, um arquivo chamado `resultado_final_blindado.xlsx` será gerado.

-----

## 🧪 Exemplo de Resultados

| Entrada (Sua Planilha) | Processamento (Fuzzy Match) | Saída (Valor FIPE) |
| :--- | :--- | :--- |
| `Toyta` - `Corola` | -\> *Toyota Corolla XEi 2.0...* | **R$ 85.400,00** |
| `Volks` - `Gol G5` | -> *VW - VolksWagen Gol 1.0...* | **R$ 22.100,00** |
| `Chev` - `Onix` | -\> *GM - Chevrolet Onix...* | **R$ 55.900,00** |

-----

## ⚠️ Notas Técnicas

  - **API Utilizada:** Este projeto consome a API pública da [Parallelum](https://deividfortuna.github.io/fipe/).
  - **Performance:** O script possui *delays* estratégicos para evitar bloqueios de IP pela API. O tempo médio é de 1 a 2 segundos por carro.

## 🤝 Contribuição

Sugestões e Pull Requests são bem-vindos\!

-----

Desenvolvido com ☕ e Python.

```
```