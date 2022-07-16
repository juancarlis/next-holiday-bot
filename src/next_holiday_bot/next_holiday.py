import requests
from datetime import datetime

import pandas as pd


def main():

    fecha = datetime.now()

    df = _extract(fecha.year)
    print(df)


def _extract(year: int) -> pd.DataFrame:
    """Extracts the argentinian holidays data from 
    https://pjnovas.gitbooks.io/no-laborables/content/feriados.html API's
    """
    API = f'http://nolaborables.com.ar/api/v2/feriados/{str(year)}?incluir=opcional'

    r = requests.get(API)
    
    if r.status_code == 200:
        df = pd.DataFrame.from_dict(r.json())
        df['fecha'] = df['dia'].map(str)+'/'+df['mes'].map(str)+'/'+str(year)
        df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y')
        return df
    else:
        print('API Error')
        return 1


if __name__ == '__main__':
    main()
