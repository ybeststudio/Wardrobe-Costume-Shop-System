/*********************************************************************
 * File Name : costume_shop.h
 * Author    : BestStudio
 * Version   : 1.0.0
 * Date      : 06-11-2026  
 */

#pragma once
#include "../../common/service.h"
#include <vector>

#ifdef ENABLE_COSTUME_SHOP
//	id	category	vnum	costume_coupons	mount_coupons	pet_coupons	start_time	end_time
// Categories: 1 body, 2 hair, 3 weapon, 4 wing, 5 mount, 6 pet, 7 shining.
// start/end (unix time, 0 = always) mark temporary entries.
//
//	                  CostumeShopResult <code>
enum ECostumeShop
{
	COSTUME_SHOP_NPC_VNUM			= 9393,	// Kostum Terzisi
	COSTUME_SHOP_COUPON_COSTUME		= 90020,
	COSTUME_SHOP_COUPON_MOUNT		= 90021,
	COSTUME_SHOP_COUPON_PET			= 90022,
	COSTUME_SHOP_COUPON_COUNT		= 3,
	COSTUME_SHOP_MAX_BUY			= 8,
	COSTUME_SHOP_NPC_DISTANCE		= 2000,
};

enum ECostumeShopResult
{
	COSTUME_SHOP_RESULT_OK				= 0,
	COSTUME_SHOP_RESULT_FAR				= 1,
	COSTUME_SHOP_RESULT_INVALID			= 2,	// unknown / expired entry
	COSTUME_SHOP_RESULT_NO_COUPON		= 3,
	COSTUME_SHOP_RESULT_NO_SPACE		= 4,
};

void CostumeShop_Open(LPCHARACTER ch, LPCHARACTER npc);
void CostumeShop_Command(LPCHARACTER ch, const char* argument);
#ifdef ENABLE_WARDROBE_SYSTEM
void CostumeShop_GetCatalog(std::vector<DWORD>& vecVnum);
#endif
#endif
