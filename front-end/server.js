const http = require('http');
const fs = require('fs');
const url = require('url');
const path = require('path');
const { exec } = require('child_process');

const port = 3000;

const requestHandler = (req, res) => {
  const parsedUrl = url.parse(req.url, true); // Analisa a URL e obtém parâmetros de consulta
  
    // FRONT END HTML GET
    if (req.method === 'GET' && req.url === '/') {
        const filePath = path.join(__dirname, 'index.html');
        fs.readFile(filePath, (err, data) => {
            if (err) {
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('500 Server Error');
                return;
            }
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(data);
            return;
        });
    } else if (req.method === 'POST' && req.url === '/generate') {
      // Check if the request method is POST and the request URL is /generate
      //GERAÇÃO E ASSINATURA DO CERTIFICADO
        let body = '';
        req.on('data', chunk => {
            // Append the chunk of data to the body variable
            body += chunk.toString();
        });
        req.on('end', () => {
            const data = JSON.parse(body);
            const textInput = data.textInput;
            const fileContent = data.fileContent;
            const textInputWithoutSpaces = textInput.replace(/\s/g, '');

            // console.log("Texto com espacos:", textInput);
            // console.log("Texto sem espacos:", textInputWithoutSpaces);

            if (textInput && fileContent) {
                // Define the folder path
                const folderPath = path.join(__dirname, '/files/', textInputWithoutSpaces, '/');

                // Check if folder exists, if not, create it
                fs.access(folderPath, fs.constants.F_OK, (err) => {
                    if (err) {
                        // Folder does not exist, create it
                        fs.mkdir(folderPath, { recursive: true }, (err) => {
                            if (err) {
                                res.writeHead(500, { 'Content-Type': 'text/plain' });
                                res.end('500 Internal Server Error: Could not create directory');
                                return;
                            }

                            // Save the file content to a file
                            saveAndRunScript(folderPath, fileContent, textInputWithoutSpaces, res);
                        });
                    } else {
                        // Folder exists, send a 400 response
                        res.writeHead(400, { 'Content-Type': 'text/plain' });
                        res.end('400 Bad Request: Index meessage already exists');
                        return;
                    }
                });
            } else {
                // Missing parameters, send a 400 response
                res.writeHead(400, { 'Content-Type': 'text/plain' });
                res.end('400 Bad Request: Missing parameters');
            }
        });
    } else if (req.method === 'POST' && req.url === '/revoke'){
      // Check if the request method is POST and the request URL is /revoke
      //REVOCAÇÃO DO CERTIFICADO
      let body = '';

        req.on('data', chunk => {
            body += chunk.toString();
        });

        req.on('end', () => {
            const data = JSON.parse(body);
            console.log("Dados recebidos para revogar:", data);
            res.writeHead(400, { 'Content-Type': 'text/plain' });
            res.end('Logica da revogação não implementada!');
        });
    } else if (req.method === 'GET' && parsedUrl.pathname === '/view') {
      // Check if the request method is GET and the request URL is /view
      //BUSCA DO CERTIFICADO
      const certId = parsedUrl.query.certId; // Obtém o parâmetro certId

        if (certId) {
            // Aqui você pode buscar o certificado com o ID fornecido e retornar os dados
            console.log("ID do certificado:", certId);

            // Exemplo de resposta, substitua isso com sua lógica para buscar o certificado
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end('Logica da busca não implementada!');
            // res.end(JSON.stringify({ certId: certId, status: 'Certificado encontrado!' }));
        } else {
            res.writeHead(400, { 'Content-Type': 'text/plain' });
            res.end('400 Bad Request: Certificado ID não fornecido!');
        }
    } else {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not Found');
    }

};

const server = http.createServer(requestHandler);

server.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});

const saveAndRunScript = (folderPath, fileContent, textInputWithoutSpaces, res) => {
  const filePath = path.join(folderPath, 'private.key');
  fs.writeFile(filePath, fileContent, (err) => {
      if (err) {
          res.writeHead(500, { 'Content-Type': 'text/plain' });
          res.end('500 Internal Server Error: Could not write file');
          return; 
      }

      exec(`./generate.sh "${textInputWithoutSpaces}" "private.key"`, (err, stdout, stderr) => {
          if (err) {
              res.writeHead(500, { 'Content-Type': 'text/plain' });
              res.end('500 Internal Server Error: Script execution failed');
              console.error(err);
              return; 
          }
          res.writeHead(200, { 'Content-Type': 'text/plain' });
          res.end(`Script executed successfully: ${stdout}`);
      });
  });
};