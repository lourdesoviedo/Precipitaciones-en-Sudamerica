#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 11:12:08 2025

@author: Estudiante
"""

#tp final de LPIM
#inciso a
#importo librerias
import netCDF4 as nc
import datetime
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import os

#ruta de archivos y graficos
os.chdir(r"C:\Users\lulio\Documents\tp_final")
data=nc.Dataset(r"precip.mon.mean.nc")

a=list(data.variables.keys())

data2={clave: data.variables[clave][:].filled() for clave in a} #saco las variables del netcdf como una comrpehension dict

data.variables["time"]#veo que empieza el empieza el 1-1-1 00:00:0.0 #datos estan en horas
data.variables["precip"] 
#veo que los valores erroneos que estan codificados para el inciso b
data.close() #cierro el netcdf
                                                                        
inicio=datetime.datetime(1,1,1,0,0,0)
fechas=[inicio + datetime.timedelta(hours=t) for t in data2["time"]] #array de fechas

#funcion para encontrar las latitudes y longitudes en el diccionario
def buscador(lat,LAT,):
    """Ingresa el nombre del diccionario "lat" o "lon" y busca el inicio y el final del 
        vector y te devuelve un string con el nombre de la variable, el inicio y el final"""
    i=data2[lat][0]
    f=data2[lat][-1]
    p=f"{LAT}:({i} a {f})"
    return p

#defino las variables que voy a usar para mi diccionario
#alguna manera de poner todo esto y noi definir variables, puedo hacer una fucnion sino????


nombre_archivo = "precip.mon.mean.nc" #nombre del netcdf
cant_datos = len(data2["lon"]) * len(data2["lat"]) * len(data2["time"]) #cantidad de datos
#preguntar como multiplicarlo o como busco la cantidad de datos
nombre_variables = f"{a[0]}, {a[1]}, {a[2]}, {a[3]}" #nombre de las variables del netcdf
periodo = f"{fechas[0]} a {fechas[-1]}" #periodo de fechas del netcdf
lat = buscador("lat", "Lat") #uso las funciones para buscar las lats y lons
lon = buscador("lon", "Lon")
region = f"{lat}, {lon}" #defino como un string usando la funcion buscador
atributos = f"{a[0]}:grados, {a[1]}: grados, {a[2]}: hs, {a[3]}: mm/day" #unidades


#creo mi diccionario con los datos de arriba
#el formato que tiene es para que coincida con un dataframe y poder guardarlo como archivo 
#ascii, por eso algunas cosas estan como strings
d = {"Data":["Nombre del Archivo", "Cantidad de variables", "Nombre de las variables",
           "Cantidad de datos", "Periodo", "Region", "Atributos"],
           "Variables": [nombre_archivo, str(len(a)), nombre_variables,
                        str(cant_datos), periodo, region, atributos]}

#creo un data frame apartir del diccionario
df = pd.DataFrame(d)

#guardo el archivo como ascii
df.to_csv(r'datos_precipitaciones.txt', sep='\t', index=False, header=None)



#%%
#inciso b

pp = data2["precip"] #defino un array de las precipitaciones fuera del diccionario
 #antes ya vi que los valores erroneos estan codificados con este numero
num = -9.96921e+36

pp[pp==num] =np.nan #pido que todos los valores dentro del array que cumplen con la condicion
#o sea que son iguales al num de valor erroneos se codifiquen como np.nan

#mi array de pp tiene todo los meses durante 33 años excepto el ultimo
#mes como se puede ver usando el array de fechas, creo una matriz llena de np.nan del
#tamaño de la reticula para luego hacer un reshape de 33 años por 12 meses y luego calcular 
#las medias y desvios pedidas mediante funciones del tipo "np.nanmean" o "np.nanstd" que 
#ignoran los valores codificados como nan

shape=(1, 72, 144) #un mes de toda la reticula
na=np.full((shape), np.nan) #creo un array del tamaño de la reticula lleno de"np.nan" para
#agregarlo al ultimo mes de mi array de precipitaciones "pp"

pp = np.concatenate((pp, na), axis=0) #agrego al array de precipitaciones, mi array de "np.nan" 
shape_am = (33, 12, 72, 144) #tengo 12 meses durante 33 años
pp = pp.reshape(shape_am) #hago un reshape para separar por años y meses

#calculo el promedio de los desvios en el eje de los años
desvios_mensuales = np.nanstd(pp, axis=0) #desvios
medias_mensuales = np.nanmean(pp, axis=0) #medias

#calculo las medias del trimetsre DEF
mes_d = 11
mes_e = 0
mes_m = 2
medias_dic = medias_mensuales[mes_d, :, :]  #agarro el array del mes de diciembre
medias_dic = medias_dic.reshape(shape) #reshape para que tengan ambos arrays mismas 
                                        #dimensiones para despues concatenarlos
medias_ef = medias_mensuales[mes_e:mes_m, :, :] #agarro el array de los meses de enero y febrero

medias_def = np.concatenate((medias_dic, medias_ef), axis=0)#concateno los meses de DEF

#calculo las medias para el mes def por separado porque asi despues hago un ciclo que 
#empieze desde el segundo mes y que ietere cada dos, como este me pide el mes 12,0,1 no es 
# tan directo
medias_def = np.nanmean((medias_def), axis=0) #calculo las medias de DEF

medias_estacionales = [] #creo una lista vacia para agregar los arrays de las iteraciones del
#las otras estaciones
medias_estacionales.append(medias_def) #agrego el array de DEF

#itero para agregar los meses cada 3 meses y calculo las medias estacionales, luego las 
#agrego a la lista
for i in range (2, 9, 3):
    medias = medias_mensuales[i:i + 3, :, :]
    medias = np.nanmean((medias), axis=0)
    medias_estacionales.append(medias)

#calculo los desvios del trimetsre DEF
desvios_dic = desvios_mensuales[mes_d, :, :]  #agarro el array del mes de diciembre
desvios_dic = desvios_dic.reshape(shape) #reshape para que tengan ambos arrays mismas 
                                        #dimensiones para despues concatenarlos
desvios_ef = desvios_mensuales[mes_e:mes_m, :, :] #agarro el array de los meses de enero y febrero

desvios_def = np.concatenate((desvios_dic, desvios_ef), axis=0)#concateno los meses de DEF

#calculo los desvios para el mes DEF por separado porque asi despues hago un ciclo que 
#empieze desde el segundo mes y que ietere cada dos, como este me pide el mes 12,0,1 no es 
# tan directo
desvios_def = np.nanstd((desvios_def),axis=0) #calculo los desvios de DEF

desvios_estacionales = [] #creo una lista vacia para agregar los arrays de las iteraciones del
#las otras estaciones
desvios_estacionales.append(desvios_def) #agrego el array de DEF

#itero para agregar los meses cada 3 meses y calculo los desvios estacionales, luego las 
#agrego a la lista
for i in range (2, 9, 3):
    desvios = desvios_mensuales[i:i + 3, :, :]
    desvios = np.nanstd((desvios), axis=0)
    desvios_estacionales.append(desvios)
#%% segundo grafico
#graficaado de las medias estacionales
#defino las latitudes y las longitudes de sudamerica
latinf = -55
latsup = 12
lonsup = 326
loninf = 279

#busco las latitudes y longitudes que coinciden con las de sudamerica (las anteriores)
lat=data2["lat"][(data2["lat"]<=latsup) & (data2["lat"]>=latinf)] #latitudes
lon=data2["lon"][(data2["lon"]<=lonsup) & (data2["lon"]>=loninf)] #longitudes

#uso la funcion "np.where" para que me devuelva las posiciones donde empieza y terminan las 
#latitudes y longitudes de sudamerica o sea [0]=inicial, [-1]= ultima
#"np.where" te devuelve una tupla de una serie(en este caso puntual) con las ubicaciones, 
#entonces, lo indexo
lat_pos_inf = (np.where(data2["lat"]==lat[0]))[0][0]
lat_pos_sup = (np.where(data2["lat"]==lat[-1]))[0][0]
lon_pos_inf = (np.where(data2["lon"]==lon[0]))[0][0]
lon_pos_sup = (np.where(data2["lon"]==lon[-1]))[0][0]

#tengo que recortar la reticula para los 4 trimestres, uso un ciclo

medias_estacionales_recortadas = [] #creo una lista donde voy a colocar las medias 
#cuatrimestrales de la reticula de sudamerica

#recorto la reticula para sudamerica
for i in range(4):
    medias = medias_estacionales[i][lat_pos_inf: lat_pos_sup+1, lon_pos_inf: lon_pos_sup+1]
    medias_estacionales_recortadas.append(medias)

mxp = np.max(medias_estacionales_recortadas)

titulos = ["DEF", "MAM", "JJA", "SON"] #titulos de los subplots

#grafico
#uso subplots para visualizar en una imagen los cuatro ploteos de precipitacion juntos

#creo una figura de 2 columnas, 2 filas con el tipo de proyeccion para sudamerica
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(8, 8),
                        subplot_kw={'projection': ccrs.Robinson(central_longitude=300,
                                                                globe=None)})


fig.subplots_adjust(hspace=0.1, wspace = -0.9) #distancia entre figuras
axs = axs.flatten()
for i in range(4):
    ax = axs[i]
    ax.add_feature(cfeature.COASTLINE) #limites del continente
    ax.add_feature(cfeature.BORDERS, linestyle='-', alpha=0.5) #separacion de paises
    
    # Contornos
    im = ax.contourf(lon, lat, medias_estacionales_recortadas[i], levels=np.arange(1.5,mxp,1.5), 
                     cmap="YlGnBu", extend = "both", transform=ccrs.PlateCarree())
    # Líneas de grilla SOLO en los bordes laterales e inferior
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray',
                     alpha=0.5, linestyle='--') #grilla
    gl.top_labels = False #saco los valores de arriba de los ejes
    gl.right_labels = (i % 2 != 0)#derecha solo en los paneles derechos
    gl.left_labels = (i % 2 == 0) 
    gl.ylabel_style =  {"size":8}  #tamaño de los valores del eje y
    gl.bottom_labels = (i >= 2) 
    gl.xlabel_style =  {"size":8}  #tamaño de los valores del eje x
    ax.set_title(f"{titulos[i]}") #titulos de los subplots


# barra de colores
cbar_ax = fig.add_axes([0.25, 0.07, 0.5, 0.025]) #ejes de la barra de colores
cbar = fig.colorbar(im, cax=cbar_ax, orientation='horizontal') #tamaño y orientacion
cbar.set_label("Precipitación (mm/day)") #nombre

fig.suptitle("Precipitación de medias estacionales\n de Sudamérica - 1979-2011", fontsize=16, y=0.93) #preguntare si esta bi9en bajar el tiutlo
fig.tight_layout(rect = [0, 0.1, 1, 0.95])

#guardo la figura
fig.savefig(r"precipitaciones_sudamerica_medias.png", dpi=500, bbox_inches='tight')
plt.show()

#%%
desvios_estacionales_recortadas = [] #creo una lista donde voy a colocar las medias 
#cuatrimestrales de la reticula de sudamerica

#recorto la reticula para sudamerica
for i in range(4):
    desvios = desvios_estacionales[i][lat_pos_inf: lat_pos_sup+1, lon_pos_inf: lon_pos_sup+1]
    desvios_estacionales_recortadas.append(desvios)

mxx=np.max(desvios_estacionales_recortadas)
titulos = ["DEF", "MAM", "JJA", "SON"] #titulos de los subplots

#grafico
#uso subplots para visualizar en una imagen los cuatro ploteos de precipitacion juntos

#creo una figura de 2 columnas, 2 filas con el tipo de proyeccion para sudamerica
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(8, 8),
                        subplot_kw={'projection': ccrs.Robinson(central_longitude=300, 
                                                                globe=None)})


fig.subplots_adjust(hspace=0.1, wspace = -0.9) #distancia entre figuras
axs = axs.flatten()
for i in range(4):
    ax = axs[i]
    ax.add_feature(cfeature.COASTLINE) #limites del continente
    ax.add_feature(cfeature.BORDERS, linestyle='-', alpha=0.5) #separacion de paises
    
    # Contornos
    im = ax.contourf(lon, lat, desvios_estacionales_recortadas[i],levels=np.arange(0,mxx,0.3), cmap="OrRd", 
                     extend = "both", transform=ccrs.PlateCarree())
    # Líneas de grilla SOLO en los bordes laterales e inferior
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray',
                     alpha=0.5, linestyle='--') #grilla
    gl.top_labels = False #saco los valores de arriba de los ejes
    gl.right_labels = (i % 2 != 0)#derecha solo en los paneles derechos
    gl.left_labels = (i % 2 == 0) 
    gl.ylabel_style =  {"size":8}  #tamaño de los valores del eje y
    gl.bottom_labels = (i >= 2) 
    gl.xlabel_style =  {"size":8}  #tamaño de los valores del eje x
    ax.set_title(f"{titulos[i]}") #titulos de los subplots


# barra de colores
cbar_ax = fig.add_axes([0.25, 0.07, 0.5, 0.025]) #ejes de la barra de colores
cbar = fig.colorbar(im, cax=cbar_ax, orientation='horizontal') #tamaño y orientacion
cbar.set_label("Precipitación (mm/day)") #nombre

fig.suptitle("Precipitación de desvíos estacionales\n de Sudamérica - 1979-2011", fontsize=16, y=0.93) #preguntare si esta bi9en bajar el tiutlo
fig.tight_layout(rect=[0, 0.1, 1, 0.95])

#guardo la figura
fig.savefig(r"precipitaciones_sudamerica_desvios.png", dpi=300, bbox_inches='tight')
plt.show()
#%%
#inciso c tercer grafico

#data frame con los datos que me dieron en la tabla
d = {"Acronym":["Am", "SAM", "NeB", "SACZ", "LPB"], "Name": ["Amazonia", 
    "South American Monsoon", "North-eastern Brazil", "South Atlantic Convergence Zone", 
    "La Plata Basin"], "Latitud inferior": [-13.75, -16.25, -16.25, -26.25, -38.75],
     "Latitud superior": [1.25, -3.75, -1.25, -16.25, -23.75],
     "Longitud inferior": [291.25, 301.25, 313.75, 308.75, 296.25],
     "Longitud superior": [303.75, 316.25, 326.25, 321.25, 308.75]}

dff = pd.DataFrame(d)

regiones = {} #diccionario vacio

for i in range (5):
    lats = data2["lat"][(data2["lat"] <= dff["Latitud superior"][i]) & (data2["lat"] >= dff["Latitud inferior"][i])]
    lons = data2["lon"][(data2["lon"] <= dff["Longitud superior"][i]) & (data2["lon"] >= dff["Longitud inferior"][i])]

    lats_inf = (np.where(data2["lat"] == lats[0]))[0][0]
    lats_sup = (np.where(data2["lat"] == lats[-1]))[0][0]
    lons_inf = (np.where(data2["lon"] == lons[0]))[0][0]
    lons_sup = (np.where(data2["lon"] == lons[-1]))[0][0]
    mediass = medias_mensuales[:,lats_inf:lats_sup, lons_inf:lons_sup]
    mediass = np.nanmean(mediass,axis = (1,2)) #media de la reticula
    regiones[dff["Acronym"][i]] = mediass

#grafico, serie temporal
   
# Interfaz Orientada a Objetos
fig = plt.figure() #Generamos la figura
ax = plt.axes() #Generamos el objeto de los ejes de graficado
meses = np.arange(1,13) #array numerando los meses

for i in range (5):
    reg = dff["Acronym"][i] #nombre de los lugares de las series temporales
    plt.plot(meses, regiones[reg], label=reg)

ax.set_title("Marchas anuales de precipitación") #titulo
ax.set_xlabel("Meses") #titulo del eje x
plt.xticks(ticks = np.arange(1,13)) #cada cuanto quiero que me muestre valores en

#el eje x
ax.margins(x=0.05) #agrega un espacio entre los ejes
ax.set_ylabel ("Precipitación (mm/day)")
ax.grid(True, ls="--", alpha=0.5) #grilla
plt.legend() #
ax.legend(loc="lower left") 
plt.show()

#guardo la figura
fig.savefig(r"marcha_anuales_precipitacion.png", dpi=500, bbox_inches='tight')