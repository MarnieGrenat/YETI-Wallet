'''
Esse arquivo é responsável por hospedar o servidor localmente.
Somente esse arquivo deve ser executado. Outros arquivos deste
projeto são dependências deste arquivo/projeto.
'''
from http.server import BaseHTTPRequestHandler, HTTPServer
from webserver import webserver as ws

def run_server():
    HOST = 'localhost'
    PORT = 8000

    # Criando o servidor HTTP
    server = HTTPServer((HOST, PORT), ws.RequestHandler)
    print(f'''
                  ===================================
                        Running webserver at:
                        http://localhost:{PORT}
                  ===================================
                  ''')
    server.serve_forever()

def main():
      run_server()

if __name__ == '__main__':
    main()