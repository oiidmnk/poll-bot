# This is a sample Python script.
import discord
import typing
from discord import app_commands
import os
from discord.ext.commands import bot
from random import choice


# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def open_token():
    # gets token from environment variable DISCORD_TOKEN
    token = os.getenv("DISCORD_TOKEN")
    if token is None:
        print("DISCORD_TOKEN not found")
        exit(1)

    return token


def open_id1():
    # gets id1 from environment variable ID1
    id1 = os.getenv("ID1")
    if id1 is None:
        print("ID1 not found")
        exit(1)

    return id1


def open_id2():
    # gets id2 from environment variable ID2
    id2 = os.getenv("ID2")
    if id2 is None:
        print("ID2 not found")
        exit(1)

    return id2


def main():
    # Use a breakpoint in the code line below to debug your script.
    numbers_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    yes_no_emojis = ["✅", "❌"]
    default_split = ";"

    token = open_token()
    id1 = open_id1()
    id2 = open_id2()

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    @tree.command(name="poll",
                  description=f"does poll (answers seperated by `{default_split}` can be specified by optional split "
                              "argument)", guilds=[discord.Object(id=id1),
                                                   discord.Object(id=id2)])
    async def poll( interaction: discord.Interaction, question: str,
                    answers: typing.Optional[str] = f"yes{default_split}no",
                    split: typing.Optional[str] = f"{default_split}"):

        print("question: " + question + " answers: " + answers + " split: " + split)

        message = "New poll: " + question + "\n"
        if answers == f"yes{default_split}no":
            answers = f"yes{split}no"

        answers = answers.split(split)

        if len(answers) > 9:
            await interaction.response.send_message("Too many answers")
            return

        if len(answers) == 2:
            if answers[0].lower().strip() == "yes" and answers[1].lower().strip() == "no":
                await interaction.response.send_message(message)
                message = await interaction.original_response()
                for i in range(len(yes_no_emojis)):
                    await message.add_reaction(yes_no_emojis[i])
                return

        for i in range(len(answers)):
            message += numbers_emojis[i] + " " + answers[i].strip() + "\n"

        await interaction.response.send_message(message)
        message = await interaction.original_response()
        print("GOT MESSAGE: " + str(message.content))

        for i in range(len(answers)):
            await message.add_reaction(numbers_emojis[i])

    @tree.command(  name="oracle",
                    description=f"answers your question, syntax like poll + additional custom answer option",
                    guilds=[discord.Object(id=id1),
                            discord.Object(id=id2)])
    async def oracle(   interaction: discord.Interaction, question: str,
                        answers: typing.Optional[str] = f"yes{default_split}no",
                        split: typing.Optional[str] = f"{default_split}",
                        custom_answer: typing.Optional[str] = "According to my calculations you should",
                        custom_answer_end: typing.Optional[str] = ".",):

        message = "New question: " + question + "\n"
        if answers == f"yes{default_split}no":
            answers = f"yes{split}no"

        answers = answers.split(split)

        if len(answers) > 9:
            await interaction.response.send_message("Too many answers")
            return

        if len(answers) == 2:
            if answers[0].lower().strip() == "yes" and answers[1].lower().strip() == "no":
                message += f'\n\n{choice(["Yes", "No", "Definitely", "Absolutely not"])}'
                await interaction.response.send_message(message)
                return
                
        for i in range(len(answers)):
            message += numbers_emojis[i] + " " + answers[i].strip() + "\n"
            chosen = choice(range(len(answers)))
            
        message += f"\n\n{custom_answer} {numbers_emojis[chosen] + ' ' + answers[chosen].strip()}{custom_answer_end}"
        await interaction.response.send_message(message)

    @client.event
    async def on_ready():
        print("Ready0!")
        await client.change_presence(activity=discord.Game("with some bitches\nplayers: (-1 of 2)"))
        await tree.sync(guild=discord.Object(id=id1))
        print("Ready1!")
        await tree.sync(guild=discord.Object(id=id2))
        print("Ready2!")

    client.run(token)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
