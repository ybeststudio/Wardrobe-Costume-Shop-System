// Ara:
static DWORD PetEvolutionLevelCap(DWORD dwEvolution);

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
#include "wardrobe.h"
#endif


// LPGROWTH_PET CGrowthPet::Summon(LPITEM pSummonItem, bool bIsResummon) icinde:
// Ara:
		if (dwCostumeMob)
			dwPetVnum = dwCostumeMob;
	}

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	dwPetVnum = Wardrobe_VisualPetMob(m_pOwner, dwPetVnum);
#endif

