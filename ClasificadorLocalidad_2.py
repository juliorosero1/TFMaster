


diccionario={ "Argentina":['argentina', 'buenos aires', 'mar del plata', 'buenos aire', 'rio cuarto', 'río cuarto'],
              "Bolivia":['bolivia', 'sucre'],
              "Chile":["chile", 'viña del mar', 'valparaíso', 'valparaiso'],
              "Colombia":["colombia", "bogota", 'bogotá', 'barranquilla', 'medellin', 'medellín', 'cartagena', 'antioquia'],
              "Costa Rica":["costa rica", 'san josé', 'san jose'],
              'Ecuador': ['ecuador', 'quito', 'guayaquil', 'manta', 'santo domingo', 'cuenca', 'los ríos', 'los rios', 'manta', 'babahoyo','tulcán', 'tulcan'],
              'El Salvador':['el salvador', 'san salvador'],
              'Guatemala':['guatemala'],
              'Honduras': ['honduras', 'tegucigalpa'],
              'Mexico':['mexico', 'méxico', 'guadalajara', 'yucatan', 'yucatán', 'monterrey', 'chihuahua', 'oaxaca', 'cdmx', 'acapulco', 'guanajuato', 'santa fe', 'culiacan', 'culiacán'],
              'Nicaragua':['nicaragua', 'managua'],
              'Panama':['panama', 'panamá'],
              'Uruguay':['uruguay', 'montevideo'],
              'Peru':['peru', 'perú', 'lima'],
              'Paraguay':['paraguay', 'asuncion','asunción'],
              'Venezuela':['venezuela', 'caracas', 'maracaibo', 'la guaira', 'vzla'],
              'España':['españa', 'spain', 'madrid', 'barcelona', 'murcia', 'canarias', 'mallorca', 'andalucía', 'andalucia', 'valencia', 'catalunya', 'toluca', 'zaragoza', 'sevilla', 'valladolid'],
              'EEUU':['eeuu', 'usa', 'miami', 'estados unidos', 'washington', 'california','united states', 'new york', 'los angeles', 'orlando', 'seattle', 'puerto rico', 'tucson','brooklyn', 'ny', 'jupiter'],
              'Cuba':['cuba'],
              'Republica Dominicana':['republica dominicana', 'república dominicana', 'dominican republic']
            }


def clasificarPais(texto):
    paisC=""
    encontrado=False
    indice=-1
    #Busca si existen campos vacíos y de ser así asigna NA
    if texto!="NA":
        for clave in diccionario:
            for lugar in diccionario[clave]:
                if texto.lower().find(lugar)>=0:
                    paisC= clave

    else:
        paisC=None
    return paisC
