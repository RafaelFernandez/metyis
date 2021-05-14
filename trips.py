# Se importan las liberías necesarias
import pandas as pd
import matplotlib.pyplot as plt
import json

DATA_PATH = './data/'
IMG_PATH = './img/'


class TripsYearRepo:
  """ Repositoro de los viajes de un año, leídos de un fichero csv """

  def __init__(self, year):
    self.year = year
    # Se lee el fichero csv de viajas del año correspondiente
    self.trips = pd.read_csv(f'{DATA_PATH}OD_{year}.csv', low_memory=False)

    # Se calcula la duración de los viajes en minutos
    self.trips['duration_min'] = self.trips['duration_sec'] / 60
    self.trips['end_station_code'] = self.trips['end_station_code'].apply(self.clean_station).astype('int')

  def duration_hist(self):
    """ Genera el histograma de los tiempos de viaje del año en un fichero """

    plt.figure(0)
    plt.hist(self.trips['duration_min'], bins=23)
    plt.xlabel('Minutos')
    plt.ylabel('Nº de viajes')
    plt.title(f'Histograma de tiempos de viaje en {self.year}')
    plt.grid(True)
    plt.savefig(f'{IMG_PATH}duracion_viajes_{self.year}')

  def rush_hour_hist(self):
    """ Calcula la hora punta (mayor número de viajes)
    y genera un histograma en un fichero """

    hour = pd.to_datetime(self.trips['start_date']).dt.hour
    plt.figure(1)
    plt.hist(hour, bins=24)
    plt.xlabel('Horas')
    plt.ylabel('Nº de viajes')
    plt.title(f'Viajes por hora en {self.year}')
    plt.grid(True)
    plt.savefig(f'{IMG_PATH}viajesxhora_{self.year}')
    return hour.value_counts().head(1).index[0]
  
  def clean_station(self, x):
    """ If the value is a string and numeric, can be converted to int
    otherwise, return 0 """

    return x if str(x).isnumeric() else 0

  def topN(self, N, stations, stations_repo):
    """ Se agrupan los datos por el código de estación de salida para contar los viajes por estación
    El resultado está en orden descendente y se toman los N primeros 
    Recibe el repositorio de estaciones para poder obtener la info de las mismas (nombre, localización) """

    grouped = stations.value_counts().head(N)
    columns = {'station': grouped.index, 'count': grouped}
    topN_stations = pd.DataFrame(columns)
    topN_stations['station'] = topN_stations['station']
    return stations_repo.get_info(topN_stations, 'station')

  def topN_start_stations(self, N, stations_repo):
    start_stations = self.trips['start_station_code']
    return self.topN(N, start_stations, stations_repo)

  def topN_end_stations(self, N, stations_repo):
    end_stations = self.trips['end_station_code']
    return self.topN(N, end_stations, stations_repo)
  

  def topN_start_end_stations(self, N, stations_repo):
    """ Concatenan los códigos de las estaciones de salida con los de llegada para luego agruparlos """

    stations = pd.concat([self.trips['start_station_code'], self.trips['end_station_code']], ignore_index=True)
    stations.name = 'stations'
    return self.topN(N, stations, stations_repo)

  def topN_trips(self, N, stations_repo):
    """ Agrupa los datos por el código de estación de salida y de llegada para contar los viajes por estación
    Se ordena el resultado en orden descendente y se toman los N primeros """

    grouped_trip = self.trips.groupby(['start_station_code','end_station_code'])['start_date'].count().sort_values(ascending=False).head(N)
    columns = {'start_code': grouped_trip.index.get_level_values(0), 
              'end_code': grouped_trip.index.get_level_values(1), 
              'count': grouped_trip }
    topN = pd.DataFrame(columns, index=None)
    topN = stations_repo.get_info(topN, 'start_code')
    topN = stations_repo.get_info(topN, 'end_code')
    return topN[['start_code', 'name_x', 'end_code', 'name_y', 'count']]

  def total_trips(self):
    """ Cuenta el número de filas del dataframe de viajes """

    return self.trips['start_station_code'].count()

  def total_time(self):
    """ Suma de la duración de los viajes en minutos """
    return round(self.trips['duration_min'].sum())
       
    

class StationsYearRepo:
  """ Repositorio con la información maestra de las estaciones por año """

  def __init__(self, year):
    self.year = year
    # Se lee el fichero csv de estaciones del año correspondiente
    self.stations = pd.read_csv(f'{DATA_PATH}Stations_{year}.csv')

  
  def get_info(self, stations, left_name):
    """ Se unen con los datos de estaciones para obtener el nombre y la posición """

    info = pd.merge(left = stations, right = self.stations,
                    left_on = left_name, right_on = 'code').drop('code', axis=1)
    return info
    

class StationsStatus:
  """ Repositorio con el último estado de las estaciones obtenido de un fichero json
  Contiene entre otros el número de terminales y bicicletas disponibles """

  def __init__(self):
    # Se lee el fichero json de capacidad
    with open(f'{DATA_PATH}stations.json') as f:
      data = json.load(f)
      self.status = pd.DataFrame.from_records(data['stations'])
      self.status['n'] = self.status['n'].apply(self.clean_station).astype('int')
    
  def available_terminals(self):
    return self.status['da'].sum()

  def available_bikes(self):
    return self.status['ba'].sum()

  def available_terminals_bikes(self, stations_repo):
    info = pd.merge(left = self.status, right = stations_repo.stations,
                    left_on = 'n', right_on = 'code')
    return (info['da'].sum(),  info['ba'].sum())

  def clean_station(self, x):
    """ If the value is a string and numeric, can be converted to int
    otherwise, return  """
    return x if str(x).isnumeric() else 0


