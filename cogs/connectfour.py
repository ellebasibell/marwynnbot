import asyncio
import json
import random

import discord
from discord.ext import commands
from globalcommands import GlobalCMDS as gcmds
import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    board = np.flip(board, 0)
    string = ":one:  :two:  :three:  :four:  :five:  :six:  :seven:\n"
    for row in range(ROW_COUNT):
        for column in range(COLUMN_COUNT):
            if board[row][column] == 0:
                string += "⚫  "
            elif board[row][column] == 1:
                string += "🔴  "
            elif board[row][column] == 2:
                string += "🔵  "
            elif board[row][column] == 3:
                string += "❤  "
            elif board[row][column] == 4:
                string += "💙  "
            column += 1
        string += "\n"
    return string


def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                if piece == 1:
                    board[r][c] = 3
                    board[r][c + 1] = 3
                    board[r][c + 2] = 3
                    board[r][c + 3] = 3
                if piece == 2:
                    board[r][c] = 4
                    board[r][c + 1] = 4
                    board[r][c + 2] = 4
                    board[r][c + 3] = 4
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                if piece == 1:
                    board[r][c] = 3
                    board[r + 1][c] = 3
                    board[r + 2][c] = 3
                    board[r + 3][c] = 3
                if piece == 2:
                    board[r][c] = 4
                    board[r + 1][c] = 4
                    board[r + 2][c] = 4
                    board[r + 3][c] = 4
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                if piece == 1:
                    board[r][c] = 3
                    board[r + 1][c + 1] = 3
                    board[r + 2][c + 2] = 3
                    board[r + 3][c + 3] = 3
                if piece == 2:
                    board[r][c] = 4
                    board[r + 1][c + 1] = 4
                    board[r + 2][c + 2] = 4
                    board[r + 3][c + 3] = 4
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                if piece == 1:
                    board[r][c] = 3
                    board[r - 1][c + 1] = 3
                    board[r - 2][c + 2] = 3
                    board[r - 3][c + 3] = 3
                if piece == 2:
                    board[r][c] = 4
                    board[r - 1][c + 1] = 4
                    board[r - 2][c + 2] = 4
                    board[r - 3][c + 3] = 4
                return True


async def win(ctx, member: discord.Member):
    load = False
    success = False
    init = {'ConnectFour': {}}
    gcmds.json_load(gcmds, 'gamestats.json', init)
    with open('gamestats.json', 'r') as f:
        file = json.load(f)
        while not load:
            try:
                file['ConnectFour'][str(member.id)]['win']
            except KeyError:
                if not success:
                    try:
                        file['ConnectFour'][str(member.id)]
                    except KeyError:
                        try:
                            file['ConnectFour']
                        except KeyError:
                            file['ConnectFour'] = {}
                        file['ConnectFour'][str(member.id)] = {}
                        success = True
                file['ConnectFour'][str(member.id)]['win'] = 0
            else:
                file['ConnectFour'][str(member.id)]['win'] += 1
                load = True
        with open('gamestats.json', 'w') as f:
            json.dump(file, f, indent=4)
    gcmds.ratio(gcmds, ctx.author, 'gamestats.json', 'ConnectFour')

    initBal = {'Balance': {}}
    gcmds.json_load(gcmds, 'balance.json', initBal)
    spell = "credits"
    random_number = random.randint(1, 100001)
    if 1 <= random_number <= 10000:
        award_amount = 1
        spell = "credit"
    elif 10001 <= random_number <= 30000:
        award_amount = 2
    elif 30001 <= random_number <= 70000:
        award_amount = 3
    elif 70001 <= random_number <= 90000:
        award_amount = 4
    elif 90001 <= random_number <= 100000:
        award_amount = 5
    elif random_number == 100001:
        award_amount = 1000000

    with open('balance.json', 'r') as f:
        file = json.load(f)
        try:
            file['Balance'][str(member.id)]
        except KeyError:
            file['Balance'][str(member.id)] = 1000 + award_amount
            balance = 1000
            initEmbed = discord.Embed(title="Initialised Credit Balance",
                                      description=f"{member.mention}, you have been credited `{balance}` credits "
                                                  f"to start!\n\nCheck your current"
                                                  f" balance using `{gcmds.prefix(gcmds, ctx)}balance`",
                                      color=discord.Color.blue())
            initEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/734962101432615006"
                                        "/738390147514499163/chips.png")
            await ctx.channel.send(embed=initEmbed, delete_after=10)
        else:
            file['Balance'][str(member.id)] += award_amount
    with open('balance.json', 'w') as f:
        json.dump(file, f, indent=4)
        f.close()

    if award_amount == 1000000:
        title = "JACKPOT!!!"
    else:
        title = "Winnings"

    rewardEmbed = discord.Embed(title=title,
                                description=f"{member.mention}, you won ```{award_amount} {spell}!```",
                                color=discord.Color.blue())
    rewardMessage = await ctx.channel.send(embed=rewardEmbed)
    if award_amount == 1000000:
        await rewardMessage.pin(reason=f"{member.name} hit the jackpot for winning a game of Connect Four!")


