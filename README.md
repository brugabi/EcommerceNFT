
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
4. Opcionalmente, instale as ferramentas de verificação:
   ```bash
   pip install -r requirements-dev.txt
   ```
5. Execute a aplicação:
   ```bash
   python app.py
   ```

## Segurança
- Para proteger a tela administrativa, defina `ADMIN_TOKEN` antes de iniciar o Flask e acesse `/adm?admin_token=SEU_TOKEN`.
- O modo debug fica desligado por padrão. Use `FLASK_DEBUG=1` apenas em desenvolvimento local.
- O Dependabot verifica dependências Python semanalmente e abre pull requests para atualizações de segurança.
- O workflow `Security` roda `pip check`, compilação dos arquivos Python e `pip-audit -r requirements.txt`.
- Antes de enviar alterações, rode:
  ```bash
  python -m pip check
  python -m compileall app.py modules teste.py
  pip-audit -r requirements.txt
  ```

## Observações
- A aplicação é local e não faz chamadas externas.
- O sistema de frete simula um cálculo baseado em um mapeamento simples em grafos de alguns bairros de Salvador.
