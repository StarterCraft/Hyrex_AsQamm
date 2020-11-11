from kivy.lang import Builder

from kivymd.app import MDApp


KV = """
Screen:

    MDToolbar:
        title: "My first app"
        elevation: 10
        md_bg_color: app.theme_cls.primary_color
        left_action_items: [["menu", lambda x: x]]
        pos_hint: {"top": 1}

    MDRaisedButton:
        text: "Hello World"
        pos_hint: {"center_x": .5, "center_y": .5}
"""


class HelloWorld(MDApp):
    def build(self):
        return Builder.load_string(KV)


HelloWorld().run()