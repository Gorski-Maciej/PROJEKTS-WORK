import asyncio
import json
import logging
import os

import flet as ft
import websockets

ENGINE_WS_URL = os.getenv("ENGINE_WS_URL", "ws://localhost:8001/ws")
WS_RECONNECT_SECONDS = float(os.getenv("WS_RECONNECT_SECONDS", "3"))

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("netguardian-dashboard")


class AlertDashboard:
    def __init__(self):
        self.alerts_list = ft.ListView(expand=True, spacing=5)
        self.status_text = ft.Text("Disconnected")

    async def connect_websocket(self, page: ft.Page):
        while True:
            try:
                self.status_text.value = "Connecting..."
                page.update()

                async with websockets.connect(ENGINE_WS_URL) as websocket:
                    self.status_text.value = "Connected"
                    page.update()
                    logger.info("connected to %s", ENGINE_WS_URL)

                    while True:
                        message = await websocket.recv()
                        alert = json.loads(message)
                        self.alerts_list.controls.append(
                            ft.ListTile(
                                title=ft.Text(f"Alert from {alert.get('src_ip', 'unknown')}"),
                                subtitle=ft.Text(f"Score: {alert.get('score', 0):.3f}"),
                                leading=ft.Icon(ft.icons.WARNING),
                            )
                        )
                        page.update()
            except Exception as exc:  # keep dashboard alive on transient websocket failures
                logger.warning("websocket error: %s", exc)
                self.status_text.value = f"Disconnected (retry in {WS_RECONNECT_SECONDS:.0f}s)"
                page.update()
                await asyncio.sleep(WS_RECONNECT_SECONDS)


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
