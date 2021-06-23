import os

from transmission_rpc import Client



import urllib.request, json
with urllib.request.urlopen("http://bidentify.jerryhopper.com/api/hashes.list") as url:
    data = json.loads(url.read().decode())
    print(data)

class nodeTorrent:

    def __init__(self,host,port,usern,passw):
        self.host = host
        self.port = port
        self.usern = usern
        self.passw = passw

        self.optionVerbose=False

    def seedTorrent(self,torrentFile,downloadDir):
       if not os.path.exists(torrentFile):
          print("error, torrent not found.")
          sys.exit()
       if not os.path.exists(downloadDir):
          print("error, download-dir doesnt exist.")
          sys.exit()
       if not os.path.isdir(downloadDir):
          print("error, download-dir isnt a directory")
          sys.exit()

       c = Client(host=self.host, port=self.port, username=self.usern, password=self.passw)
       c.add_torrent(torrentFile, download_dir=downloadDir)



#filemirror = nodeTorrent("localhost",9091,"root","webturd123")
#filemirror.seedTorrent("/mnt/datavault/dietpi_userdata/bidentify-data/torrents/ffe7dd6edd28ed3f1a234f8078f8070a.torrent","/mnt/datavault/dietpi_userdata/bidentify-data")
