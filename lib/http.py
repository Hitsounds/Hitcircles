import aiohttp
import os
import discord


async def file_from_url(url):
    "returns a promise to file obj"
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
        return resp


async def sendfile(fileobj, *, d_ctx=None, filename=None, spoiler=False):
    file_size = os.fstat(fileobj.fileno()).st_size/1048576.
    if file_size < 7.9 and d_ctx != None:
        return await d_ctx.send(file=discord.File(fileobj))
    elif file_size < 500.:
        async with aiohttp.ClientSession() as session:
            resp = await session.post("https://0x0.st", data={"file": fileobj})
        return await resp.text()
    elif file_size < 9999:
        async with aiohttp.ClientSession() as session:
            resp = await session.post("https://transfer.sh", data={"file": fileobj})
        return await resp.text()
    else:
        return "Somthing went really badly wrong"