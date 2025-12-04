# Zadanie Rekrutacyjne - Python Django Developer
## Kalkulator Elektryczny


---

## 📋 Opis projektu

System do konfiguracji i wyceny obudów elektrycznych z komponentami:
- Obudowy elektryczne różnych rozmiarów
- Dławiki kablowe (cable glands) montowane w ściankach
- Terminale elektryczne montowane wewnątrz na szynach
- Automatyczne obliczanie cen i walidacja geometryczna

**Stack:** Python 3.x, Django 4.x, Django REST Framework, PostgreSQL

---

## 🎯 Twoje zadanie

Zaimplementuj system importu danych i API do tworzenia zamówień z automatycznym obliczaniem cen.

### Co dostarczamy:

W folderze `fixtures/` znajdziesz:
- **Dane JSON** - enclosures.json, glands.json, terminals.json (59 produktów)
- **Szablon modelu** - simple_order_model.py
- **Szablon widoku API** - recruitment_order_view_template.py
- **Szablon serializerów** - order_serializers.py
- **Przykład zamówienia** - order_example.json

### Co musisz zrobić:

1. ✅ Stworzyć modele Django na podstawie JSON
2. ✅ Zaimplementować import danych z JSON do bazy
3. ✅ Zaimplementować obliczanie ceny zamówienia
4. ✅ Stworzyć endpoint API do tworzenia zamówień
5. 🌟 (BONUS) Dodać walidację geometryczną

---

## 📝 CZĘŚĆ 1: Modele Django (30 min, 25 pkt)

### Zadanie 1.1: Stwórz model Enclosure

Otwórz `fixtures/enclosures.json` i przeanalizuj strukturę danych.

**Plik:** `calculator/models.py`

```python
class Enclosure(models.Model):
    """
    Model obudowy elektrycznej.
    
    ZADANIE: Na podstawie enclosures.json stwórz pola modelu.
    
    Wymagane pola:
    - name (CharField, max 200)
    - code (CharField, max 50, unique) - np. "ENC-300-200-150"
    - dimension_width (IntegerField) - szerokość w mm
    - dimension_height (IntegerField) - wysokość w mm
    - dimension_depth (IntegerField) - głębokość w mm
    - price (DecimalField, max_digits=10, decimal_places=2)
    
    Pola dla obszarów montażowych (z mounting_areas w JSON):
    - mounting_area_top_x (FloatField, null=True)
    - mounting_area_top_y (FloatField, null=True)
    - mounting_area_down_x (FloatField, null=True)
    - mounting_area_down_y (FloatField, null=True)
    - mounting_area_left_x (FloatField, null=True)
    - mounting_area_left_y (FloatField, null=True)
    - mounting_area_right_x (FloatField, null=True)
    - mounting_area_right_y (FloatField, null=True)
    
    Pojemność terminali (z enclosure_terminals w JSON):
    - enclosure_terminals (JSONField, null=True)
      Przykład: {"2,5mm": 9, "4mm": 8, "6mm": 7}
    """
    
    # TODO: Zaimplementuj pola

```

**Wskazówka:** JSON ma strukturę:
```json
{
  "name": "Skrzynka 300x200x150",
  "code": "ENC-300-200-150",
  "mounting_areas": {
    "top": {"x": 280, "y": 180}
  },
  "enclosure_terminals": {
    "2,5mm": 9
  }
}
```

### Zadanie 1.2: Stwórz model Gland

**Plik:** `calculator/models.py`

```python
class Gland(models.Model):
    """
    Model dławika kablowego.
    
    ZADANIE: Na podstawie glands.json stwórz pola.
    
    Wymagane pola:
    - size (CharField, max 10) - np. "M12", "M16"
    - diameter_mm (IntegerField) - średnica nominalna
    - physical_diameter_mm (IntegerField) - fizyczna średnica (ważne!)
    - cable_range_min (FloatField) - min średnica kabla
    - cable_range_max (FloatField) - max średnica kabla
    - material (CharField, max 20) - "PA" lub "Brass"
    - price (DecimalField)
    - catalog_number (CharField, max 50)
    """
    
    # TODO: Zaimplementuj pola

```

### Zadanie 1.3: Stwórz model Terminal

**Plik:** `calculator/models.py`

```python
class Terminal(models.Model):
    """
    Model terminala elektrycznego.
    
    ZADANIE: Na podstawie terminals.json stwórz pola.
    
    Wymagane pola:
    - wire_cross_section (CharField, max 10) - np. "2,5mm"
    - width_mm (FloatField) - szerokość na szynie
    - color (CharField, max 20) - "blue", "yellow", etc.
    - voltage (IntegerField) - napięcie w V
    - current (FloatField) - prąd w A
    - price (DecimalField)
    - catalog_number (CharField, max 50)
    """
    
    # TODO: Zaimplementuj pola
    

```

