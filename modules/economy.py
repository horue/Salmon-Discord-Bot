import json
import requests
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context
from discord import Interaction

async def create_wallet(server_id, bank, wallet, id):
    request = requests.post(f'{firebase}/Servidores/{server_id}.json', json={'ID': id,'Wallet': wallet, 'Bank': bank})
    print(request)
    print(request.text)


async def add_money(server_id, user_id, amount):
    request = requests.get(f'{firebase}/Servidores/{server_id}.json')
    print(request)
    found = False
    dic_request = request.json()
    for user_id_i in dic_request:
        user = dic_request[user_id_i]['ID']
        if user == user_id:
            current_wallet = dic_request[user_id_i]['Wallet']
            new_wallet = current_wallet + amount
            url = f'{firebase}/Servidores/{server_id}/{user_id_i}.json'
            response = requests.patch(url, json={"Wallet": new_wallet})
            if response.status_code == 200:
                print(f'User: {user}, Wallet: {new_wallet}, Bank: {dic_request[user_id_i]["Bank"]}')
            else:
                print('Erro ao atualizar a carteira.')
            found = True
            break
    if not found:
        print('No wallet found for this user.')


async def check_money(ctx, server_id, user_id):
    request = requests.get(f'{firebase}/Servidores/{server_id}.json')
    print(request)
    dic_request = request.json()
    if dic_request is None:
        await ctx.send("No data found for this server.")
        await create_wallet(server_id=server_id, bank=0, wallet=0, id=user_id)
        await ctx.send('New wallet created.')
        return
    found = False
    for user_id_i in dic_request:
        user = dic_request[user_id_i]['ID']
        if user == user_id:
            wallet = dic_request[user_id_i]['Wallet']
            bank = dic_request[user_id_i]['Bank']
            await ctx.send((f'User: <@{user}>\nWallet: {wallet}\nBank: {bank}'))
            found = True
            break
    if not found:
        await ctx.send('No wallet found for this user.')
        await create_wallet(server_id=server_id, bank=0, wallet=0, id=user_id)
        await ctx.send('New wallet created.')



if __name__ == '__main__':
    asyncio.run(add_money(123,999,4500))
    asyncio.run(check_money(123, 456))
    asyncio.run(check_money(123, 789))