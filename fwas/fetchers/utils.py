import aiofiles
import aiohttp


async def download(url, output_file):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async with aiofiles.open(output_file, "wb") as tmp_file:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    await tmp_file.write(chunk)

            await response.release()
