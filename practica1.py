#!/usr/bin/python3

"""
Daniel Suarez Muñoz
Grado en Ing. en Sistemas de Telecomunicaciones
Ejercicio: Práctica 1
"""

import webapp
import csv
import urllib
import urllib.parse

form = """
    <form action="" method="POST">
        Por favor, indique la direccion url a acortar y haga clic en Submit:<br>
        <input type="text" name="url" value=""><br>
        <input type="submit" value="Submit">
    </form>
"""

class acortadora(webapp.webApp):


	largas ={}
	cortas ={}


	with open('archivo.csv') as csvfile:
		read = csv.reader(csvfile)
		for row in read:
			url_corta = row[0]
			url_larga = row[1]
			largas[url_larga] = url_corta
			cortas[url_corta] = url_larga

	def parse(self,request):
		metodo = request.split(' ',2)[0]
		recurso = request.split(' ',3)[1]
		cuerpo = request.split('=')[-1]
		return (metodo,recurso,cuerpo)

	def process(self,parsedRequest):
		metodo,recurso,cuerpo = parsedRequest

#metodo GET o POST:

		if metodo == "GET":
			print(recurso)
			if recurso == "/": 
				codigo = "200 OK"
				respuesta = ("<html><head><h1> PAGINA PARA ACORTAR URLs</h1></head><br>" +form + "<br><html><title>Aplicacion para acortar Urls</title><body>" +
                                  "URLs ya acortadas: <a href="+ str(self.largas) +'"></a>' + str(self.largas)+
                                  "</html></body>")
		
			elif recurso =="favicon.ico":
				codigo = "HTTP/1.1 404 Not Found"
				respuesta = ("<html><body><h1>Not found</h1></body></html>")
			else:
				pagina = "http://localhost:1245"+ str(recurso)
				print(pagina)
				if pagina in self.cortas: 
					codigo = "HTTP/1.1 302 Redirect"  
					respuesta = ("<html><body><h1>Redirigiendo . . . </h1></body><meta http-equiv='Refresh' " +
								 "content= 1;url=" +
								  self.cortas['http://localhost:1245'+str(recurso)] +
								  "></p></body></html>")
				else:
					print(recurso)
					codigo = "HTTP/1.1 404 Not Found"
					respuesta = ("<html><body><h1>Recurso no encontrado.. </h1></body><meta http-equiv='Refresh' " +
								 "content= 1;url=" +
								  self.cortas['http://localhost:1245'+str(recurso)] +
								  "></p></body></html>")


		elif metodo == "POST":
			if cuerpo!= "": 
				url = cuerpo.split("=")[0]
				url = urllib.parse.unquote(url,encoding = 'utf-8',errors = 'replace')
				inicio = url.split("://")[0] 
				if(inicio!= 'http')and (inicio!= 'https'):
					url = 'http://' + url
				try:
					url = self.largas[url]
					codigo = "200 OK"
					respuesta = "<html><body>URL ya modificada, vuelve a intentarlo con otra</body></html>"
					

				except KeyError:
					identificador = len(self.largas) 
					url_corta = 'http://localhost:1245/' + str(identificador) 
					self.largas[url] = url_corta
					self.cortas[url_corta] = url

					with open('archivo.csv','a') as csvfile:
						escribir = csv.writer(csvfile)
						escribir.writerow([url_corta,url])
						codigo = "HTTP/1.1 200 OK"
						respuesta = ("<html><body>URL acortada correctamente,aqui tiene los resultados:</br>" + 'Direccion URL larga -->  <a href="'+ url +'">' + url + ' </a></br>' + 'Direccion URL corta --> <a href="' + url_corta + '">' + url_corta + ' </a></br>"</body></html>')
				
				else:
					return("200 OK","<html><body><h1>La url ya esta acortada, prueba con otra!</h1> </body></html>")

		else:
			codigo = "HTTP/1.1 405 Method Not allowed"
			respuesta = ("<html><body><h1>Metodo no permitido" +
                              "</h1></body></html>")
		return (codigo, respuesta)

if __name__ == "__main__":
	testWebApp = acortadora("localhost", 1245)
		
