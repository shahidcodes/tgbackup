#!/bin/env python
import asyncio
import os
from pyrogram import Client
import config
import argparse
import subprocess

api_id = config.APP_ID
api_hash = config.APP_HASH

ONE_POINT_NINE_GB = 1.9e+9


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

    async with Client("me", api_id, api_hash, workdir=args.config_dir, no_updates=True) as app:
        for file in files:
            await app.send_document(target, file, caption=args.description, file_name=f"{os.path.basename(file)}.{ext}")
            print("document uploaded")
            os.remove(file)


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
