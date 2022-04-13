import os
from discord.ext import commands
import openai
client = commands.Bot(command_prefix='!reframe')

@client.event
async def on_ready():
    print("I'm in")
    print(client.user)

@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content.startswith('!reframe'):
            prompt = ("The following is a list of negative thoughts which are then reframed with in a more positive, hopeful way:" + "\n\nNegative: this will never work out\nPositive: I'm having trouble right now, but it's not a big deal if this doesn't work out."
            + "\nPositive: I'm having some trouble right now, but I'm making plans to solve those problems."
            + "\n\nNegative: why do i suck at this\nPositive: I have learned a lot about this topic. I want to keep learning more about it so I'll keep up the effort.\nPositive: I know what I need to improve."
            + "\n\nNegative: " + message.content.replace('!reframe', ''))

            openai.api_key = os.environ['OPENAI_API_KEY']

            response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=0.89,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n\n"]
            )

            messages = str(response["choices"][0]["text"]).split("Positive:")

            msg = "Here's another way to think about that: " + messages[1] if len(messages) >= 2 else "Our robots seem to be overly negative right now. Please try again."
            await message.channel.send(msg)

token = os.environ['DISCORD_BOT_SECRET']
client.run(token)

