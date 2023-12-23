from mitmproxy import http
import re

def request(flow: http.HTTPFlow):
    url = flow.request.url
    for url_filter in ["png", "jpg", "gif"]:
        if url_filter in url:
            flow.response = http.Response.make(
                status_code=200,
                content=b'x',
                headers={"Content-Type": "text/plain"}
            )
            return
    res = re.findall(r"/([-0-9a-zA-Z.]*)\.js$", url)
    if len(res) != 0:
        jsname = res[0]
        print(jsname)
        for white in ["room", "vendors"]:
            if white in jsname:
                return
        else:
            flow.response = http.Response.make(
                status_code=200,
                content=b'x',
                headers={"Content-Type": "text/plain"}
            )
            return
