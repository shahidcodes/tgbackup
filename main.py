#!/bin/env python
import asyncio
import os
from pyrogram import Client
import config
import argparse
import subprocess

api_id = config.APP_ID
api_hash = config.APP_HASH
bot_token = config.BOT_TOKEN

ONE_POINT_NINE_GB = 1.9e+9


parser = argparse.ArgumentParser(description="TG Backup")
parser.add_argument("--config-dir", '-cd', default='config')
parser.add_argument('--session-name', '-sm', default='tgbot')

sub_parser = parser.add_subparsers(dest="command")
auth_parser = sub_parser.add_parser("auth")
echo_parser = sub_parser.add_parser("echo")
echo_parser.add_argument('--target', '-t', type=str, required=True)
upload_parser = sub_parser.add_parser("upload")
upload_parser.add_argument("--file", "-f", type=str, required=True)
upload_parser.add_argument("--description", "-d", type=str)
upload_parser.add_argument("--target", "-t", type=str, required=True)


args = parser.parse_args()

if args.target.startswith('-100'):
    args.target = int(args.target)


app = Client(
    args.session_name,
    api_id=api_id,
    api_hash=api_hash,
    workdir=args.config_dir,
    no_updates=True,
    bot_token=bot_token
)


async def upload():
    target = args.target
    size = os.path.getsize(args.file)
    files = []
    ext = args.file.split('.')[1] or ''
    if size > ONE_POINT_NINE_GB:
        subprocess.run(
            ["split", "-b", "1800m", args.file, "splitted-file"]
        )
        for file in os.listdir('.'):
            if file.find('splitted-file') != -1:
                files.append(file)
    else:
        files.append(args.file)
    async with app:
        for file in files:
            await app.send_document(target, file, caption=args.description, file_name=f"{os.path.basename(file)}.{ext}")
            print("document uploaded")
            os.remove(file)


async def auth():
    async with app:
        await app.send_message(args.target, "echo")


async def echo():
    async with app:
        await app.send_message(args.target, "Hello from bot")


async def main():
    if args.command == 'auth':
        await auth()
    elif args.command == 'upload':
        await upload()
    elif args.command == 'echo':
        await echo()
    else:
        parser.print_help()

asyncio.run(main())
