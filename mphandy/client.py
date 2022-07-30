from mpd import MPDClient


def client_test():
    client = MPDClient()
    client.timeout = 120
    client.connect("localhost", 6600)
    print(client.mpd_version)
    ret = client.lsinfo("")
    #print(client.lsinfo("Funkwhale/Albums/By name/Homework"))
    #client.close()
    client.disconnect()
    return ret
