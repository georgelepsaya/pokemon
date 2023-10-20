import pandas as pd
import numpy as np
import requests
from io import StringIO


def extract_data(url) -> pd.DataFrame:
    response = requests.get(url, verify=False)
    data = response.content
    decoded_data = StringIO(data.decode('utf-8'))

    pokemon = pd.read_csv(decoded_data, usecols=range(22))

    # Clean up the data
    for i in range(1041, 1045):
        pokemon.iloc[i] = pokemon.iloc[i].tolist()[:5] + [np.nan] + pokemon.iloc[i].tolist()[5:7] + [np.nan, np.nan] + [float(x) for x in pokemon.iloc[i].tolist()[7:-3]]
    for i in range(1045, 1048):
        pokemon.iloc[i] = pokemon.iloc[i].tolist()[:8] + [np.nan, np.nan] + [float(x) for x in pokemon.iloc[i].tolist()[8:-2]]

    return pokemon
