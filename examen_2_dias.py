# -*- coding: utf-8 -*-
"""Examen_2_dias.ipynb"""

import requests # Para realizar la petición a la API
import pandas as pd # Para poder manipular el JSON

"""### Declaramos los datos a comparar"""

# Como primer paso, se obtuvieron algunas IP's de distintas ciudades de México, y del mundo. 
# Estas direcciones IP's fueron obtenidas de la siguiente página web: 
# https://myip.ms/browse/cities/IP_Addresses_Cities.html

# Creamos un diccionario con información de interés
IPs_info = { 'Hypothetical_city' : ["Mexico City", 'Guadalajara', "Monterrey", "Amsterdam", "London",
                                   "Tokyo", "Madrid"],
    'IP' : ["189.217.100.132", "177.234.12.202", "200.94.201.27", "37.130.224.22", "78.110.170.119",
           "110.50.243.6", "195.12.50.155"] }

# Crear un data frame a partir del diccionario anterior. Servira como variable de nuestra función
IPs_table = pd.DataFrame(IPs_info)

"""### Creamos nuestra funcion main"""

def API_requests(df):
    
    container = [] # Contenedor auxiliar para almacenar info acerca de la consulta a la API
        
    for i in range(0, len(list(df.IP))): # For para ir iterando la dirección IP 
        
        DIRECCION_IP = df.IP[i] # Tomamos la dirección IP "n", depende de la iteración
        Hip_City = df.Hypothetical_city[i] # Obtenemos nuestra ciudad hipotetica
        APIs = [f"https://geolocation-db.com/json/{DIRECCION_IP}&position=true",
        f"https://ipinfo.io/{DIRECCION_IP}/json",
        f"http://api.hostip.info/get_json.php?ip={DIRECCION_IP}&position=true",
        f"https://json.geoiplookup.io/{DIRECCION_IP}",
        f"https://freegeoip.app/json/{DIRECCION_IP}",
        f"http://ip-api.com/json/{DIRECCION_IP}"] # Lista que contiene todas las urls a las APIs
        
        results = pd.DataFrame(columns=['IP', 'Hypothetical_city', 'City_from_API', 
                                        'URL_API']) # DataFrame donde se almacenaran resultados individuales
        
        for j in range(0, len(APIs)): # For que irá recorriendo cada una de las APIs
            
            idr = requests.get(APIs[j]) # Petición tipo get a la API "n", depende de la iteración
            if idr.status_code == 200: # Si el status es igual a 200, quiere decir que la petición fue valida
                idjson = idr.json() # Pasamos de texto a json (diccionario)
                results.loc[len(results)] = [DIRECCION_IP, Hip_City, idjson['city'], APIs[j]] # Creamos una fila de datos, con la ciudad que nos regresó la API
            else:
                results.loc[len(results)] = [DIRECCION_IP, Hip_City, 'API_down', APIs[j]] # Si el estatus es distinto a 200, se colocará el valor "API_down"
                
        container.append(results) # Concatenamos nuestros dataframes en la lista inicial
            
    df[["Queries_match?", "City"]] = None # Añadimos 2 columnas vacias a nuestro df
    
    for i in range(0, len(container)): # For para determinar si coinciden o discrepan las ciudades
    
        aux_list = list(container[i].City_from_API) #Creamos una lista con las ciudades que nos devolvieron las APIs al consultar una IP especifica
        compair_list = [container[i].Hypothetical_city[0]]
        compair_list *= 6
        if compair_list == aux_list: # Comprobamos si todos los elementos de la lista son iguales
            df["Queries_match?"][i] = "coinciden" # De ser así, coinciden
            df["City"][i] = "Ciudad Origen: " + aux_list[0] # Se coloca la sentencia solicitada seguido de la ciudad en cuestion
        else:
            a = container[i].City_from_API.value_counts() # De no ser el caso, contamos la ciudad que se repita más veces
            city = a.index[0] # Seleccionamos a dicha ciudad
            df["Queries_match?"][i] = "discrepan" # De ser así, coinciden
            df["City"][i] = "Probable Ciudad Origen: " + city # Se coloca la sentencia solicitada seguido de la ciudad en cuestion
        
    final_df = pd.DataFrame() # Creamos un df vacio que contendra la info no resumida
    
    for k in range (0, len(container)): # Este for tiene intención de aplanar la lista contenedora
        final_df = pd.concat([final_df, container[0]], axis=0) # Va concatenando cada df en uno solo
        container.pop(0) # Conforme van las iteraciones, elimina el primer elemento
    final_df = final_df.reset_index(drop=True) # Se resetea el indice, y omite el colocar la columna de indices viejos
        
    return(df, final_df) # Se regresan dos df, el primero con la info resumida, el segundo con más detalles de cada consulta a las APIs