def lose(ctx, member: discord.Member):
    load = False
    success = False
    init = {'ConnectFour': {}}
    gcmds.json_load(gcmds, 'gamestats.json', init)
    with open('gamestats.json', 'r') as f:
        file = json.load(f)
        while not load:
            try:
                file['ConnectFour'][str(member.id)]['lose']
            except KeyError:
                if not success:
                    try:
                        file['ConnectFour'][str(member.id)]
                    except KeyError:
                        try:
                            file['ConnectFour']
                        except KeyError:
                            file['ConnectFour'] = {}
                        file['ConnectFour'][str(member.id)] = {}
                        success = True
                file['ConnectFour'][str(member.id)]['lose'] = 0
            else:
                file['ConnectFour'][str(member.id)]['lose'] += 1
                load = True
        with open('gamestats.json', 'w') as f:
            json.dump(file, f, indent=4)
    gcmds.ratio(gcmds, member, 'gamestats.json', 'ConnectFour')


def draw(ctx, member: discord.Member):
    load = False
    success = False
    init = {'ConnectFour': {}}
    gcmds.json_load(gcmds, 'gamestats.json', init)
    with open('gamestats.json', 'r') as f:
        file = json.load(f)
        while not load:
            try:
                file['ConnectFour'][str(ctx.author.id)]['tie']
            except KeyError:
                if not success:
                    try:
                        file['ConnectFour'][str(ctx.author.id)]
                    except KeyError:
                        try:
                            file['ConnectFour']
                        except KeyError:
                            file['ConnectFour'] = {}
                        file['ConnectFour'][str(ctx.author.id)] = {}
                        success = True
                file['ConnectFour'][str(ctx.author.id)]['tie'] = 0
            else:
                file['ConnectFour'][str(ctx.author.id)]['tie'] += 1
                load = True
        with open('gamestats.json', 'w') as f:
            json.dump(file, f, indent=4)
    with open('gamestats.json', 'r') as f:
        file = json.load(f)
        while not load:
            try:
                file['ConnectFour'][str(member.id)]['tie']
            except KeyError:
                if not success:
                    try:
                        file['ConnectFour'][str(member.id)]
                    except KeyError:
                        file['ConnectFour'][str(member.id)] = {}
                        success = True
                file['ConnectFour'][str(member.id)]['tie'] = 0
            else:
                file['ConnectFour'][str(member.id)]['tie'] += 1
                load = True
        with open('gamestats.json', 'w') as f:
            json.dump(file, f, indent=4)


