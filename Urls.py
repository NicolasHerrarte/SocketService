from Header import *
from Views import views

endpoints = [Path("/", views.landing_page),
             Path("/send_mouse_pos", views.update_user_position),
             Path("/get_mouse_data", views.get_position_data)]