### Zadanie 1.4: Dodaj model SimpleOrder

Skopiuj zawartość `fixtures/simple_order_model.py` do `calculator/models.py`.

### Zadanie 1.5: Wykonaj migracje

```bash
python manage.py makemigrations
python manage.py migrate
```


## 📥 CZĘŚĆ 2: Import danych (30 min, 25 pkt)

### Zadanie 2.1: Stwórz import dla Enclosure

### Zadanie 2.2: Analogicznie dla Gland i Terminal

### Zadanie 2.3: Uruchom import

### Zadanie 2.4: Weryfikacja

```bash
python manage.py shell
>>> from calculator.models import Enclosure, Gland, Terminal
>>> Enclosure.objects.count()  # Powinno być 10
>>> Gland.objects.count()      # Powinno być 16
>>> Terminal.objects.count()   # Powinno być 33
```

---

## 💰 CZĘŚĆ 3: Obliczanie ceny (30 min, 30 pkt)

### Zadanie 3.1: Zaimplementuj calculate_order_price

**Plik:** `calculator/infrastructure/api/recruitment_order_views.py`

Skopiuj `fixtures/recruitment_order_view_template.py` i uzupełnij funkcję:

```python
def calculate_order_price(order_data: dict) -> Decimal:
    """
    Oblicza cenę zamówienia.
    
    ZADANIE:
    1. Dla każdej obudowy w saveBox:
       a) Pobierz cenę obudowy z bazy (Enclosure.objects.get(code=...))
       b) Pomnóż przez ilość (quantity)
       c) Dodaj ceny dławików
       d) Dodaj ceny terminali
    2. Zsumuj wszystko
    
    WSKAZÓWKA:
    - Używaj Decimal() dla precyzyjnych obliczeń
    - Pamiętaj o quantity dla każdego elementu
    """
    total_price = Decimal('0.00')
    
    for box_data in order_data.get('saveBox', []):
        # 1. Cena obudowy   
        
        # 2. Ceny dławików
         
        # 3. Ceny terminali
        pass  
    
    return total_price
```

### Zadanie 3.2: Zintegruj z create_order

W funkcji `create_order()` w tym samym pliku:

```python
# KROK 4: Obliczenie ceny
try:
    total_price = calculate_order_price(validated_data)
    
    # KROK 5: Zapisanie zamówienia
    order = SimpleOrder.objects.create(
        customer_name=validated_data['name'],
        customer_email=validated_data['email'],
        user_information=validated_data.get('userInformation', ''),
        order_data=validated_data,
        total_price=total_price,
        geometry_validation_passed=True
    )
    
    # KROK 6: Zwróć odpowiedź
    return Response({
        "success": True,
        "order_id": str(order.id),
        "total_price": str(total_price),
        "message": "Zamówienie utworzone pomyślnie"
    }, status=status.HTTP_201_CREATED)
```

### Zadanie 3.3: Dodaj serializery

Skopiuj `fixtures/order_serializers.py` do `calculator/infrastructure/api/serializers/recruitment_order_serializers.py`

### Zadanie 3.4: Zarejestruj endpoint

**Plik:** `calculator/api/urls.py`

```python
from calculator.infrastructure.api.recruitment_order_views import create_order

urlpatterns = [
    # ... istniejące URLe
]
```

### Zadanie 3.5: Testuj API

```bash
curl -X POST http://localhost:8000/api/recruitment/orders/create/ \
  -H "Content-Type: application/json" \
  -d @fixtures/order_example.json
```

**Oczekiwana odpowiedź:**
```json
{
  "success": true,
  "order_id": "abc-123-def",
  "total_price": "387.10",
  "message": "Zamówienie utworzone pomyślnie"
}
```

**Obliczenia dla order_example.json:**
- 1x Skrzynka 300x200x150: 125.50 PLN
- 3x M20 PA: 3 × 4.10 = 12.30 PLN
- 2x M16 PA: 2 × 3.20 = 6.40 PLN
- 4x M12 Brass: 4 × 4.80 = 19.20 PLN
- 8x Terminal 2,5mm blue: 8 × 1.20 = 9.60 PLN
- 5x Terminal 4mm blue: 5 × 1.35 = 6.75 PLN
- **Razem × 2 (quantity):** (125.50 + 12.30 + 6.40 + 19.20 + 9.60 + 6.75) × 2 = **359.50 PLN**

