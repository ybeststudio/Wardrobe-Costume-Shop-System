# GameWindow icinde ara:
			if window:
				window.OnMissionResult(result, bossIdx, no)

# Altina ekle:
	if app.ENABLE_WARDROBE_SYSTEM:
		def __GetWardrobeController(self):
			if not self.interface:
				return None
			return self.interface.GetWardrobeController()

		def __WardrobeCatalogBegin(self, serial, rows):
			controller = self.__GetWardrobeController()
			if controller:
				controller.OnCatalogBegin(serial, rows)

		def __WardrobeCatalogCat(self, serial, categoryId, key):
			controller = self.__GetWardrobeController()
			if controller:
				controller.OnCatalogCategory(serial, categoryId, key)

		def __WardrobeCatalogRows(self, serial, data):
			controller = self.__GetWardrobeController()
			if controller:
				controller.OnCatalogRows(serial, data)

		def __WardrobeCatalogEnd(self, serial):
			controller = self.__GetWardrobeController()
			if controller:
				controller.OnCatalogEnd(serial)

		def __WardrobeOutfitsBegin(self, serial, count, remembered, applied):
			controller = self.__GetWardrobeController()
			if controller:
				controller.OnOutfitsBegin(serial, count, remembered, applied)

		def __WardrobeOutfitRow(self, serial, slot, revision, nameHex, l0, l1, l2, l3, l4, l5, l6, l7, l8):
			controller = self.__GetWardrobeController()
			if controller:
				controller.OnOutfitRow(serial, slot, revision, nameHex, l0, l1, l2, l3, l4, l5, l6, l7, l8)

		def __WardrobeOutfitsEnd(self, serial):
			controller = self.__GetWardrobeController()
			if controller:
				controller.OnOutfitsEnd(serial)

		def __WardrobeResult(self, serial, code):
			controller = self.__GetWardrobeController()
			if controller:
				controller.OnResult(serial, code)

		def __WardrobeAppearance(self, l0, l1, l2, l3, l4, l5, l6, l7, l8):
			controller = self.__GetWardrobeController()
			if controller:
				controller.OnAppearance(l0, l1, l2, l3, l4, l5, l6, l7, l8)

		def __WardrobeOpenInventory(self, lookSlot):
			if self.interface:
				try:
					self.interface.OpenWardrobeInventory(int(lookSlot))
				except ValueError:
					self.interface.OpenWardrobeInventory()

		def __WardrobeProgress(self, costumes, level, totalExp, expInLevel, expPerLevel):
			controller = self.__GetWardrobeController()
			if controller:
				controller.OnProgress(costumes, level, totalExp, expInLevel, expPerLevel)

	if app.ENABLE_COSTUME_SHOP:
		def __CostumeShopClear(self):
			if self.interface:
				self.interface.CostumeShopClear()

		def __CostumeShopAdd(self, data):
			if self.interface:
				self.interface.CostumeShopAdd(data)

		def __CostumeShopOpen(self, serverTime):
			if self.interface:
				self.interface.CostumeShopOpen(int(serverTime))

		def __CostumeShopResult(self, result):
			if self.interface:
				self.interface.CostumeShopResult(int(result))


# GameWindow.__ServerCommand_Build icinde ara:
		if app.ENABLE_GLOBAL_RANKING:
			serverCommandList["LoadRankData"] = self.__LoadRankData

# Altina ekle:
		if app.ENABLE_WARDROBE_SYSTEM:
			serverCommandList["WardrobeCatalogBegin"] = self.__WardrobeCatalogBegin
			serverCommandList["WardrobeCatalogCat"] = self.__WardrobeCatalogCat
			serverCommandList["WardrobeCatalogRows"] = self.__WardrobeCatalogRows
			serverCommandList["WardrobeCatalogEnd"] = self.__WardrobeCatalogEnd
			serverCommandList["WardrobeOutfitsBegin"] = self.__WardrobeOutfitsBegin
			serverCommandList["WardrobeOutfitRow"] = self.__WardrobeOutfitRow
			serverCommandList["WardrobeOutfitsEnd"] = self.__WardrobeOutfitsEnd
			serverCommandList["WardrobeResult"] = self.__WardrobeResult
			serverCommandList["WardrobeAppearance"] = self.__WardrobeAppearance
			serverCommandList["WardrobeProgress"] = self.__WardrobeProgress
			serverCommandList["OpenWardrobeInventory"] = self.__WardrobeOpenInventory

		if app.ENABLE_COSTUME_SHOP:
			serverCommandList["CostumeShopClear"] = self.__CostumeShopClear
			serverCommandList["CostumeShopAdd"] = self.__CostumeShopAdd
			serverCommandList["CostumeShopOpen"] = self.__CostumeShopOpen
			serverCommandList["CostumeShopResult"] = self.__CostumeShopResult

