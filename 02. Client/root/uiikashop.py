# GetSellableSlotTypes icinde ara:
def GetSellableSlotTypes():
	types = [player.SLOT_TYPE_DRAGON_SOUL_INVENTORY, player.SLOT_TYPE_INVENTORY]

# Altina ekle:
	if app.ENABLE_WARDROBE_ITEM_TRANSFER:
		types.append(player.SLOT_TYPE_WARDROBE)

