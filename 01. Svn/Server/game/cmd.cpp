// Ara:
ACMD(do_guild_quest);

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
ACMD(do_costume_shop);
#ifdef ENABLE_WARDROBE_SYSTEM
ACMD(do_wardrobe);
#endif
#endif


// Ara:
	{ "guild_quest", do_guild_quest, 0, POS_DEAD, GM_PLAYER },

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
	{ "costume_shop", do_costume_shop, 0, POS_DEAD, GM_PLAYER },
#ifdef ENABLE_WARDROBE_SYSTEM
	{ "wardrobe", do_wardrobe, 0, POS_DEAD, GM_PLAYER },
#endif
#endif

