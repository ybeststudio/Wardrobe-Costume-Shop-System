# Wardrobe & Costume Shop System

Gardırop ve Kostüm Mağazası. Kostüm görünümlerini gardıropta saklar, kıyafet setleri kaydedip tek tıkla uygular; Kostüm Mağazası'nda kategori, cinsiyet ve canlı önizleme ile kostüm satın alınır.

![Önizleme](preview.png)

---

## Ne var?

- Gardırop penceresi (`uiwardrobe.py`): görünüm kataloğu, kıyafet setleri, uygula / kaldır
- Kostüm, saç, kanat, silah ve binek görünümleri; parlama (shining) desteği
- Gardıroba eşya aktarma ve otomatik saklama *(opsiyonel flag)*
- Kostüm Mağazası (`uicostumeshop.py`): kategori, cinsiyet filtresi, render target önizleme
- Envanterden mağazayı açma *(opsiyonel flag)*
- Panoya kopyalama (`app.SetClipboardText`)

## Paket yapısı

```
01. Svn/          → Client & Game source (Ara / Altına ekle / Bul / Değiştir patch dosyaları + yeni dosyalar)
02. Client/       → root, uiscript, locale, d_/ymir work assetleri
03. Server/       → MySQL tabloları, quest ve sunucu verileri
Added/            → Değişikliklerin uygulanmış hali (tam dosyalar, karşılaştırma için)
```

## Flagler

**Client** (`Locale_inc.h`):
- `ENABLE_CLIPBOARD_TEXT`
- `ENABLE_WARDROBE_ITEM_TRANSFER`
- `ENABLE_WARDROBE_SYSTEM`
- `ENABLE_COSTUME_SHOP`

**Game** (`service.h`):
- `ENABLE_WARDROBE_AUTO_STORE`
- `ENABLE_WARDROBE_ITEM_TRANSFER`
- `ENABLE_WARDROBE_SYSTEM`
- `ENABLE_COSTUME_SHOP`
- `ENABLE_COSTUME_SHOP_INVENTORY_OPEN`

Client ve game tarafında aynı isimli flagler birlikte açık olmalı; tek taraf açıkken paket / komut uyumsuzluğu olur.

## Kurulum (kısaca)

1. `01. Svn` altındaki patch dosyalarını kendi source ağacına uygula. Her blokta `// Ara:` satırlarını bul, `// Altına ekle:` kısmını altına ekle; `// Bul:` / `// Degistir:` bloklarında bulduğun satırları verilen blokla değiştir.
2. Yeni dosyaları (`wardrobe.cpp`, `wardrobe.h`, `costume_shop.cpp`, `costume_shop.h`) ilgili klasöre kopyala; game için `Makefile`, client için `vcxproj.txt` notuna göre projeye ekle.
3. `02. Client/root` ve `02. Client/uiscript` içindeki tam dosyaları pack'e kopyala, patch dosyalarını (`# Ara:` / `# Altına ekle:`) kendi dosyalarına uygula.
4. `02. Client/locale/<dil>/` satırlarını kendi locale dosyalarının sonuna ekle.
5. `02. Client/d_/ymir work/` görsellerini pack'e ekle (`d:/ymir work/...`).
6. `03. Server` içindeki SQL ve verileri sunucuya uygula.
7. Client + game + db rebuild, pack güncelle.

## Bağımlılıklar

- Render Target sistemi (`renderTarget` modülü)
- Kanat görünümleri için kuşak (acce) skin sistemi
- `uiadvancedgameoptions.py` patch'i yalnızca **Advanced Game Options** paketi kuruluysa gerekli.

## Notlar

- `03. Server/share/locale/europe/` altındaki dosyaları kendi sunucu locale klasörüne kopyala (ör. `share/locale/turkey/`).
- Quest dosyasını kendi quest listene ekle, `quest_functions` satırlarını ekleyip questleri yeniden derle.
- Locale dosyalarında yalnızca bu sisteme ait anahtarlar var; `new_locale_*` kendi eklediğimiz, `locale_game` / `locale_interface` resmi istemcide olmayan anahtarlar. Türkçe dosyalar cp1254.
- Patch'lerde başka sistemlere ait satırlar görürsen (farklı `#ifdef`), o sistem sende yoksa yok say.
- Fork farklıysa paket header / struct sıralamasını kontrol et.

---

## İletişim

Sorular için Discord'dan yazabilirsin.

| | |
|---|---|
| GitHub | [github.com/ybeststudio](https://github.com/ybeststudio) |
| Discord | [discord.gg/NXmc6JrwYr](https://discord.gg/NXmc6JrwYr) |
| Discord ID | `beststudio` |
| Web | [bestpro.dev](https://bestpro.dev) |
| TurkMMO | [Best Studio](https://forum.turkmmo.com/uye/2104546-best-studio/) |
| YouTube | [@ybeststudio](https://www.youtube.com/@ybeststudiotr) |
| Instagram | [@ybeststudio](https://www.instagram.com/ybeststudio) |
| Facebook | [ybeststudio](https://www.facebook.com/ybeststudio/) |
| Twitter | [@ybeststudio](https://twitter.com/ybeststudio) |
| TikTok | [@ybeststudio](https://tiktok.com/@ybeststudio) |

---

**Best Studio** — Metin2 private server çözümleri
