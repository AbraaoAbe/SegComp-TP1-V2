# Trabalho Prático Segurança em Computação

Este trabalho foi desenvolvido utilizando Python para o back-end da Cartesi e JavaScript para o front-end. Além disso, foram empregados scripts em Shell para facilitar o tratamento e envio dos dados, tornando o processo mais simples e automatizado.


## Requisitos

1. **Cartesi CLI**: É necessário instalar o Cartesi para o funcionamento do projeto. Siga o tutorial disponível em [Cartesi Rollups Installation](https://docs.cartesi.io/cartesi-rollups/1.3/development/installation/) para a instalação.

2. **OpenSSL**: Você precisará do OpenSSL para gerar e assinar certificados. Caso não tenha utilize o seguinte comando:

    ```bash
    sudo apt install openssl
    ```
3. **jq**: O shell script irá precisar para concatenar os arquivos de entrada em formato json. Caso não tenha utilize o seguinte comando:
    
    ```bash
    sudo apt install jq
    ```
4. **Node.js**: O cartesi CLI ja exige o node na instalação, mas como utilizamos no front-end, fica aqui um reforço

## Preparando o ambiente

1. **Geração da Chave Privada**: Coloque sua chave privada `private.key` dentro do diretório `/PK`.

   Para gerar a chave privada, utilize o seguinte comando OpenSSL:

    ```bash
    openssl genpkey -algorithm RSA -out ./PK/private.key
    ```

## Execução e Teste

1. **Construção e Execução do Cartesi**:
   
   Navegue até o diretório `/backend` e execute os seguintes comandos para construir e iniciar o Cartesi:

    ```bash
    cd /backend
    cartesi build
    cartesi run
    ```
    - OBS.: Essa parte pode demorar um pouco, ou até dar alguns erros dependendo da sua CPU, tenha paciência e repita os comandos. Tente fechar e abrir sua IDE e/ou terminais novamente.
2. **Execução do Front-end**:

    Agora em outro terminal, navegue até o diretório `/front-end` e rode o arquivo `server.js`:

    ```bash
    cd /front-end
    node server.js
    ```
3. **Testando**:
   
   Acesse o endereço do front-end: `http://localhost:3000`
   Você verá as páginas de Geração de certificado, Revogação de certificado e a página Ver Certificado para ver o status atual do certificado (Ativo ou Inativo). 

4. **Geração de certificado**: `advance`

    - Nessa página você irá escolher um identificador único para o certificado e escreve-lo na caixa de texto. (exemplo: `meuid`)
    - Logo depois irá fazer upload da sua chave privada `private.key` anteriormente gerada.
    - Ao clicar em Enviar, será gerado um certificado e uma assinatura a partir da sua chave e do identificador escrito.
    - A aplicação, neste momento, irá fazer o envio do certificado para a blockchain (pode demorar alguns segundos)

5. **Ver Certificado**: `inspect`
    - Agora que acabou de gerar e enviar seu certificado e sua assinatura, verifique o estado atual do seu certificado.
    - Digite o identificador unico do seu certificado na caixa de texto e clique em Buscar

6. **Revogar Certificado**: `advance`
    - Agora que ja sabe que seu certificado está na blockchain, caso queira, você pode revoga-lo.
    - Na página de revogar o certificado você precisará fornecer o identificador do certificado e a sua assinatura.
    - A assinatura gerada está localizada no subdiretório `/front-end/files/<meuidentificador>/assinatura_base64.txt`.
    - Faça o upload do arquivo da assinatura e digite o identificador único do certificado
    - Clique em Revogar e aguarde alguns segundos
    - Você pode conferir o estado atual do seu certificado retornando à pagina Ver Certificado

### Verificação de assinatura

    Você pode acompanhar durante a revogação, a verificação da assinatura através do terminal da Cartesi, caso gere 2 certificados e tente enviar a assinatura de um com o identificador do outro, verá a seguinte mensagem:

    ![Erro de verificação de assinatura](/img/LogErroAssinatura.png)

## Link do vídeo

https://drive.google.com/file/d/10pOpFLrWHcnANOSRPVpoHsDK8cdvK2BX/view?usp=sharing