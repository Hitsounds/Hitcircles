import discord
from discord.ext import commands
import praw
import os
import aiohttp
import asyncio
import random

class fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reddit = praw.Reddit(client_id=os.environ.get("REDDIT_ID"), client_secret=os.environ.get("REDDIT_S"), user_agent='A discord bot | https://github.com/Hitsounds/discord-bot')


    @commands.command(name='anime', aliases=['manga'])
    async def kitsu_search(self, ctx, *, search: str):
        async with ctx.message.channel.typing():
            search = search.replace(" ","%20")
            async with aiohttp.ClientSession() as session:
                resp = await session.get(f"https://kitsu.io/api/edge/{ctx.invoked_with}?filter[text]={search}&page[limit]=1")
                resp = await resp.json()
                resp = resp["data"][0]["attributes"]
            embed=discord.Embed(title="Rating: {}%".format(resp["averageRating"]), description=resp["synopsis"], color=0x4d30d6)
            embed.set_author(name="{} ({})".format(resp["canonicalTitle"],resp["subtype"]), url="https://kitsu.io/{}/{}".format(ctx.invoked_with, resp["slug"]))
            embed.set_thumbnail(url=resp["posterImage"]["original"])
            embed.add_field(name="Start", value=resp["startDate"], inline=True)
            embed.add_field(name="End", value=resp["endDate"], inline=True)
            embed.add_field(name="Status", value=resp["status"], inline=True)
            embed.add_field(name="Next Release", value=resp["nextRelease"], inline=True)
            embed.set_footer(text=resp["ageRatingGuide"])
            await ctx.send(embed=embed)


    @commands.group()
    async def bws(self, ctx):
        if ctx.invoked_subcommand is None:
            bwl = self.reddit.subreddit('awwnime').hot()
            for i in range(0,random.randint(1, 10)):
                submission = next(x for x in bwl if not x.stickied)
            await ctx.send(submission.url)


    @bws.command()
    async def dump(self, ctx):
        sreddit = self.reddit.subreddit('awwnime')
        bwl = self.reddit.subreddit('awwnime').hot()
        embed=discord.Embed(title="Current bws selection", url="https://www.reddit.com/r/awwnime/hot/")
        embed.set_author(name="Source", url="https://www.reddit.com/r/awwnime/", icon_url=sreddit.icon_img)
        embed.set_thumbnail(url="https://cdn.awwni.me/13dgm.png")
        for i in range(0, 10):
            embed.add_field(name="#{}".format(i+1), value="[{url}]({url})".format(url = next(x for x in bwl if not x.stickied).url), inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(fun(client))
