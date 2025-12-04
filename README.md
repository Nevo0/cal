# 🎯 Zadanie Rekrutacyjne - Grupa Wolff
## Python Django Developer - Kalkulator Elektryczny

Witaj! To zadanie rekrutacyjne potrwa około 2 godzin.

**Cel:** Stwórz kalkulator elektryczny do wyceny zamówień na obudowy elektryczne z terminałami i dławikami.

---

## 📂 Co znajduje się w tym folderze?

### 📘 Dokumentacja:
1. **`fixtures/ZADANIE_REKRUTACYJNE.md`** ⭐ **START TUTAJ**
   - Kompletny opis zadania głównego (3 części + bonusy)
   - Instrukcje krok po kroku
   - Zawiera również zadania dodatkowe do wyboru

### 📊 Dane testowe (JSON):
- **`fixtures/enclosures.json`** - 10 obudów elektrycznych
- **`fixtures/glands.json`** - 16 dławików kablowych (PA i Brass)
- **`fixtures/terminals.json`** - 33 terminale elektryczne
- **`fixtures/order_example.json`** - Przykład kompletnego zamówienia

**Razem: 59 produktów gotowych do importu**

### 🐍 Szablony kodu (Python):
- **`fixtures/simple_order_model.py`** - Model Django dla zamówień
- **`fixtures/recruitment_order_view_template.py`** - Widok API do implementacji
- **`fixtures/order_serializers.py`** - Serializery DRF do walidacji

---

## 🚀 Jak zacząć?

### Krok 1: Pobierz kod zadania
```bash
# Sklonuj to repozytorium
git clone git@github.com:Nevo0/cal.git
cd cal
```

### Krok 2: Utwórz NOWE, PUSTE i PRYWATNE repozytorium
**⚠️ WAŻNE:** Nie rób fork! Utwórz nowe repozytorium:

1. Przejdź na GitHub/GitLab
2. Kliknij "New repository"
3. Nazwa: `wolff-recruitment-task` (lub dowolna)
4. **Zaznacz: Private (prywatne)**
5. **NIE** inicjalizuj z README, .gitignore ani licencją
6. Utwórz repozytorium

### Krok 3: Podłącz swoje repozytorium
```bash
# Usuń połączenie z oryginalnym repo
git remote remove origin

# Dodaj swoje nowe, puste repozytorium
git remote add origin <TWOJE_NOWE_REPO_URL>

# Wypchnij kod do swojego prywatnego repo
git branch -M main
git push -u origin main
```

### Krok 4: Przeczytaj zadanie
```bash
# Otwórz główny plik z zadaniem
cat fixtures/ZADANIE_REKRUTACYJNE.md
```

### Krok 5: Zapoznaj się z danymi
```bash
# Zobacz jakie dane będziesz importować
cat fixtures/enclosures.json
cat fixtures/glands.json
cat fixtures/terminals.json
```

### Krok 6: Rozpocznij implementację
Otwórz `fixtures/ZADANIE_REKRUTACYJNE.md` i postępuj zgodnie z instrukcjami.

---

## 📋 Zakres zadania (skrót)

### ✅ Część 1: Modele Django (30 min, 25 pkt)
- Stwórz modele `Enclosure`, `Gland`, `Terminal` na podstawie JSON
- Dodaj model `SimpleOrder` dla zamówień
- Wykonaj migracje

### ✅ Część 2: Import danych (30 min, 25 pkt)
- Stwórz 3 management commands do importu
- Zaimportuj 59 produktów z JSON do bazy
- Zweryfikuj poprawność

### ✅ Część 3: API i obliczanie ceny (30 min, 30 pkt)
- Zaimplementuj `calculate_order_price()`
- Utwórz endpoint API `POST /api/recruitment/orders/create/`
- Przetestuj z `order_example.json`