class ConnectFour(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['connectfour', 'c4', 'conn', 'connect'])
    async def connectFour(self, ctx, member: discord.Member = None):
        await gcmds.invkDelete(gcmds, ctx)

        if member is None:
            error = discord.Embed(title="No Opponent Selected",
                                  description=f"{ctx.author.mention}, please mention another member to start a game "
                                              f"with them",
                                  color=discord.Color.dark_red())
            await ctx.channel.send(embed=error, delete_after=10)
            return
        elif member == ctx.author:
            error = discord.Embed(title="No Opponent Selected",
                                  description=f"{ctx.author.mention}, you cannot play with yourself, please mention "
                                              "another member to start the game with them",
                                  color=discord.Color.dark_red())
            await ctx.channel.send(embed=error, delete_after=10)
            return
        else:
            opponent = member

        board = create_board()
        description = print_board(board)

        c4 = discord.Embed(title="Connect Four",
                           description=f"{ctx.author.mention}'s turn\n\n{description}",
                           color=discord.Color.red())
        c4.set_footer(text=member.display_name,
                      icon_url=member.avatar_url)
        c4.set_author(name=f"{ctx.author.display_name}",
                      icon_url=ctx.author.avatar_url)
        c4.set_thumbnail(url="https://studio.code.org/v3/assets/dQveW7B23TPYvHgQmNOvkf1v_fQW5hO1TOBfPkuJM0Y"
                             "/DanYr4AVMAABJ_K.png")
        message = await ctx.channel.send(embed=c4)

        turn = 0

        r1 = '1️⃣'
        r2 = '2️⃣'
        r3 = '3️⃣'
        r4 = '4️⃣'
        r5 = '5️⃣'
        r6 = '6️⃣'
        r7 = '7️⃣'
        r8 = "❌"
        rlist = [r1, r2, r3, r4, r5, r6, r7, r8]

        for r in rlist:
            await message.add_reaction(r)

        def check(reaction, user):
            if ctx.author == user and reaction.emoji in rlist:
                return True
            if member == user and reaction.emoji in rlist:
                return True

        turn_count = 0

        while turn_count < 43:
            confirm_turn = False
            while not confirm_turn:
                try:
                    choice = await commands.AutoShardedBot.wait_for(self.client, 'reaction_add', timeout=60.0,
                                                                    check=check)
                except asyncio.TimeoutError:
                    await message.clear_reactions()
                    canceled = discord.Embed(title="Game Timeout",
                                             description=f"Connect4 game canceled due to inactivity, "
                                                         f"create a new game",
                                             color=discord.Color.dark_red())
                    canceled.set_thumbnail(url='https://cdn.discordapp.com/attachments/734962101432615006'
                                               '/738083697726849034/nocap.jpg')
                    canceled.set_footer(text=f"No valid reaction provided within 60 seconds")
                    await message.edit(embed=canceled, delete_after=10)
                    return
                else:
                    for item in choice:
                        if isinstance(item, discord.Reaction):
                            if str(item) in rlist:
                                choice_piece = rlist.index(str(item))
                                emoji = str(item)
                        if isinstance(item, discord.Member):
                            if item.id is ctx.author.id:
                                player = ctx.author
                            elif item.id is member.id:
                                player = member

                    await message.remove_reaction(emoji, player)

                    if emoji == r8:
                        valid = False
                        if turn == 0 and player == ctx.author:
                            description = f"{ctx.author.mention} canceled the game"
                            valid = True
                        if turn == 1 and player == member:
                            description = f"{member.mention} canceled the game"
                            valid = True
                        if valid:
                            await message.clear_reactions()
                            c4 = discord.Embed(title="Connect Four Game Canceled",
                                               description=description,
                                               color=discord.Color.dark_red())
                            c4.set_thumbnail(
                                url="https://studio.code.org/v3/assets/dQveW7B23TPYvHgQmNOvkf1v_fQW5hO1TOBfPkuJM0Y"
                                    "/DanYr4AVMAABJ_K.png")
                            await message.edit(embed=c4, delete_after=20)
                            return

                    if turn == 0 and player == ctx.author:
                        color = discord.Color.red()
                        board_color = discord.Color.blue()
                        aname = member.display_name
                        aurl = member.avatar_url
                        fname = ctx.author.display_name
                        furl = ctx.author.avatar_url
                        if is_valid_location(board, choice_piece):
                            row = get_next_open_row(board, choice_piece)
                            drop_piece(board, row, choice_piece, 1)
                            printed_board = print_board(board)
                            description = f"{member.mention}'s turn\n\n{printed_board}"
                            confirm_turn = True
                            if winning_move(board, 1):
                                await message.clear_reactions()
                                printed_board = print_board(board)
                                c4 = discord.Embed(title="Connect Four",
                                                   description=f"{ctx.author.mention} wins!\n\n{printed_board}",
                                                   color=color)
                                c4.set_footer(text=member.display_name,
                                              icon_url=member.avatar_url)
                                c4.set_author(name=f"{ctx.author.display_name}",
                                              icon_url=ctx.author.avatar_url)
                                c4.set_thumbnail(
                                    url="https://studio.code.org/v3/assets"
                                        "/dQveW7B23TPYvHgQmNOvkf1v_fQW5hO1TOBfPkuJM0Y/DanYr4AVMAABJ_K.png")
                                await message.edit(embed=c4)
                                await win(ctx, ctx.author)
                                lose(ctx, opponent)
                                gcmds.incrCounter(gcmds, ctx, 'connectFour')
                                return

                    if turn == 1 and player == member:
                        color = discord.Color.blue()
                        board_color = discord.Color.red()
                        aname = ctx.author.display_name
                        aurl = ctx.author.avatar_url
                        fname = member.display_name
                        furl = member.avatar_url
                        if is_valid_location(board, choice_piece):
                            row = get_next_open_row(board, choice_piece)
                            drop_piece(board, row, choice_piece, 2)
                            printed_board = print_board(board)
                            description = f"{ctx.author.mention}'s turn\n\n{printed_board}"
                            confirm_turn = True
                            if winning_move(board, 2):
                                await message.clear_reactions()
                                printed_board = print_board(board)
                                c4 = discord.Embed(title="Connect Four",
                                                   description=f"{member.mention} wins!\n\n{printed_board}",
                                                   color=color)
                                c4.set_author(name=member.display_name,
                                              icon_url=member.avatar_url)
                                c4.set_footer(text=f"{ctx.author.display_name}",
                                              icon_url=ctx.author.avatar_url)
                                c4.set_thumbnail(
                                    url="https://studio.code.org/v3/assets"
                                        "/dQveW7B23TPYvHgQmNOvkf1v_fQW5hO1TOBfPkuJM0Y/DanYr4AVMAABJ_K.png")
                                await message.edit(embed=c4)
                                await win(ctx, opponent)
                                lose(ctx, ctx.author)
                                gcmds.incrCounter(gcmds, ctx, 'connectFour')
                                return

            c4 = discord.Embed(title="Connect Four",
                               description=description,
                               color=board_color)
            c4.set_author(name=aname,
                          icon_url=aurl)
            c4.set_footer(text=fname,
                          icon_url=furl)
            c4.set_thumbnail(url="https://studio.code.org/v3/assets/dQveW7B23TPYvHgQmNOvkf1v_fQW5hO1TOBfPkuJM0Y"
                                 "/DanYr4AVMAABJ_K.png")
            await message.edit(embed=c4)

            turn += 1
            turn_count += 1
            turn = turn % 2

        aname = member.display_name
        aurl = member.avatar_url
        fname = ctx.author.display_name
        furl = ctx.author.avatar_url
        c4 = discord.Embed(title="Connect Four",
                           description=f"Draw!\n\n{printed_board}",
                           color=discord.Color.green())
        c4.set_author(name=aname,
                      icon_url=aurl)
        c4.set_footer(text=fname,
                      icon_url=furl)
        c4.set_thumbnail(url="https://studio.code.org/v3/assets/dQveW7B23TPYvHgQmNOvkf1v_fQW5hO1TOBfPkuJM0Y"
                             "/DanYr4AVMAABJ_K.png")
        await message.edit(embed=c4)
        draw(ctx, member)
        gcmds.incrCounter(gcmds, ctx, 'connectFour')


def setup(client):
    client.add_cog(ConnectFour(client))
