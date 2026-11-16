// Ara:
const DWORD c_DragonSoul_Inventory_Start = 0;
const DWORD c_DragonSoul_Inventory_Box_Size = 32;

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
const DWORD c_Wardrobe_Count = 4500;
#endif


// Ara:
	SLOT_TYPE_OFFLINESHOP,

// Altina ekle:
#ifdef ENABLE_WARDROBE_ITEM_TRANSFER
	SLOT_TYPE_WARDROBE,
#endif


// Ara:
	IKASHOP_OFFLINESHOP = 16,
	IKASHOP_SAFEBOX = 17,
	IKASHOP_AUCTION = 18,

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	WARDROBE = 20,
#endif


// Ara:
			case SWITCHBOT:
				return cell < SWITCHBOT_SLOT_COUNT;
				break;

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
			case WARDROBE:
				return cell < c_Wardrobe_Count;
				break;
#endif

