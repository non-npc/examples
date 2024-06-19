from typing import List

import flet as ft
from components.app_view import AppView
from components.new_message_view import NewMessageWebView


class SecondaryMenuAction(ft.TextButton):
    def __init__(self, text, icon, on_click):
        super().__init__()
        self.content = ft.Row(
            controls=[
                ft.Icon(icon),
                ft.Text(text),
            ]
        )
        self.style = ft.ButtonStyle(
            padding=10
            # bgcolor={
            #     ft.ControlState.HOVERED: ft.colors.PRIMARY_CONTAINER,
            #     ft.ControlState.FOCUSED: ft.colors.RED,
            #     ft.ControlState.DEFAULT: ft.colors.SURFACE,
            # }
        )
        self.on_click = on_click


class WebView(AppView):
    def __init__(self):
        super().__init__()
        self.logo = ft.Row(
            controls=[
                ft.Container(
                    padding=5, content=ft.Image(src=f"logo.svg"), width=50, height=50
                ),
                ft.Text(
                    "FletMail",
                    width=100,
                    style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD),
                ),
            ]
        )

        self.nav_rail_destinations = [
            ft.NavigationRailDestination(
                label="Mail",
                icon=ft.icons.MAIL_OUTLINED,
            ),
            ft.NavigationRailDestination(
                label="Chat",
                icon=ft.icons.CHAT_BUBBLE_OUTLINE,
            ),
            ft.NavigationRailDestination(
                label="Meet",
                icon=ft.icons.VIDEO_CHAT_OUTLINED,
            ),
        ]
        self.open_menu_button = ft.IconButton(
            icon=ft.icons.MENU, on_click=self.open_close_secondary_menu
        )
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            # width=100,
            min_extended_width=400,
            leading=self.open_menu_button,
            expand=True,
            group_alignment=-0.9,
            destinations=self.nav_rail_destinations,
            on_change=self.nav_rail_changed,
        )

        self.compose_button = ft.FloatingActionButton(
            icon=ft.icons.CREATE, text="Compose", on_click=self.compose_clicked
        )
        self.mail_actions = ft.Column(
            [
                SecondaryMenuAction(
                    text="Inbox", icon=ft.icons.MAIL, on_click=self.inbox_clicked
                ),
                SecondaryMenuAction(
                    text="Starred", icon=ft.icons.STAR, on_click=self.starred_clicked
                ),
                SecondaryMenuAction(
                    text="Spam", icon=ft.icons.DELETE, on_click=self.spam_clicked
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=0,
        )
        self.chat_actions = ft.Column([ft.TextButton("Chat1"), ft.TextButton("Chat2")])

        self.mail_menu = ft.Column(
            [self.compose_button, self.mail_actions],
            width=150,
        )
        self.chat_menu = ft.Column([self.compose_button, self.chat_actions], width=150)

        self.messages_list = ft.ListView(controls=self.get_message_tiles(), expand=True)

        self.message_view = ft.Column(
            controls=[
                ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.back_to_messages),
                ft.Text(value="This is the email message"),
            ],
            visible=False,
        )

        self.mail_view = ft.Row(
            controls=[
                self.mail_menu,
                ft.Container(
                    content=ft.Column([self.messages_list, self.message_view]),
                    expand=True,
                    bgcolor=ft.colors.WHITE,
                ),
            ],
            expand=True,
        )

        self.chat_view = ft.Row(
            controls=[
                self.chat_menu,
                ft.Container(
                    content=ft.Text("Chat View"),
                    expand=True,
                    bgcolor=ft.colors.WHITE,
                ),
            ],
            expand=True,
            visible=False,
        )

        self.meet_view = ft.Container(
            content=ft.Text("Meet View"),
            expand=True,
            bgcolor=ft.colors.WHITE,
            visible=False,
        )

        self.controls = [
            ft.Row(
                [
                    ft.Column(
                        controls=[
                            self.rail,
                        ],
                    ),
                    ft.Pagelet(
                        appbar=ft.AppBar(
                            leading=self.logo,
                            actions=[
                                ft.CircleAvatar(
                                    foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
                                    content=ft.Text("FF"),
                                ),
                            ],
                        ),
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    self.mail_view,
                                    self.chat_view,
                                    self.meet_view,
                                ],
                            ),
                            expand=True,
                        ),
                        expand=True,
                    ),
                ],
                expand=True,
            )
        ]

    def inbox_clicked(self, e):
        print("Inbox clicked")
        # e.control.style.bgcolor = ft.colors.SECONDARY_CONTAINER
        self.page.update()

    def starred_clicked(self, e):
        print("Starred clicked")

    def spam_clicked(self, e):
        print("Spam clicked")

    def nav_rail_changed(self, e):
        print(f"Selected action: {e.control.selected_index}")
        if e.control.selected_index == 0:
            self.display_inbox()

        if e.control.selected_index == 1:
            self.display_chat()

        if e.control.selected_index == 2:
            self.display_meet()

        self.update()

    def open_close_secondary_menu(self, e):
        print("Open secondary menu or close secondary menu")
        self.mail_menu.visible = not self.mail_menu.visible
        self.chat_menu.visible = not self.chat_menu.visible
        self.update()

    def compose_clicked(self, e):
        print("Open new message dialog")
        self.page.views.append(NewMessageWebView())
        self.page.update()

    def get_message_tiles(self):
        messages_list = []
        for message in self.messages:
            messages_list.append(
                ft.ListTile(
                    # data=message.id,
                    data=message,
                    leading=ft.Row(
                        width=150,
                        controls=[ft.Checkbox(), ft.Text(message.author, size=14)],
                    ),
                    title=ft.Text(
                        spans=[
                            ft.TextSpan(
                                text=message.title,
                                style=ft.TextStyle(weight=ft.FontWeight.W_600, size=14),
                            ),
                            ft.TextSpan(
                                text=f" - {message.body}",
                                style=ft.TextStyle(weight=ft.FontWeight.W_100, size=14),
                            ),
                        ],
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    trailing=ft.Text(value=message.date),
                    on_click=self.message_clicked,
                )
            )
        return messages_list

    # def get_message(self, id):
    #     for message in self.messages:
    #         if message.id == int(id):
    #             print("Found message!")
    #             return message

    def message_clicked(self, e):
        print("Message clicked!")
        # self.selected_message_id = e.control.data
        self.selected_message_id = e.control.data.id
        self.display_message(e.control.data)
        route = f"{self.page.route}/{e.control.data.id}"
        self.page.go(route)

    def display_message(self, message):
        print(f"Display message for {message.id}")
        self.messages_list.visible = False
        self.message_view.visible = True
        self.message_view.controls[1].value = message.body  # Body of the message
        self.page.update()

    def back_to_messages(self, e):
        print("Go back to messages!")
        self.selected_message_id = None
        self.messages_list.visible = True
        self.message_view.visible = False
        self.page.go("/inbox")

    def display_inbox(self):
        print("Display inbox")
        self.mail_view.visible = True
        self.chat_view.visible = False
        self.meet_view.visible = False
        if self.selected_message_id == None:
            self.page.go("/inbox")
        else:
            self.page.go(f"/inbox/{self.selected_message_id}")

    def display_chat(self):
        print("Display chat")
        self.mail_view.visible = False
        self.chat_view.visible = True
        self.meet_view.visible = False
        self.page.go("/chat")

    def display_meet(self):
        print("Display meet")
        self.mail_view.visible = False
        self.chat_view.visible = False
        self.meet_view.visible = True
        self.page.go("/meet")
