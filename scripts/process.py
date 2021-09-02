
from threading import Event
from brownie import chain, Contract, convert, network
from brownie.network.event import EventLookupError
from brownie.network.web3 import _resolve_address
from ..my_details import handle, my_addresses, skip_confirm, reimbursement_address
from pprint import pprint
import os, csv, requests, pandas, click
from datetime import datetime


def read_checkpoint(address):
    try:
        with open(f'checkpoints/{address}.csv','r') as checkpoints:
            rows = csv.reader(checkpoints)
            #rows = rows
            for row in rows:
                startBlock = int(row[0]) + 1
        print(f"last checkpoint at block {startBlock}")
        return startBlock
    except FileNotFoundError:
        print('no checkpoint found, starting from block 0')
        return 0

def checkpoint(address, block):
    with open(f'checkpoints/{address}.csv','w') as checkpoints:
        writer = csv.writer(checkpoints)
        writer.writerow((str(block),None))
    print(f"checkpoint for {address} set to block {block}")

def fetch_txs(address, startBlock):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock={startBlock}&sort=asc&apikey={os.environ['ETHERSCAN_TOKEN']}"
    response = requests.get(url).json()['result']
    for item in response:
        item['tx_type'] = 'transaction'
        item['from'] = convert.to_address(item['from'])
    df = pandas.DataFrame(response)
    if(len(df)) > 0:
        df = df.drop(columns=['input','cumulativeGasUsed','confirmations'])
        print(df.columns)
        return df[df['from'] == address]
    return df

def fetch_internal_txs(address, startBlock):
    url = f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={address}&startblock={startBlock}&sort=asc&apikey={os.environ['ETHERSCAN_TOKEN']}"
    response = requests.get(url).json()['result']
    for item in response:
        item['tx_type'] = 'internal'
        item['from'] = convert.to_address(item['from'])
    df = pandas.DataFrame(response)
    # NOTE We don't want to count gas here, just value moved
    try:
        df = df[df['isError'] == 0]
        df = df.drop(columns=['gasUsed','gasPrice'],errors='ignore')
    except KeyError:
        pass
    if(len(df)) > 0:
        return df[df['from'] == address]
    print(df.columns)
    return df


def Spender(event):
    try:
        return Contract(event['_spender'])
    except EventLookupError:
        try:
            return Contract(event['spender'])
        except EventLookupError:
            return Contract(event['guy'])

def ValueToken(event,token):
    try:
        return event['amount'] / 10 ** token.decimals()
    except EventLookupError:
        try:
            return event['value'] / 10 ** token.decimals()
        except EventLookupError:
            try:
                return event['_value'] / 10 ** token.decimals()
            except:
                return event['wad'] / 10 ** token.decimals()

def Recipient(event):
    print(event)
    try:
        return Contract(event['dst'])
    except ValueError:
        return event['dst']
    except EventLookupError:
        try:
            return Contract(event['to'])
        except ValueError:
            return event['to']
        except EventLookupError:
            try:
                return Contract(event['receiver'])
            except ValueError:
                return event['receiver']


def fetch_filtered_txs_list():
    addresses = [_resolve_address(address) for address in my_addresses]
    df = None
    for address in addresses:
        print(address)
        startBlock = read_checkpoint(address)
        txs = fetch_txs(address, startBlock)

        # NOTE: We may decide we want this later but for now we do not
        #internal_txs = fetch_internal_txs(address, startBlock)
        #all = txs.append(internal_txs)
        all = txs

        all['weiSpentOnGas'] = all['gasUsed'].apply(int) * all['gasPrice'].apply(int)
        all['weiSpentOnGas'] = all['weiSpentOnGas'].apply(int)
        
        df = all if df is None else df.append(all)
        counter = len(df)
        if not skip_confirm:
            for i, row in df.iterrows():
                hash = row['hash']
                receipt = chain.get_transaction(hash)
                fn_name = receipt.fn_name
                print(' ')
                print(f"tx: https://etherscan.io/tx/{hash}")
                print(f"timestamp: {datetime.utcfromtimestamp(int(row['timeStamp']))} UTC")

                # NOTE: we do this so we know for sure brownie will find the events we're looking for
                eventcontractgetter = [Contract(address) for address in set(event.address for event in receipt.events)]

                if fn_name == 'approve':
                    event = receipt.events['Approval'][0]
                    token = Contract(event.address)
                    symbol = token.symbol()
                    spender = Spender(event)
                    value = ValueToken(event,token)
                    print(f"approved {value} {symbol} to {spender.__dict__['_build']['contractName']} {spender}")
                elif fn_name == 'transfer':
                    event = receipt.events['Transfer'][0]
                    token = Contract(event.address)
                    symbol = token.symbol()
                    recip = Recipient(event)
                    value = ValueToken(event,token)
                    try:
                        print(f"transfered {value} {symbol} to {recip.__dict__['_build']['contractName']} {recip}")
                    except KeyError:
                        print(f"transfered {value} {symbol} to {recip}")
                elif fn_name is None:
                    to = row['to']
                    try:
                        to = Contract(to)
                        print(f"sent {int(row['value']) / 10 ** 18} ETH to: {to.__dict__['_build']['contractName']} {to}")
                    except AttributeError:
                        print(f"sent {int(row['value']) / 10 ** 18} ETH to: {to}")
                elif row['contractAddress']:
                    deployed = Contract(row['contractAddress'])
                    print(f"deployed contract {deployed.__dict__['_build']['contractName']} {deployed}")
                else:
                    print(f"called function: {fn_name}")
                    try:
                        to = Contract(row['to'])
                        print(f"on contract: {to.__dict__['_build']['contractName']} {to}")
                    except (UnboundLocalError, ValueError):
                        to = row['to']
                        print(f"on: {to}")
                print(f"gas used: {row['weiSpentOnGas']} wei")
                print(' ')
                keep = click.confirm('Should this tx be reimbursed?')
                if not keep:
                    df.drop(i)
                counter -= 1
                print(f"{counter} remaining")
        if len(df) > 0:
            endBlock = all['blockNumber'].max()
            all.loc['Total', 'weiSpentOnGas']= all['weiSpentOnGas'].sum()
            checkpoint(address,endBlock)
        else:
            print('no new reimbursement txs for this address')
    return df

def main():
    df = fetch_filtered_txs_list()
    #df = df.drop(['isError','cumulativeGasUsed','confirmations'],errors='ignore')
    print(df.columns)
    df.to_csv(f'pending/{reimbursement_address} - {handle}.csv', index=False)
    print('export successful!')
    print('please make a PR to submit your reimbursements to the DAO')