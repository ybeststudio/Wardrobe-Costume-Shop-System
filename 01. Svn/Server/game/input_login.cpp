// Dosyanin uygun bir yerine ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	#include "wardrobe.h"
#ifdef ENABLE_MOKOKO_SYSTEM
#include "mokoko.h"
#ifdef ENABLE_ENERGY_CRYSTAL
#include "energy_crystal.h"
#endif
#endif
#endif


// void CInputLogin::Entergame(LPDESC d, const char * data) icinde:
// Ara:
	CSwitchbotManager::Instance().EnterGame(ch);

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	Wardrobe_OnLogin(ch);
#endif

