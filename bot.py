from ntpath import join
from re import M
from sqlite3 import Timestamp
import discord
from discord.ext import commands
import datetime
import time
import os

#Start----------------------------------------------------------------------------------------

intents = discord.Intents.default()
intents.members=True

client = commands.Bot(command_prefix = '+', intents = intents)

@client.event
async def on_ready():
    print('Le bot est opérationnel !')

#Bienvenue------------------------------------------------------------------------------------

@client.event
async def on_member_join(member):
    embed = discord.Embed(title=f"Bienvenue {member.name}!", description=f"Merci d'avoir rejoint le serveur {member.guild.name}! \nN'oublie pas de lire le règlement <a:pikawink:978770606667468850>", color = 0xFFFFFF, timestamp = datetime.datetime.utcnow())
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_image(url = 'https://c.tenor.com/VkScszX7f3YAAAAC/discord-banner.gif')
    await client.get_channel(978956333145534495).send(embed=embed)

#Modération-----------------------------------------------------------------------------------

@client.command()
@commands.has_role('ADMINISTRATEUR')
async def ban(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason = reason)
    embed = discord.Embed(
        title = "**BAN**",
        description = f"L'utilisateur {user.mention} a été banni avec succès \n**Raison :** {reason}",
        color = 0x000000
    )
    embed.set_thumbnail(url = user.avatar_url)
    msg = await ctx.send(embed = embed)

@client.command()
@commands.has_role('ADMINISTRATEUR')
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user, reason = reason)
            embed = discord.Embed(
                title = "**UNBAN**",
                description = f"L'utilisateur {user} a été unban avec succès !",
                color = 0x000000
            )
            msg = await ctx.send(embed = embed)
            return
    
    embed = discord.Embed(
                title = "**ERREUR**",
                description = f"L'utilisateur {user} n'est pas banni !",
                color = 0x000000
            )
    msg = await ctx.send(embed = embed)

@client.command()
@commands.has_role('ADMINISTRATEUR')
async def kick(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason = reason)
    embed = discord.Embed(
        title = "**KICK**",
        description = f"{user.mention} a été kick avec succès ! \n**Raison :** {reason}",
        color = 0x000000
    )
    embed.set_thumbnail(url = user.avatar_url)
    msg = await ctx.send(embed = embed)

@client.command()
@commands.has_role('MODERATEUR')
async def clear(ctx, nombre : int):
    messages = await ctx.channel.history(limit = nombre + 1).flatten()
    for message in messages:
        await message.delete()
    embed = discord.Embed(
        title = "**CLEAR**",
        description = f"{nombre} messages ont été supprimés avec succès !",
        color = 0x000000
    )
    msg = await ctx.send(embed = embed)

#Reaction Role--------------------------------------------------------------------------------

@client.command(pass_context = True)
async def verification(ctx):
    embed = discord.Embed(
        title = "Bienvenue sur le serveur !",
        description = "Pour accéder à la totalité du serveur, veuillez cliquer sur l'emoji ci-dessous.",
        color = 0xf772b5
    )
    embed.set_image(url="https://i.pinimg.com/originals/36/d5/fd/36d5fd4baf95540b2ba2b633c49b1713.jpg")
    msg = await ctx.send(embed = embed)

    await msg.add_reaction('pinkcrown:978996817935085568')

#Règles---------------------------------------------------------------------------------------

@client.command()
@commands.has_role('ADMINISTRATEUR')
async def regles(ctx):
    embed = discord.Embed(
        title = "**Règlement !**",
        description = "**1. Être respectueux**\nVous devez respecter tous les utilisateurs, quel que soit votre goût envers eux. Traitez les autres comme vous aimeriez être traité.\n\n**2. Pas de langage inapproprié**\nL\'utilisation de blasphèmes doit être réduite au minimum. Cependant, tout langage désobligeant envers tout utilisateur est interdit.\n\n**3. Pas de spam**\nN\'envoyez pas beaucoup de petits messages les uns après les autres. Ne perturbez pas le chat en spammant.\n\n**4. Pas de matériel pornographique/adulte/autre NSFW**\nCeci est un serveur communautaire et n\'est pas destiné à partager ce type de matériel.\n\n**5. Pas de publicité**\nNous ne tolérons aucun type de publicité, que ce soit pour d\'autres communautés ou flux. Vous pouvez publier votre contenu dans le canal média s'il est pertinent et apporte une valeur réelle (Vidéo/Art)\n\n**6. Pas de noms ni de photos de profil offensants**\nIl vous sera demandé de changer votre nom ou votre photo si le personnel les juge inappropriés.\n\n**7. Raid de serveur**\nLes raids ou les mentions de raids ne sont pas autorisés.\n\n**8. Menaces directes et indirectes**\nLes menaces envers d\'autres utilisateurs de DDoS, Death, DoX, abus et autres menaces malveillantes sont absolument interdites et interdites.\n\n**9. Suivez les directives de la communauté Discord **\nVous pouvez les trouver ici : https://discordapp.com/guidelines\n\n**Si vous vous sentez maltraité, contactez un administrateur et nous résoudrons le problème.**\n\n**Votre présence sur ce serveur implique l\'acceptation de ces règles, y compris toutes les modifications ultérieures. Ces changements peuvent être effectués à tout moment sans préavis, il est de votre responsabilité de les vérifier.**",
        color = 0x000000
    )
    msg = await ctx.send(embed = embed)

#Ticket---------------------------------------------------------------------------------------

@client.listen()
async def on_raw_reaction_add(payload):
    message_id1 = 978997148089729037
    if message_id1 == payload.message_id:
        members = payload.member
        guild = members.guild

        emoji = payload.emoji.name
        if emoji == 'pinkcrown':
            roles = discord.utils.get(guild.roles, name = "MEMBRE")
            await members.add_roles(roles)

