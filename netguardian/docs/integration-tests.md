# NetGuardian 2.0 — testy integracyjne i scenariusze ataku

## Cel
Zweryfikować pełny przepływ: agent -> Kafka -> engine -> Redis -> dashboard + reakcje (blokada, notyfikacje, honeypot).

## Wymagania
- Uruchomione środowisko: `docker compose up --build`
- Skonfigurowane `.env` (Slack/AbuseIPDB/MISP opcjonalnie)
- Wgrane klucze SSH (`engine/ssh/id_rsa`, `agent/authorized_keys`)

## Scenariusz 1: SYN flood
1. Wejdź do kontenera agenta i doinstaluj `hping3` (lub przygotuj oddzielny kontener atakujący).
2. Uruchom:
   ```bash
   ./scripts/attacks/ddos_syn_flood.sh engine 80
   ```
3. Oczekiwane wyniki:
   - alert na `ws://localhost:8001/ws`
   - wpis `blocked_ips` w `GET /status`
   - log `Blocking IP ...` w engine

## Scenariusz 2: skanowanie portów
```bash
./scripts/attacks/port_scan.sh engine 1-100
```
Sprawdź alerty i korelacje w logach engine.

## Scenariusz 3: DNS tunneling simulation
```bash
python scripts/attacks/dns_tunnel_sim.py 8.8.8.8 200
```
Sprawdź alerty DNS/exfiltration.

## Dowody do portfolio
- zrzut dashboardu z alertem
- log engine z decyzją blokowania
- wynik `curl /status`
- wygenerowany raport `GET /report`


## Scenariusz 4: brute force SSH
```bash
./scripts/attacks/ssh_bruteforce.sh agent root /tmp/pass.txt
```
Sprawdź alert i reakcję playbooka, plus wpisy blokady IP.

## Checklist walidacyjny
- Alert pojawia się na dashboardzie WS.
- `GET /status` pokazuje `blocked_ips` po reakcji.
- Slack notif pojawia się przy aktywnym webhooku.
- Dla odpowiedniego scenariusza uruchamia się honeypot.
