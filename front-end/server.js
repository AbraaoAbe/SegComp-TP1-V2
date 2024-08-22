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
    } else if (req.method === 'POST' && req.url === '/revoke') {
      let body = '';
  
      req.on('data', chunk => {
          body += chunk.toString();
      });
  
      req.on('end', () => {
          const data = JSON.parse(body);
          console.log("Dados recebidos para revogar:", data);
          
          // Acessa os valores corretamente a partir do JSON recebido
          const certId = data.certId;
          const fileContent = data.fileContent;
          const certIdWithoutSpaces = certId.replace(/\s/g, '');
  
          if (certIdWithoutSpaces && fileContent) {
              // Comando para revogação do certificado
              exec(`./revoke.sh "${certIdWithoutSpaces}" "${fileContent}"`, (err, stdout, stderr) => {
                  if (err) {
                      res.writeHead(500, { 'Content-Type': 'text/plain' });
                      res.end('500 Internal Server Error: Script execution failed');
                      console.error('Erro na execução do script:', err);
                      return;
                  }
                  res.writeHead(200, { 'Content-Type': 'text/plain' });
                  res.end(`Script executado com sucesso: ${stdout}`);
              });
          } else {
              // Parâmetros ausentes, enviar uma resposta 400
              res.writeHead(400, { 'Content-Type': 'text/plain' });
              res.end('400 Bad Request: Missing parameters');
          }
      });
    }else {
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