@client.listen()
async def on_raw_reaction_add(payload):
    message_id2 = 979081127983726673

    if message_id2 == payload.message_id:
        members = payload.member
        guild = members.guild
        emoji = payload.emoji.name
        if emoji == 'handboost':
            channel = await guild.create_text_channel(f'support {payload.member}')
            channel_id = channel.id
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = client.get_user(payload.user_id)
            emoji = client.get_emoji(978770606839463977)
            await message.remove_reaction(emoji, user)
            await guild.get_channel(channel_id).set_permissions(guild.default_role, view_channel=False)
            await guild.get_channel(channel_id).set_permissions(guild.get_role(978960990051909662), view_channel = False)
            await guild.get_channel(channel_id).set_permissions(user, view_channel = True, send_messages = True)
            embed = discord.Embed(
                title = "**TICKET**",
                description = f"{user.mention} vient d'ouvrir un ticket. Veuillez patienter le temps qu'un modérateur / administrateur vous réponde. \n**Merci de votre patience.** \n \nPour fermer le ticket, veuillez cliquer sur l'emoji ci-dessous.",
                color = 0xFFFFFF
            )
            
            msg = await guild.get_channel(channel_id).send(embed = embed)
            await msg.add_reaction('no:979127700360949770')
            msg_id = msg.id
            @client.listen()
            async def on_raw_reaction_add(payload):
                if payload.member.id == 978399610781466654:
                    return
                else:
                     if msg_id == payload.message_id:
                        members = payload.member
                        guild = members.guild
                        emoji = payload.emoji.name
                        if emoji == 'no':
                            channel = client.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)
                            user = client.get_user(payload.user_id)
                            emoji = client.get_emoji(979127700360949770)
                            await message.remove_reaction(emoji, user)

                            embed = discord.Embed(
                                title = "**FERMETURE**",
                                description = f"{user.mention}, votre ticket va se supprimer automatiquement dans 5 secondes !",
                                color = 0xFFFFFF
                            )
                            await guild.get_channel(channel_id).send(embed = embed)
                            time.sleep(5)

                            await guild.get_channel(channel_id).delete()

