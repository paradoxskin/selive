from mitmproxy import http
import re

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
    res = re.findall(r"/([-0-9a-zA-Z.]*)\.js$", url)
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
            # TODO
            print(packet)

addons = [
    SniffWebSocket()
]
