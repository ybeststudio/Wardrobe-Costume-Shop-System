// BYTE SlotTypeToInvenType(BYTE bSlotType) icinde:
// Ara:
	if (bSlotType == SLOT_TYPE_SHOP_REPURCHASE)
		return SHOP_REPURCHASE;

// Altina ekle:
#ifdef ENABLE_WARDROBE_ITEM_TRANSFER
	if (bSlotType == SLOT_TYPE_WARDROBE)
		return WARDROBE;
#endif