@client.listen()
async def on_raw_reaction_add(payload):
    message_id3 = 979361602820247612
    if message_id3 == payload.message_id:
        members = payload.member
        guild = members.guild
        emoji = payload.emoji.name
        if emoji == 'diamond1':
            channel = await guild.create_text_channel(f'achat {payload.member}')
            channel_id = channel.id
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = client.get_user(payload.user_id)
            emoji = client.get_emoji(978770605438541845)
            await message.remove_reaction(emoji, user)
            await guild.get_channel(channel_id).set_permissions(guild.default_role, view_channel=False)
            await guild.get_channel(channel_id).set_permissions(guild.get_role(978960990051909662), view_channel = False)
            await guild.get_channel(channel_id).set_permissions(user, view_channel = True, send_messages = True)
            await guild.get_channel(channel_id).send(f"{user.mention}")
            embed = discord.Embed(
                title = "**ACHAT**",
                description = f"{user.mention} merci d'avoir ouvert un ticket.\nPour choisir votre produit, veuillez réagir sous ce message à l'aide d'un emoji. \n \nPour fermer le ticket, veuillez cliquer sur l'emoji <a:no:979127700360949770>",
                color = 0xFFFFFF
            )
            
            msg = await guild.get_channel(channel_id).send(embed = embed)
            msg2 = await guild.get_channel(channel_id).send("**<a:nitroclassic:978770606717796372> Nitro Classic <a:pinkarrow:979497113908047922> 3€ **\n**<a:nitroboost:978770605832814592> Nitro Boost <a:pinkarrow:979497113908047922> 6€ **\n**<a:handboost:978770606839463977> Nitro Boost 3 mois (+) <a:pinkarrow:979497113908047922> 3€**\n\n**<a:nitrogem:978770605631496222> 2 Boosts (3 mois) <a:pinkarrow:979497113908047922> 3€ **\n**<a:nitrofly:978770606713610280> Technique Nitros Boosts 3 mois illimités (+) <a:pinkarrow:979497113908047922> 6€ **\n\n**<a:pepemoney:980149383788101673> Technique 1-3€/jour (++) <a:pinkarrow:979497113908047922> 5€ **\n**<a:animateddollar:980149427530506300> Technique 2-5€/mois (+++) <a:pinkarrow:979497113908047922> 0,5€ **\n**<a:moneyfly:980149466088751114> Technique 5€/jour (++++) <a:pinkarrow:979497113908047922> 10€ **\n\n**<a:bitcoin:980149507180347462> Crypto wallet sans vérification d'identité <a:pinkarrow:979497113908047922> 1€ **\n**<a:creditcard:980149547282104432> Carte bancaire (pour vérifier PayPal... etc) <a:pinkarrow:979497113908047922> 1€ **\n**<a:badges:978770605128167524> Numéros virtuels illimités <a:pinkarrow:979497113908047922> 1€ **\n**<a:eye:979128740892246016> Technique faux documents d'identité illimités <a:pinkarrow:979497113908047922> 1€**")
            await msg.add_reaction('nitroclassic:978770606717796372')
            await msg.add_reaction('nitroboost:978770605832814592')
            await msg.add_reaction('handboost:978770606839463977')
            await msg.add_reaction('nitrogem:978770605631496222')
            await msg.add_reaction('nitrofly:978770606713610280')
            await msg.add_reaction('pepemoney:980149383788101673')
            await msg.add_reaction('animateddollar:980149427530506300')
            await msg.add_reaction('moneyfly:980149466088751114')
            await msg.add_reaction('bitcoin:980149507180347462')
            await msg.add_reaction('creditcard:980149547282104432')
            await msg.add_reaction('badges:978770605128167524')
            await msg.add_reaction('eye:979128740892246016')
            await msg.add_reaction('no:979127700360949770')

            msg_id = msg.id
            @client.listen()
            async def on_raw_reaction_add(payload):
                if payload.member.id == 978399610781466654:
                    return
                else:
                    ######
                    montant1 = "3"
                    montant2 = "6"
                    montant3 = "3"
                    montant4 = "3"
                    montant5 = "6"
                    montant6 = "5"
                    montant7 = "0,5"
                    montant8 = "10"
                    montant9 =  "1"

                    paypal_link = "https://paypal.me/far3000yt (en amis proches, sinon pas de remboursement en cas de problème !)"
                    usdt_adress = "``0xa42134b4b1a4ae27fc60174f66b428b456c7509a`` (Arbitrum One / BSC / BEP20 / ERC20 / MATIC) ou ``1EYaCok2AQXStr1bFcMgHdAVBVDiFYRBEn`` (OMNI) ou ``4qgCL37jQUJLqTgvL7vq6Hd1Z3gU5RLqgMAshPy1DQQp`` (SOL) ou ``TG31aT7jHbXng3avwnhHNh2ZVX7n29uLwW`` (TRC20)"
                    btc_adress = "``17rx1Y3Xgfd7td3R9y8FdhJebVHVGjP4xw``"
                    eth_adress = "``0xa42134b4b1a4ae27fc60174f66b428b456c7509a`` (Arbitrum One / BCP / BEP20 / ERC / OPTIMISM seulement)"
                    ltc_adress = "``LYAqCBkCrxtU9UcU3aZihK9CePCAYtjWN2``"
                    bnb_adress = "``0xa42134b4b1a4ae27fc60174f66b428b456c7509a`` (BSC / BEP20 seulement)"
                    ######

                    if msg_id == payload.message_id:
                        members = payload.member
                        guild = members.guild
                        emoji = payload.emoji.name
                        if emoji == 'no':
                            channel = client.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)
                            user = client.get_user(payload.user_id)
                            emoji = client.get_emoji(979127700360949770)
                            await message.remove_reaction(emoji, user)

                            embed = discord.Embed(
                                title = "**FERMETURE**",
                                description = f"{user.mention}, votre ticket va se supprimer automatiquement dans 5 secondes !",
                                color = 0xFFFFFF
                            )
                            await guild.get_channel(channel_id).send(embed = embed)
                            time.sleep(5)

                            await guild.get_channel(channel_id).delete()

                        elif emoji == 'nitroclassic':
                            channel = client.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)
                            user = client.get_user(payload.user_id)
                            emoji = client.get_emoji(978770606717796372)
                            await message.remove_reaction(emoji, user)
                            await msg2.delete()
                            embed = discord.Embed(
                                title = "**PAIEMENT**",
                                description = f"{user.mention}, vous avez choisi d'acheter un Nitro Classic <a:pikawink:978770606667468850>\nVeuillez choisir votre moyen de paiement :\n<:paypal:979360481666031666> PayPal (paiement en amis proches)\n<:usdt:978993142915293214> United States Dollar Tether (USDT)\n<:btc:978993142915285022> Bitcoin (BTC)\n<:eth:978993142860754994> Ethereum (ETH)\n<:ltc:978993142877548565> Litecoin (LTC)\n<:bnb:978993142902689822> Binance Coin (BNB)",
                                color = 0xFFFFFF
                            )
                            msg3 = await guild.get_channel(channel_id).send(embed = embed)
                            await msg3.add_reaction('paypal:979360481666031666')
                            await msg3.add_reaction('usdt:978993142915293214')
                            await msg3.add_reaction('btc:978993142915285022')
                            await msg3.add_reaction('eth:978993142860754994')
                            await msg3.add_reaction('ltc:978993142877548565')
                            await msg3.add_reaction('bnb:978993142902689822')

                            msg3_id = msg3.id

                            @client.listen()
                            async def on_raw_reaction_add(payload):
                                if payload.member.id == 978399610781466654:
                                    return
                                else:
                                    if msg3_id == payload.message_id:
                                        members = payload.member
                                        guild = members.guild
                                        emoji = payload.emoji.name
                                        if emoji == 'paypal':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(979360481666031666)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement paypal ! Veuillez envoyer {montant1}€ grâce au lien suivant : {paypal_link}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'usdt':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915293214)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'USDT ! Veuillez envoyer {montant1}€ à l'adresse USDT suivante : {usdt_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'btc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915285022)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BTC ! Veuillez envoyer {montant1}€ à l'adresse BTC suivante : {btc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'eth':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142860754994)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'ETH ! Veuillez envoyer {montant1}€ à l'adresse ETH suivante : {eth_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'ltc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142877548565)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le LTC ! Veuillez envoyer {montant1}€ à l'adresse LTC suivante : {ltc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'bnb':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142902689822)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BNB ! Veuillez envoyer {montant1}€ à l'adresse BNB suivante : {bnb_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)

                        elif emoji == 'nitroboost':
                            channel = client.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)
                            user = client.get_user(payload.user_id)
                            emoji = client.get_emoji(978770605832814592)
                            await message.remove_reaction(emoji, user)
                            await msg2.delete()
                            embed = discord.Embed(
                                title = "**PAIEMENT**",
                                description = f"{user.mention}, vous avez choisi d'acheter un Nitro Boost <a:pikawink:978770606667468850>\nVeuillez choisir votre moyen de paiement :\n<:paypal:979360481666031666> PayPal (paiement en amis proches)\n<:usdt:978993142915293214> United States Dollar Tether (USDT)\n<:btc:978993142915285022> Bitcoin (BTC)\n<:eth:978993142860754994> Ethereum (ETH)\n<:ltc:978993142877548565> Litecoin (LTC)\n<:bnb:978993142902689822> Binance Coin (BNB)",
                                color = 0xFFFFFF
                            )
                            msg3 = await guild.get_channel(channel_id).send(embed = embed)
                            await msg3.add_reaction('paypal:979360481666031666')
                            await msg3.add_reaction('usdt:978993142915293214')
                            await msg3.add_reaction('btc:978993142915285022')
                            await msg3.add_reaction('eth:978993142860754994')
                            await msg3.add_reaction('ltc:978993142877548565')
                            await msg3.add_reaction('bnb:978993142902689822')
                            msg3_id = msg3.id

                            @client.listen()
                            async def on_raw_reaction_add(payload):
                                if payload.member.id == 978399610781466654:
                                    return
                                else:
                                    if msg3_id == payload.message_id:
                                        members = payload.member
                                        guild = members.guild
                                        emoji = payload.emoji.name
                                        if emoji == 'paypal':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(979360481666031666)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement paypal ! Veuillez envoyer {montant2}€ grâce au lien suivant : {paypal_link}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'usdt':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915293214)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'USDT ! Veuillez envoyer {montant2}€ à l'adresse USDT suivante : {usdt_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'btc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915285022)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BTC ! Veuillez envoyer {montant2}€ à l'adresse BTC suivante : {btc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'eth':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142860754994)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'ETH ! Veuillez envoyer {montant2}€ à l'adresse ETH suivante : {eth_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'ltc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142877548565)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le LTC ! Veuillez envoyer {montant2}€ à l'adresse LTC suivante : {ltc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'bnb':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142902689822)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BNB ! Veuillez envoyer {montant2}€ à l'adresse BNB suivante : {bnb_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)

                        elif emoji == 'handboost':
                            channel = client.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)
                            user = client.get_user(payload.user_id)
                            emoji = client.get_emoji(978770606839463977)
                            await message.remove_reaction(emoji, user)
                            await msg2.delete()
                            embed = discord.Embed(
                                title = "**PAIEMENT**",
                                description = f"{user.mention}, vous avez choisi d'acheter un Nitro Boost 3 mois (pour les nouveaux comptes seulement) <a:pikawink:978770606667468850>\nVeuillez choisir votre moyen de paiement :\n<:paypal:979360481666031666> PayPal (paiement en amis proches)\n<:usdt:978993142915293214> United States Dollar Tether (USDT)\n<:btc:978993142915285022> Bitcoin (BTC)\n<:eth:978993142860754994> Ethereum (ETH)\n<:ltc:978993142877548565> Litecoin (LTC)\n<:bnb:978993142902689822> Binance Coin (BNB)",
                                color = 0xFFFFFF
                            )
                            msg3 = await guild.get_channel(channel_id).send(embed = embed)
                            await msg3.add_reaction('paypal:979360481666031666')
                            await msg3.add_reaction('usdt:978993142915293214')
                            await msg3.add_reaction('btc:978993142915285022')
                            await msg3.add_reaction('eth:978993142860754994')
                            await msg3.add_reaction('ltc:978993142877548565')
                            await msg3.add_reaction('bnb:978993142902689822')
                            msg3_id = msg3.id

                            @client.listen()
                            async def on_raw_reaction_add(payload):
                                if payload.member.id == 978399610781466654:
                                    return
                                else:
                                    if msg3_id == payload.message_id:
                                        members = payload.member
                                        guild = members.guild
                                        emoji = payload.emoji.name
                                        if emoji == 'paypal':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(979360481666031666)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement paypal ! Veuillez envoyer {montant3}€ grâce au lien suivant : {paypal_link}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'usdt':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915293214)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'USDT ! Veuillez envoyer {montant3}€ à l'adresse USDT suivante : {usdt_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'btc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915285022)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BTC ! Veuillez envoyer {montant3}€ à l'adresse BTC suivante : {btc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'eth':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142860754994)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'ETH ! Veuillez envoyer {montant3}€ à l'adresse ETH suivante : {eth_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'ltc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142877548565)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le LTC ! Veuillez envoyer {montant3}€ à l'adresse LTC suivante : {ltc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'bnb':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142902689822)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BNB ! Veuillez envoyer {montant3}€ à l'adresse BNB suivante : {bnb_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)

                        elif emoji == 'nitrogem':
                            channel = client.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)
                            user = client.get_user(payload.user_id)
                            emoji = client.get_emoji(978770605631496222)
                            await message.remove_reaction(emoji, user)
                            await msg2.delete()
                            embed = discord.Embed(
                                title = "**PAIEMENT**",
                                description = f"{user.mention}, vous avez choisi d'acheter un 2 Boosts pour une durée de 3 mois <a:pikawink:978770606667468850>\nVeuillez choisir votre moyen de paiement :\n<:paypal:979360481666031666> PayPal (paiement en amis proches)\n<:usdt:978993142915293214> United States Dollar Tether (USDT)\n<:btc:978993142915285022> Bitcoin (BTC)\n<:eth:978993142860754994> Ethereum (ETH)\n<:ltc:978993142877548565> Litecoin (LTC)\n<:bnb:978993142902689822> Binance Coin (BNB)",
                                color = 0xFFFFFF
                            )
                            msg3 = await guild.get_channel(channel_id).send(embed = embed)
                            await msg3.add_reaction('paypal:979360481666031666')
                            await msg3.add_reaction('usdt:978993142915293214')
                            await msg3.add_reaction('btc:978993142915285022')
                            await msg3.add_reaction('eth:978993142860754994')
                            await msg3.add_reaction('ltc:978993142877548565')
                            await msg3.add_reaction('bnb:978993142902689822')
                            msg3_id = msg3.id

                            @client.listen()
                            async def on_raw_reaction_add(payload):
                                if payload.member.id == 978399610781466654:
                                    return
                                else:
                                    if msg3_id == payload.message_id:
                                        members = payload.member
                                        guild = members.guild
                                        emoji = payload.emoji.name
                                        if emoji == 'paypal':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(979360481666031666)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement paypal ! Veuillez envoyer {montant4}€ grâce au lien suivant : {paypal_link}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'usdt':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915293214)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'USDT ! Veuillez envoyer {montant4}€ à l'adresse USDT suivante : {usdt_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'btc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915285022)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BTC ! Veuillez envoyer {montant4}€ à l'adresse BTC suivante : {btc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'eth':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142860754994)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'ETH ! Veuillez envoyer {montant4}€ à l'adresse ETH suivante : {eth_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'ltc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142877548565)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le LTC ! Veuillez envoyer {montant4}€ à l'adresse LTC suivante : {ltc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'bnb':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142902689822)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BNB ! Veuillez envoyer {montant4}€ à l'adresse BNB suivante : {bnb_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)

                        elif emoji == 'nitrofly':
                            channel = client.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)
                            user = client.get_user(payload.user_id)
                            emoji = client.get_emoji(978770606713610280)
                            await message.remove_reaction(emoji, user)
                            await msg2.delete()
                            embed = discord.Embed(
                                title = "**PAIEMENT**",
                                description = f"{user.mention}, vous avez choisi d'acheter la technique Nitro Boost 3 mois illimités <a:pikawink:978770606667468850>\nVeuillez choisir votre moyen de paiement :\n<:paypal:979360481666031666> PayPal (paiement en amis proches)\n<:usdt:978993142915293214> United States Dollar Tether (USDT)\n<:btc:978993142915285022> Bitcoin (BTC)\n<:eth:978993142860754994> Ethereum (ETH)\n<:ltc:978993142877548565> Litecoin (LTC)\n<:bnb:978993142902689822> Binance Coin (BNB)",
                                color = 0xFFFFFF
                            )
                            msg3 = await guild.get_channel(channel_id).send(embed = embed)
                            await msg3.add_reaction('paypal:979360481666031666')
                            await msg3.add_reaction('usdt:978993142915293214')
                            await msg3.add_reaction('btc:978993142915285022')
                            await msg3.add_reaction('eth:978993142860754994')
                            await msg3.add_reaction('ltc:978993142877548565')
                            await msg3.add_reaction('bnb:978993142902689822')
                            msg3_id = msg3.id

                            @client.listen()
                            async def on_raw_reaction_add(payload):
                                if payload.member.id == 978399610781466654:
                                    return
                                else:
                                    if msg3_id == payload.message_id:
                                        members = payload.member
                                        guild = members.guild
                                        emoji = payload.emoji.name
                                        if emoji == 'paypal':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(979360481666031666)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement paypal ! Veuillez envoyer {montant5}€ grâce au lien suivant : {paypal_link}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'usdt':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915293214)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'USDT ! Veuillez envoyer {montant5}€ à l'adresse USDT suivante : {usdt_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'btc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915285022)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BTC ! Veuillez envoyer {montant5}€ à l'adresse BTC suivante : {btc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'eth':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142860754994)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'ETH ! Veuillez envoyer {montant5}€ à l'adresse ETH suivante : {eth_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'ltc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142877548565)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le LTC ! Veuillez envoyer {montant5}€ à l'adresse LTC suivante : {ltc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'bnb':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142902689822)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BNB ! Veuillez envoyer {montant5}€ à l'adresse BNB suivante : {bnb_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)

                        elif emoji == 'pepemoney':
                            channel = client.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)
                            user = client.get_user(payload.user_id)
                            emoji = client.get_emoji(980149383788101673)
                            await message.remove_reaction(emoji, user)
                            await msg2.delete()
                            embed = discord.Embed(
                                title = "**PAIEMENT**",
                                description = f"{user.mention}, vous avez choisi d'acheter la technique 1-3€/jour (passivement) <a:pikawink:978770606667468850>\nVeuillez choisir votre moyen de paiement :\n<:paypal:979360481666031666> PayPal (paiement en amis proches)\n<:usdt:978993142915293214> United States Dollar Tether (USDT)\n<:btc:978993142915285022> Bitcoin (BTC)\n<:eth:978993142860754994> Ethereum (ETH)\n<:ltc:978993142877548565> Litecoin (LTC)\n<:bnb:978993142902689822> Binance Coin (BNB)",
                                color = 0xFFFFFF
                            )
                            msg3 = await guild.get_channel(channel_id).send(embed = embed)
                            await msg3.add_reaction('paypal:979360481666031666')
                            await msg3.add_reaction('usdt:978993142915293214')
                            await msg3.add_reaction('btc:978993142915285022')
                            await msg3.add_reaction('eth:978993142860754994')
                            await msg3.add_reaction('ltc:978993142877548565')
                            await msg3.add_reaction('bnb:978993142902689822')
                            msg3_id = msg3.id

                            @client.listen()
                            async def on_raw_reaction_add(payload):
                                if payload.member.id == 978399610781466654:
                                    return
                                else:
                                    if msg3_id == payload.message_id:
                                        members = payload.member
                                        guild = members.guild
                                        emoji = payload.emoji.name
                                        if emoji == 'paypal':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(979360481666031666)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement paypal ! Veuillez envoyer {montant6}€ grâce au lien suivant : {paypal_link}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'usdt':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915293214)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'USDT ! Veuillez envoyer {montant6}€ à l'adresse USDT suivante : {usdt_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'btc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915285022)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BTC ! Veuillez envoyer {montant6}€ à l'adresse BTC suivante : {btc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'eth':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142860754994)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'ETH ! Veuillez envoyer {montant6}€ à l'adresse ETH suivante : {eth_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'ltc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142877548565)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le LTC ! Veuillez envoyer {montant6}€ à l'adresse LTC suivante : {ltc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'bnb':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142902689822)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BNB ! Veuillez envoyer {montant6}€ à l'adresse BNB suivante : {bnb_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)

                        elif emoji == 'animateddollar':
                            channel = client.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)
                            user = client.get_user(payload.user_id)
                            emoji = client.get_emoji(980149427530506300)
                            await message.remove_reaction(emoji, user)
                            await msg2.delete()
                            aembed = discord.Embed(
                                title = "**PAIEMENT**",
                                description = f"{user.mention}, vous avez choisi d'acheter la technique 2-5€/mois (passivment) <a:pikawink:978770606667468850>\nVeuillez choisir votre moyen de paiement :\n<:paypal:979360481666031666> PayPal (paiement en amis proches)\n<:usdt:978993142915293214> United States Dollar Tether (USDT)\n<:btc:978993142915285022> Bitcoin (BTC)\n<:eth:978993142860754994> Ethereum (ETH)\n<:ltc:978993142877548565> Litecoin (LTC)\n<:bnb:978993142902689822> Binance Coin (BNB)",
                                color = 0xFFFFFF
                            )
                            msg3 = await guild.get_channel(channel_id).send(embed = embed)
                            await msg3.add_reaction('paypal:979360481666031666')
                            await msg3.add_reaction('usdt:978993142915293214')
                            await msg3.add_reaction('btc:978993142915285022')
                            await msg3.add_reaction('eth:978993142860754994')
                            await msg3.add_reaction('ltc:978993142877548565')
                            await msg3.add_reaction('bnb:978993142902689822')
                            msg3_id = msg3.id

                            @client.listen()
                            async def on_raw_reaction_add(payload):
                                if payload.member.id == 978399610781466654:
                                    return
                                else:
                                    if msg3_id == payload.message_id:
                                        members = payload.member
                                        guild = members.guild
                                        emoji = payload.emoji.name
                                        if emoji == 'paypal':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(979360481666031666)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement paypal ! Veuillez envoyer {montant7}€ grâce au lien suivant : {paypal_link}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'usdt':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915293214)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'USDT ! Veuillez envoyer {montant7}€ à l'adresse USDT suivante : {usdt_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'btc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915285022)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BTC ! Veuillez envoyer {montant7}€ à l'adresse BTC suivante : {btc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'eth':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142860754994)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'ETH ! Veuillez envoyer {montant7}€ à l'adresse ETH suivante : {eth_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'ltc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142877548565)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le LTC ! Veuillez envoyer {montant7}€ à l'adresse LTC suivante : {ltc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'bnb':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142902689822)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BNB ! Veuillez envoyer {montant7}€ à l'adresse BNB suivante : {bnb_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)

                        elif emoji == 'moneyfly':
                            channel = client.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)
                            user = client.get_user(payload.user_id)
                            emoji = client.get_emoji(980149466088751114)
                            await message.remove_reaction(emoji, user)
                            await msg2.delete()
                            embed = discord.Embed(
                                title = "**PAIEMENT**",
                                description = f"{user.mention}, vous avez choisi d'acheter la technique 5€/jour (passivement, mais attention, la technique n'a pas été approuvée donc si elle ne fonctionne pas, vous aurez le droit à un remboursement) <a:pikawink:978770606667468850>\nVeuillez choisir votre moyen de paiement :\n<:paypal:979360481666031666> PayPal (paiement en amis proches)\n<:usdt:978993142915293214> United States Dollar Tether (USDT)\n<:btc:978993142915285022> Bitcoin (BTC)\n<:eth:978993142860754994> Ethereum (ETH)\n<:ltc:978993142877548565> Litecoin (LTC)\n<:bnb:978993142902689822> Binance Coin (BNB)",
                                color = 0xFFFFFF
                            )
                            msg3 = await guild.get_channel(channel_id).send(embed = embed)
                            await msg3.add_reaction('paypal:979360481666031666')
                            await msg3.add_reaction('usdt:978993142915293214')
                            await msg3.add_reaction('btc:978993142915285022')
                            await msg3.add_reaction('eth:978993142860754994')
                            await msg3.add_reaction('ltc:978993142877548565')
                            await msg3.add_reaction('bnb:978993142902689822')
                            msg3_id = msg3.id

                            @client.listen()
                            async def on_raw_reaction_add(payload):
                                if payload.member.id == 978399610781466654:
                                    return
                                else:
                                    if msg3_id == payload.message_id:
                                        members = payload.member
                                        guild = members.guild
                                        emoji = payload.emoji.name
                                        if emoji == 'paypal':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(979360481666031666)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement paypal ! Veuillez envoyer {montant8}€ grâce au lien suivant : {paypal_link}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'usdt':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915293214)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'USDT ! Veuillez envoyer {montant8}€ à l'adresse USDT suivante : {usdt_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'btc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915285022)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BTC ! Veuillez envoyer {montant8}€ à l'adresse BTC suivante : {btc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'eth':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142860754994)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'ETH ! Veuillez envoyer {montant8}€ à l'adresse ETH suivante : {eth_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'ltc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142877548565)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le LTC ! Veuillez envoyer {montant8}€ à l'adresse LTC suivante : {ltc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'bnb':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142902689822)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BNB ! Veuillez envoyer {montant8}€ à l'adresse BNB suivante : {bnb_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)

                        elif emoji == 'bitcoin':
                            channel = client.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)
                            user = client.get_user(payload.user_id)
                            emoji = client.get_emoji(980149507180347462)
                            await message.remove_reaction(emoji, user)
                            await msg2.delete()
                            embed = discord.Embed(
                                title = "**PAIEMENT**",
                                description = f"{user.mention}, vous avez choisi d'acheter la technique pour créer un wallet crypto sans vérification d'identité <a:pikawink:978770606667468850>\nVeuillez choisir votre moyen de paiement :\n<:paypal:979360481666031666> PayPal (paiement en amis proches)\n<:usdt:978993142915293214> United States Dollar Tether (USDT)\n<:btc:978993142915285022> Bitcoin (BTC)\n<:eth:978993142860754994> Ethereum (ETH)\n<:ltc:978993142877548565> Litecoin (LTC)\n<:bnb:978993142902689822> Binance Coin (BNB)",
                                color = 0xFFFFFF
                            )
                            msg3 = await guild.get_channel(channel_id).send(embed = embed)
                            await msg3.add_reaction('paypal:979360481666031666')
                            await msg3.add_reaction('usdt:978993142915293214')
                            await msg3.add_reaction('btc:978993142915285022')
                            await msg3.add_reaction('eth:978993142860754994')
                            await msg3.add_reaction('ltc:978993142877548565')
                            await msg3.add_reaction('bnb:978993142902689822')
                            msg3_id = msg3.id

                            @client.listen()
                            async def on_raw_reaction_add(payload):
                                if payload.member.id == 978399610781466654:
                                    return
                                else:
                                    if msg3_id == payload.message_id:
                                        members = payload.member
                                        guild = members.guild
                                        emoji = payload.emoji.name
                                        if emoji == 'paypal':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(979360481666031666)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement paypal ! Veuillez envoyer {montant9}€ grâce au lien suivant : {paypal_link}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'usdt':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915293214)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'USDT ! Veuillez envoyer {montant9}€ à l'adresse USDT suivante : {usdt_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'btc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915285022)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BTC ! Veuillez envoyer {montant9}€ à l'adresse BTC suivante : {btc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'eth':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142860754994)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'ETH ! Veuillez envoyer {montant9}€ à l'adresse ETH suivante : {eth_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'ltc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142877548565)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le LTC ! Veuillez envoyer {montant9}€ à l'adresse LTC suivante : {ltc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'bnb':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142902689822)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BNB ! Veuillez envoyer {montant9}€ à l'adresse BNB suivante : {bnb_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)

                        elif emoji == 'creditcard':
                            channel = client.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)
                            user = client.get_user(payload.user_id)
                            emoji = client.get_emoji(980149547282104432)
                            await message.remove_reaction(emoji, user)
                            await msg2.delete()
                            embed = discord.Embed(
                                title = "**PAIEMENT**",
                                description = f"{user.mention}, vous avez choisi d'acheter la technique permettant d'avoir une carte bancaire (pour vérifier votre compte paypal... etc) <a:pikawink:978770606667468850>\nVeuillez choisir votre moyen de paiement :\n<:paypal:979360481666031666> PayPal (paiement en amis proches)\n<:usdt:978993142915293214> United States Dollar Tether (USDT)\n<:btc:978993142915285022> Bitcoin (BTC)\n<:eth:978993142860754994> Ethereum (ETH)\n<:ltc:978993142877548565> Litecoin (LTC)\n<:bnb:978993142902689822> Binance Coin (BNB)",
                                color = 0xFFFFFF
                            )
                            msg3 = await guild.get_channel(channel_id).send(embed = embed)
                            await msg3.add_reaction('paypal:979360481666031666')
                            await msg3.add_reaction('usdt:978993142915293214')
                            await msg3.add_reaction('btc:978993142915285022')
                            await msg3.add_reaction('eth:978993142860754994')
                            await msg3.add_reaction('ltc:978993142877548565')
                            await msg3.add_reaction('bnb:978993142902689822')
                            msg3_id = msg3.id

                            @client.listen()
                            async def on_raw_reaction_add(payload):
                                if payload.member.id == 978399610781466654:
                                    return
                                else:
                                    if msg3_id == payload.message_id:
                                        members = payload.member
                                        guild = members.guild
                                        emoji = payload.emoji.name
                                        if emoji == 'paypal':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(979360481666031666)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement paypal ! Veuillez envoyer {montant9}€ grâce au lien suivant : {paypal_link}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'usdt':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915293214)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'USDT ! Veuillez envoyer {montant9}€ à l'adresse USDT suivante : {usdt_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'btc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915285022)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BTC ! Veuillez envoyer {montant9}€ à l'adresse BTC suivante : {btc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'eth':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142860754994)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'ETH ! Veuillez envoyer {montant9}€ à l'adresse ETH suivante : {eth_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'ltc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142877548565)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le LTC ! Veuillez envoyer {montant9}€ à l'adresse LTC suivante : {ltc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'bnb':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142902689822)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BNB ! Veuillez envoyer {montant9}€ à l'adresse BNB suivante : {bnb_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)

                        elif emoji == 'badges':
                            channel = client.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)
                            user = client.get_user(payload.user_id)
                            emoji = client.get_emoji(978770605128167524)
                            await message.remove_reaction(emoji, user)
                            await msg2.delete()
                            embed = discord.Embed(
                                title = "**PAIEMENT**",
                                description = f"{user.mention}, vous avez choisi d'acheter la technique permettant d'avoir des numéros de téléphones virtuels en illimité <a:pikawink:978770606667468850>\nVeuillez choisir votre moyen de paiement :\n<:paypal:979360481666031666> PayPal (paiement en amis proches)\n<:usdt:978993142915293214> United States Dollar Tether (USDT)\n<:btc:978993142915285022> Bitcoin (BTC)\n<:eth:978993142860754994> Ethereum (ETH)\n<:ltc:978993142877548565> Litecoin (LTC)\n<:bnb:978993142902689822> Binance Coin (BNB)",
                                color = 0xFFFFFF
                            )
                            msg3 = await guild.get_channel(channel_id).send(embed = embed)
                            await msg3.add_reaction('paypal:979360481666031666')
                            await msg3.add_reaction('usdt:978993142915293214')
                            await msg3.add_reaction('btc:978993142915285022')
                            await msg3.add_reaction('eth:978993142860754994')
                            await msg3.add_reaction('ltc:978993142877548565')
                            await msg3.add_reaction('bnb:978993142902689822')
                            msg3_id = msg3.id

                            @client.listen()
                            async def on_raw_reaction_add(payload):
                                if payload.member.id == 978399610781466654:
                                    return
                                else:
                                    if msg3_id == payload.message_id:
                                        members = payload.member
                                        guild = members.guild
                                        emoji = payload.emoji.name
                                        if emoji == 'paypal':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(979360481666031666)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement paypal ! Veuillez envoyer {montant9}€ grâce au lien suivant : {paypal_link}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'usdt':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915293214)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'USDT ! Veuillez envoyer {montant9}€ à l'adresse USDT suivante : {usdt_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'btc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915285022)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BTC ! Veuillez envoyer {montant9}€ à l'adresse BTC suivante : {btc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'eth':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142860754994)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'ETH ! Veuillez envoyer {montant9}€ à l'adresse ETH suivante : {eth_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'ltc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142877548565)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le LTC ! Veuillez envoyer {montant9}€ à l'adresse LTC suivante : {ltc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'bnb':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142902689822)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BNB ! Veuillez envoyer {montant9}€ à l'adresse BNB suivante : {bnb_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)

                        elif emoji == 'eye':
                            channel = client.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)
                            user = client.get_user(payload.user_id)
                            emoji = client.get_emoji(979128740892246016)
                            await message.remove_reaction(emoji, user)
                            await msg2.delete()
                            embed = discord.Embed(
                                title = "**PAIEMENT**",
                                description = f"{user.mention}, vous avez choisi d'acheter la technique permettant de créer des faux documents d'identité en illimité <a:pikawink:978770606667468850>\nVeuillez choisir votre moyen de paiement :\n<:paypal:979360481666031666> PayPal (paiement en amis proches)\n<:usdt:978993142915293214> United States Dollar Tether (USDT)\n<:btc:978993142915285022> Bitcoin (BTC)\n<:eth:978993142860754994> Ethereum (ETH)\n<:ltc:978993142877548565> Litecoin (LTC)\n<:bnb:978993142902689822> Binance Coin (BNB)",
                                color = 0xFFFFFF
                            )
                            msg3 = await guild.get_channel(channel_id).send(embed = embed)
                            await msg3.add_reaction('paypal:979360481666031666')
                            await msg3.add_reaction('usdt:978993142915293214')
                            await msg3.add_reaction('btc:978993142915285022')
                            await msg3.add_reaction('eth:978993142860754994')
                            await msg3.add_reaction('ltc:978993142877548565')
                            await msg3.add_reaction('bnb:978993142902689822')
                            msg3_id = msg3.id

                            @client.listen()
                            async def on_raw_reaction_add(payload):
                                if payload.member.id == 978399610781466654:
                                    return
                                else:
                                    if msg3_id == payload.message_id:
                                        members = payload.member
                                        guild = members.guild
                                        emoji = payload.emoji.name
                                        if emoji == 'paypal':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(979360481666031666)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement paypal ! Veuillez envoyer {montant9}€ grâce au lien suivant : {paypal_link}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'usdt':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915293214)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'USDT ! Veuillez envoyer {montant9}€ à l'adresse USDT suivante : {usdt_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'btc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142915285022)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BTC ! Veuillez envoyer {montant9}€ à l'adresse BTC suivante : {btc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'eth':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142860754994)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement l'ETH ! Veuillez envoyer {montant9}€ à l'adresse ETH suivante : {eth_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'ltc':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142877548565)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le LTC ! Veuillez envoyer {montant9}€ à l'adresse LTC suivante : {ltc_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)
                                        elif emoji == 'bnb':
                                            channel = client.get_channel(payload.channel_id)
                                            message = await channel.fetch_message(payload.message_id)
                                            user = client.get_user(payload.user_id)
                                            emoji = client.get_emoji(978993142902689822)
                                            await message.remove_reaction(emoji, user)
                                            await msg3.delete()
                                            embed = discord.Embed(
                                                title = "**PAIEMENT**",
                                                    description = f"{user.mention}, vous avez choisi comme moyen de paiement le BNB ! Veuillez envoyer {montant9}€ à l'adresse BNB suivante : {bnb_adress}",
                                                color = 0xFFFFFF
                                            )
                                            await guild.get_channel(channel_id).send(embed = embed)

@client.command()
@commands.has_role('ADMINISTRATEUR')
async def support(ctx):
    embed = discord.Embed(
        title = "**TICKET**",
        description = "Pour créer un ticket, veuillez appuyer sur le bouton ci-dessous. \nTout abus sera sanctionné.",
        color = 0xFFB6C1
    )
    msg = await ctx.send(embed = embed)
    await msg.add_reaction('handboost:978770606839463977')

@client.command()
@commands.has_role('ADMINISTRATEUR')
async def ticket(ctx):
    embed = discord.Embed(
        title = "**TICKET**",
        description = "<a:diamond2:978770605274959873> **Pour créer un ticket, veuillez appuyer sur le bouton ci-dessous.** \n\nVeuillez ouvrir un ticket seulement pour acheter un objet présent dans le shop ! \nMerci de votre compréhension. \nTout abus sera sanctionné. ",
        color = 0xFFFFFF
    )
    msg = await ctx.send(embed = embed)
    await msg.add_reaction('diamond1:978770605438541845')
    await ctx.send("**__Moyens de paiements acceptés :__** \n<:paypal:979360481666031666> PayPal \n<:usdt:978993142915293214> USDT \n<:btc:978993142915285022> BTC \n<:eth:978993142860754994> ETH \n<:ltc:978993142877548565> LTC \n<:bnb:978993142902689822> BNB")

@client.command()
@commands.has_role('ADMINISTRATEUR')
async def nuke(ctx):
    channel2 = await ctx.channel.clone()
    embed = discord.Embed(
        title = "**NUKE**",
        description = "Le channel a été nuke avec succès !",
        color = 0x000000,
        timestamp = datetime.datetime.utcnow()
    )
    embed.set_image(url = "https://i.giphy.com/media/HhTXt43pk1I1W/200.gif")
    await channel2.send(embed = embed)
    await ctx.channel.delete()

#Run------------------------------------------------------------------------------------------

client.run(os.environ('DISCORD_TOKEN'))
