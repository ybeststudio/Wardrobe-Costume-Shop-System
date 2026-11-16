// Ara:
	CPythonPlayer::Instance().SendClickItemPacket(ivid);
	return Py_BuildNone();
}

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
// occupied wardrobe storage cells
PyObject* playerGetWardrobeCells(PyObject* poSelf, PyObject* poArgs)
{
	CPythonPlayer& rkPlayer = CPythonPlayer::Instance();
	PyObject* poList = PyList_New(0);
	for (DWORD i = 0; i < c_Wardrobe_Count; ++i)
	{
		const TItemData* p = rkPlayer.GetItemData(TItemPos(WARDROBE, i));
		if (p && p->vnum)
		{
			PyObject* poCell = PyInt_FromLong(i);
			PyList_Append(poList, poCell);
			Py_DECREF(poCell);
		}
	}
	return poList;
}

PyObject* playerGetWardrobeInventoryRevision(PyObject* poSelf, PyObject* poArgs)
{
	return Py_BuildValue("i", CPythonPlayer::Instance().GetItemRevision());
}

PyObject* playerGetOwnedCostumeVnums(PyObject* poSelf, PyObject* poArgs)
{
	CPythonPlayer& rkPlayer = CPythonPlayer::Instance();
	std::set<DWORD> setVnum;
	for (DWORD i = 0; i < c_Inventory_Count; ++i)
	{
		const TItemData* p = rkPlayer.GetItemData(TItemPos(INVENTORY, i));
		if (p && p->vnum)
			setVnum.insert(p->vnum);
	}
	for (DWORD i = 0; i < c_Wardrobe_Count; ++i)
	{
		const TItemData* p = rkPlayer.GetItemData(TItemPos(WARDROBE, i));
		if (p && p->vnum)
			setVnum.insert(p->vnum);
	}
	PyObject* poList = PyList_New(0);
	for (DWORD dwVnum : setVnum)
	{
		PyObject* poVnum = PyInt_FromLong(dwVnum);
		PyList_Append(poList, poVnum);
		Py_DECREF(poVnum);
	}
	return poList;
}
#endif


// void initPlayer() icinde:
// Ara:
		{ "ClearSkillDict", playerClearSkillDict, METH_VARARGS },
		{ "DisableToggleSkill", playerDisableToggleSkill, METH_VARARGS },
		{ "GetItemIndex", playerGetItemIndex, METH_VARARGS },

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
		{ "GetWardrobeCells", playerGetWardrobeCells, METH_VARARGS },
		{ "GetWardrobeInventoryRevision", playerGetWardrobeInventoryRevision, METH_VARARGS },
		{ "GetOwnedCostumeVnums", playerGetOwnedCostumeVnums, METH_VARARGS },
#endif


// void initPlayer() icinde:
// Ara:
	PyModule_AddIntConstant(poModule, "SLOT_TYPE_OFFLINESHOP",				SLOT_TYPE_OFFLINESHOP);

// Altina ekle:
#ifdef ENABLE_WARDROBE_ITEM_TRANSFER
	PyModule_AddIntConstant(poModule, "SLOT_TYPE_WARDROBE",				SLOT_TYPE_WARDROBE);
#endif


// void initPlayer() icinde:
// Ara:
	PyModule_AddIntConstant(poModule, "BELT_INVENTORY", BELT_INVENTORY);
	PyModule_AddIntConstant(poModule, "GROUND",								GROUND);

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	PyModule_AddIntConstant(poModule, "WARDROBE", WARDROBE);
	PyModule_AddIntConstant(poModule, "WARDROBE_SLOT_COUNT", c_Wardrobe_Count);
#endif

