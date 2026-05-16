import json
import os
import threading
from typing import Any

import flet as ft
import requests
from websocket import WebSocketApp

ENGINE_URL = os.getenv('ENGINE_URL', 'http://localhost:8000')
API_USER = os.getenv('DASHBOARD_USER', 'viewer')
API_PASS = os.getenv('DASHBOARD_PASSWORD', 'viewer123')


def get_token() -> str | None:
    try:
        response = requests.post(
            f'{ENGINE_URL}/token',
            data={'username': API_USER, 'password': API_PASS},
            timeout=5,
        )
        response.raise_for_status()
        return response.json().get('access_token')
    except Exception:
        return None


def fetch_json(path: str, token: str | None) -> Any:
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    response = requests.get(f'{ENGINE_URL}{path}', headers=headers, timeout=5)
    response.raise_for_status()
    return response.json()


def main(page: ft.Page):
    page.title = 'InfraFlow Dashboard'
    page.scroll = ft.ScrollMode.AUTO

    title = ft.Text('InfraFlow Dashboard', size=26, weight=ft.FontWeight.BOLD)
    health_text = ft.Text('Engine health: loading...')
    ws_text = ft.Text('WebSocket: connecting...', color=ft.Colors.BLUE_GREY)

    servers_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('Name')),
            ft.DataColumn(ft.Text('Host')),
            ft.DataColumn(ft.Text('Tags')),
            ft.DataColumn(ft.Text('Action')),
        ],
        rows=[],
    )

    incidents_list = ft.Column([], spacing=6)
    action_status = ft.Text('')


    def post_action(server_name: str, action: str):
        token = get_token()
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        try:
            response = requests.post(f'{ENGINE_URL}/servers/{server_name}/actions/{action}', headers=headers, timeout=5)
            response.raise_for_status()
            action_status.value = f'Executed {action} on {server_name}'
        except Exception as exc:
            action_status.value = f'Action failed: {exc}'
        page.update()


    def start_ws_listener():
        token = get_token()
        ws_url = ENGINE_URL.replace('http://', 'ws://').replace('https://', 'wss://') + '/ws'

        def on_message(_ws, message: str):
            try:
                payload = json.loads(message)
                if payload.get('server'):
                    ws_text.value = f"WS update: {payload.get('server')} {payload.get('check')}={payload.get('value')}"
                else:
                    ws_text.value = f"WS: {payload.get('status', 'message')}"
            except Exception:
                ws_text.value = f'WS raw: {message}'
            page.update()

        def on_error(_ws, error):
            ws_text.value = f'WebSocket error: {error}'
            page.update()

        headers = [f"Authorization: Bearer {token}"] if token else []
        app = WebSocketApp(ws_url, header=headers, on_message=on_message, on_error=on_error)
        threading.Thread(target=app.run_forever, daemon=True).start()

    def load_data(_=None):
        token = get_token()
        try:
            health = fetch_json('/health', None)
            health_text.value = f"Engine health: {health.get('status', 'unknown')}"

            servers = fetch_json('/servers', token)
            servers_table.rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(s.get('name', '-'))),
                        ft.DataCell(ft.Text(s.get('host', '-'))),
                        ft.DataCell(ft.Text(', '.join(s.get('tags', [])))),
                        ft.DataCell(ft.ElevatedButton('Restart', on_click=lambda _e, n=s.get('name',''): post_action(n, 'restart_service'))),
                    ]
                )
                for s in servers
            ]

            incidents = fetch_json('/incidents?limit=10', token)
            incidents_list.controls = [
                ft.Text(f"[{i.get('priority', 'info')}] {i.get('server_name', '-')}: {i.get('description', '-')}")
                for i in incidents
            ]
        except Exception as exc:
            health_text.value = f'Error loading data: {exc}'
        page.update()

    refresh_button = ft.ElevatedButton('Refresh', on_click=load_data)

    page.add(
        title,
        health_text,
        ws_text,
        action_status,
        refresh_button,
        ft.Text('Servers', size=20, weight=ft.FontWeight.W_600),
        servers_table,
        ft.Text('Recent incidents', size=20, weight=ft.FontWeight.W_600),
        incidents_list,
    )

    load_data()
    start_ws_listener()


ft.app(target=main, view=ft.WEB_BROWSER, port=8080)
