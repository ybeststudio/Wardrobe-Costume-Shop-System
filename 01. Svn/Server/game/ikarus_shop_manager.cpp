// Ara:
	std::transform(res.begin(), res.end(), res.begin(), lower);
	return res;
}

// Altina ekle:
#ifdef ENABLE_WARDROBE_ITEM_TRANSFER
#include "wardrobe.h"
#endif


// static LPITEM GetShopSourceItem(LPCHARACTER ch, const TItemPos& pos) icinde:
// Ara:
static LPITEM GetShopSourceItem(LPCHARACTER ch, const TItemPos& pos)
{

// Altina ekle:
#ifdef ENABLE_WARDROBE_ITEM_TRANSFER
	if (pos.window_type == WARDROBE)
		return ch->GetWardrobeItem(pos.cell);
#endif


// Ara:
		memcpy(sitem.aAttr, item->GetAttributes(),	sizeof(sitem.aAttr));
		memcpy(sitem.alSockets, item->GetSockets(), sizeof(sitem.alSockets));
		MoveAndDestroyInstance(item, IKASHOP_OFFLINESHOP, destPos);

// Altina ekle:
#ifdef ENABLE_WARDROBE_ITEM_TRANSFER
		if (pos.window_type == WARDROBE)
			Wardrobe_OnItemLeft(ch);
#endif

