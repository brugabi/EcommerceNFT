
# 🖼️ E-commerce de NFTs

## Descrição
Aplicação web simples que simula a compra de NFTs. Antes da finalização do pedido, o sistema calcula o frete e a previsão de entrega com base no bairro de Salvador escolhido pelo usuário.

## Tecnologias Utilizadas
- **Backend**: Python, Flask  
- **Frontend**: HTML, CSS puro  

## Funcionalidades
- Visualização de imagens NFT disponíveis para compra.
- Cálculo automático de frete e previsão de entrega com base no destino.

## Como Executar
1. Clone o repositório.
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```bash
   python app.py
   ```

## Observações
- A aplicação é local e não faz chamadas externas.
- O sistema de frete simula um cálculo baseado em um mapeamento simples em grafos de alguns bairros de Salvador.
