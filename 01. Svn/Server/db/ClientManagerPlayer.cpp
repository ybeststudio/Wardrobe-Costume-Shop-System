// static const char* GetPlayerItemWindowList() icinde:
// Bul:
		snprintf(s_szList, sizeof(s_szList), "%d,%d,%d,%d,%d", INVENTORY, EQUIPMENT, DRAGON_SOUL_INVENTORY, BELT_INVENTORY, SWITCHBOT);

// Degistir:
#ifdef ENABLE_WARDROBE_SYSTEM
		snprintf(s_szList, sizeof(s_szList), "%d,%d,%d,%d,%d,%d", INVENTORY, EQUIPMENT, DRAGON_SOUL_INVENTORY, BELT_INVENTORY, SWITCHBOT, WARDROBE);
#else
		snprintf(s_szList, sizeof(s_szList), "%d,%d,%d,%d,%d", INVENTORY, EQUIPMENT, DRAGON_SOUL_INVENTORY, BELT_INVENTORY, SWITCHBOT);
#endif

