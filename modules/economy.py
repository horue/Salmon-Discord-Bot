import json
import requests
import asyncio
from firebase import link as firebase

async def create_wallet(server_id, bank, wallet, id):
    request = requests.post(f'{firebase}/Servidores/{server_id}.json', json={'ID': id,'Wallet': wallet, 'Bank': bank})
    print(request)
    print(request.text)

async def check_money(server_id, user_id):
    request = requests.get(f'{firebase}/Servidores/{server_id}.json')
    print(request)
    dic_request = request.json()
    for user_id_i in dic_request:
        user = dic_request[user_id_i]['ID']
        if user == user_id:
            wallet = dic_request[user_id_i]['Wallet']
            bank = dic_request[user_id_i]['Bank']
            print(f'User: {user}, Wallet: {wallet}, Bank: {bank}')
        else:
            print('No wallet found for this user.')


if __name__ == '__main__':
    #asyncio.run(create_wallet(123, 10, 10, 999))
    asyncio.run(check_money(123, 999))
    asyncio.run(check_money(123, 789))