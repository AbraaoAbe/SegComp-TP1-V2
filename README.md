# Trabalho Prático de Faculdade

## Requisitos

1. **Cartesi**: É necessário instalar o Cartesi para o funcionamento do projeto. Siga o tutorial disponível em [Cartesi Rollups Installation](https://docs.cartesi.io/cartesi-rollups/1.3/development/installation/) para a instalação.

2. **OpenSSL**: Você precisará do OpenSSL para gerar e assinar certificados. Caso não tenha utilize o seguinte comando:

    ```bash
    sudo apt install openssl
    ```
3. **jq**: O shell script irá precisar para concatenar os arquivos de entrada em formato json. Caso não tenha utilize o seguinte comando:
    
    ```bash
    sudo apt install jq
    ```

## Preparando o ambiente

1. **Geração da Chave Privada**: Coloque sua chave privada `private.key` dentro do diretório `/PK`.

   Para gerar a chave privada, utilize o seguinte comando OpenSSL:

    ```bash
    openssl genpkey -algorithm RSA -out /PK/private.key
    ```

2. **Mensagem para Assinatura**: Coloque uma mensagem sem espaços no arquivo localizado em `/INPUT/message.txt`. Exemplo de mensagem:

    ```
    uma_mensagem_qualquer
    ```

## Scripts

1. **Geração e Assinatura do Certificado**:
   
   Execute o script `certificate_gen.sh` para gerar e assinar o certificado. Este script utiliza a chave privada para criar e assinar o certificado.

    ```bash
    ./certificate_gen.sh
    ```

2. **Geração da Mensagem Assinada**:
   
   Execute o script `signature_gen.sh` para gerar a assinatura necessária para verificação dentro da dApp.

    ```bash
    ./signature_gen.sh
    ```

## Execução e Teste

1. **Construção e Execução**:
   
   Navegue até o diretório `/backend` e execute os seguintes comandos para construir e iniciar o Cartesi:

    ```bash
    cd /backend
    cartesi build
    cartesi run
    ```

2. **Teste**:
   
   Abra um novo terminal e execute o script `send_generic.sh` para testar o sistema.

    ```bash
    ./send_generic.sh
    ```
3. **Observe a movimentação da dApp pelo LOG do cartesi**

    Se tudo der certo você verá uma saida no terminal parecida com essa aqui:

    {imagem do terminal}

## F
