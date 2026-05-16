import os, requests, flet as ft
ENGINE_URL=os.getenv('ENGINE_URL','http://localhost:8000')

def main(page: ft.Page):
    page.title='InfraFlow Dashboard'
    status=requests.get(f'{ENGINE_URL}/health', timeout=5).json()
    page.add(ft.Text(f"Engine health: {status.get('status')}", size=24))

ft.app(target=main, view=ft.WEB_BROWSER, port=8080)
