import http.server
import socketserver
import cv2
import base64 
import random
import os


from signature_verificator import SignatureVerificator

class SignatureVerificationHTTPRequest(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        f = open("index.html",'rb')
        self.send_response(200)
        self.send_header('Content-type',    'text/html')
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
        return

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):        
        self._set_headers()
        file_size = self.headers['Content-Length']        
        data = self.rfile.read(int(file_size))

        trozos = data.split(b"\r\n\r\n")

        file_name_1 = "file1.png" + str(random.randint(0,2000000000))
        file_name_2 = "file2.png" + str(random.randint(0,2000000000))

        f = open(file_name_1, "wb")
        f.write(trozos[1])
        f.close()

        f = open(file_name_2, "wb")
        f.write(trozos[2])
        f.close()

        SIGNATURE_IMG_A1 = cv2.imread(file_name_1, 0)
        SIGNATURE_IMG_A2 = cv2.imread(file_name_2, 0)
        result = s.verify(SIGNATURE_IMG_A1, SIGNATURE_IMG_A2)
        
        os.remove(file_name_1) 
        os.remove(file_name_2) 

        image1_64_encode = base64.encodebytes(trozos[1])
        image2_64_encode = base64.encodebytes(trozos[2])

        img1 = f'<img src="data:image/png;base64,{image1_64_encode.decode()}" height="128px">\n'
        img2 = f'<img src="data:image/png;base64,{image2_64_encode.decode()}" height="128px"></p>\n'
        table = f'<table border="|"><tbody><tr><td>Signature A</td><td>Signature B</td></tr><tr><td>{img1}</td><td>{img2}</td></tr></tbody></table></p>'
        result_str = f'The similarity between signatures A and B is {int(result*100)}%</p>\n'

        self.wfile.write(b"<html>\n<body>\n<h1>Result</h1></p>\n")
        self.wfile.write(bytes(table,encoding='utf-8'))
        self.wfile.write(bytes(result_str,encoding='utf-8'))
        self.wfile.write(b'<a href="http://193.147.52.134:9000">Compare more signatures</a></p></body>\n</html>\n')

s = SignatureVerificator()
PORT = 9000

http_server = socketserver.TCPServer(("", PORT), SignatureVerificationHTTPRequest)
print("serving at port", PORT)
http_server.serve_forever()

