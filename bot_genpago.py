import discord
from discord import app_commands
from discord.ext import commands
import random
import json
import os

# Configurações do Bot
TOKEN = 'SEU_TOKEN_AQUI'
INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(command_prefix='!', intents=INTENTS)

# Dicionário para simular o banco de dados de contas
# Na prática, você usaria um banco de dados como SQLite, MySQL ou MongoDB
accounts_db = {
    'Netflix': ['netflix_user1:pass1', 'netflix_user2:pass2', 'netflix_user3:pass3'],
    'Steam (Busca por Jogo)': ['steam_user1:pass1', 'steam_user2:pass2'],
    'HboMax': ['hbo_user1:pass1', 'hbo_user2:pass2'],
    'PrimeVideo': ['prime_user1:pass1', 'prime_user2:pass2'],
    'Crunchyroll': ['crunchy_user1:pass1', 'crunchy_user2:pass2'],
    'Deezer': ['deezer_user1:pass1', 'deezer_user2:pass2'],
    'Lol': ['lol_user1:pass1', 'lol_user2:pass2'],
    'Paramount': ['paramount_user1:pass1', 'paramount_user2:pass2'],
    'Riotgames': ['riot_user1:pass1', 'riot_user2:pass2'],
    'Steam': ['steam_full_user1:pass1', 'steam_full_user2:pass2'],
    'Valorant': ['valorant_user1:pass1', 'valorant_user2:pass2']
}

# Função para carregar as contas de um arquivo JSON (opcional, para persistência)
def load_accounts(filename='contas.json'):
    global accounts_db
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            accounts_db = json.load(f)

# Função para salvar as contas em um arquivo JSON
def save_accounts(filename='contas.json'):
    with open(filename, 'w') as f:
        json.dump(accounts_db, f, indent=4)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    # Sincronizar comandos de barra (/)
    try:
        synced = await bot.tree.sync()
        print(f'Sincronizados {len(synced)} comando(s)')
    except Exception as e:
        print(e)

# Comando principal para gerar contas
@bot.tree.command(name='gerar', description='Gera uma conta premium')
@app_commands.describe(categoria='A categoria do serviço desejado')
@app_commands.choices(categoria=[
    app_commands.Choice(name='Netflix', value='Netflix'),
    app_commands.Choice(name='Steam (Busca por Jogo)', value='Steam (Busca por Jogo)'),
    app_commands.Choice(name='HboMax', value='HboMax'),
    app_commands.Choice(name='PrimeVideo', value='PrimeVideo'),
    app_commands.Choice(name='Crunchyroll', value='Crunchyroll'),
    app_commands.Choice(name='Deezer', value='Deezer'),
    app_commands.Choice(name='Lol', value='Lol'),
    app_commands.Choice(name='Paramount', value='Paramount'),
    app_commands.Choice(name='Riotgames', value='Riotgames'),
    app_commands.Choice(name='Steam', value='Steam'),
    app_commands.Choice(name='Valorant', value='Valorant')
])
async def gerar_conta(interaction: discord.Interaction, categoria: app_commands.Choice[str]):
    # Verificar se o usuário está verificado (simulação)
    # Na prática, você verificaria um banco de dados de usuários autorizados
    if not hasattr(interaction.user, 'verificado') or not interaction.user.verificado:
        await interaction.response.send_message("Você precisa se verificar primeiro usando o comando `/verificar`.", ephemeral=True)
        return

    # Pegar as contas da categoria escolhida
    if categoria.value not in accounts_db or not accounts_db[categoria.value]:
        await interaction.response.send_message(f"Estoque de {categoria.value} esgotado! Tente novamente mais tarde.", ephemeral=True)
        return

    # Retirar uma conta aleatória do estoque
    conta_gerada = random.choice(accounts_db[categoria.value])
    accounts_db[categoria.value].remove(conta_gerada)
    
    # Salvar o novo estoque
    save_accounts()

    # Criar o embed de resposta
    embed = discord.Embed(
        title=f"🎉 Conta {categoria.value} Gerada!",
        description="Aqui estão os seus dados de acesso:",
        color=discord.Color.blue()
    )
    embed.add_field(name="Categoria", value=categoria.value, inline=True)
    embed.add_field(name="Usuário:Senha", value=f"||{conta_gerada}||", inline=False)
    embed.set_footer(text="Lembre-se de não compartilhar suas contas!")
    
    # Enviar a resposta no canal privado do usuário (DM)
    try:
        await interaction.user.send(embed=embed)
        await interaction.response.send_message("Sua conta foi enviada no privado! (DM)", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("Erro: Você tem as DMs fechadas. Não foi possível enviar a conta.", ephemeral=True)

# Comando de verificação
@bot.tree.command(name='verificar', description='Verifica seu usuário no sistema')
async def verificar_usuario(interaction: discord.Interaction):
    # Simulação de verificação
    # Na prática, você salvaria o ID do usuário em um banco de dados
    embed = discord.Embed(
        title="✅ Usuário Verificado",
        description="Seu usuário foi verificado com sucesso no sistema! Agora você pode usar o comando `/gerar`.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run(TOKEN)
