#!/usr/bin/env python

import os
import sys
from argparse import ArgumentParser

import eyed3
from gmusicapi import Mobileclient
from gmusicapi.exceptions import InvalidDeviceId
from goldfinch import validFileName as vfn
from tqdm import tqdm

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

def npath(path):
    return vfn(path, space='keep', initCap=False).decode('utf-8').rstrip('.')

parser = ArgumentParser()
parser.add_argument(dest='mail',
    help='Your google mail for login.')
parser.add_argument('-o', '--output', dest='output',
                    default=os.path.join(os.getcwd(), 'Music'),
    help='Destination to download files to. Default is ./Music/ (same folder)')
#parser.add_argument('-p', '--password', dest='passwd')
parser.add_argument('-i', '--device-id', dest='device_id', default=0,
    help='Device ID to use - run without argument first to see available device IDs and then use one.')
parser.add_argument('-l', '--log', dest='log', action='store_true',
    help='Enable to have log printed to "log.txt".')

args, unknown = parser.parse_known_args()

login = args.mail
targetDir = args.output

#log_path = os.path.join(os.getcwd(), 'log.txt') if args.log else None

device_id = args.device_id

eyed3.log.setLevel('ERROR')

api = Mobileclient(debug_logging=True)

if not os.path.exists(api.OAUTH_FILEPATH):
    api.perform_oauth(
        storage_filepath=api.OAUTH_FILEPATH,
        open_browser=True
    )

try:
    logged_in = api.oauth_login(
        args.device_id
    )
except InvalidDeviceId as e:
    print(str(e))
    sys.exit()

print('\nSuccessful login:', logged_in)
if not logged_in:
    exit()

pbar = tqdm(api.get_all_songs())

skipped = []
downloaded = []
failed = []

for song in pbar:  # album['tracks']:
    dirName = os.path.join(
        npath(song['artist']),
        npath(song['album'])
    )
    dirPath = os.path.join(
        targetDir,
        dirName
    )

    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

    fileName = '{:02d}. {}'.format(
        song['trackNumber'],
        npath(song['title'])
    )


    filePath = os.path.join(dirPath, fileName)

    if os.path.exists(filePath):
        skipped.append(fileName)
        continue

    #print('downloading: ' + fileName)
    pbar.set_description(fileName)
    try:
        url = api.get_stream_url(song_id=song['id'], quality='hi')
        urlretrieve(url, filePath)
        downloaded.append(fileName)
    except Exception as e:
        print(str(e))
        failed.append(fileName)
        continue

    audio = eyed3.load(filePath)
    if audio.tag is None:
        audio.tag = eyed3.id3.Tag()
        audio.tag.file_info = eyed3.id3.FileInfo(filePath)
    audio.tag.artist = song['artist']
    audio.tag.album = song['album']
    audio.tag.title = song['title']
    audio.tag.track_num = song['trackNumber']
    audio.tag.save()

if args.log:
    try:
        with open('log.txt', 'w') as f:
            f.write(
                (
                    'D: {} F: {} S: {}\n'
                    'Downloaded:\n'
                    '\t{}\n'
                    'Failed:\n'
                    '\t{}\n'
                    'Skipped:\n'
                    '\t{}\n'
                ).format(
                    len(downloaded), len(failed), len(skipped),
                    '\n\t'.join(downloaded),
                    '\n\t'.join(failed),
                    '\n\t'.join(skipped),
                )
            )
    except Exception as e:
        print(str(e))

print('done!')
