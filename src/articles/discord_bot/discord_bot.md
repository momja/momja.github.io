---
title: "Writing a Discord bot with Python and aiocron"
description: "A quick example with discord.py's 2.0 framework"
publish_date: 2023-04-22
---

# Writing a Diiscord bot with Python and aiocron
I wanted to write a Discord bot to provide simple scheduled alerts for the [hackerspace](https://noisebridge.net) I am a part of. We have a channel for the woodshop, and every so often, we need to empty the dust collector and scrap bins.

After some basic research, I found it was pretty straightforward how to set up a bot in the discord developer portal, so I'm not going to go through that here, but if you need help, you can check out [this realpython article](https://realpython.com/how-to-make-a-discord-bot-python/).

Instead, I want to focus on a snag I ran into while trying to use [aiocron](https://github.com/gawel/aiocron) with [discord.py](https://discordpy.readthedocs.io/en/stable/). The python discord library now offers some neat tricks for timing method runs with the annotation `@tasks.loop(...)`, but this doesn't let you _schedule_ async method calls by day or time, so you have to provide some extra code to make sure you start the loop at the right moment in time for it to work correctly. aiocron is neat because it uses crontab format for scheduling method calls. 

Now, when I first tried to get this running, I encountered issues with the event loop. My understanding is that the discord library made [some changes](https://discordpy.readthedocs.io/en/stable/migrating.html?highlight=2%200#asyncio-event-loop-changes) in it's 2.0 version that allows you to create your own asynchronous loop for running the bot. If you _don't_ use this loop, I'm not sure how you set up other asynchronous code.

```python
import os

import discord
import aiocron
import asyncio

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
WOODSHOP_CHANNEL = os.getenv('WOODSHOP_CHANNEL')

trash_message = "This is your friendly reminder to take out the shop bins and empty the dust collector!"

bot = commands.Bot(case_insensitive=TRUE, intents=discord.Intents.all(), help_command=None)

loop = asyncio.get_event_loop()

@aiocron.crontab('0 12 * * 0', start=False, loop=loop) # every sunday at noon
async def trash_reminder():
    woodshop_channel = bot.get_channel(int(WOODSHOP_CHANNEL))
    await woodshop_channel.send(trash_message)

async def main():
    async with bot:
        trash_reminder.start()
        await bot.start(TOKEN)
    
loop.run_until_complete(main())

```

By using the variable `loop` as my async loop, I can provide that to the crontab annotation, and voila! Things start working.

Now, if you are like me and don't know that format off the top of your head, what I did is ask old ChatGPT, who gave a prompt answer and description. Work smarter, not harder!

Not so much of a tutorial, but I'm hoping someone finds this code snippet helpful, because I couldn't find an example of this myself. I did, however find [some](https://www.reddit.com/r/Discord_Bots/comments/vxknqz/aiocroncronjob_not_working_with_discordpy_v20/) [people](https://github.com/Rapptz/discord.py/issues/7986) running into similar issues.

Anyways, happy hacking!
