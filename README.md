# PROJEKTS-WORK

Repozytorium zawiera 4 niezależne projekty uruchamiane przez Docker Compose:

- `cloudbudget/` – platforma FinOps do analizy i optymalizacji kosztów cloud.
- `infraflow/` – platforma obserwowalności i automatyzacji operacyjnej infrastruktury.
- `netguardian/` – platforma SecOps/SIEM/SOAR do monitorowania bezpieczeństwa sieci.
- `netaegis/` – platforma agentowa z MCP do orkiestracji działań bezpieczeństwa.

## Unikalność portów (docker-compose)

Zweryfikowano pliki:

- `cloudbudget/docker-compose.yml`
- `infraflow/docker-compose.yml`
- `netguardian/docker-compose.yml`
- `netaegis/docker-compose.yml`

Wszystkie porty hosta są unikalne między projektami (brak kolizji).

### Automatyczna weryfikacja

W katalogu głównym znajduje się skrypt:

```bash
./verify_all_ports.sh
```

Skrypt:
1. parsuje mapowania portów z wszystkich plików `docker-compose.yml`,
2. wykrywa duplikaty portów hosta,
3. wyświetla raport końcowy i zwraca kod błędu przy konflikcie.

## Uruchamianie projektów

### Wszystkie projekty jednocześnie

```bash
make all
```

### Pojedynczy projekt

Uruchom wybrany projekt z jego katalogu:

```bash
cd cloudbudget && docker compose up -d
cd infraflow && docker compose up -d
cd netguardian && docker compose up -d
cd netaegis && docker compose up -d
```

### Zatrzymywanie

Wszystkie:

```bash
make down
```

Pojedynczo:

```bash
cd <projekt> && docker compose down
```

## Rozwiązywanie problemów (checklista)

1. **Pamięć RAM**
   - Upewnij się, że Docker ma wystarczająco RAM (minimum 8 GB zalecane dla uruchamiania wszystkich stacków).
   - Przy problemach z restartami kontenerów sprawdź `docker stats` oraz logi.

2. **Porty**
   - Przed startem uruchom `./verify_all_ports.sh`.
   - Jeśli port jest zajęty lokalnie, zmień mapowanie tylko po stronie hosta w odpowiednim `docker-compose.yml`.

3. **Zależności i środowisko**
   - Sprawdź, czy Docker i Docker Compose działają poprawnie.
   - Upewnij się, że pliki `.env` zostały utworzone tam, gdzie wymagane.
   - W razie błędów uruchom `docker compose logs -f` w katalogu projektu i zweryfikuj brakujące sekrety/klucze.
