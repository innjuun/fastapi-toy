import os

import aiohttp
import asyncio

import random


async def attack_to_server():
    async with aiohttp.ClientSession() as session:
        for _ in range(1000):
            # print(os.getpid())
            num = random.randint(1, 1000000)
            body = {
                "name": f"아이템{num}",
                "price": num * 100,
                "is_offer": True,
            }
            url = f"http://ec2-54-180-123-157.ap-northeast-2.compute.amazonaws.com:8000/items/{num}"
            async with session.post(
                url=url, json=body
            ) as resp:
                response_body = await resp.json()
                # print(response_body)
        # print(response)


if __name__ == "__main__":
    asyncio.run(attack_to_server())
