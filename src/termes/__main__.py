import asyncio
import secrets

from sqlalchemy.ext.asyncio import create_async_engine
from typer import Typer
from rich import print

from termes import database
from termes.application import settings
from termes.models.models import Base

app = Typer()


async def create_tables():
    if settings.DATABASE_URL is None:
        print("Error: DATABASE_URL not defined (run 'export DATABASE_URL=\"your_database_url\"')")
        return
    database.engine = create_async_engine(settings.DATABASE_URL, echo=True)
    async with database.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    print(f"Created tables in '{settings.DATABASE_URL}'")


async def setup():
    print("[bold]Welcome to Termes Server setup helper[/]")
    print()
    print("First, set the [yellow]DATABASE URL[/] (example: 'sqlite+aiosqlite:///filename.sqlite' for SQLite database)")
    database_url = input("DATABASE URL: ")
    print()
    print("Next, set [yellow]PASSWORD HASH SALT[/] if exist, else skip this step (press Enter)")
    password_hash_salt = input("PASSWORD HASH SALT: ")
    if len(password_hash_salt) == 0:
        password_hash_salt = secrets.token_hex(32)
        print(f"Generated new [yellow]PASSWORD HASH SALT[/]: {password_hash_salt!r}")
    print()
    print("Set session [yellow]TOKEN HASH SALT[/] if exist, else skip this step (press Enter)")
    token_hash_salt = input("TOKEN HASH SALT: ")
    if len(token_hash_salt) == 0:
        token_hash_salt = secrets.token_hex(32)
        print(f"Generated new [yellow]TOKEN HASH SALT[/]: {token_hash_salt!r}")
    print()
    print("Set [yellow]SESSION TOKEN LENGTH[/]")
    try:
        session_token_length = int(input("SESSION TOKEN LENGTH: "))
    except ValueError:
        print("[bold red]Setup failed![/] [yellow]SESSION TOKEN LENGTH[/] must be an integer value")
        return
    print("Set [yellow]SESSION LIFETIME[/]")
    try:
        session_lifetime = int(input("SESSION LIFETIME: "))
    except ValueError:
        print("[bold red]Setup failed![/] [yellow]SESSION LIFETIME[/] must be an integer value")
        return
    print(
        f"""
        Check configuration:
        - [yellow]DATABASE URL[/]: {database_url!r}
        - [yellow]PASSWORD HASH SALT[/]: {password_hash_salt!r}
        - [yellow]TOKEN HASH SALT[/]: {token_hash_salt!r}
        - [yellow]SESSION TOKEN LENGTH[/]: {session_token_length!r}
        - [yellow]SESSION LIFETIME[/]: {session_lifetime!r}
        """
    )
    valid = input("If this valid? [Y/n]: ")
    if valid.lower() == "y":
        print("[bold green]Successful setup![/] Then run server by typing 'python3 -m termes:app'")
    else:
        print("[bold red]Setup canceled![/]")


app.command(name="create-tables")(lambda: asyncio.run(create_tables()))
app.command(name="setup")(lambda: asyncio.run(setup()))

if __name__ == "__main__":
    app()
