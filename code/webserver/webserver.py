from http.server import BaseHTTPRequestHandler, HTTPServer
from .dependencies import *

'''
Esse arquivo contém todos os handlers do servidor web. Aqui ocorrem todas as respostas do servidor para a página.
Ele é dividido em 2 partes: do_GET (responde requisições GET) e do_POST (responde requisições POST).

Foi utilizado http.server para criar o servidor web, que é uma biblioteca nativa do Python. Essa biblioteca foi utilizada com o intuito
de facilitar a criação do servidor, e facilitar também a testagem do código já que ela é simples e não requer muitas configurações.
'''
# Handlers
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # get index.html
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            
            webpage=WEBPAGE_YETI.encode('utf-8')
            self.wfile.write(webpage)
      
       # get total money value
        elif self.path == '/getValue':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            
            value = str(float(get_total()))
            self.wfile.write(value.encode('utf-8'))
            
        # get data for exportation
        elif self.path == '/exportData':
            dataset = get_df()
            if dataset.shape[0] > 0: # if there is data to export
                self.send_response(200)
                self.send_header('Content-type','text/csv')
                self.end_headers()
                self.wfile.write(dataset.to_csv(index=False, sep=';').encode('utf-8'))
            else:
                self.send_response(500)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                self.wfile.write('Erro ao exportar os dados.'.encode('utf-8'))
                
        elif self.path == '/getSixMonths':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = get_data_last_6_months()
            json_data = json.dumps(data)  # convertendo os dados em formato JSON
            self.wfile.write(json_data.encode('utf-8'))
            
        elif self.path == '/getThisMonth':
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            data= get_data_this_month()
            self.wfile.write(str(data).encode('utf-8'))
        
    def do_POST(self):
        if (self.path == '/addBill') or (self.path == '/addIncome'):
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            add_data(request_body)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Post realizado com sucesso')  
            
        if self.path == '/mergeData':
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            merge_data(request_body[0], request_body[1])
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Post realizado com sucesso')
            
        if self.path == '/deleteAllData':
            rm_last_data()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Post realizado com sucesso')