// Ara:
	LPITEM pDSItems[DRAGON_SOUL_INVENTORY_MAX_NUM];
	WORD wDSItemGrid[DRAGON_SOUL_INVENTORY_MAX_NUM];

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	LPITEM pWardrobeItems[WARDROBE_MAX_NUM];
#endif


// Ara:
		LPITEM GetItem(TItemPos Cell) const;
		LPITEM GetInventoryItem(WORD wCell) const;

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
		LPITEM GetWardrobeItem(WORD wCell) const;
		WORD GetVisualPart(BYTE bPartPos) const;
#endif

