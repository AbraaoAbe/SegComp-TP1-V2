const fs = require('fs');
const message_path = './INPUT/message.txt';

const fetchNotices = async () => {
  try {
    // Le o conteúdo do arquivo message.txt
    fs.readFile(message_path, 'utf8', async (err, message) => {
      if (err) {
        console.error('Erro ao ler o arquivo message.txt:', err);
        return;
      }

      // Cria a URL baseada no conteúdo do arquivo
      const url = `http://localhost:8080/inspect/${encodeURIComponent(message)}`;
      console.log(`Fetching from URL: ${url}`);

      // Faz o fetch para a URL criada
      const response = await fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });

      // Verifica se a resposta foi bem-sucedida
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();

      // Verifica se a resposta contém os dados esperados
      if (result.reports && result.reports.length > 0) {
        // Processa o primeiro relatório (ou itere sobre todos se necessário)
        const report = result.reports[0];
        const payloadHex = report.payload;

        // Remove o prefixo '0x' se presente
        const hexStringWithoutPrefix = payloadHex.startsWith('0x') ? payloadHex.slice(2) : payloadHex;

        // Converte hexadecimal para bytes
        const bytes = Buffer.from(hexStringWithoutPrefix, 'hex');
        const decodedString = bytes.toString('utf8');

        // Exibe a mensagem decodificada
        console.log('Certificado Encontrado:', decodedString);
      } else {
        console.log('Nenhum certificado encontrado.');
      }
    });
  } catch (error) {
    console.error('Erro ao buscar dados:', error);
  }
};

fetchNotices();
