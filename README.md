# Instalación

## Datos
Para evitar el acceso a un servidor externo, los datos se encuentran en el repositorio bajo la carpeta 'data'.
Debido al tamaño, los ficheros csv de los viajes (OD_2014.csv, OD_2015.csv, OD_2016.csv y OD_2017.csv) se encuentran comprimidos. 
Es necesario descomprimir estos ficheros y dejarlos en la carpeta **data** de su equipo junto con el resto de ficheros csv.
 
## Prerequisitos
Para resolver el desafío se ha construído un programa python.
Es necesario que su computadora tenga instalado Python 3.
Se necesitan las librerías de python: pandas, matplotlib y json.
Se proporciona el fichero requirements.txt con las dependencias.

## Ejecución
Ejecutar: python3 metyis.py

## Notas
- El progrma principal se encuentra en metyis.py. Utiliza las clases del módulo trips.py
- Genera en la carpeta de imagenes 'img' ficheros .png con los histogramas.
- Se documenta también con un notebook de Jupyter que se encuentra en el repositorio.