### 🌟 Bonusy (opcjonalnie, +40 pkt)
- Walidacja geometryczna dławików (20 pkt)
- Walidacja pojemności terminali (10 pkt)
- Endpoint walidacji bez zapisu (5 pkt)
- Testy jednostkowe (5 pkt)

---

## 📊 Struktura danych (przykłady)

### Enclosure (obudowa):
```json
{
  "name": "Skrzynka 300x200x150",
  "code": "ENC-300-200-150",
  "dimension_width": 300,
  "dimension_height": 200,
  "dimension_depth": 150,
  "price": "125.50",
  "mounting_areas": {
    "top": {"x": 280, "y": 180},
    "down": {"x": 280, "y": 180},
    "left": {"x": 180, "y": 130},
    "right": {"x": 180, "y": 130}
  },
  "enclosure_terminals": {
    "1,5mm": 12,
    "2,5mm": 9,
    "4mm": 8,
    "6mm": 7,
    "10mm": 5,
    "16mm": 3,
    "25mm": 2,
    "35mm": 1
  }
}
```

### Gland (dławik):
```json
{
  "size": "M20",
  "diameter_mm": 20,
  "physical_diameter_mm": 25,
  "cable_range_min": 6,
  "cable_range_max": 13,
  "material": "PA",
  "price": "4.10",
  "catalog_number": "GLD-M20-PA"
}
```

### Terminal:
```json
{
  "wire_cross_section": "2,5mm",
  "width_mm": 6.2,
  "color": "blue",
  "voltage": 800,
  "current": 24,
  "price": "1.20",
  "catalog_number": "TERM-2.5-BL"
}
```

---

## 🎯 Co będziemy oceniać?

### Funkcjonalność (80 pkt):
- ✅ Modele działają poprawnie (25 pkt)
- ✅ Import danych zakończony sukcesem (25 pkt)
- ✅ API zwraca poprawną cenę (30 pkt)

### Jakość kodu:
- Czytelność i organizacja
- Obsługa błędów (try/except)
- Użycie `Decimal` dla cen
- Dokumentacja (docstringi)
- Commity git (opisowe)

### Bonusy (+40 pkt):
- Walidacja geometryczna
- Testy
- Dodatkowe funkcje

---

## 💡 Wskazówki

### 1. Czytaj JSON uważnie
Struktura danych jest zagnieżdżona. Zwróć uwagę na:
- `mounting_areas` to dict z 4 kluczami (top, down, left, right)
- `enclosure_terminals` to dict z pojemnościami dla różnych przekrojów
- Ceny są floatami w JSON - konwertuj na `Decimal`!

### 2. Decimal dla cen
```python
from decimal import Decimal


price = Decimal('125.50')


```

### 3. Testuj na bieżąco
```bash
# Django shell to Twój przyjaciel
python manage.py shell

>>> from calculator.models import *
>>> Enclosure.objects.count()
>>> Gland.objects.first()
```

### 4. Git commits
```bash
git commit -m "feat: Add Enclosure model with mounting areas"
git commit -m "feat: Implement import_enclosures command"
git commit -m "feat: Add price calculation for orders"
```

---

## 📦 Dostarczone pliki - szczegóły

| Plik | Rozmiar | Opis |
|------|---------|------|
| `fixtures/ZADANIE_REKRUTACYJNE.md` | ~35 KB | Główne zadanie + bonusy |
| `fixtures/enclosures.json` | 6 KB | 10 obudów |
| `fixtures/glands.json` | 4 KB | 16 dławików |
| `fixtures/terminals.json` | 7 KB | 33 terminale |
| `fixtures/order_example.json` | 2 KB | Przykład |
| `fixtures/simple_order_model.py` | 4 KB | Model zamówienia |
| `fixtures/recruitment_order_view_template.py` | 6 KB | Widok API |
| `fixtures/order_serializers.py` | 2 KB | Serializery |

---

## 🧪 Test API (po implementacji)

