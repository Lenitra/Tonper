import datetime
import interactions
from interactions import Permissions, slash_option, Embed
import time
import os
import json
import psutil

bot = interactions.Client()


@interactions.listen()
async def on_startup():
    await bot.change_presence(
        status=interactions.Status.ONLINE,
        activity=interactions.Activity(
            "avec une machine Linux", interactions.ActivityType.PLAYING
        ),
    )
    print("Bot is ready!")


@interactions.slash_command(description="Affiche les perfs de ta machine")
async def perfs(ctx):
    with open("config.json", "r") as f:
        data = json.load(f)
    if str(ctx.author.id) in data["cmd_perfs"] or str(ctx.author.id) in data["cmd_*"]:
        ramp = f"{round(psutil.virtual_memory()[2], 2)}%"
        ramu = f"{round(psutil.virtual_memory()[3]/1000000000, 2)}/{int(round(psutil.virtual_memory()[0]/1000000000, 0))} Go"

        cpup = f"{psutil.cpu_percent()}%"

        diskp = f"{round(psutil.disk_usage('/')[3], 2)}%"
        disku = f"{round(psutil.disk_usage('/')[1]/1000000000, 2)}/{int(round(psutil.disk_usage('/')[0]/1000000000, 0))} Go"

        embed = Embed(
            title="Perfs de la machine",
            description=f"**RAM**: {ramp}\n_{ramu}_\n\n**CPU**: {cpup}\n\n**Disque**: {diskp}\n_{disku}_",
            color=0x00FF00,
        )
        await ctx.send(embed=embed)

    else:
        msg = await ctx.send("Vous n'avez pas la permission pour cette commande !")
        time.sleep(3)
        await msg.delete()


@interactions.slash_command(description="Redémarrer la machine")
async def reboot(ctx):
    with open("config.json", "r") as f:
        data = json.load(f)
    if str(ctx.author.id) in data["cmd_reboot"] or str(ctx.author.id) in data["cmd_*"]:
        os.system("sudo reboot")
        msg = await ctx.send("Commande éxecutée !")
        time.sleep(3)
        await msg.delete()
    else:
        msg = await ctx.send("Vous n'avez pas la permission pour cette commande !")
        time.sleep(3)
        await msg.delete()


@interactions.slash_command(description="Executer une commande sur le serveur")
@slash_option(
    "commande",
    "La commande à éxecuter sur la machine",
    interactions.OptionType.STRING,
    required=True,
)
async def commande(ctx, commande):
    with open("config.json", "r") as f:
        data = json.load(f)
    if (
        str(ctx.author.id) in data["cmd_commande"]
        or str(ctx.author.id) in data["cmd_*"]
    ):
        os.system(commande)
        msg = await ctx.send("Commande éxecutée !")
        time.sleep(3)
        await msg.delete()
    else:
        msg = await ctx.send("Vous n'avez pas la permission pour cette commande !")
        time.sleep(3)
        await msg.delete()



os.system("git pull origin main")


with open("token.txt", "r") as f:
    token = f.read()
bot.start(token)
