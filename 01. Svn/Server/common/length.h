// Ara:
};

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
enum EWardrobeValues
{
	WARDROBE_MAX_NUM = 4500,
	WARDROBE_LOOK_COUNT = 9,			// body, hair, mount, sash, weapon, sash skin, pet, shining weapon, shining armor
	WARDROBE_OUTFIT_MAX = 15,
	WARDROBE_OUTFIT_NAME_MAX = 48,		// bytes
	WARDROBE_EXP_PER_COSTUME = 100,
	WARDROBE_EXP_PER_LEVEL = 1000,
};

enum EWardrobeLookSlots
{
	WARDROBE_LOOK_BODY,
	WARDROBE_LOOK_HAIR,
	WARDROBE_LOOK_MOUNT,
	WARDROBE_LOOK_ACCE,
	WARDROBE_LOOK_WEAPON,
	WARDROBE_LOOK_ACCE_SKIN,
	WARDROBE_LOOK_PET,
	WARDROBE_LOOK_SHINING_WEAPON,
	WARDROBE_LOOK_SHINING_ARMOR,
};
#endif


// Ara:
	IKASHOP_OFFLINESHOP = 16,
	IKASHOP_SAFEBOX = 17,
	IKASHOP_AUCTION = 18,

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	WARDROBE = 20,			// fixed (same in the client): player.item `window` enum member 20 is 'WARDROBE' (the number is stored)
#endif

