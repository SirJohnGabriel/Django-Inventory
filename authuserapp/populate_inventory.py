from authuserapp.models import InventoryItem

mock_data = [
    ('ABC123', 12.50, 30, 'available'),
    ('DEF456', 45.00, 0, 'unavailable'),
    ('GHI789', 99.99, 10, 'available'),
]

for sku, price, count, status in mock_data:
    InventoryItem.objects.create(sku=sku, price=price, count=count, status=status)

print("Mock items added.")
