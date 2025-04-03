import random
import asyncio
import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
import wikipedia
from deep_translator import GoogleTranslator
import praw
import mysql.connector
import string
import random




#BASE DE DONNÉS
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Connexion à la base de données MySQL
db = mysql.connector.connect(
    host="localhost",     # Remplace par l'hôte de ton serveur MySQL
    user="root",          # Remplace par ton utilisateur MySQL
    password="",          # Remplace par ton mot de passe MySQL
    database="discord_bot"  # Base de données créée précédemment
)

cursor = db.cursor()

def get_xp(user_id):
    """Récupère l'XP d'un utilisateur dans la base de données."""
    cursor.execute("SELECT xp FROM user_xp WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0

def add_xp(user_id, amount):
    """Ajoute de l'XP à un utilisateur."""
    current_xp = get_xp(user_id)
    new_xp = current_xp + amount

    cursor.execute("INSERT INTO user_xp (user_id, xp) VALUES (%s, %s) ON DUPLICATE KEY UPDATE xp = %s",
                   (user_id, new_xp, new_xp))
    db.commit()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------









# Charger les variables d'environnement depuis un fichier .env
load_dotenv()  # Charge les variables d'environnement depuis le fichier .env (par exemple, un jeton d'API)
TOKEN = os.getenv("DISCORD_TOKEN")  # Récupère le jeton du bot depuis les variables d'environnement



# Définition des intents (permissions avancées du bot)
intents = discord.Intents.default()  # Crée un objet d'intents avec les valeurs par défaut
intents.members = True  # Permet au bot de gérer les membres, comme ajouter ou retirer des rôles
intents.messages = True  # Permet au bot d'accéder aux messages envoyés sur le serveur
intents.guilds = True  # Permet au bot de gérer les rôles, salons, et autres aspects du serveur
intents.reactions = True  # Permet au bot d'interagir avec les réactions sur les messages
intents.message_content = True  # Permet au bot d'accéder au contenu des messages

# Création du bot avec un préfixe de commande "!"
bot = commands.Bot(command_prefix="!", intents=intents)  # Crée un bot avec le préfixe "!" et les intents définis

# Dictionnaire pour activer/désactiver certaines fonctionnalités
enabled_features = {
    "wiki": False,  # Fonctionnalité Wikipedia désactivée par défaut
    "translate": False,  # Fonctionnalité de traduction désactivée par défaut
    "meme": False,  # Fonctionnalité des mèmes désactivée par défaut
    "xp": False,  # Fonctionnalité XP désactivée par défaut
    "economy": False,  # Fonctionnalité économique désactivée par défaut
    "ai": False,  # Fonctionnalité IA désactivée par défaut
    "meme":False, # Fonctionnalité MEME désactivée par défaut
    "eightball":True,
    "duel":True,
    "leaderboard":True
}








#ACTIVER ET DESACTIVER UNE OPTION
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Commande pour activer une fonctionnalité spécifique
@bot.command()
@commands.has_permissions(administrator=True)  # Cette commande peut uniquement être utilisée par un administrateur
async def enable(ctx, feature: str):
    """Active une fonctionnalité optionnelle du bot."""
    if feature in enabled_features:  # Vérifie si la fonctionnalité existe dans le dictionnaire
        enabled_features[feature] = True  # Active la fonctionnalité en modifiant sa valeur à True
        await ctx.send(f"La fonctionnalité {feature} a été activée.")  # Envoie un message de confirmation
    else:
        await ctx.send("Fonctionnalité inconnue.")  # Envoie un message si la fonctionnalité est inconnue

# Commande pour désactiver une fonctionnalité spécifique
@bot.command()
@commands.has_permissions(administrator=True)  # Cette commande peut uniquement être utilisée par un administrateur
async def disable(ctx, feature: str):
    """Désactive une fonctionnalité optionnelle du bot."""
    if feature in enabled_features:  # Vérifie si la fonctionnalité existe dans le dictionnaire
        enabled_features[feature] = False  # Désactive la fonctionnalité en modifiant sa valeur à False
        await ctx.send(f"La fonctionnalité {feature} a été désactivée.")  # Envoie un message de confirmation
    else:
        await ctx.send("Fonctionnalité inconnue.")  # Envoie un message si la fonctionnalité est inconnue

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





#ROLE ET ATTRIBUTION
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def autorole(ctx, role1: discord.Role, role2: discord.Role, role3: discord.Role):
    """Définit les rôles automatiques attribués aux nouveaux membres."""

    global auto_roles
    auto_roles = [role1.id, role2.id, role3.id]  # Stocke les IDs des rôles

    await ctx.send(f"✅ Les rôles attribués aux nouveaux membres seront : {role1.name}, {role2.name}, {role3.name}")



captcha_data = {}

@bot.command()
async def captcha(ctx, member: discord.Member):
    """Envoie un code captcha à vérifier."""
    captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    captcha_data[member.id] = captcha_code

    await member.send(f"🛑 Vérification de sécurité ! Tape `{captcha_code}` dans `!verify [code]` pour être accepté.")

@bot.command()
async def verify(ctx, code: str):
    """Vérifie si l'utilisateur a bien saisi son captcha."""
    if ctx.author.id in captcha_data and captcha_data[ctx.author.id] == code:
        del captcha_data[ctx.author.id]
        await ctx.author.send("✅ Vérification réussie ! Bienvenue sur le serveur.")
    else:
        await ctx.author.send("❌ Code incorrect. Essaye encore.")

@bot.event
async def on_member_join(member):
    """Attribue automatiquement les rôles définis aux nouveaux membres."""
    try:
        if auto_roles:
            for role_id in auto_roles:
                role = member.guild.get_role(role_id)
                if role:
                    await member.add_roles(role)
            await member.guild.system_channel.send(f"👋 Bienvenue {member.mention} ! Tes rôles ont été attribués.")
    except Exception as e:
        print(f"Erreur lors de l'attribution automatique des rôles : {e}")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------








# Commande !wiki pour rechercher un terme sur Wikipédia
@bot.command()
async def wiki(ctx, *, search: str):
    """Recherche un terme sur Wikipédia et renvoie un résumé de la page."""
    if enabled_features["wiki"]:  # Vérifie si la fonctionnalité "wiki" est activée
        try:
            summary = wikipedia.summary(search, sentences=2)  # Cherche un résumé sur Wikipédia du terme donné
            await ctx.send(f"**{search}** : {summary}")  # Envoie le résumé au canal
        except wikipedia.exceptions.DisambiguationError as e:  # Si plusieurs pages correspondent, attrape l'erreur
            await ctx.send(f"Plusieurs résultats trouvés : {', '.join(e.options[:5])}")  # Envoie les 5 premiers résultats
        except wikipedia.exceptions.PageError:  # Si aucune page n'a été trouvée
            await ctx.send("Aucune page trouvée.")  # Envoie un message indiquant qu'aucune page n'a été trouvée
    else:
        await ctx.send("La fonctionnalité `wiki` est désactivée.")  # Si la fonctionnalité wiki est désactivée, informe l'utilisateur

# Commande !translate pour traduire du texte


@bot.command()
async def translate(ctx, lang: str = None, *, text: str = None):
    """Traduire un texte dans la langue spécifiée avec Deep Translator."""

    if not enabled_features["translate"]:
        await ctx.send("❌ La fonctionnalité `translate` est désactivée.")
        return

    if lang is None or text is None:
        await ctx.send("❌ Utilisation correcte : `!translate [langue] [texte]`\nExemple : `!translate en Bonjour tout le monde`")
        return

    try:
        translation = GoogleTranslator(source="auto", target=lang).translate(text)
        await ctx.send(f"🌍 **Traduction en `{lang}` :**\n{translation}")

    except Exception as e:
        await ctx.send(f"❌ Erreur lors de la traduction : {str(e)}")


# Commande de bannissement d'un utilisateur
@bot.command()
@commands.has_permissions(ban_members=True)  # Cette commande peut uniquement être utilisée par ceux ayant la permission de bannir
async def ban(ctx, member: discord.Member, *, reason=None):
    """Bannir un utilisateur du serveur avec une raison optionnelle."""
    await member.ban(reason=reason)  # Bannir l'utilisateur spécifié avec une raison (si fournie)
    await ctx.send(f"{member.mention} a été banni. Raison: {reason}")  # Informe le serveur que l'utilisateur a été banni

# Commande d'expulsion d'un utilisateur
@bot.command()
@commands.has_permissions(kick_members=True)  # Cette commande peut uniquement être utilisée par ceux ayant la permission d'expulser
async def kick(ctx, member: discord.Member, *, reason=None):
    """Expulser un utilisateur du serveur avec une raison optionnelle."""
    await member.kick(reason=reason)  # Expulse l'utilisateur spécifié avec une raison (si fournie)
    await ctx.send(f"{member.mention} a été expulsé. Raison: {reason}")  # Informe le serveur que l'utilisateur a été expulsé

# Commande pour rendre un utilisateur muet temporairement
@bot.command()
@commands.has_permissions(manage_roles=True)  # Cette commande peut uniquement être utilisée par ceux ayant la permission de gérer les rôles
async def mute(ctx, member: discord.Member, time: int):
    """Rendre un utilisateur muet pour un certain temps en minutes."""
    role = discord.utils.get(ctx.guild.roles, name="Muted")  # Cherche le rôle "Muted" dans le serveur
    if not role:  # Si le rôle "Muted" n'existe pas
        role = await ctx.guild.create_role(name="Muted")  # Crée un rôle "Muted"
        for channel in ctx.guild.channels:  # Parcourt tous les salons du serveur
            await channel.set_permissions(role, send_messages=False)  # Empêche ce rôle d'envoyer des messages
    await member.add_roles(role)  # Ajoute le rôle "Muted" à l'utilisateur
    await ctx.send(f"{member.mention} a été muté pour {time} secondes.")  # Informe que l'utilisateur a été muté
    await asyncio.sleep(time)  # Attend le nombre de secondes spécifié
    await member.remove_roles(role)  # Retire le rôle "Muted" après le temps écoulé
    await ctx.send(f"{member.mention} n'est plus muté.")  # Informe que l'utilisateur n'est plus muté

# Commande pour activer le mode lent sur un salon
@bot.command()
@commands.has_permissions(manage_channels=True)  # Cette commande peut uniquement être utilisée par ceux ayant la permission de gérer les salons
async def slowmode(ctx, seconds: int):
    """Active le mode lent sur le canal."""
    await ctx.channel.edit(slowmode_delay=seconds)  # Modifie les paramètres du salon pour ajouter un délai entre les messages
    await ctx.send(f"Mode lent activé : {seconds} secondes par message.")  # Informe l'utilisateur que le mode lent a été activé

# Commande pour gérer les logs modérateurs
@bot.command()
@commands.has_permissions(administrator=True)  # Cette commande peut uniquement être utilisée par un administrateur
async def logs(ctx):
    """Crée ou récupère un canal de logs."""
    log_channel = discord.utils.get(ctx.guild.text_channels, name="logs")  # Cherche un salon nommé "logs"
    if not log_channel:  # Si le canal n'existe pas
        log_channel = await ctx.guild.create_text_channel("logs")  # Crée un canal "logs"
    await ctx.send(f"Les logs seront enregistrés dans {log_channel.mention}")  # Informe l'utilisateur du canal de logs

# Événement : Attribution automatique d'un rôle à un nouveau membre
@bot.event
async def on_member_join(member):
    """Attribution automatique d'un rôle à un nouveau membre."""
    role = discord.utils.get(member.guild.roles, name="Membre")  # Cherche le rôle "Membre"
    if role:  # Si le rôle existe
        await member.add_roles(role)  # Attribue le rôle "Membre" au nouvel utilisateur
        await member.guild.system_channel.send(f"Bienvenue {member.mention} ! Vous avez reçu le rôle {role.name}.")  # Envoie un message de bienvenue

# Événement : Suivi des changements de pseudo et d'avatars
@bot.event
async def on_member_update(before, after):
    """Surveille les changements de pseudo et d'avatar d'un membre."""
    log_channel = discord.utils.get(before.guild.text_channels, name="logs")  # Récupère le canal "logs"
    if before.nick != after.nick:  # Si le pseudo de l'utilisateur a changé
        await log_channel.send(f"{before.mention} a changé son pseudo de {before.nick} à {after.nick}.")  # Envoie un message dans les logs
    if before.avatar != after.avatar:  # Si l'avatar de l'utilisateur a changé
        await log_channel.send(f"{before.mention} a changé son avatar.")  # Envoie un message dans les logs
# Commande !balance pour voir les crédits virtuels
@bot.command()
async def balance(ctx):
    """Affiche la balance de crédits virtuels d'un utilisateur."""
    if enabled_features["economy"]:
        await ctx.send(f"{ctx.author.mention}, vous avez 500 crédits !")  # À intégrer avec une base de données
    else:
        await ctx.send("La fonctionnalité `economy` est désactivée.")

# Commande !duel pour affronter un autre joueur
@bot.command()
async def duel(ctx, member: discord.Member):
    """Permet de lancer un duel contre un autre utilisateur."""
    if enabled_features["economy"]:
        winner = random.choice([ctx.author, member])
        await ctx.send(f"🎭 {ctx.author.mention} affronte {member.mention}... et le gagnant est {winner.mention} !")
    else:
        await ctx.send("La fonctionnalité `economy` est désactivée.")

# Commande !config pour personnaliser les paramètres du bot
@bot.command()
@commands.has_permissions(administrator=True)
async def config(ctx, setting: str, value: str):
    """Modifie une configuration avancée du bot."""
    await ctx.send(f"Configuration `{setting}` mise à jour avec la valeur `{value}`")

# Commande !poll pour créer un sondage
@bot.command()
async def poll(ctx, question: str, *options):
    """Crée un sondage avec plusieurs options de vote."""
    if len(options) < 2:
        await ctx.send("Vous devez fournir au moins deux options.")
        return
    poll_embed = discord.Embed(title=question, description="\n".join([f"{i+1}\ufe0f⃣ {option}" for i, option in enumerate(options)]), color=discord.Color.blue())
    message = await ctx.send(embed=poll_embed)
    reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    for i in range(len(options)):
        await message.add_reaction(reactions[i])

# Commande !event pour organiser un événement
@bot.command()
async def event(ctx, name: str, date: str):
    """Crée un événement avec un nom et une date spécifiée."""
    event_embed = discord.Embed(title=f"📅 Événement: {name}", description=f"Date et heure : {date}", color=discord.Color.green())
    await ctx.send(embed=event_embed)

# Commande !8ball pour une réponse aléatoire
# Commande !8ball pour une réponse aléatoire
@bot.command()
async def eightball(ctx, *, question: str):
    """Fournit une réponse aléatoire à une question posée."""
    responses = ["Oui", "Non", "Peut-être", "Je ne sais pas", "Absolument"]
    await ctx.send(f"🎱 {random.choice(responses)}")

# Commande !xp pour voir son niveau
@bot.command()
async def xp(ctx):
    """Affiche l'XP actuel d'un utilisateur depuis la base de données."""
    user_xp = get_xp(ctx.author.id)
    await ctx.send(f"{ctx.author.mention}, tu as actuellement **{user_xp} XP** !")



# Commande !warn pour avertir un utilisateur
@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    """Avertit un utilisateur et enregistre la raison."""
    await ctx.send(f"{member.mention} a été averti pour : {reason}")

@bot.command()
async def leaderboard(ctx):
    """Affiche le classement des membres par XP."""
    cursor.execute("SELECT user_id, xp FROM user_xp ORDER BY xp DESC LIMIT 10")
    results = cursor.fetchall()

    if not results:
        await ctx.send("Aucun XP enregistré pour le moment.")
        return

    leaderboard_msg = "**🏆 Classement des joueurs :**\n"
    for i, (user_id, xp_amount) in enumerate(results, start=1):
        user = await bot.fetch_user(int(user_id))
        leaderboard_msg += f"{i}. {user.name} - {xp_amount} XP\n"

    await ctx.send(leaderboard_msg)

@bot.event
async def on_message(message):
    """Ajoute de l'XP à un utilisateur lorsqu'il envoie un message."""
    if message.author.bot:
        return  # Ignore les bots

    add_xp(message.author.id, random.randint(5, 15))  # Ajoute entre 5 et 15 XP aléatoirement
    await bot.process_commands(message)



# Chargement des identifiants Reddit depuis .env
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

@bot.command()
async def meme(ctx):
    """Envoie un mème aléatoire depuis Reddit."""
    if not enabled_features["meme"]:
        await ctx.send("❌ La fonctionnalité `meme` est désactivée.")
        return

    try:
        subreddit = reddit.subreddit("memes")  # Choix du subreddit
        memes = list(subreddit.hot(limit=50))  # Récupère les 50 mèmes les plus populaires
        random_meme = random.choice(memes)  # Sélectionne un mème aléatoire

        # Vérifie si le post contient bien une image
        if random_meme.url.endswith((".jpg", ".png", ".jpeg")):
            embed = discord.Embed(title=random_meme.title, color=discord.Color.blue(), url=random_meme.url)
            embed.set_image(url=random_meme.url)
            embed.set_footer(text=f"👍 {random_meme.score} | 💬 {random_meme.num_comments} commentaires")
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Aucun mème image trouvé, réessaie !")

    except Exception as e:
        await ctx.send(f"❌ Erreur lors de la récupération du mème : {str(e)}")

print("Commandes disponibles :", [command.name for command in bot.commands])
# Lancement du bot
bot.run(TOKEN)  # Lance le bot avec le jeton d'authentification
