import asyncio
from pyrogram import Client
import config
import argparse

api_id = config.APP_ID
api_hash = config.APP_HASH


parser = argparse.ArgumentParser(description="TG Backup")
parser.add_argument("--config-dir", '-cd', default='config')

sub_parser = parser.add_subparsers(dest="command")

auth_parser = sub_parser.add_parser("auth")

upload_parser = sub_parser.add_parser("upload")
upload_parser.add_argument("--file", "-f", type=str, required=True)
upload_parser.add_argument("--description", "-d", type=str)
upload_parser.add_argument("--channel", "-c", type=int)
upload_parser.add_argument("--me", "-m", type=bool)
upload_parser.add_argument("--username", '-u', type=str)

args = parser.parse_args()


async def upload():
    if not (args.channel or args.me or args.username):
        print("Please pass either --channel --me or --username")
        exit(-1)
    target = args.channel or args.me or args.username
    async with Client("me", api_id, api_hash, workdir=args.config_dir, no_updates=True) as app:
        await app.send_document(target, args.file, caption=args.description)
        print("document uploaded")


async def auth():
    async with Client("me", api_id, api_hash, workdir=args.config_dir, no_updates=True) as app:
        await app.send_message("self", "Authenticated")


async def main():
    if args.command == 'auth':
        await auth()
    elif args.command == 'upload':
        await upload()
    else:
        parser.print_help()

asyncio.run(main())
