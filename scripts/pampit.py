import json, os, requests
import pandas as pd
from ..team_details import DEFAULT_COMMENT, HANDLE_TO_COMMENT

def main():
    files = [file for file in os.listdir('./pending') if file != 'EVERYBODY.csv']
    all = []
    for filename in files:
        handle = filename[:-4]
        filepath = f"./pending/{filename}"
        df = pd.read_csv(filepath)
        df['weiSpentOnGas'] = df.gasUsed * df.gasPrice

        totalWei = sum(df['weiSpentOnGas'])
        totalEth = totalWei / 10 ** 18
        totalNonGas = sum(df['value'])
        print(totalWei)
        print(totalEth)
        print(totalNonGas)
        #totalWei += totalNonGas
        #totalEth += totalNonGas / 10 ** 18
        print(df)
        try:
            comment = HANDLE_TO_COMMENT[handle]
        except KeyError:
            comment = DEFAULT_COMMENT
        with open(filepath,'r') as file:
            filecontents = file.read()
        print(filecontents)
        auth_token = f"token {os.environ['GH_PERSONAL_AUTH_TOKEN']}"
        print(auth_token)
        data = {
            filename: {
                'content': filecontents
            }
        }
        headers = {
            'Authoriation': auth_token
        }
        params={'scope':'gist'}
        response = requests.post('https://api.github.com/gists',headers=headers,params=params,data=data).json()
        print(response)
        details = {
            'id': None,
            'address': None,
            'name': handle,
            'eth': totalEth,
            'raw': totalWei,
            'tx': 'pending',
            'link': None,
            'comment': comment
        }
        all.append(details)
        
    df = pd.DataFrame(all)
    df.to_csv('pending/EVERYBODY.csv')
    print(df)