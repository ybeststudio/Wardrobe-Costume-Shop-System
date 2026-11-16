// Dosyanin uygun bir yerine ekle:
#ifdef ENABLE_WARDROBE_AUTO_STORE
#include "wardrobe.h"
#endif


// LPITEM CItem::RemoveFromCharacter() icinde:
// Ara:
					pOwner->SetItem(TItemPos(SWITCHBOT, m_wCell), NULL);
				}
			}

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
			else if (m_bWindow == WARDROBE)
			{
				if (m_wCell >= WARDROBE_MAX_NUM)
					sys_err("CItem::RemoveFromCharacter: pos >= WARDROBE_MAX_NUM");
				else
					pOwner->SetItem(TItemPos(WARDROBE, m_wCell), NULL);
			}
#endif


// bool CItem::AddToCharacter(LPCHARACTER ch, TItemPos Cell) icinde:
// Ara:
{
	assert(GetSectree() == NULL);
	assert(m_pOwner == NULL);

// Altina ekle:
#ifdef ENABLE_WARDROBE_AUTO_STORE
	if (INVENTORY == Cell.window_type && Cell.cell < INVENTORY_MAX_NUM)
	{
		const int iWardrobeCell = Wardrobe_RedirectCell(ch, this);
		if (iWardrobeCell >= 0)
			Cell = TItemPos(WARDROBE, iWardrobeCell);
	}
#endif


// bool CItem::AddToCharacter(LPCHARACTER ch, TItemPos Cell) icinde:
// Ara:
			return false;
		}
	}

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	else if (WARDROBE == window_type)
	{
		if (pos >= WARDROBE_MAX_NUM)
		{
			sys_err("CItem::AddToCharacter: wardrobe cell overflow: %s to %s cell %d", m_pProto->szName, ch->GetName(), pos);
			return false;
		}
	}
#endif


// DWORD CItem::GetMountSkinVnum() icinde:
// Ara:
DWORD CItem::GetMountSkinVnum()
{
	DWORD dwVnum = GetValue(1);

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
	if (!dwVnum && GetProto())
	{
		for (int i = 0; i < ITEM_APPLY_MAX_NUM; ++i)
		{
			if (GetProto()->aApplies[i].bType == APPLY_MOUNT && GetProto()->aApplies[i].lValue > 0)
				return GetProto()->aApplies[i].lValue;
		}
	}
#endif

