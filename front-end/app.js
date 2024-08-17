const fs = require('fs');
const message_path = '../message.txt';

const fetchNotices = async () => {
  try {
    // Leia o conteúdo do arquivo message.txt
    fs.readFile(message_path, 'utf8', async (err, message) => {
      if (err) {
        console.error('Erro ao ler o arquivo message.txt:', err);
        return;
      }

      // Crie a URL baseada no conteúdo do arquivo
      const url = `http://localhost:8080/graphql/${encodeURIComponent(message)}`;
      console.log(`Fetching from URL: ${url}`);

      // Faça o fetch para a URL criada
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: "{ notices { edges { node { payload } } } }" }),
      });

      // Verifica se a resposta foi bem-sucedida
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();

      // Verifica se a resposta contém a estrutura esperada
      if (result.data && result.data.notices && result.data.notices.edges) {
        for (const edge of result.data.notices.edges) {
          const payload = edge.node.payload;
          // Converte hexadecimal para bytes e depois para string
          try {
            const hexStringWithoutPrefix = payload.startsWith('0x') ? payload.slice(2) : payload;
            const bytes = Buffer.from(hexStringWithoutPrefix, 'hex');
            const decodedString = bytes.toString('utf8');
            console.log(decodedString);
          } catch (error) {
            console.error('Erro ao decodificar a string hexadecimal:', error);
          }
          
          // Exibe o payload
        }
      } else {
        console.error('Unexpected response structure:', result);
      }
    });
  } catch (error) {
    console.error('Error fetching notices:', error);
  }
};

// Executa a função
fetchNotices();
