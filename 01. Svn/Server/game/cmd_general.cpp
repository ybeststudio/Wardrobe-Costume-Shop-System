// Ara:
{
	GuildQuest_Reward(ch);
}

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
#include "costume_shop.h"
ACMD(do_costume_shop)
{
	CostumeShop_Command(ch, argument);
}

#ifdef ENABLE_WARDROBE_SYSTEM
#include "wardrobe.h"
ACMD(do_wardrobe)
{
	Wardrobe_Command(ch, argument);
}
#endif
#endif

