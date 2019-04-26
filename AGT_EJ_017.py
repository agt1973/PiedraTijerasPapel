#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AGT
# Copyright 2019 Ariel H Garcia Traba <ariel.garcia.traba@gmail.com>


print ("https://www.youtube.com/watch?v=eZpSGS7vF5Y")
print ("""
			pip3 install sklearn
			pip3 install matplotlib
			pip3 install ipython
""")
def limpiar():
	import os
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')
opciones = ["piedra", "tijeras", "papel"]
def comprobar_Ganador(Jugada_de_A, Respuesta_de_B):
	if Jugada_de_A == Respuesta_de_B:
		Ganador = 0

	elif Jugada_de_A == "piedra" and Respuesta_de_B == "tijeras":
		Ganador = 1
	elif Jugada_de_A == "piedra" and Respuesta_de_B == "papel":
		Ganador = 2
	elif Jugada_de_A == "tijeras" and Respuesta_de_B == "piedra":
		Ganador = 2
	elif Jugada_de_A == "tijeras" and Respuesta_de_B == "papel":
		Ganador = 1
	elif Jugada_de_A == "papel" and Respuesta_de_B == "piedra":
		Ganador = 1
	elif Jugada_de_A == "papel" and Respuesta_de_B == "tijeras":
		Ganador = 2
	return Ganador
#-------------test del juego para ver su funcionamiento 
"""
comprobar_Ganador("papel", "tijeras")
test = [
		["piedra", "piedra", 0],
		["piedra", "tijeras", 1],
		["piedra", "papel", 2]
		]
for partida in test:
	print("jugador_A: %s jugador_B: %s Ganador: %s Validation: %s" % (partida[0], partida[1], comprobar_Ganador(partida[0], partida[1]), partida[2] ))
"""

from random import choice
def jugada_al_azar():
	return choice(opciones)
for i in range(10):
	jugador_A = jugada_al_azar()
	jugador_B = jugada_al_azar()
	print("jugador_A: %s jugador_B: %s Ganador: %s " % (jugador_A, jugador_B, comprobar_Ganador(jugador_A, jugador_B)))
	
def lista_opciones_de_jugadas(opciones):
	if opciones=="piedra":
		respuesta = [1,0,0]
	elif opciones=="tijeras":
		respuesta = [0,1,0]
	else:#	 por descarte solo queda papel
		respuesta = [0,0,1]
	return respuesta

dato_ingreso = list(map(lista_opciones_de_jugadas, ["piedra", "tijeras", "papel"]))
dato_respuesta = list(map(lista_opciones_de_jugadas, ["papel", "piedra", "tijeras"]))
print(f"\n\nReglas del juego\n    Papel cubre pieda | Piedra rompe Tijera | Tijera corta Papel")
print ("#-------------Jugadas----------------------------------")
print ("              piedra  |  tijeras |   papel")
print(f"             {dato_ingreso}")
print ("#-------------Respuesta Ganadora-----------------------")
print(f"              papel   |  piedra  | tijeras")
print(f"             {dato_respuesta}")

#-------------Prueba-en-red-neuronal------------
print ("\n#-------------Prueba-en-red-neuronal-------------------")
input ("Intro para continuar...")
from sklearn.neural_network import MLPClassifier#					 importo librerial 

clasificar = MLPClassifier(verbose=False, warm_start=True)

modelo_predictivo = clasificar.fit([dato_ingreso[0]], [dato_respuesta[0]])
print ("\n#-------------Respuesta de la libreria sklearn---------")
print("Modelo Predictivo :", modelo_predictivo)

#-------------aprender_desde_jugadas------------
print ("-------------aprender_desde_jugadas---------------------")
input ("Intro para continuar...")

def aprender_desde_jugadas(cant_jugadas, debug=False, jugador_A_ingreso="AZAR" ):#		por defecto entreno con 10 jugadas
	resultado = {"Ganadas": 0, "Perdidas": 0, "Totales": 0, "Porcentaje_ganado": 0 }
	
	dato_ingreso = []
	dato_respuesta = []
	
	for i in range(cant_jugadas):
		if jugador_A_ingreso=="AZAR" :
			jugador_A = jugada_al_azar()
