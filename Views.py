import os
from Header import HttpResponseFormat as HRES
from Header import Content
import json
import Options

root_template_dir = "templates"


class ServerViews:
    def __init__(self):
        self.connections = 0
        self.session_data = {}

    def landing_page(self, request):
        response = HRES()
        res_content = Content(os.path.join(root_template_dir, "base.html"), "PATH")
        response.content = res_content
        response.content_type = "text/html"

        cookies = request.strip_cookies()

        if "session_id" not in cookies.keys():
            self.connections += 1
            response.add_header_option(bytes(f"Set-Cookie: session_id={self.connections}", "utf-8"))

        return response

    def document_fetch(self, request):
        response = HRES()
        if request.method == "GET":
            file_path = request.directory
            path_args = tuple(file_path.split("/"))

            accept_type = request.get_value_header("Accept")

            res_content = Content(os.path.join("static", *path_args), "PATH")
            response.content = res_content
            response.content_type = accept_type
        else:
            response.status = 400

        return response

    def update_user_position(self, request):
        response = HRES()
        if request.method == "POST":

            cookies = request.strip_cookies()
            if "session_id" in cookies.keys():
                with open('session_data.json', 'r') as file:
                    temp_session_data = json.load(file)
                    temp_session_data[cookies["session_id"]] = request.content
                with open('session_data.json', 'w') as file:
                    json.dump(temp_session_data, file)

                print("Updating XY")
                print(temp_session_data)

                response.add_all_header_options(Options.cors_options)
        else:
            response.status = 400

        return response

    def get_position_data(self, request):
        response = HRES()
        if request.method == "GET":
            cookies = request.strip_cookies()
            if "session_id" in cookies.keys():
                with open('session_data.json', 'r') as file:
                    filtered_session_data = json.load(file)
                    del filtered_session_data[cookies["session_id"]]

                res_content = Content(filtered_session_data,"DICT")
                response.content = res_content
                response.content_type = "application/json"
                print("Sending XY")
        else:
            response.status = 400

        return response


views = ServerViews()
