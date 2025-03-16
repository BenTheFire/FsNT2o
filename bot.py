import discord
from discord.ext import commands
import DnDWiki5e as DnD

admin_ids = [872960398922489896, 1241889974425616515, 292736680665022464]

# region - Bot Setup
with open('token.txt', 'r') as file:
    TOKEN = file.read().strip()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
# endregion

# region - Event Handlers
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")
# endregion


# region - Debug Commands
@bot.tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    print(f"Got Hello-d by {interaction.user} at {interaction.created_at}")
    await interaction.response.send_message("Hello!")


@bot.tree.command(name="request_data", description="Request data of a user")
async def request_data(interaction: discord.Interaction):
    user = interaction.user
    embed = discord.Embed(title="User Data", description=f"Data of {user.mention}")
    # region
    embed.add_field(name="Name", value=user.name)
    embed.add_field(name="ID", value=user.id)
    embed.add_field(name="Created At", value=user.created_at)
    embed.add_field(name="Server", value=interaction.guild.name)
    embed.add_field(name="Server ID", value=interaction.guild.id)
    embed.add_field(name="Channel", value=interaction.channel.name)
    embed.add_field(name="Channel ID", value=interaction.channel.id)
    embed.add_field(name="Category", value=interaction.channel.category.name)
    embed.add_field(name="Category ID", value=interaction.channel.category.id)
    # endregion
    await interaction.response.send_message(embed=embed)
# endregion


# region - Mod Info Commands
@bot.tree.command(name="server_categories", description="List all categories in the server")
async def server_categories(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title="Server Categories", description=f"Categories in {guild.name}")
    for category in guild.categories:
        embed.add_field(name=category.name, value=category.id)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="mod_server_info", description="Get the server initialization info")
async def mod_server_info(interaction: discord.Interaction):
    guild = interaction.guild
    owner = interaction.guild.owner
    bot_user = bot.user
    user_req = interaction.user
    if user_req.id not in admin_ids:
        await interaction.response.send_message("You are not allowed to use this command")
        return
    embed = discord.Embed(title="Server Initialization Info", description="Information about the server")
    embed.add_field(name="Server Name", value=guild.name)
    embed.add_field(name="Server ID", value=guild.id)
    embed.add_field(name="Server Created At", value=guild.created_at)
    if owner:
        embed.add_field(name="Server Owner", value=owner.mention)
        embed.add_field(name="Server Owner ID", value=owner.id)
    else:
        embed.add_field(name="Server Owner", value="Not Found")

    if bot_user:
        embed.add_field(name="Bot User", value=bot_user.mention)
        embed.add_field(name="Bot User ID", value=bot_user.id)
    else:
        embed.add_field(name="Bot User", value="Not Found")

    if user_req:
        embed.add_field(name="User Requesting", value=user_req.mention)
        embed.add_field(name="User Requesting ID", value=user_req.id)
    else:
        embed.add_field(name="User Requesting", value="Not Found")

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="get_user_by_id", description="Get the server info")
async def get_user_by_id(interaction: discord.Interaction, user: discord.User):
    if interaction.user.id not in admin_ids:
        await interaction.response.send_message("You are not allowed to use this command")
        return
    if not user:
        await interaction.response.send_message("User not found")
        return
    embed = discord.Embed(title="User Info", description=f"Information about {user.mention}")
    embed.add_field(name="Name", value=user.name)
    embed.add_field(name="ID", value=user.id)
    embed.add_field(name="Created At", value=user.created_at)
    embed.add_field(name="Joined At", value=user.joined_at)
    await interaction.response.send_message(embed=embed)
# endregion


# region - DnD Commands
@bot.tree.command(name="get_dnd_spell", description="Get a spell information lookup from https://DnDWikidot.com")
async def get_dnd_spell(interaction: discord.Interaction, spell_name: str):
    spell: DnD.SpellReference = DnD.dnd_wikidot_lookup_spell(spell_name)
    embed = discord.Embed(title=spell.spell_name)
    embed.add_field(name="Source", value=spell.source, inline=False)
    if spell.level == 0:
        embed.add_field(name="Level", value="Cantrip")
    else:
        embed.add_field(name="Level", value=spell.level, )
    embed.add_field(name="School", value=spell.school)
    embed.add_field(name="Casting Time", value=spell.casting_time, inline=False)
    embed.add_field(name="Range", value=spell.range, inline=False)
    embed.add_field(name="Components", value=spell.components, inline=False)
    embed.add_field(name="Duration", value=spell.duration, inline=False)
    embed.add_field(name="Description", value=spell.description_text, inline=False)
    if spell.at_higher_levels:
        embed.add_field(name="At Higher Levels", value=spell.at_higher_levels, inline=False)
    embed.set_footer(text="Data provided by DnD Wikidot - https://dnd5e.wikidot.com/")
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="roll_dice", description="Roll dice with the given dice string")
async def roll_dice(interaction: discord.Interaction, ammount: int, sides: int):
    import random
    rolls = [random.randint(1, sides) for _ in range(ammount)]
    embed = discord.Embed(title="Dice Roll", description=f"Rolling {ammount}d{sides}")
    if len(rolls) <= 5:
        embed.add_field(name="Rolls", value=", ".join(map(str, rolls)))
    else:
        embed.add_field(name="Rolls", value="Too many to display")
    embed.add_field(name="Total", value=sum(rolls))
    await interaction.response.send_message(embed=embed)
# endregion

bot.run(TOKEN)
