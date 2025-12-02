import json

# UTF-8 dosyasını oku
with open('doevent_backup_utf8.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Django sistem tablolarını filtrele (bunlar otomatik oluşturuluyor)
exclude_models = [
    'contenttypes.contenttype',
    'auth.permission',
    'admin.logentry',
    'sessions.session'
]

filtered_data = [
    item for item in data 
    if item['model'] not in exclude_models
]

# Filtrelenmiş veriyi kaydet
with open('doevent_backup_filtered.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

print(f"Orijinal kayıt sayısı: {len(data)}")
print(f"Filtrelenmiş kayıt sayısı: {len(filtered_data)}")
print(f"Çıkarılan kayıt sayısı: {len(data) - len(filtered_data)}")
print("\nFiltreden geçen model tipleri:")
model_types = set(item['model'] for item in filtered_data)
for model in sorted(model_types):
    count = sum(1 for item in filtered_data if item['model'] == model)
    print(f"  - {model}: {count} kayıt")
