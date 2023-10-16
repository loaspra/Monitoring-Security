import sys
import pandas as pd
import numpy as np
import random as rd
import os
import requests
import json

class JmilesBot:
    def __init__(self):
        self.APP_URL = os.getenv('APP_URL')
        self.POKEAPI_PORT = os.getenv('POKEAPI_PORT')
        self.POKESTATS_PORT = os.getenv('POKESTATS_PORT')
        self.df = pd.read_csv('history.csv')
        
    def CheckLatency(self, module, range):
        df = self.df[self.df['module'] == module]
        df = df.tail(range)
        return df[['fecha','latency']].reset_index(drop=True)

    def CheckAvailability(self, module, range):
        df = self.df[self.df['module'] == module]
        df = df.tail(range)
        return df[['fecha','availability']].reset_index(drop=True)

    def RenderGraph(self, module, type, range):        
        df = self.df[self.df['module'] == module]

        d_max = 10/df[type].max()
        size_max = df[type].apply(lambda  x: len(str(x))).max()
        rows = df[type].apply(lambda x: int(x * d_max)).tolist()

        data = df[type].tolist()

        data1 =  data.pop(0)
        size1 = rows.pop(0)

        s_data1 = str(data1)
        dates = df['fecha'].tolist()
        date = dates.pop(0)

        s_fecha1 = f"{date.split('-')[-1]}/{date.split('-')[-2]}"

        width = size_max + 4

        height_max = np.max(rows)

        arr1 = np.array(['*']).repeat(width).reshape(width, 1).repeat(size1, axis = 1)

        for i in range(len(s_data1)):
            arr1[2 + i, -1] = s_data1[i]

            
        arr1_p = np.pad(arr1, ((1, 2), (2, (height_max + 2) - arr1.shape[1] + 2)), 'constant', constant_values=' ')

        for i in range(len(s_fecha1)):
            arr1_p[2 + i, 0] = s_fecha1[i]

        # the rest concat
        for i in range(len(data)):
            dataX =  data[i]
            sizeX = rows[i]

            s_dataX = str(dataX)
            date = dates[i]

            s_fechaX = f"{date.split('-')[-1]}/{date.split('-')[-2]}"

            arr2 = np.array(['*']).repeat(width).reshape(width, 1).repeat(sizeX, axis = 1)

            for i in range(len(s_dataX)):
                arr2[2 + i, -1] = s_dataX[i]

            arr2_p = np.pad(arr2, ((1, 2), (2, (height_max + 2) - arr2.shape[1] + 2)), 'constant', constant_values=' ')

            for i in range(len(s_fechaX)):
                arr2_p[2 + i, 0] = s_fechaX[i]

            arr1_p = np.concatenate((arr1_p, arr2_p))


        final = arr1_p.T

        for i in range(final.shape[0] - 1, -1, -1):
            for j in range(final.shape[1]):
                print(final[i, j], end = '')
            print("")



    def GetPokemon(self):
        response = requests.get(self.APP_URL + ':' + self.POKEAPI_PORT + '/pokemon')
        return response.json()

    def GetPokemonStats(self, pokemon):
        response = requests.get(self.APP_URL + ':' + self.POKESTATS_PORT + '/pokemon/' + pokemon)
        return response.json()

    def GetPokemonImage(self, pokemon):
        response = requests.get(self.APP_URL + ':' + self.POKEAPI_PORT + '/pokemon/' + pokemon + '/image')
        return response.json()


# Main
def get_range(raw_range):
    raw = raw_range.lower()
    if raw.find("Last"): # Last10days
        return int(raw[4:-4])
    
    else: # -01/10 -05/10 (from 1st to 5th) 
        return int(raw[1:3]) - int(raw[7:9])

if __name__ == '__main__':

    bot = JmilesBot()
    
    # Usage of the script: python bot.py <function> <module> <args>
    # Get the function
    function = sys.argv[1]

    pokemon = 'Pikachu'

    function = function.lower()

    if function == 'checklatency':
        module = sys.argv[2].lower()
        range = get_range(sys.argv[3])
        print(bot.CheckLatency(module, range))

    elif function == 'checkavailability':
        module = sys.argv[2].lower()
        range = get_range(sys.argv[3])
        print(bot.CheckAvailability(module, range))

    elif function == 'rendergraph':
        module = sys.argv[2].lower()
        type = sys.argv[3].lower()
        # range = get_range(sys.argv[4])
        print(bot.RenderGraph(module, type, range))

    else:
        raise NotImplementedError('Function not implemented')
