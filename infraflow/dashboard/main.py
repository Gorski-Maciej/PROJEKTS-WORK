import flet as ft

def main(page: ft.Page):
    page.title = "InfraFlow Dashboard"
    page.add(ft.Text("InfraFlow Dashboard", style=ft.TextThemeStyle.HEADLINE_MEDIUM))
    page.add(ft.Text("Servers online: 3"))

ft.app(target=main, view=ft.WEB_BROWSER, port=8080)