```bash
# Test 1: Prosty request
curl -X POST http://localhost:8000/api/recruitment/orders/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jan Kowalski",
    "email": "jan@example.com",
    "saveBox": [
      {
        "selectedBox": {"code": "ENC-300-200-150"},
        "currentConfig": {
          "quantity": 1,
          "box_type": "terminal_boxe",
          "glands": [],
          "terminals": []
        }
      }
    ]
  }'

# Test 2: Kompletny przykład
curl -X POST http://localhost:8000/api/recruitment/orders/create/ \
  -H "Content-Type: application/json" \
  -d @fixtures/order_example.json
```

**Oczekiwana odpowiedź:**
```json
{
  "success": true,
  "order_id": "abc-123-def",
  "total_price": "359.50",
  "message": "Zamówienie utworzone pomyślnie"
}
```

---

## 📞 Pytania?

To nie egzamin! Możesz pytać o:
- Wymagania biznesowe
- Strukturę danych
- Oczekiwane zachowanie API
- Niejasności w zadaniu

**Kontakt:** r.piecyk@grupa-wolff.com

---

## 🌟 Dla ambitnych

Jeśli skończyłeś przed czasem, w pliku `fixtures/ZADANIE_REKRUTACYJNE.md` znajdziesz sekcję z zadaniami dodatkowymi:
1. Przejdź do sekcji z bonusami
2. Wybierz zadania które Cię interesują
3. Zaimplementuj (każdy bonus to dodatkowe punkty!)

**Przykładowe bonusy:**
- 🎨 Generator CNC (15 pkt)
- 📊 Statystyki (10 pkt)
- 📧 Email potwierdzenia (10 pkt)
- 🧪 Testy integracyjne (10 pkt)
- ... i wiele więcej!

---


## 🚀 Ostatni check przed startem

1. ✅ Mam ~2 godziny wolnego czasu
2. ✅ Python 3.x i Django 4.x zainstalowane
3. ✅ Baza danych działa (migrate wykonany)
4. ✅ Przeczytałem `fixtures/ZADANIE_REKRUTACYJNE.md`
5. ✅ Zapoznałem się z danymi JSON
6. ✅ Utworzyłem własne PRYWATNE repozytorium na GitHub/GitLab

## 👉 Jeśli wszystko OK, otwórz:
## `fixtures/ZADANIE_REKRUTACYJNE.md`

---

## 📤 Jak oddać zadanie?

### 1. Zatwierdź ostatnie zmiany
```bash
git add .
git commit -m "feat: Complete recruitment task"
git push origin main
```

### 2. Dodaj plik IMPLEMENTATION_NOTES.md
W głównym katalogu projektu utwórz plik z opisem:
- Jak uruchomić projekt (krok po kroku)
- Co zostało zaimplementowane
- Jakie bonusy wykonałeś (jeśli są)
- Ewentualne problemy/uwagi

### 3. Udostępnij prywatne repozytorium
**⚠️ Twoje repo jest PRYWATNE, więc musisz dać nam dostęp:**

Na GitHubie:
1. Przejdź do swojego repozytorium
2. Settings → Collaborators
3. Kliknij "Add people"
4. Dodaj użytkownika: **[Nevo0]**

Na GitLabie:
1. Przejdź do swojego repozytorium
2. Settings → Members
3. Dodaj użytkownika z rolą "Reporter"

### 4. Wyślij link do repozytorium
📧 **r.piecyk@grupa-wolff.com**

**Temat:** Zadanie rekrutacyjne - [Twoje Imię Nazwisko]

**Treść maila:**
```
Dzień dobry,

Przesyłam rozwiązanie zadania rekrutacyjnego na stanowisko Python Django Developer.

Link do repozytorium: [LINK_DO_TWOJEGO_REPO]

Imię i nazwisko: [...]
Czas realizacji: [np. 2h 15min]
Zaimplementowane bonusy: [jeśli są]

Pozdrawiam,
[Imię Nazwisko]
```

---

**Powodzenia!** 🎉

*Grupa Wolff - Kalkulator Elektryczny*  


