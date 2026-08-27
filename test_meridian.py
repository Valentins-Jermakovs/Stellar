import asyncio

from stellar.clients.meridian import MeridianClient


async def main() -> None:

    client = MeridianClient()

    tokens = await client.login(
        login="valentins",
        password="12345678",
    )

    print("Access token:")
    print(tokens.access_token)

    print("\nRefresh token:")
    print(tokens.refresh_token)

    user = await client.get_current_user(
        tokens.access_token,
    )

    print("\nCurrent user:")
    print(user)


if __name__ == "__main__":
    asyncio.run(main())