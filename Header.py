import os
import re
import json

import Options
from Options import *
from Utils import auto_string_conversion

class Path:
    def __init__(self, url, response):
        self.url = url
        self.response = response

class Content:
    def __init__(self, source, src_type):
        self.source = source
        self.src_type = src_type

    def serve(self):
        if self.src_type == "PATH":
            with open(self.source, "rb") as f:
                content = f.read()

        elif self.src_type == "DICT":
            content = json.dumps(self.source).encode('utf-8')

        return content


class HttpResponseFormat:
    def __init__(self, status=200):
        self.status = status
        self.header_options = []
        self.content = None
        self.content_type = None

    def add_header_option(self, option, position=None):
        if position is None:
            self.header_options.append(option)
        else:
            self.header_options.insert(position, option)

    def add_all_header_options(self, options):
        for option in options:
            self.header_options.append(option)

    def __call__(self):
        byte_string = b""

        if self.status == 200:
            self.add_header_option(Options.success, 0)

        if self.status == 400:
            self.add_header_option(Options.error, 0)

        if self.content_type is not None:
            self.add_header_option(Options.document_type(self.content_type))

        for hopt in self.header_options:
            byte_string = byte_string + hopt + b"\r\n"

        byte_string = byte_string + b"\r\n"

        if self.content is None:
            return byte_string

        try:
            content = self.content.serve()
        except:
            print(f"There was an error getting content")
            print(self.content.source)
            error_response = HttpResponseFormat(400)
            return error_response()

        byte_response = byte_string + content

        return byte_response

    def __str__(self):
        return self().decode("utf-8")

class HttpRequestFormat:
    def __init__(self, request):
        self.header_options = self.get_options_header(request)
        self.content = self.get_response_values(request)
        self.cookies = self.strip_cookies()
        self.method, self.directory, self.version = self.get_head_values()

    def get_head(self):
        return self.header_options[0]

    def get_head_values(self):
        head = self.get_head()
        method, directory, version = head.decode("utf-8").split(" ")
        return method, directory, version

    def get_type_header(self, header_type):
        pattern = re.compile(bytes(f"^{header_type}:\s", "utf-8"))
        match_arr = [x for x in self.header_options if pattern.match(x)]
        if len(match_arr) > 0:
            return match_arr[0]
        else:
            return None

    def get_value_header(self, header_type):
        header_line = self.get_type_header(header_type)
        if header_line is None:
            return None

        header_value = header_line[len(f"{header_type}: "):]
        return header_value.decode("utf-8")

    def strip_cookies(self):
        cookies_line = self.get_type_header("Cookie")
        if cookies_line is None:
            return {}

        cookies_raw = cookies_line[len("Cookie: "):].split(b";")
        cookies_dict = {}
        for c in cookies_raw:
            equal_index = c.index(b"=")
            # Will strip every " in the string so cookies should not include "
            # It will be fixed
            cookies_dict[c[:equal_index].strip().decode("utf-8")] = c[equal_index + 1:].strip().replace(b"\"", b"").decode("utf-8")

        return cookies_dict

    def get_response_values(self, body_request):
        body_index = body_request.find(b"\r\n\r\n")
        if body_index == -1 or (body_index+4) == len(body_request):
            return {}

        body_raw = body_request[body_index + 4:]
        body_arr = body_raw.split(b"&")
        body_dict = {}
        for raw in body_arr:
            #print(raw)
            k, v = raw.split(b"=")
            body_dict[k.decode("utf-8")] = auto_string_conversion(v)

        return body_dict

    def get_options_header(self, body_request):
        body_index = body_request.find(b"\n\n")
        print(body_request)
        body_trimmed = bytes(body_request)
        if body_index != -1:
            body_trimmed = body_trimmed[:body_index]

        headers_arr = body_trimmed.splitlines()
        return headers_arr





