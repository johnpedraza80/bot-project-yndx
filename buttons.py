import discord
import sqlite3


class Buttons(discord.ui.View):
    def __init__(self):
        super(Buttons, self).__init__()

    @discord.ui.button(label="Учавствовать", style=discord.ButtonStyle.primary)
    async def add_whitelist(self, interaction, button):
        button.disabled = True
        button.label = "Вы внесены"
        await interaction.response.edit_message(view=self)
        await data(interaction.user)


async def data(player):
    connect = sqlite3.connect("data/poker_players.sqlite")
    cursor = connect.cursor()

    cursor.execute('''INSERT INTO session (names, cards) VALUES (?, ?)''',
                   (str(player), "None"))
    connect.commit()
