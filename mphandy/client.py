from mpd import MPDClient
import mpd
import time

class mpdclient():
    def __init__(self,):
        self.client = MPDClient()
        self.client.timeout = 120

    def conn_test(self):
        while self.client.mpd_version is None:
            try:
                try:
                    self.client.connect("localhost", 6600)
                except ConnectionRefusedError:
                    print("Connection refused, waiting 5 seconds")
                    time.sleep(5)
                    self.conn_test()
            except RecursionError:
                exit()

    def get_song_info(self):
        self.conn_test()
        return self.client.status()

def client_test():
    client = MPDClient()
    client.timeout = 120
    client.connect("localhost", 6600)
    ret = client.lsinfo("")
    #print(client.lsinfo("Funkwhale/Albums/By name/Homework"))
    #client.close()
    client.disconnect()
    return ret
