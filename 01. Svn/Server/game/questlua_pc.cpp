// Ara:
		lua_pushstring(L, LC_LOCALE(LOCALE_DEFAULT));
		return 1;
	}

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
	int pc_open_costume_shop(lua_State* L)
	{
		CQuestManager& q = CQuestManager::instance();
		LPCHARACTER ch = q.GetCurrentCharacterPtr();
		LPCHARACTER npc = q.GetCurrentNPCCharacterPtr();
		if (ch && npc)
			CostumeShop_Open(ch, npc);
		return 0;
	}
#endif


// Ara:
			{ "get_leadership",									pc_get_leadership						},
			{ "getqf",											pc_get_quest_flag						},
			{ "setqf",											pc_set_quest_flag						},

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
			{ "open_costume_shop",								pc_open_costume_shop					},
#endif