---

## 🌟 ZADANIA BONUS (+40 pkt)

### BONUS 1: Walidacja geometryczna dławików (20 pkt)

**Plik:** `calculator/domain/services/gland_layout_validator.py`

```python
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class MountingArea:
    width: float  # mm
    height: float  # mm
    side: str

class GlandLayoutValidator:
    """
    Walidator rozmieszczenia dławików w obszarze montażowym.
    
    Parametry:
    - MIN_SPACING = 8mm (odstęp między dławikami)
    - EDGE_MARGIN = 15mm (margines od krawędzi)
    
    Algorytm First Fit Decreasing:
    1. Posortuj dławiki od największego do najmniejszego
    2. Rozmieść w rzędach (od lewej do prawej)
    3. Sprawdź czy wszystko mieści się w wysokości
    """
    
    MIN_SPACING = 8
    EDGE_MARGIN = 15
    
    def validate_gland_layout(
        self,
        glands: List[dict],  # [{"size": "M20", "quantity": 3}, ...]
        mounting_area: MountingArea,
        glands_data: dict  # {"M20": {"physical_diameter_mm": 25}}
    ) -> Tuple[bool, str]:
        """
        ZADANIE: Zaimplementuj walidację.
        
        Returns:
            (is_valid, error_message)
        """
        
        # TODO: Implementacja
        # 1. Stwórz listę wszystkich dławików (rozwiń quantity)
        # 2. Sortuj po diameter DESC
        # 3. Rozmieść w rzędach
        # 4. Oblicz całkowitą wysokość
        # 5. Sprawdź czy mieści się
        
        return True, "OK"
```


### BONUS 2: Walidacja pojemności terminali (10 pkt)

**Plik:** `calculator/domain/services/terminal_capacity_validator.py`

```python
def validate_terminal_capacity(
    terminals: List[dict],  # [{"size": "2,5mm", "quantity": 8}]
    enclosure_capacity: dict  # {"2,5mm": 9, "4mm": 8}
) -> Tuple[bool, str, dict]:
    """
    ZADANIE: Sprawdź czy terminale zmieszczą się w skrzynce.
    
    Returns:
        (is_valid, message, details)
    """
    
    details = {}   

    
    return True, "OK", details
```


### BONUS 3: Testy jednostkowe (5 pkt)

**Plik:** `calculator/tests/test_recruitment.py`

```python
from django.test import TestCase
from calculator.models import Enclosure, Gland, Terminal

class CalculateOrderPriceTest(TestCase):
    def setUp(self):
        # TODO: Stwórz dane testowe
        pass
    
    def test_simple_enclosure_only(self):
        # TODO: Test z samą obudową
        pass
    
    def test_enclosure_with_glands(self):
        # TODO: Test z dławikami
        pass
```

---

## 🌐 BONUS 4: Frontend helper - kalkulator na żywo (10 pkt)

### Zadanie

Endpoint zwracający cenę bez zapisywania zamówienia.

**Endpoint:** `POST /api/recruitment/orders/calculate-price/`

```python
@api_view(['POST'])
def calculate_price_only(request):
    """
    Oblicza cenę bez tworzenia zamówienia.
    
    Przydatne dla frontendu - pokazywanie ceny na żywo
    podczas konfigurowania zamówienia.
    """
    
    serializer = OrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    try:
        total_price = calculate_order_price(serializer.validated_data)
        
        # TODO: Zwróć szczegółowy breakdown
        return Response({
            "total_price": str(total_price),
            "breakdown": {
                "enclosures": "...",
                "glands": "...",
                "terminals": "..."
            }
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status=400)
```

---


---

## 🎨 BONUS 5: Django Admin customization (5 pkt)

### Zadanie

Stwórz ładny interfejs admin dla zarządzania danymi.

**Plik:** `calculator/admin.py`

```python
from django.contrib import admin
from .models import Enclosure, Gland, Terminal, SimpleOrder
```

---

---

## 🔐 BONUS 6: Autoryzacja API Token (10 pkt)

### Zadanie

Dodaj autoryzację przez tokeny dla API.

```python
def create_order(request):
    """
    Wymaga tokenu autoryzacyjnego.
    
    Header: Authorization: Token abc123...
    """
    # TODO: Implementacja
```

---


---

## 🎯 BONUS 7: Endpoint duplikacji zamówienia (5 pkt)

### Zadanie

**Endpoint:** `POST /api/recruitment/orders/{order_id}/duplicate/`

