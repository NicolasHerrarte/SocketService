success = b"HTTP/1.1 200 OK"
error = b"HTTP/1.1 400 Bad Request"

cors_options = [b"Access-Control-Allow-Origin: *",
                b"Access-Control-Allow-Methods: POST, GET, OPTIONS",
                b"Access-Control-Allow-Headers: *"]

def document_type(t):
    return f"Content-Type: {t}".encode("utf-8")
