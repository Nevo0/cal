"""
Prosty model zamówienia dla zadania rekrutacyjnego.

Skopiuj/dodaj ten model do calculator/models.py
"""

from django.db import models
from decimal import Decimal
import uuid


class SimpleOrder(models.Model):
    """
    Uproszczony model zamówienia dla zadania rekrutacyjnego.
    
    Przechowuje kompletne dane zamówienia w JSON + obliczoną cenę.
    """
    
    # ID zamówienia
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unikalny identyfikator zamówienia"
    )
    
    # Dane klienta
    customer_name = models.CharField(
        max_length=255,
        help_text="Imię i nazwisko klienta"
    )
    customer_email = models.EmailField(
        help_text="Email klienta"
    )
    user_information = models.TextField(
        blank=True,
        null=True,
        help_text="Dodatkowe informacje od użytkownika"
    )
    
    # Dane zamówienia (JSON)
    order_data = models.JSONField(
        help_text="Kompletne dane zamówienia (obudowy, dławiki, terminale)"
    )
    
    # Obliczone ceny
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Całkowita cena zamówienia (PLN)"
    )
    
    enclosures_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Suma cen obudów"
    )
    
    glands_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Suma cen dławików"
    )
    
    terminals_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Suma cen terminali"
    )
    
    # Status walidacji geometrycznej
    geometry_validation_passed = models.BooleanField(
        default=False,
        help_text="Czy walidacja geometryczna przeszła pomyślnie"
    )
    
    geometry_validation_errors = models.JSONField(
        null=True,
        blank=True,
        help_text="Błędy walidacji geometrycznej (jeśli były)"
    )
    
    # Metadane
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Data i czas utworzenia zamówienia"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Data i czas ostatniej aktualizacji"
    )
    
    class Meta:
        db_table = 'simple_orders'
        verbose_name = 'Zamówienie (Simple)'
        verbose_name_plural = 'Zamówienia (Simple)'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.id} - {self.customer_name} - {self.total_price} PLN"
    
    def save(self, *args, **kwargs):
        """
        Przy zapisywaniu automatycznie oblicz cenę jeśli nie jest ustawiona.
        """
        if self.total_price == Decimal('0.00'):
            self.calculate_total_price()
        
        super().save(*args, **kwargs)
    
    def calculate_total_price(self):
        """
        Oblicza całkowitą cenę zamówienia.
        
        TODO: Zaimplementuj tę metodę!
        Powinna sumować ceny:
        - obudów (enclosures_price)
        - dławików (glands_price)
        - terminali (terminals_price)
        
        I zapisać do self.total_price
        """
        self.total_price = Decimal('0.00')
        # TODO: Implementacja dla kandydata
        pass


# Migracja:
# python manage.py makemigrations
# python manage.py migrate