```python
@api_view(['POST'])
def duplicate_order(request, order_id):
    """
    Duplikuje istniejące zamówienie.
    
    TODO:
    1. Pobierz order po ID
    2. Stwórz nowy order z tymi samymi danymi
    3. Zmień customer_email na nowy (z request)
    4. Przelicz cenę (mogły się zmienić)
    """
    
```

---

---

## 📊 BONUS 8: Dashboard z wykresami (20 pkt)

### Zadanie

Stwórz prosty dashboard z statystykami.

**Endpoint:** `GET /api/recruitment/dashboard/`

```python
@api_view(['GET'])
def dashboard_stats(request):
    """
    Zwraca dane dla dashboard.
    
    TODO: Agreguj dane dla wykresów:
    - Zamówienia w czasie (ostatnie 30 dni)
    - Top produkty (najczęściej zamawianie)
    - Przychody w czasie
    - Średnia wartość zamówienia w czasie
    """
    
    # TODO: Więcej agregacji
    
    return Response({
        "orders_by_day": list(),
        "top_enclosures": ...,
        "revenue_trend": ...
    })
```



---
## 📧 BONUS 9: Email z potwierdzeniem zamówienia (10 pkt)

### Zadanie

Po utworzeniu zamówienia wyślij email do klienta.

**Plik:** `calculator/services/email_service.py`

```python
from django.core.mail import send_mail
from django.template.loader import render_to_string

class OrderEmailService:
    """Serwis wysyłania emaili o zamówieniach."""
    
    def send_order_confirmation(self, order: SimpleOrder):
        """
        Wysyła email z potwierdzeniem zamówienia.
        
        TODO:
        1. Stwórz szablon HTML (templates/emails/order_confirmation.html)
        2. Wygeneruj treść z danymi zamówienia
        3. Wyślij email
        """
        
        subject = f"Potwierdzenie zamówienia #{order.id}"
        
        # TODO: Renderuj szablon
    
        
        # TODO: Wyślij email
   
```

---

## 🎨 BONUS 1: Generowanie programów CNC (15 pkt)

### Opis
Na podstawie pozycji dławików wygeneruj program CNC (G-code) do automatycznego wiercenia otworów.

### Zadanie

**Plik:** `calculator/services/cnc_generator.py`

```python
from typing import List
from decimal import Decimal

class CNCProgramGenerator:
    """
    Generator programów CNC dla otworów dławików.
    """
    
    def generate_gcode(
        self,
        gland_positions: List[dict],  # [{"x": 27.5, "y": 27.5, "diameter": 25}]
        material_thickness: float = 2.0,  # mm
        drill_speed: int = 3000  # RPM
    ) -> str:
        """
        Generuje G-code dla wiercenia otworów.
        
        Przykładowy G-code:
        G21 (mm mode)
        G90 (absolute positioning)
        M03 S3000 (spindle on, 3000 RPM)
        
        G00 Z5.0 (move above work)
        G00 X27.5 Y27.5 (position 1)
        G01 Z-2.5 F100 (drill)
        G00 Z5.0 (retract)
        
        G00 X60.5 Y27.5 (position 2)
        G01 Z-2.5 F100
        G00 Z5.0
        
        M05 (spindle off)
        M30 (end program)
        """
        
        gcode_lines = [
            "G21 (Millimeter mode)",
            "G90 (Absolute positioning)",
            f"M03 S{drill_speed} (Spindle on)",
            "G00 Z5.0 (Safe height)",
            ""
        ]
        
        # TODO: Dla każdej pozycji dodaj:
        # - Pozycjonowanie (G00 X... Y...)
        # - Wiercenie (G01 Z-... F...)
        # - Wycofanie (G00 Z5.0)
        
        for idx, position in enumerate(gland_positions, 1):
            gcode_lines.append(f"(Hole {idx} - {position['size']})")
            # TODO: Dodaj komendy G-code
        
        gcode_lines.extend([
            "",
            "M05 (Spindle off)",
            "M30 (End program)"
        ])
        
        return "\n".join(gcode_lines)
    
```

**Integracja:**
Po utworzeniu zamówienia wygeneruj plik CNC i zapisz w `media/cnc_programs/`.

---

## 📝 Oddanie rozwiązania

1. **Utwórz branch:** `recruitment/[twoje-imie-nazwisko]`
2. **Commituj regularnie** z opisowymi komentarzami
3. **Utwórz Pull Request** z opisem
4. **Dołącz plik:** `IMPLEMENTATION_NOTES.md` zawierający:
   - Czas wykonania każdej części
   - Napotkane problemy i ich rozwiązania

---

## 📞 Kontakt

W razie pytań:
- Email: r.piecyk@grupa-wolff.com

**Powodzenia!** 🚀

---

