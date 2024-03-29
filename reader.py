import zlib, brotli, json
import time

showed = set()
gift = set()
come = set()
def decode(data):
    global showed, come, gift
    protocol = int.from_bytes(data[6:8])
    if protocol == 1 or protocol > 3:
        return
    msgs = split_msg([lambda x:x, None,
                      lambda x:zlib.decompress(x[16:]),
                      lambda x:brotli.decompress(x[16:])][protocol](data))
    for i in msgs:
        if i['cmd'] == "DANMU_MSG": #发弹幕
            tm = int(i['info'][9]['ts'])
            uname = i['info'][2][1]
            token = f"{tm}#{uname}"
            if token not in showed and tm > time.time() - 10:
                if len(showed) == 2000:
                    showed = set(sorted(showed)[1500:])
                showed.add(token)
                tm = ts2time(tm)
                return f"[{tm}] {uname}: {i['info'][1]}"
        elif i['cmd'] == "INTERACT_WORD": # 进房间
            tm = int(i['data']['timestamp'])
            uname = i['data']['uname']
            token = f"{tm}^{uname}"
            if token not in come and tm > time.time() - 10:
                if len(come) == 2000:
                    come = set(sorted(come)[1500:])
                come.add(token)
                tm = ts2time(tm)
                return f"@C󰍖 [{tm}] {uname}"
        elif i['cmd'] == "WATCHED_CHANGE": # 历史观看人数变化
            return f"@W{i['data']['num']}"
        elif i['cmd'] == "SEND_GIFT": # 送礼物
            tm = int(i['data']['timestamp'])
            uname = i['data']['uname']
            token = f"{tm}!{uname}"
            if token not in gift and tm > time.time() - 10:
                if len(gift) == 2000:
                    gift = set(sorted(gift)[1500:])
                gift.add(token)
                tm = ts2time(tm)
                return f"@G󱛱 [{tm}] {i['data']['uname']} -> {i['data']['num']} {i['data']['giftName']}"
        #else:
        #    return i['cmd']
        # TODO?

def ts2time(ts):
    return time.strftime("%H:%M:%S", time.localtime(ts))

def split_msg(all:bytes):
    msgs = []
    start = 0
    end = len(all)
    while start < end:
        msgend = start + int.from_bytes(all[start:start+4])
        msgs.append(json.loads(all[start:msgend][16:].decode()))
        start = msgend
    return msgs
    
def test():
    # heart beat
    #size = [4, 2, 2, 4, 4]
    data = b'\x00\x00\x02\xbe\x00\x10\x00\x03\x00\x00\x00\x05\x00\x00\x00\x00\x1b\x85\x05\x00\x9c\x059\x19\xbe\n\'\xf5\xc40\xc5\xf1\xb7M\x91\xcd\xee$\xcf,\x87$jmAY\x10X@\xffV\xea\xac\xea\xb7\xbeLt\x06\xea\x9e+\xc0\xca\xf2\x9c\x93\xc8a\x85\xa4G\x8d\x8b\xae\xf9\xe7b\xd1\xb1\xd9,\xe5\xab\xc9\x85o`\x89\xaf\x12\xd0\xe5\xfc\xe2^\x0b\xf6\xf1F\x10\xd7\xbf\x9b\x97\xda\x1b\xd0\x9f\x00\x05#zsV:\x1d\xf3-\xe89+\xc2W\xad\x1b \x07\xe3d\xa5\xeb\x8b\x14\x13k\x10\xa7GW\x97\x8fry\x7f\x01\x82\xbe\x7f\x86u\xad\x88)J\x89\xb3\xccT\x01q\xceV\x087QM\x1apb%?=\xefB\x8a0\xc9\x85K{@\xbdz\x81\x8d.\xf4\xf0\x06\xb8\xaf\x8a\x8a\xa0\x8e]\xf4\xb7J \x18\xc0\xce\xebB\x04\r\xdf[\xc5\xac\x86\xd8N#\xc5l\x9a\x87U\xef}\x1a~HiT\xda\xe54\x8c\xe5\x07$J\x02\xab\xf8+\xabQE\x07\x88\x04\x1f)o\xd7\x04\xd4\xf0\x94\x9eF\xa5\x11\xc5&l\xc9\xfbVI~\x86H\xe3\xdeJ\xa8p"d;\xbb\xf5q\xb5Kt\x18\x8d\x81\xc6\xf9c\rt\x12\x15H0\xa5\xa5M*A\x80\xc8J\n\xaeM\xa2V\x14c\xc5@\xb02\xd5\xd2~X\xa6\x18C\xd0\xcd\xddJ~\xc6\x14<\xae{\xd8z\x95:d\x91\x04T\xa6\xf6\xd6\x8d\xe6\x92]\xf0\x0f\xe4m\x00EO\x87\xf5\x96J\xe1\x86\xf8\xedi\'\x93]\xf4\xc6i4@\xb1@\xe8\xdd\x9as\x1aU\xcf\xa9i,\x9c\x0co#\xf6\x9d\xc9\x88\xbe\x85\x11\xe7\x0f\xa1\xfa}\xb63\x1a\x95\x8d\xfd\xca\xe6\xedh\xcf:2\x81@\xb1\xff\x8b\x8ft\x03cc\np\xff\x15\xd6\xdc~|\x1a?%\xc4.<\x81\xab\xf5\xa9\xe8\xa0\xf1\x16\x00\x82\xb1\r\x9cX8\xe9\xe8\xeb*G\xe6\x0bO\xa1\xb6\xe3mN\xf5\xa0\xbcz\t\x06<-\x0c2\x17\xf4\x04\x08EN \x121\x81\xc8?\xe2dK\x1dEr\x81\xf9\xa7\x9dY\xf0on\xdcz\xdc\x89\xb2\xe3\xa9\x1b\xe2<=\x8c\x95\x8f\xcd\x8d\xef\x97:\x8b\xcc\xcb\xcb2\x1ep\x8a5\xba\xd9\xe4n\x86\x98\xb6&\x02\xe8j\xdc\x9d\xc10\xba\x0c\x12lgFk\xb790\xf5 R\x90;K\x1a\xb9\x7fIR@\x07rJK\xbbC\x80@\x86v\xc4\x85\x9e\xddl\xbd8\x9f%DUCU\x96z\xa8v\x01lF\x17\xc9\xb2bnC\x11\xa0\xc1\xf3\x12\xfe\x90\x0e\xc9\xff\xf5\xf3\xe6\xdf\xea\xeb\xe7\xc9w/\xb0\x12\xa1LE\x1e8\x01\xa4\x88\xa30U\xc4\x17b\xdd\x9dp\xa8\x9e<\xd1O\x8be\x11\xa7\xc0\x84e\x8f\xf4.\x04G\x1e\xe2\x83\x17\x10\xcft\xec\x85\x07\x01\xdea#\xfc\x04a\xe2\x11\xc9Q\xa4\xefY\xfe\xa2\'t\xfe0\xab(b\xa6\x9a\x9b\x9f\xbc\x8d>\xe5}\x8e<d\xed\x01'
    decode(data)

if __name__ == "__main__":
    test()
