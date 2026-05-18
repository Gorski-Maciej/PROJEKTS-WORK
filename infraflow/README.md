# InfraFlow – Samonaprawiający się System Zarządzania Infrastrukturą

![Self-Healing](https://img.shields.io/badge/Self--Healing-ready-green)

InfraFlow to autonomiczny system, który cyklicznie monitoruje serwery Linux i Windows, wykrywa problemy (wysokie CPU, pełny dysk, zatrzymane usługi) i automatycznie je naprawia. Konfiguracja w YAML (Infrastructure as Code) jest wersjonowana w Git, a wszystkie akcje są logowane z pełnym audytem.

## 🚀 Kluczowe cechy
- **Bezagentowy monitoring** – połączenie przez SSH (Linux) i WinRM (Windows)
- **Automatyczne akcje naprawcze** – restart usług, czyszczenie logów, rozszerzanie LVM, aktualizacje pakietów
- **Predykcja awarii** – Isolation Forest na danych historycznych z TimescaleDB
- **Dynamiczne playbooki** – reguły warunkowe z bezpiecznym silnikiem AST
- **Wersjonowanie konfiguracji** – każda zmiana w YAML zapisywana jest w Git
- **Powiadomienia** – Slack, email, webhook (PagerDuty)

## ⚡ Szybki start
```bash
cd infraflow
cp .env.example .env
bash scripts/setup.sh
```