# Ejecutamos nuestra función, y guardamos los dfs que nos regresa está, en dos variables distintas
Resumen, Explicito = API_requests(IPs_table)

#Desplegamos los resultados como se solicitan
display(Resumen)

# Info más detallada acerca de cada una de las consultas realizadas
display(Explicito)

"""# Problema 1 (2 horas)

## Calcetines
"""

# Primero comenzaremos contando la cantidad de calcetines pares limpios

por_lavar = 10 # Cantidad por ciclo de lavado, máximo es 2
limpios = [1, 2, 1, 1, 2, 2, 8] # Limpios
sucios =[1, 4, 3, 1, 2, 4] # Sucios


def solucion(K,L,S):

    #Contamos la cantidad de pares de calcetines limpios
    clean_pairs = dict((i, L.count(i)) for i in L if L.count(i)>1)
    
    #Separamos por colores (numero) y la cantidad de repeticiones
    colors = list(clean_pairs.keys())
    repeated = list(clean_pairs.values())
    
    # Contamos la cantidad de repeticiones por color, 
    # y comprobamos si hay cantidad de calcetines pares o nones.
    
    total_pairs = []
    alone_socks = []
    
    for i in range (0, len(repeated)):
        total_pairs.append(repeated[i]//2)
        alone_socks.append(repeated[i]%2)
        
    # Hacemos una relación de la cantidad de pares limpios por color
    # Y en caso de existir, calcetines limpios que no tienen par
    clean_pairs_colors = dict(zip(colors, total_pairs))
    clean_alone_colors= dict(zip(colors, alone_socks))
    
    L = set(L)
    L = list(L)
    
    for i in range (0, len(colors)):
        L.remove(colors[i])
    
    # Por cada clave en el diccionario
    for key in clean_alone_colors:
        if clean_alone_colors[key] != 0:
            L.append(key)
    
    print("Relacion de color y cantidad de pares limpios de calcetines: ", clean_pairs_colors)
    print("Color de calcetines impares limpios: ", L)
    
    if K <= 1:
        
        return(print("Está disponible el lavar un calcetin sucio más, pero no tendría sentido"))
    
    if K != 0:
        
        clean_and_dirty = list(set(L) & set(S))
        print("Color de calcetines sucios del mismo color que impares limpios: ", clean_and_dirty)
        
        clean_keys = list(clean_pairs_colors.keys())
        
        if K <= len(clean_and_dirty):
            
            for i in range(0, K):
                
                if clean_and_dirty[i] in clean_keys:
                    clean_pairs_colors[clean_and_dirty[i]] = clean_pairs_colors[clean_and_dirty[i]] + 1
                else:
                    clean_pairs_colors.update({clean_and_dirty[i]: 1})
            
            return(print("Actualizacion de color de calcetines, y cantidad de pares limpios: ", clean_pairs_colors))
            
        else:
            
            for i in range(0, len(clean_and_dirty)):
                
                if clean_and_dirty[i] in clean_keys:
                    clean_pairs_colors[clean_and_dirty[i]] = clean_pairs_colors[clean_and_dirty[i]] + 1
                else:
                    clean_pairs_colors.update({clean_and_dirty[i]: 1})
            
                K = K - 1
                
            print("Actualizacion de color de calcetines, y cantidad de pares limpios: ", clean_pairs_colors)
            
            
            if K < 2:
                
                return(print("Está disponible el lavar un calcetin sucio más (o en caso de haber ingresado cero, ninguno), pero no tendría sentido"))
                
            else:
            
                # Actualización de calcetines sucios
        
                for i in range (0, len(clean_and_dirty)):
                    aux = S.index(clean_and_dirty[i])
                    S.pop(aux)
                
                #Contamos la cantidad de pares de calcetines sucios
                dirty_pairs = dict((i, S.count(i)) for i in S if S.count(i)>1)
                
                #Separamos por colores (numero) y la cantidad de repeticiones
                colors = list(dirty_pairs.keys())
                repeated = list(dirty_pairs.values())
                
                # Contamos la cantidad de repeticiones por color, 
                # y comprobamos si hay cantidad de calcetines pares o nones.
                
                total_pairs = []
                alone_socks = []
                
                for i in range (0, len(repeated)):
                    total_pairs.append(repeated[i]//2)
                    alone_socks.append(repeated[i]%2) 
                    
                # Hacemos una relación de la cantidad de pares sucios por color
                # Y en caso de existir, calcetines sucios que no tienen par
                dirty_pairs_colors = dict(zip(colors, total_pairs))
                dirty_alone_colors= dict(zip(colors, alone_socks))
                
                S = set(S)
                S = list(S)
                
                total_calcetines = sum(repeated)
                
                if K > total_calcetines:
                    
                    for i in range (0, len(colors)):
                        S.remove(colors[i])
                    
                    # Por cada clave en el diccionario
                    for key in dirty_alone_colors:
                        if dirty_alone_colors[key] != 0:
                            S.append(key)
                    
                    print("Relacion de color y cantidad de pares limpios (que estaban sucios) de calcetines: ", dirty_pairs_colors)
                    print("Color de calcetines impares sucios: ", S)
                    
                    print("\nRelacion final de calcetines limpios", clean_pairs_colors | dirty_pairs_colors )
                    
                else:
                    
                    new = total_calcetines%K
                    
                    for i in range (0, new):
                        S.remove(colors[i])
                    
                    # Por cada clave en el diccionario
                    for key in dirty_alone_colors:
                        if dirty_alone_colors[key] != 0:
                            S.append(key)
                    
                    print("Relacion de color y cantidad de pares limpios (que estaban sucios) de calcetines: ", dirty_pairs_colors)
                    print("Color de calcetines impares sucios: ", S)
                    
                    print("\nRelacion final de calcetines limpios", clean_pairs_colors | dirty_pairs_colors)
                    
solucion(por_lavar, limpios, sucios)

# Para la cuestión de delimitar las condiciones que se solicitan:
# k= entero del 0 al 50
# L = Array de enteros del 1 al 50
# S = Array de enteros del 1 al 50
# Se utilizó la librería random para generar los numeros aleatorios para L, y S.
# Esta librería no afecta en el algoritmo como tal, solo es para agilizar el llenado de los arreglos

import random

def L_random(n):
    lista = []
    for i in range(n):
        lista.insert(i, random.randrange(1, 50))
    return lista

def S_random(n):
    lista = []
    for i in range(n):
        lista.insert(i, random.randrange(1, 50))
    return lista

while True:
    try:
        n = int(input("Ingrese los ciclos de lavado para K: "))
    except ValueError:
        print("Ingrese los ciclos de lavado para K: ")
        continue
    if n < 0:
        print("Debes escribir un número positivo.")
        continue
    if n > 50:
        print("K debe de ser menor a 50")
        continue
    else:
        break

K = n
print(K)


while True:
    try:
        n = int(input("Ingrese cuantos numeros aleatorios desea obtener para L: "))
    except ValueError:
        print("Ingrese cuantos numeros aleatorios desea obtener para L")
        continue
    if n < 1:
        print("Debes escribir un número positivo.")
        continue
    if n > 50:
        print("L debe de ser menor a 50")
        continue
    else:
        break

L = L_random(n)
print(L)

while True:
    try:
        n = int(input("Ingrese cuantos numeros aleatorios desea obtener para S: "))
    except ValueError:
        print("Ingrese cuantos numeros aleatorios desea obtener para S")
        continue
    if n < 1:
        print("Debes escribir un número positivo.")
        continue
    if n > 50:
        print("S debe de ser menor a 50")
        continue
    else:
        break

S = S_random(n)
print(S)

print("\n")

solucion(K, L, S)