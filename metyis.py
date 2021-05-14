from trips import TripsYearRepo
from trips import StationsYearRepo
from trips import StationsStatus

DATA_YEARS = ['2014', '2015', '2016', '2017']

def ask_year(ask, year1 = '9999'):
  year = '0'
  while year not in DATA_YEARS or year == year1:
    print(ask)
    year = input()
  return year

def ask_N(ask):
  N = '0'
  while not N.isnumeric() or int(N) < 1 or int(N) > 100:
    print(ask)
    N = input()
  return int(N)

def pause(ask):
  print(ask)
  input()

def main():
  print("\nANALISIS DEL CONJUNTO DE DATOS DE BIXI")

  # Solicitar el año a analizar
  year = ask_year('\nIntroduzca el año a analizar (2014-2017): ')  

  # Cargar el repositorio de estaciones y de viajes del año seleccionado
  print('\nAnalizando datos..........')
  stations = StationsYearRepo(year)
  trips = TripsYearRepo(year)

  # Histograma de tiempos de viaje para el año dado
  print('\nHistograma de tiempos de viaje generado en la carpeta imagenes')
  trips.duration_hist()
  
  # Listado del Top N de estaciones más utilizadas
  N = ask_N('\nListado de las Top N estaciones. Introduzca N (1-100): ')

  # Por estación de salida
  print(f'\nListado de las {N} primeras estaciones por estación de salida')
  print(trips.topN_start_stations(N, stations))
  pause('Pulse ENTER para continuar')

  # Por estación de llegada
  print(f'\nListado de las {N} primeras estaciones por estación de llegada')
  print(trips.topN_end_stations(N, stations))
  pause('Pulse ENTER para continuar')

  # Por estación de salida y llegada
  print(f'\nListado de las {N} primeras estaciones por estación de salida y llegada')
  print(trips.topN_start_end_stations(N, stations))
  pause('Pulse ENTER para continuar')

  # Por viaje
  print(f'\nListado de las {N} primeras estaciones por viaje')
  print(trips.topN_trips(N, stations))
  pause('Pulse ENTER para continuar')

  # Identificación de horas punta para un año determinado sin tener en cuenta el día
  print("\nGenerado el histograma de horas punta en la carpeta de imagenes")
  print(f'Se observa que las {trips.rush_hour_hist()} horas es la hora con mayor número de viajes')

  # Comparación de utilización del sistema entre dos años cualesquiera
  year2 = ask_year('\nIntroduzca un segundo año diferente al primero para comparar (2014-2017): ', year)

  # Cargar el repositorio de estaciones y de viajes del año seleccionado
  trips2 = TripsYearRepo(year2)

  # Cantidad de viajes totales
  print('\nViajes totales')
  print(f'Año {year}: {trips.total_trips():,} viajes')
  print(f'Año {year2}: {trips2.total_trips():,} viajes')

  # Tiempo total de utilización del sistema
  print('\nTiempo total de utilización del sistema')
  print(f'Año {year}: {trips.total_time():,} minutos')
  print(f'Año {year2}: {trips2.total_time():,} minutos')

  # Capacidad instalada total
  status = StationsStatus()
  print('\nCapacidad instalada total')
  print(f'Hay {status.available_terminals()} terminales disponibles')
  print(f'Hay {status.available_bikes()} bicicletas disponibles')

  # Capacidad por año
  print('\nCapacidad por año')
  print(f'\nAño {year}:')
  terminals, bikes = status.available_terminals_bikes(stations)
  print(f'Hay {terminals} terminales disponibles')
  print(f'Hay {bikes} bicicletas disponibles')

  # Comparativa con el otro año
  print('\nCapacidad por año')
  print(f'\nAño {year2}:')
  stations2 = StationsYearRepo(year2)
  terminals, bikes = status.available_terminals_bikes(stations2)
  print(f'Hay {terminals} terminales disponibles')
  print(f'Hay {bikes} bicicletas disponibles')


if __name__ == '__main__':
    main()