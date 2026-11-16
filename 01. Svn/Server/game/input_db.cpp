// void CInputDB::ItemLoad(LPDESC d, const char * c_pData) icinde:
// Ara:
		if ((p->window == INVENTORY && ch->GetInventoryItem(p->pos)) ||
				(p->window == EQUIPMENT && ch->GetWear(p->pos))

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
				|| (p->window == WARDROBE && (p->pos >= WARDROBE_MAX_NUM || ch->GetWardrobeItem(p->pos)))
#endif


// void CInputDB::ItemLoad(LPDESC d, const char * c_pData) icinde:
// Ara:
				case SWITCHBOT:

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
				case WARDROBE:
#endif