#			print (jugador_A)
		else:
			jugador_A = jugador_A_ingreso
#			print (jugador_A)
		prediccion_prueba = modelo_predictivo.predict_proba([lista_opciones_de_jugadas(jugador_A)])[0]# solo se le da la jugada "A"
		
		if prediccion_prueba[0] >= 0.95:
			jugador_B = opciones[0]
		elif prediccion_prueba[1] >= 0.95:
			jugador_B = opciones[1]
		elif prediccion_prueba[2] >= 0.95:
			jugador_B = opciones[2]
		else:
			jugador_B = jugada_al_azar()#                  		si todas las predicciones es menor al 95 %
			
		if debug==True:
			print("jugador_A en tirada al azar:  "+str(jugador_A))
			print("prediccion de la jugada       "+str(prediccion_prueba))
			print("jugador_B en tirada al azar:  "+str(jugador_B))
		
		Ganador = comprobar_Ganador(jugador_A, jugador_B)
#		print("En Jugada Nº"+ str(i)+" el Ganador (con ambas tiradas al azar) es el jugador Nº: "+str(Ganador))		
		if debug==True:
			print("Comprobamos mediante la funcion comprobar_Ganador :")
			print("Ganador (con ambas tiradas al azar) es el jugador Nº: "+str(Ganador)+"\n")	

		if Ganador==2:
			dato_ingreso.append(lista_opciones_de_jugadas(jugador_A))
			dato_respuesta.append(lista_opciones_de_jugadas(jugador_B))
			resultado["Ganadas"]+=1
		else:
			resultado["Perdidas"]+=1
		resultado["Totales"]+=1
		resultado["Porcentaje_ganado"] = (int(resultado["Ganadas"]) / int(resultado["Totales"])*100)

	return resultado, dato_ingreso, dato_respuesta, jugador_A, jugador_B

#-------------Entrenamiento 1 de Prueba------------
print ("-------------Entrenamiento 1 de Prueba------------")
input ("Intro para continuar...")
resultado, dato_ingreso, dato_respuesta, jugador_A_ultima, jugador_B_ultima = aprender_desde_jugadas(1, debug=True)
print(f"resultado: {resultado}")
if len(dato_ingreso):
	prediccion = modelo_predictivo.partial_fit(dato_ingreso, dato_respuesta)
#-------------Entrenamiento 3 de Pruebas-----------
print ("-------------Entrenamiento 3 de Pruebas-----------")
input ("Intro para continuar...")
resultado, dato_ingreso, dato_respuesta, jugador_A_ultima, jugador_B_ultima = aprender_desde_jugadas(3, debug=True)
print(f"resultado: {resultado}")
if len(dato_ingreso):
	prediccion = modelo_predictivo.partial_fit(dato_ingreso, dato_respuesta)
#-------------Entrenamiento 10 de Pruebas----------
print ("-------------Entrenamiento 10 de Prueba-----------")
input ("Intro para continuar...")
resultado, dato_ingreso, dato_respuesta, jugador_A_ultima, jugador_B_ultima = aprender_desde_jugadas(10, debug=True)
print("Azar      :",dato_ingreso)
print("Respuesta :",dato_respuesta)
print(f"resultado: {resultado}")
if len(dato_ingreso):
	prediccion = modelo_predictivo.partial_fit(dato_ingreso, dato_respuesta)
#-------------aprendizaje con series de 100 Pruebas----------
print ("-------------aprendizaje con 1000 Prueba-----------")
input ("Intro para continuar...")
series = 0
historico_de_jugadas_ganadas_en_porcentaje = []
while True:
	series+=1
	cantidad_entrenamientos_en_cada_serie=100
	resultado, dato_ingreso, dato_respuesta, jugador_A_ultima, jugador_B_ultima = aprender_desde_jugadas(cantidad_entrenamientos_en_cada_serie, debug=False)#entrenamiento con 100 series de juegos
