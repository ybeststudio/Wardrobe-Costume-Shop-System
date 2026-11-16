/*********************************************************************
 * File Name : wardrobe.h
 * Author    : BestStudio
 * Version   : 1.0.0
 * Date      : 02-11-2026  
 */

#pragma once
#include "../../common/service.h"

#ifdef ENABLE_WARDROBE_SYSTEM
//
// Storage: item window WARDROBE (WARDROBE_MAX_NUM cells, one item per cell). Items keep all their data.
//
//	/wardrobe catalog <s> 0 0 0
//	/wardrobe outfits <s> 0
//	/wardrobe deposit <s> <inventory cell> <item vnum>
//	/wardrobe withdraw <s> <wardrobe cell> <item vnum>
//	/wardrobe apply <s> <0 | outfit slot + 1> <9 vnums>
//	/wardrobe save <s> <slot> <revision> <name hex> <9 vnums>
//	/wardrobe rename <s> <slot> <revision> <name hex>
//	/wardrobe delete <s> <slot> <revision>
//	WardrobeCatalogBegin <s> <rows>, WardrobeCatalogCat <s> <id> <name hex>, WardrobeCatalogRows <s> <vnum,cat,slot;...>,
//	WardrobeCatalogEnd <s>
//	WardrobeOutfitsBegin <s> <count> <remembered slot + 1> <applied slot + 1>,
//	WardrobeOutfitRow <s> <slot> <revision> <name hex | -> <9 vnums>, WardrobeOutfitsEnd <s>
//	WardrobeResult <s> <code>, WardrobeAppearance <9 vnums>,
//	WardrobeProgress <costumes> <level> <total exp> <exp in level> <exp per level>
enum EWardrobeResult
{
	WARDROBE_RESULT_OK			= 0,
	WARDROBE_RESULT_ERROR		= 1,
	WARDROBE_RESULT_INVALID		= 2,
	WARDROBE_RESULT_FULL		= 3,
	WARDROBE_RESULT_BUSY		= 4,	// rate limit
	WARDROBE_RESULT_UNOWNED		= 5,
	WARDROBE_RESULT_BLOCKED		= 6,	// exchange, shop, safebox ... open
};

void Wardrobe_Command(LPCHARACTER ch, const char* argument);
void Wardrobe_OnLogin(LPCHARACTER ch);
void Wardrobe_OnDestroy(LPCHARACTER ch);
#ifdef ENABLE_WARDROBE_ITEM_TRANSFER
void Wardrobe_OnItemLeft(LPCHARACTER ch);
#endif

DWORD Wardrobe_VisualMountVnum(const CHARACTER* ch, DWORD dwMountVnum);
DWORD Wardrobe_VisualShining(const CHARACTER* ch, int iIndex, DWORD dwVnum);
DWORD Wardrobe_VisualPetMob(const CHARACTER* ch, DWORD dwMobVnum);
WORD Wardrobe_VisualPart(const CHARACTER* ch, BYTE bPartPos, WORD wPart);

#ifdef ENABLE_WARDROBE_AUTO_STORE
bool Wardrobe_StoreNewItem(LPCHARACTER ch, LPITEM item);
bool Wardrobe_StoreFromInventory(LPCHARACTER ch, LPITEM item);
int Wardrobe_AutoStoreCell(LPCHARACTER ch, LPITEM item);
void Wardrobe_OnUnequipStored(LPCHARACTER ch, LPITEM item);
int Wardrobe_RedirectCell(LPCHARACTER ch, LPITEM item);
#endif
#endif
