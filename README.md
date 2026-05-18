# PROJEKTS-WORK

Monorepo zawiera 4 projekty demonstracyjne:
- `cloudbudget`
- `infraflow`
- `netguardian`
- `netaegis`

## One-click demo (lokalnie)

```bash
./setup.sh
./run_all_demos.sh
```

`setup.sh` uruchamia dedykowane setupy projektowe:
- `cloudbudget/scripts/setup.sh`
- `infraflow/scripts/setup.sh`
- `netguardian/scripts/setup.sh`
- `netaegis/scripts/setup.sh`

Dla uruchomienia wszystkich projektów jednocześnie używane są pliki `docker-compose.demo.yml` (unikalne porty, brak konfliktów).

Skrypty `setup.sh`, `run_all_demos.sh` i `stop_all_demos.sh` korzystają ze wspólnej matrycy projektów: `scripts/demo_projects.sh` (jedno źródło prawdy dla katalogów/override compose/setup).

## Zatrzymanie

```bash
./stop_all_demos.sh
```

## Adresy po uruchomieniu

- CloudBudget frontend: http://localhost:3000
- CloudBudget API docs: http://localhost:8000/docs
- InfraFlow dashboard: http://localhost:8180
- InfraFlow API docs: http://localhost:8100/docs
- NetGuardian dashboard: http://localhost:8280
- NetGuardian API docs: http://localhost:8200/docs
- NetAegis frontend: http://localhost:3300
- NetAegis Main MCP docs: http://localhost:8300/docs
- NetAegis Operational MCP docs: http://localhost:8301/docs

> Uwaga: NetGuardian enrichment GeoIP wymaga pliku `GeoLite2-City.mmdb` (MaxMind).


## Weryfikacja przed demo

```bash
./scripts/demo_doctor.sh
```

Uruchamia walidację: wymagane komendy, obecność `.env.example`, wykonywalność setup scripts i poprawność `docker compose config` dla każdego projektu.

Możesz też uruchomić wszystko jednym poleceniem razem z setupem:

```bash
./run_all_demos.sh --with-setup
```


## Generowanie brakujących plików z _nn.txt

Repo zawiera generator, który tworzy brakujące pliki bootstrap/demo na podstawie wytycznych z `_yy.txt`:

```bash
python tools/generate_from_nn.py
```

Wygenerowana skrócona instrukcja: `RUN_DEMO.md`.


## Uruchomienie jednym poleceniem (Makefile)

```bash
make demo-start
```

Dodatkowe komendy:

```bash
make demo-check
make demo-stop
make generate-from-nn
```


Generator wspiera tryby:

```bash
python tools/generate_from_nn.py --dry-run
python tools/generate_from_nn.py --sync
```

`--sync` nadpisuje wyłącznie pliki oznaczone markerem zarządzania generatora.


Generator tworzy również `NN_TASKS.json` (mapa zadań per projekt wyciągnięta z `_yy.txt`), co ułatwia dalsze wdrożenie „całego kodu projektu” krok po kroku.


Dodatkowo możesz wygenerować kompletny scaffold projektu z `_yy.txt`:

```bash
make nn-build
```


Aby wymusić generowanie dokładnie z `_nn.txt`:

```bash
python tools/generate_from_nn.py --sync --source _nn.txt
python tools/nn_build_project.py --source _nn.txt
```


## CI dla generatora _nn

Dodano workflow `nn-generated-project-ci`, który uruchamia `./tests_test_nn_build.sh` dla zmian w `tools/nn_build_project.py`, `_nn.txt` i test harnessie.
