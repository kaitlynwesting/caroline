import asyncio
from datetime import datetime, timezone

from utils import constants, embed_template, time_converter
from pymongo import MongoClient
import random

cluster = MongoClient(
    "mongodb://cakeHeadChef:cakeHeadChef@buttercream-shard-00-00.ilbju.mongodb.net:27017,buttercream-shard-00-01."
    "ilbju.mongodb.net:27017,buttercream-shard-00-02.ilbju.mongodb.net:27017/Discord?"
    "ssl=true&replicaSet=atlas-65nepc-shard-0&authSource=admin&retryWrites=true&w=majority"
)

db = cluster["Discord"]
collection = db["Nickname Jail"]


async def animalise(
        ctx,
        infraction_member,
        infraction_time,
        infraction_reason='',
):
    if collection.find_one({'prisoner_id': infraction_member.id}) is None:
        pass
    else:
        await ctx.send(f"{infraction_member} is already in nickname jail.")
        return

    infraction_time_string = time_converter.time_to_string(infraction_time)
    infraction_time_date = time_converter.time_to_date(infraction_time)

    with open("texts/adjectives.txt") as adjectives:
        adjectives_lines = [line.rstrip('\n') for line in adjectives]
    with open("texts/animals.txt") as animals:
        animals_lines = [line.rstrip('\n') for line in animals]

    new_nick = f"{random.choice(adjectives_lines)} {random.choice(animals_lines)}"

    public_message = f"Your previous name, **{infraction_member.name}**, was so terrible that we had to change it. " \
                     f"Your new nickname will be **{new_nick}**.\n\n " \
                     f"**You will be muted until {infraction_time_date} UTC ({infraction_time_string})**."

    private_message = f"**Your nickname was changed by {ctx.message.author}.**\n" \
                      f"{infraction_reason}\n" \
                      f"**You will be able to change your nickname again at {infraction_time_date} UTC " \
                      f"({infraction_time_string})**."

    await embed_template.server_embed(
        ctx.channel,
        f"Congratulations!",
        f"{public_message}",
        "",
        constants.blurple
    )

    await embed_template.dm_manual_embed(
        infraction_member,
        f"Infraction received from Photoshop Discord",
        f"{private_message}",
        f"If you believe that there has been an error, please DM our Modmail bot.",
        constants.blurple
    )

    await infraction_member.edit(nick=new_nick, reason=None)

    tags_dictionary = list(collection.find())
    max_id = 0
    for d in tags_dictionary:
        if int(str(d['_id'])) > max_id:
            max_id = d['_id']

    post = {
        "_id": max_id + 1,
        "prisoner_id": infraction_member.id,
        "prisoner_nickname": new_nick,
        "entered_at": datetime.now().astimezone(timezone.utc).strftime('%B %d, %Y at %H:%M:%S'),
        "release_at": infraction_time_date,
    }

    collection.insert_one(post)

    await asyncio.sleep(time_converter.time_to_int(infraction_time))

    collection.delete_one({'prisoner_id': infraction_member.id})
