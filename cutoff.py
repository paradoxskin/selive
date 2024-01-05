from mitmproxy import http, ctx
from reader import decode
from ui import UI
from re import findall
from threading import Thread, Condition
#from subprocess import Popen
from time import sleep
from se import start_se

# step 1. start ui
ui = UI()
ui.change_title("waiting...")
ui.echo("[i] hi~")
ui.send_gift("󱛯 ")
ui.come_in("󰍖 ")

# step 2. start selenium
shutdown = Condition()
se = Thread(target=start_se,
            args=(ui.echo,
                  shutdown))
sleep(.2)
se.start()
ui.echo("[i] se starting...")
#process = Popen(["python", "./se.py"])

# step 3. keyboard listen
def quitall():
    with shutdown:
        shutdown.notify()
    ctx.master.shutdown()
    ui.echo("[+] bye ~")
    sleep(1)
keyboard = Thread(target=ui.start,
                  args=(quitall,))
keyboard.start()

# rules
def request(flow: http.HTTPFlow):
    url = flow.request.url
    for url_filter in ["png", "jpg", "gif", "wpeg"]:
        if url_filter in url:
            flow.response = http.Response.make(
                status_code=200,
                content=b'x',
                headers={"Content-Type": "text/plain"}
            )
            return
    res = findall(r"/([-0-9a-zA-Z.]*)\.js$", url)
    # js blacklist
    if len(res) != 0:
        jsname = res[0]
        for black in ["skin", "fonts", "theme", "navbar", "log", "pv", "perform", "remote", "magic"]:
            if black in jsname:
                flow.response = http.Response.make(
                    status_code=200,
                    content=b'x',
                    headers={"Content-Type": "text/plain"}
                )
                return

class SniffWebSocket:
    def __init__(self):
        pass
    def websocket_message(self, flow: http.HTTPFlow):
        msgs = []
        for flow_msg in flow.websocket.messages:
            packet = flow_msg.content
            msg = decode(packet)
            if msg == None:
                continue
            msgs.append(msg)
        msgs.sort()
        for msg in msgs:
            if msg[0] == "[":
                ui.echo(msg)
            elif msg[:2] == "@W":
                ui.change_title(f"󰓠 {msg[2:]}")
            elif msg[:2] == "@C":
                ui.come_in(msg[2:])
            elif msg[:2] == "@G":
                ui.send_gift(msg[2:])

addons = [SniffWebSocket()]
