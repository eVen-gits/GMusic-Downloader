# GMusic-Downloader - FULL LIBRARY EDITION
Download music from Google Play Music

based on [wlp2s0/GMusic-Downloader](https://github.com/wlp2s0/GMusic-Downloader) - thank you very much for this!

## Motivation

Since Google Play Music is being discontinued, I needed a quick way to recover my music before it's gone forever.
Google's client didn't work for me, nor did the sync or manual download (various reasons).
Luckly, *wlp2s0* had created a template from which I was able to extend this piece of software to download entire library.
I haven't tested it extensively, so bugs are very likely. I don't know how it works with libraries based on GPM's subscription.
Either way, I hope this helps someone. If you find some bugs, let me know and I'll try to find some time to fix it.

```
pip install -r requirements.txt
python gmusic-dl.py [-h] [-o OUTPUT] [-i DEVICE_ID] mail
```
## Example:

```
python gmusic-dl.py -o "/home/even-gits/Music/" foo@bar.com
```

It will fail at start and print out your available device identifiers. Use one and proceed with additional command switch like so:

```
python gmusic-dl.py -o "/home/even-gits/Music/" -i "123123123" foo@bar.com
```
