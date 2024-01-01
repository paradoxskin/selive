from mitmproxy import http, ctx
from reader import decode
from ui import UI
from re import findall
from threading import Thread
from subprocess import Popen
from time import sleep

# step 1. start ui
ui = UI()
ui.change_title("hello, world")
ui.echo("hi~")

# step 2. start selenium
process = Popen(["python", "./se.py"])
sleep(.5)
ui.echo("[+] start selenium")

# step 3. keyboard listen
keyboard = Thread(target=ui.start,
                            args=(lambda :(ctx.master.shutdown(),
                                           process.send_signal(2) ),))
keyboard.start()
sleep(.5)
ui.echo('[i] press "q" to quit')

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
        for flow_msg in flow.websocket.messages:
            packet = flow_msg.content
            ui.echo(decode(packet))

addons = [SniffWebSocket()]
