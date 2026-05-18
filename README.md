# PROJEKTS-WORK

Repozytorium ma **celowo minimalistyczną strukturę**:

```text
PROJEKTS-WORK/
├── README.md
├── cloudbudget/
├── infraflow/
├── netguardian/
└── netaegis/
```

W katalogu głównym znajduje się wyłącznie ten plik oraz 4 katalogi projektowe. Wszystkie skrypty uruchomieniowe, pliki konfiguracyjne i pliki startowe znajdują się wewnątrz odpowiednich projektów.

---

## 1) cloudbudget/

**CloudBudget 2.0** – autonomiczna platforma FinOps dla środowisk multi-cloud (AWS/Azure/GCP/on-prem).

### Kluczowe elementy
- Agregacja kosztów multi-cloud.
- Rekomendacje optymalizacyjne (idle resources, rightsizing, itp.).
- Symulacje kosztowe (what-if).
- Predykcja kosztów i alerty budżetowe.
- Automatyzacja wybranych akcji optymalizacyjnych.

### Szybki start
```bash
cd cloudbudget
cp .env.example .env
bash scripts/setup.sh
```

---

## 2) infraflow/

**InfraFlow** – system monitorowania i samonaprawy infrastruktury (Linux/Windows) z regułami YAML.

### Kluczowe elementy
- Monitoring bezagentowy (SSH/WinRM).
- Automatyczne akcje naprawcze (restart usług, porządki, itp.).
- Audyt i historia incydentów.
- Integracje powiadomień (np. Slack/email/webhook).

### Szybki start
```bash
cd infraflow
cp .env.example .env
bash scripts/setup.sh
```

---

## 3) netguardian/

**NetGuardian 2.0** – platforma monitoringu i reakcji bezpieczeństwa sieciowego (SIEM/SOAR).

### Kluczowe elementy
- Detekcja anomalii i korelacja zdarzeń.
- Automatyczna reakcja (np. blokady IP, playbooki).
- Dashboard czasu rzeczywistego.
- Integracje threat intelligence.

### Szybki start
```bash
cd netguardian
cp .env.example .env
bash scripts/setup.sh
```

---

## 4) netaegis/

**NetAegis** – platforma SOAR oparta o architekturę agentową i centralny MCP.

### Kluczowe elementy
- Agenci zbierający dane i zdarzenia.
- Centralny silnik reguł (MCP).
- Orkiestracja reakcji na incydenty.
- Interfejs operacyjny do obserwacji i sterowania.

### Szybki start
```bash
cd netaegis
cp .env.example .env
bash scripts/setup.sh
```

---

## Zasada repo

- **1 README.md w root** (ten plik).
- **4 katalogi = 4 projekty**.
- Brak dodatkowych katalogów narzędziowych i dokumentacyjnych w root.
