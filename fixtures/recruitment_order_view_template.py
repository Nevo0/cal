"""
Szablon widoku API dla zadania rekrutacyjnego.

Ten plik pokazuje uproszczoną strukturę widoku.
"""

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from decimal import Decimal
import logging

from fixtures.simple_order_model import SimpleOrder

from .order_serializers import OrderSerializer


# TODO: Import walidatorów (po implementacji)


logger = logging.getLogger(__name__)


@api_view(['POST'])
def create_order(request):
    """
    Tworzy nowe zamówienie z walidacją geometryczną.
    
    Endpoint: POST /api/orders/create/
    
    Request body: OrderSerializer (JSON)
    
    Returns:
        201: Zamówienie utworzone pomyślnie
        400: Błąd walidacji danych lub geometrii
        401: Brak autoryzacji
        500: Błąd serwera
    """
    
    # KROK 1: Walidacja autoryzacji (opcjonalne dla zadania rekrutacyjnego)

    
    # KROK 2: Walidacja danych wejściowych (serializacja)
    serializer = OrderSerializer(data=request.data)
    if not serializer.is_valid():
        logger.error(f"Validation error: {serializer.errors}")
        return Response(
            {
                "success": False,
                "errors": serializer.errors,
                "message": "Dane wejściowe są niepoprawne"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # KROK 3: Walidacja geometryczna - ZADANIE DLA KANDYDATA
    validated_data = serializer.validated_data
    
    # TODO: (OPCJONALNIE) Zaimplementuj walidację geometryczną   
    # validation_errors = []
    # for box_data in validated_data.get('saveBox', []):
    #     # Walidacja dławików i terminali
    #     pass
    # 
    # if validation_errors:
    #     return Response({
    #         "success": False,
    #         "errors": validation_errors
    #     }, status=status.HTTP_400_BAD_REQUEST)
  
    # KROK 4: Obliczenie ceny - ZADANIE DLA KANDYDATA
    try:
        total_price = calculate_order_price(validated_data)
        
        # KROK 5: Zapisanie zamówienia do bazy
        order = SimpleOrder.objects.create(
            customer_name=validated_data['name'],
            customer_email=validated_data['email'],
            user_information=validated_data.get('userInformation', ''),
            order_data=validated_data,
            total_price=total_price,
            # TODO: Dodaj pozostałe ceny
            # enclosures_price=...,
            # glands_price=...,
            # terminals_price=...,
            geometry_validation_passed=True  # TODO: Użyj wyniku walidacji
        )
        
        # KROK 6: Zwróć odpowiedź
        return Response({
            "success": True,
            "order_id": str(order.id),
            "total_price": str(total_price),
            "message": "Zamówienie utworzone pomyślnie"
        }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}", exc_info=True)
        return Response(
            {
                "success": False,
                "error": str(e),
                "message": "Wystąpił błąd podczas tworzenia zamówienia"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def validate_order_layout(request):
    """
    Waliduje układ komponentów bez tworzenia zamówienia.
    
    Endpoint: POST /api/orders/validate/
    
    To jest endpoint BONUS - pozwala frontendowi sprawdzić
    czy komponenty zmieszczą się PRZED utworzeniem zamówienia.
    
    Request body: OrderSerializer (JSON)
    
    Returns:
        200: Walidacja pomyślna + szczegóły (pozycje dławików, etc.)
        400: Błąd walidacji
    """
    
    # TODO: Zaimplementuj walidację bez tworzenia zamówienia
    # Bardzo podobne do create_order, ale:
    # 1. Nie tworzy zamówienia w bazie
    # 2. Zwraca szczegółowe info o rozmieszczeniu komponentów
    
    serializer = OrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "valid": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    validated_data = serializer.validated_data
    
    # TODO: Uruchom walidatory geometryczne
    # Zwróć szczegółowe informacje:
    response_data = {
        "valid": True,
        "message": "Wszystkie komponenty zmieszczą się w wybranych obudowach",
        "details": {
           
        }
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


# Pomocnicze funkcje

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

