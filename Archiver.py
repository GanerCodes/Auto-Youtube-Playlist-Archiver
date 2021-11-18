import json, re, subprocess, os, sys, requests
os.chdir(os.path.split(os.path.abspath(sys.argv[0]))[0])

config = json.load(open("config.json"))
webhook_url = config["discord_webhook_url"]
playlists = [[i, v] for i, v in config['playlists'].items()]

playlists = [[i[0], re.sub(r"watch\?v=.{5,}&(?=list)", "playlist?", i[1])] for i in playlists]

currentDirs = os.listdir()
for i in playlists:
    if i[0] not in currentDirs:
        os.mkdir(i[0])

getList = lambda: [[i[0], len(os.listdir(i[0]))] for i in playlists]

beforeList = getList()

currentProcesses = [
	subprocess.Popen([
		"yt-dlp", "-q", "--no-progress", "--download-archive", 
		f"{i[0]}/archive.txt", "--embed-thumbnail", "--no-post-overwrites", "-ciw", "-x", "-f", "bestaudio", "--audio-format", "mp3",
		"--cookies", "cookies.txt", "-o", f"{i[0]}/%(title)s_%(id)s.%(ext)s", i[1]]
	) for i in playlists
]
[i.wait() for i in currentProcesses]

afterList = getList()

url = "DISCORD WEBHOOK URL"
j = requests.post(url, data = {
    'Content-type': 'application/json',
    "username": "Joe",
    "avatar_url": "https://upload.wikimedia.org/wikipedia/en/9/9a/Trollface_non-free.png",
    "content": '\n'.join(f"Downloaded {afterList[i][1] - beforeList[i][1]} new videos to playlist {v[0]}" for i, v in enumerate(beforeList))
})
