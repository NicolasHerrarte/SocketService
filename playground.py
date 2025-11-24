post_req = b"""POST / HTTP/1.1
Host: 127.0.0.1:65432
Connection: keep-alive
Content-Length: 11
sec-ch-ua-platform: "Windows"
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
sec-ch-ua: "Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"
Content-Type: application/x-www-form-urlencoded
sec-ch-ua-mobile: ?0
Accept: */*
Origin: http://localhost:65432
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: http://localhost:65432/
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: es-419,es;q=0.9,en;q=0.8

x=498&y=496"""

body_index = post_req.find(b"\n\n")
body_raw = post_req[:body_index]

print(body_raw)



