import asyncio
import json
import os

import flet as ft
import websockets

ENGINE_WS_URL = os.getenv("ENGINE_WS_URL", "ws://localhost:8001/ws")


class AlertDashboard:
    def __init__(self):
        self.alerts_list = ft.ListView(expand=True, spacing=5)
        self.status_text = ft.Text("Disconnected")

    async def connect_websocket(self, page: ft.Page):
        async with websockets.connect(ENGINE_WS_URL) as websocket:
            self.status_text.value = "Connected"
            page.update()
            while True:
                message = await websocket.recv()
                alert = json.loads(message)
                self.alerts_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(f"Alert from {alert['src_ip']}"),
                        subtitle=ft.Text(f"Score: {alert['score']:.3f}"),
                        leading=ft.Icon(ft.icons.WARNING),
                    )
                )
                page.update()


def main(page: ft.Page):
    page.title = "NetGuardian Dashboard"
    page.theme_mode = ft.ThemeMode.DARK
    dash = AlertDashboard()

    header = ft.Text("NetGuardian 2.0 - Live Alerts", style=ft.TextThemeStyle.HEADLINE_MEDIUM)
    status_row = ft.Row([ft.Text("WebSocket: "), dash.status_text])
    alerts_container = ft.Container(
        content=dash.alerts_list,
        border=ft.border.all(1, ft.colors.OUTLINE),
        border_radius=5,
        padding=10,
        expand=True,
    )

    page.add(header, status_row, alerts_container)
    page.run_task(dash.connect_websocket, page)


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8080)
