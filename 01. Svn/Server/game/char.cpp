// Ara:
	using namespace std;

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
#include "wardrobe.h"
#ifdef ENABLE_MOKOKO_SYSTEM
#include "mokoko.h"
#endif
#endif


// void CHARACTER::Destroy() icinde:
// Ara:
	SetIkarusShopSafebox(nullptr);
	SetIkarusAuction(nullptr);
	SetIkarusAuctionGuest(nullptr);

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	if (IsPC())
		Wardrobe_OnDestroy(this);
#endif


// void CHARACTER::EncodeInsertPacket(LPENTITY entity) icinde:
// Bul:
		addPacket.awPart[CHR_EQUIPPART_ARMOR] = GetPart(PART_MAIN);
		addPacket.awPart[CHR_EQUIPPART_WEAPON] = GetPart(PART_WEAPON);
		addPacket.awPart[CHR_EQUIPPART_HEAD] = GetPart(PART_HEAD);
		addPacket.awPart[CHR_EQUIPPART_HAIR] = GetPart(PART_HAIR);

// Degistir:
#ifdef ENABLE_WARDROBE_SYSTEM
		addPacket.awPart[CHR_EQUIPPART_ARMOR] = GetVisualPart(PART_MAIN);
		addPacket.awPart[CHR_EQUIPPART_WEAPON] = GetVisualPart(PART_WEAPON);
		addPacket.awPart[CHR_EQUIPPART_HEAD] = GetPart(PART_HEAD);
		addPacket.awPart[CHR_EQUIPPART_HAIR] = GetVisualPart(PART_HAIR);
#else
		addPacket.awPart[CHR_EQUIPPART_ARMOR] = GetPart(PART_MAIN);
		addPacket.awPart[CHR_EQUIPPART_WEAPON] = GetPart(PART_WEAPON);
		addPacket.awPart[CHR_EQUIPPART_HEAD] = GetPart(PART_HEAD);
		addPacket.awPart[CHR_EQUIPPART_HAIR] = GetPart(PART_HAIR);
#endif


// void CHARACTER::EncodeInsertPacket(LPENTITY entity) icinde:
// Bul:
		addPacket.awPart[CHR_EQUIPPART_ACCE] = GetPart(PART_ACCE);

// Degistir:
#ifdef ENABLE_WARDROBE_SYSTEM
		addPacket.awPart[CHR_EQUIPPART_ACCE] = GetVisualPart(PART_ACCE);
#else
		addPacket.awPart[CHR_EQUIPPART_ACCE] = GetPart(PART_ACCE);
#endif


// void CHARACTER::EncodeInsertPacket(LPENTITY entity) icinde:
// Bul:
		addPacket.dwMountVnum = GetMountVnum();

// Degistir:
#ifdef ENABLE_WARDROBE_SYSTEM
		addPacket.dwMountVnum = Wardrobe_VisualMountVnum(this, GetMountVnum());
#else
		addPacket.dwMountVnum = GetMountVnum();
#endif


// void CHARACTER::EncodeInsertPacket(LPENTITY entity) icinde:
// Ara:
		{
			LPITEM pkShining = IsPC() ? GetWear(WEAR_SHINING_WEAPON + i) : NULL;
			addPacket.adwShining[i] = pkShining ? pkShining->GetVnum() : 0;

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
			addPacket.adwShining[i] = Wardrobe_VisualShining(this, i, addPacket.adwShining[i]);
#endif


// void CHARACTER::UpdatePacket() icinde:
// Bul:
	pack.awPart[CHR_EQUIPPART_ARMOR] = GetPart(PART_MAIN);
	pack.awPart[CHR_EQUIPPART_WEAPON] = GetPart(PART_WEAPON);
	pack.awPart[CHR_EQUIPPART_HEAD] = GetPart(PART_HEAD);
	pack.awPart[CHR_EQUIPPART_HAIR] = GetPart(PART_HAIR);

// Degistir:
#ifdef ENABLE_WARDROBE_SYSTEM
	pack.awPart[CHR_EQUIPPART_ARMOR] = GetVisualPart(PART_MAIN);
	pack.awPart[CHR_EQUIPPART_WEAPON] = GetVisualPart(PART_WEAPON);
	pack.awPart[CHR_EQUIPPART_HEAD] = GetPart(PART_HEAD);
	pack.awPart[CHR_EQUIPPART_HAIR] = GetVisualPart(PART_HAIR);
#else
	pack.awPart[CHR_EQUIPPART_ARMOR] = GetPart(PART_MAIN);
	pack.awPart[CHR_EQUIPPART_WEAPON] = GetPart(PART_WEAPON);
	pack.awPart[CHR_EQUIPPART_HEAD] = GetPart(PART_HEAD);
	pack.awPart[CHR_EQUIPPART_HAIR] = GetPart(PART_HAIR);
#endif


// void CHARACTER::UpdatePacket() icinde:
// Bul:
	pack.awPart[CHR_EQUIPPART_ACCE] = GetPart(PART_ACCE);

// Degistir:
#ifdef ENABLE_WARDROBE_SYSTEM
	pack.awPart[CHR_EQUIPPART_ACCE] = GetVisualPart(PART_ACCE);
#else
	pack.awPart[CHR_EQUIPPART_ACCE] = GetPart(PART_ACCE);
#endif


// void CHARACTER::UpdatePacket() icinde:
// Bul:
	pack.dwMountVnum	= GetMountVnum();

// Degistir:
#ifdef ENABLE_WARDROBE_SYSTEM
	pack.dwMountVnum	= Wardrobe_VisualMountVnum(this, GetMountVnum());
#else
	pack.dwMountVnum	= GetMountVnum();
#endif


// void CHARACTER::UpdatePacket() icinde:
// Ara:
	{
		LPITEM pkShining = IsPC() ? GetWear(WEAR_SHINING_WEAPON + i) : NULL;
		pack.adwShining[i] = pkShining ? pkShining->GetVnum() : 0;

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
		pack.adwShining[i] = Wardrobe_VisualShining(this, i, pack.adwShining[i]);
#endif


// void CHARACTER::PetSummon(LPITEM petItem) icinde:
// Ara:
		mobVnum = petSkinItem->GetValue(1);
	else
		mobVnum = petItem->GetValue(1) ? petItem->GetValue(1) : petItem->GetValue(0);

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	mobVnum = Wardrobe_VisualPetMob(this, mobVnum);
#endif

