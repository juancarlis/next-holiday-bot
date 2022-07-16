from datetime import datetime, date

import pandas as pd
import requests


def main():

    fecha = date.today()

    df = _extract(year=fecha.year)
    df = _transform(df=df, fecha=fecha)

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


def _transform(df: pd.DataFrame, fecha: date) -> pd.DataFrame:
    """Removes unwanted holidays from original dataframe by
    filtering off Judaism and Musulman holidays from the dataframe
    and by droping oldest dates than the given one at [fecha]. 
    """
    df = df.loc[(df['religion'] != 'judaísmo') & (df['religion'] != 'musulman'), :]

    fecha = datetime(fecha.year, fecha.month, fecha.day)
    df = df.loc[df['fecha'] >= fecha, :].reset_index()

    return df
    

if __name__ == '__main__':
    main()
