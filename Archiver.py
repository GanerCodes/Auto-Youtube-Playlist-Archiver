import os, re, sys, json, requests, subprocess
# os.chdir(os.path.split(os.path.abspath(sys.argv[0]))[0])

config = json.load(open("config.json"))
webhook_url = config["discord_webhook_url"]
cookies_path = config['cookies']

playlists = [[i, v, True] for i, v in config['audio_playlists'].items()] + [[i, v, False] for i, v in config['video_playlists'].items()]

playlists = [[i[0], re.sub(r"watch\?v=.{5,}&(?=list)", "playlist?", i[1]), i[2]] for i in playlists]

def tryMakeDir(name, folds):
    if name in folds:
        print(f"Found directory {name}")
    else:
        os.mkdir(i[0])
        print(f"Created directory {name}")

folds = os.listdir()
for i in playlists: tryMakeDir(i[0], folds)

getList = lambda: [[i[0], len(os.listdir(i[0]))] for i in playlists]
def downloader(i):
    return subprocess.Popen(
        ["yt-dlp", "--download-archive", f"{i[0]}/archive.txt", "--embed-thumbnail", "--cookies", cookies_path, "-ciwq"] + (
            ["-x", "-f", "bestaudio", "--audio-format", "mp3"] if i[2] else ["--recode-video", "mp4"]
        ) + ["-o", f"{i[0]}/%(title)s_%(id)s.%(ext)s", i[1]]
    )

def waitDownload(p, i):
    p.wait()
    print(f"Finished downloading playlist {i[0]}")

beforeList = getList()
for p in [(downloader(i), i) for i in playlists]: waitDownload(*p)
afterList = getList()

requests.post(config['discord_webhook_url'], data = {
    'Content-type': 'application/json',
    "username": "Joe",
    "avatar_url": "https://upload.wikimedia.org/wikipedia/en/9/9a/Trollface_non-free.png",
    "content": '\n'.join(f"Downloaded {afterList[i][1] - beforeList[i][1]} new videos to playlist {v[0]}" for i, v in enumerate(beforeList))
})
