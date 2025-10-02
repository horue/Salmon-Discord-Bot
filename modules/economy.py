import json
import requests
import asyncio
import discord
from modules.firebase import link
from discord.ext import commands
from discord import app_commands
from discord import Interaction

firebase = link

async def create_wallet(server_id, bank, wallet, id):
    id = int(id)
    check_request = requests.get(f'{firebase}/Servidores/{server_id}.json')
    existing_data = check_request.json() or {}
    for key in existing_data:
        if existing_data[key]['ID'] == id:
            print("User already has a wallet. Skipping creation.")
            return
    request = requests.post(
        f'{firebase}/Servidores/{server_id}.json',
        json={'ID': id, 'Wallet': wallet, 'Bank': bank}
    )
    print(request)
    print(request.text)

async def add_money(ctx, server_id, user_id, amount):
    user_id = int(user_id)
    request = requests.get(f'{firebase}/Servidores/{server_id}.json')
    print(request)
    found = False
    dic_request = request.json() or {}
    for user_key in dic_request:
        user_data = dic_request[user_key]
        if user_data['ID'] == user_id:
            current_wallet = user_data['Wallet']
            new_wallet = current_wallet + amount
            url = f'{firebase}/Servidores/{server_id}/{user_key}.json'
            response = requests.patch(url, json={"Wallet": new_wallet})
            if response.status_code == 200:
                await ctx.send(f'User: <@{user_id}>\nWallet: {new_wallet}\nBank: {user_data["Bank"]}')
            else:
                print('Erro ao atualizar a carteira.')
            found = True
            break
    if not found:
        print('No wallet found for this user.')
        await create_wallet(server_id, bank=0, wallet=amount, id=user_id)
        await ctx.send(f'New wallet created for <@{user_id}> with {amount} coins.')

async def check_money(ctx, server_id, user_id):
    user_id = int(user_id)
    request = requests.get(f'{firebase}/Servidores/{server_id}.json')
    print(request)
    dic_request = request.json() or {}
    if not dic_request:
        await ctx.send("No data found for this server.")
        await create_wallet(server_id=server_id, bank=0, wallet=0, id=user_id)
        await ctx.send('New wallet created.')
        return
    found = False
    for user_key in dic_request:
        user_data = dic_request[user_key]
        if user_data['ID'] == user_id:
            wallet = user_data['Wallet']
            bank = user_data['Bank']
            await ctx.send(f'User: <@{user_id}>\nWallet: {wallet}\nBank: {bank}')
            found = True
            break
    if not found:
        await ctx.send('No wallet found for this user.')
        await create_wallet(server_id=server_id, bank=0, wallet=0, id=user_id)
        await ctx.send('New wallet created.')

if __name__ == '__main__':
    asyncio.run(add_money(123, 999, 4500))
    asyncio.run(check_money(123, 456))
    asyncio.run(check_money(123, 789))