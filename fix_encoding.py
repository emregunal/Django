import json
import codecs

# Dosyayı farklı encoding'lerle okumayı dene
encodings = ['cp1254', 'latin-1', 'iso-8859-9']

data = None
used_encoding = None

for encoding in encodings:
    try:
        with open('doevent_backup_20251118_220758.json', 'r', encoding=encoding) as f:
            data = json.load(f)
        used_encoding = encoding
        print(f"Dosya {encoding} encoding'i ile başarıyla okundu.")
        break
    except Exception as e:
        print(f"{encoding} ile okuma başarısız: {e}")
        continue

if data:
    # UTF-8 olarak kaydet
    with open('doevent_backup_utf8.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Dosya UTF-8 olarak 'doevent_backup_utf8.json' adıyla kaydedildi.")
    print(f"Toplam {len(data)} kayıt dönüştürüldü.")
else:
    print("Dosya hiçbir encoding ile okunamadı.")