#	jugadas_ganadas = (resultado["Ganadas"]*100/(resultado["Ganadas"]+resultado["Perdidas"]))
	historico_de_jugadas_ganadas_en_porcentaje.append(resultado["Porcentaje_ganado"])
#	cantidad_entrenamientos_en_cada_serie
	print(f"Nº de serie: {series} de {cantidad_entrenamientos_en_cada_serie} entrenamientos cada una - resultado: {resultado}")
	if len(dato_ingreso):
		prediccion = modelo_predictivo.partial_fit(dato_ingreso, dato_respuesta)
		
	if (sum(historico_de_jugadas_ganadas_en_porcentaje[-10:])/10)==100:	# su en la suma de las ultimas 10 es un 100%  es que aprendio
#		print("Azar      :",dato_ingreso)
#		print("Respuesta :",dato_respuesta)
		break
total_de_entrenamientos_al_aprendizaje = series*cantidad_entrenamientos_en_cada_serie
print(f"Despues de : {series} series de {(cantidad_entrenamientos_en_cada_serie)} entrenamientos cada una.")
print(f"se obtienen 10 series con resultados seguidos con un > 95 % ganadores despues de un total de {total_de_entrenamientos_al_aprendizaje} pruebas")
print(f"Resultado final: {resultado}")
#-------------Grafica de aprendizaje------------
import matplotlib
from matplotlib import pyplot as plt
eje_x = range(len(historico_de_jugadas_ganadas_en_porcentaje))
eje_y = historico_de_jugadas_ganadas_en_porcentaje

fig, ax = plt.subplots()
ax.plot(eje_x, eje_y)

ax.set(xlabel='serie de iteraciones', ylabel='% de aciertos', title='Porcetaje de aprendizaje en cada serie de iteraciones')
ax.grid()
plt.show()

#-------------Pruebas con humano sin IA------------
print ("-------------Pruebas con humano sin IA----------------")
input ("Intro para continuar...")
limpiar()
Ganadas = 0
Perdidas = 0
Empates = 0
for i in range(5):

	while True:
		jugador_A = input("Ingrese: piedra o papel o tijeras   :")
		if jugador_A in opciones :
			break
		
	jugador_B = jugada_al_azar()
	print(f"Jugada nº {i+1}\n Ustes jugo: {jugador_A} La pc jugo: {jugador_B}", end="");
	resultado_azar = comprobar_Ganador(jugador_A, jugador_B)
	print(f" Ganador: Jugador nº", resultado_azar )
	if 	resultado_azar==2:
		Ganadas +=1
	elif resultado_azar==1:
		Perdidas +=1
	else:
		Empates +=1
print (f"Total de ganadas por el AZAR : {Ganadas} ")
print (f"Total de ganadas por la Ud.  : {Perdidas} ")	
print (f"Total de empates             : {Empates} ")
#-------------Pruebas con humano con IA ´ya enseñada´------------
print ("-------------Pruebas con humano con IA ´ya enseñada´----------------")
input ("Intro para continuar...")
Ganadas = 0
Perdidas = 0
Empates = 0
for i in range(5):
	while True:
		jugador_A_input = input("Ingrese: piedra o papel o tijeras   :")
		if jugador_A_input in opciones :
			break
	resultado, dato_ingreso, dato_respuesta, jugador_A_ultima, jugador_B_ultima = aprender_desde_jugadas(1, debug=False, jugador_A_ingreso=str(jugador_A_input) )
	print(f"Jugada nº {i+1}\n Ustes jugo: {jugador_A_ultima} La pc jugo: {jugador_B_ultima}", end="");
	resultado_AI = comprobar_Ganador(jugador_A_ultima, jugador_B_ultima)
	print(f" Ganador: Jugador nº", resultado_AI )
	if 	resultado_AI==2:
		Ganadas +=1
	elif resultado_AI==1:
		Perdidas +=1
	else:
		Empates +=1
print (f"Total de ganadas por el IA   : {Ganadas} ")
print (f"Total de ganadas por la Ud.  : {Perdidas} ")	
print (f"Total de empates             : {Empates} ")
