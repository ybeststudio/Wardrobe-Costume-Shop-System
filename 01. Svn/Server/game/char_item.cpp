// Dosyanin uygun bir yerine ekle:
#ifdef ENABLE_WARDROBE_AUTO_STORE
#include "wardrobe.h"
#endif


// Ara:
	}
	return NULL;
}

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
LPITEM CHARACTER::GetWardrobeItem(WORD wCell) const
{
	if (wCell >= WARDROBE_MAX_NUM || !m_pItemStorage)
		return NULL;
	return ItemStorage().pWardrobeItems[wCell];
}
#endif


// void CHARACTER::SetItem(TItemPos Cell, LPITEM pItem) icinde:
// Ara:
		m_pointsInstant.pSwitchbotItems[wCell] = pItem;
	}
	break;

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	case WARDROBE:
	{
		if (wCell >= WARDROBE_MAX_NUM)
		{
			sys_err("CHARACTER::SetItem: invalid wardrobe item cell %d", wCell);
			return;
		}
		if (pItem && ItemStorage().pWardrobeItems[wCell])
			return;
		ItemStorage().pWardrobeItems[wCell] = pItem;
	}
	break;
#endif


// void CHARACTER::SetItem(TItemPos Cell, LPITEM pItem) icinde:
// Ara:
			case SWITCHBOT:
				pItem->SetWindow(SWITCHBOT);
				break;

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
			case WARDROBE:
				pItem->SetWindow(WARDROBE);
				break;
#endif


// void CHARACTER::ClearItem() icinde:
// Ara:
			M2_DESTROY_ITEM(item);
		}
	}

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	for (i = 0; i < WARDROBE_MAX_NUM; ++i)
	{
		if ((item = GetWardrobeItem(i)))
		{
			item->SetSkipSave(true);
			ITEM_MANAGER::instance().FlushDelayedSave(item);

			item->RemoveFromCharacter();
			M2_DESTROY_ITEM(item);
		}
	}
#endif


// bool CHARACTER::PickupItem(DWORD dwVID) icinde:
// Ara:
				char szHint[32 + 1];
				snprintf(szHint, sizeof(szHint), "%s %u %u", item->GetName(), item->GetCount(), item->GetOriginalVnum());
				LogManager::instance().ItemLog(this, item, "GET", szHint);

// Altina ekle:
#ifdef ENABLE_WARDROBE_AUTO_STORE
				Wardrobe_StoreFromInventory(this, item);
#endif


// bool CHARACTER::PickupItem(DWORD dwVID) icinde:
// Ara:
			char szHint[32+1];
			snprintf(szHint, sizeof(szHint), "%s %u %u", item->GetName(), item->GetCount(), item->GetOriginalVnum());
			LogManager::instance().ItemLog(owner, item, "GET", szHint);

// Altina ekle:
#ifdef ENABLE_WARDROBE_AUTO_STORE
			Wardrobe_StoreFromInventory(owner, item);
#endif


// bool CHARACTER::UnequipItem(LPITEM item) icinde:
// Ara:
	int pos;
	if (false == CanUnequipNow(item))
		return false;

// Altina ekle:
#ifdef ENABLE_WARDROBE_AUTO_STORE
	const int iWardrobeCell = Wardrobe_AutoStoreCell(this, item);
#endif


// bool CHARACTER::UnequipItem(LPITEM item) icinde:
// Ara:
	item->RemoveFromCharacter();

// Altina ekle:
#ifdef ENABLE_WARDROBE_AUTO_STORE
	if (iWardrobeCell >= 0)
	{
#ifdef ENABLE_PICKUP_ITEM_EFFECT
		item->AddToCharacter(this, TItemPos(WARDROBE, iWardrobeCell), false);
#else
		item->AddToCharacter(this, TItemPos(WARDROBE, iWardrobeCell));
#endif
		Wardrobe_OnUnequipStored(this, item);
	}
	else
#endif


// void CHARACTER::AutoGiveItem(LPITEM item, bool longOwnerShip) icinde:
// Ara:
		sys_err ("item %d 's owner exists!", item->GetID());
		return;
	}

// Altina ekle:
#ifdef ENABLE_WARDROBE_AUTO_STORE
	if (Wardrobe_StoreNewItem(this, item))
		return;
#endif

