# Moduły detekcji i reakcji

## Detection
- `beacon_detector.py`: wykrywanie wzorców beaconingu C2.
- `dns_analyzer.py`: heurystyki anomalii DNS (np. entropia).
- `exfiltration.py`: wykrywanie potencjalnej eksfiltracji po wolumenie ruchu.
- `window_analyzer.py`: analiza okien czasowych i uruchamianie modelu IF.

## Correlation / Reputation
- `correlator.py`: korelacja zdarzeń z wielu źródeł.
- `scorer.py`: scoring reputacyjny adresów i sygnałów TI.

## Response
- `executor.py`: uruchamianie playbooków reakcji.
- `notifiers.py`: wysyłanie notyfikacji (Slack).
- `honeypot.py`: uruchamianie honeypotów przez Docker API.
- `response/playbooks/*.yml`: reguły reakcji dla klas incydentów.
