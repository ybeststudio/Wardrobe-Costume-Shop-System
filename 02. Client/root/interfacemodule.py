# Ara:
if app.ENABLE_GLOBAL_RANKING:
	import uiglobalranking

# Altina ekle:
if app.ENABLE_COSTUME_SHOP:
	import uicostumeshop

if app.ENABLE_WARDROBE_SYSTEM:
	import uiwardrobe


# Interface.__init__ icinde ara:
		if app.ENABLE_RANKING:
			self.wndRanking = None

# Altina ekle:
		if app.ENABLE_COSTUME_SHOP:
			self.wndCostumeShop = None

		if app.ENABLE_WARDROBE_SYSTEM:
			self.wndWardrobe = None
			self.wardrobeController = uiwardrobe.WardrobeController()
			self.wardrobeController.SetChangeEvent(self.__OnWardrobeChanged)
			self.wardrobeController.resultEvent = self.__OnWardrobeResult


# Interface.Close icinde ara:
				self.wndRanking.Destroy()
				del self.wndRanking

# Altina ekle:
		if app.ENABLE_COSTUME_SHOP:
			if self.wndCostumeShop:
				self.wndCostumeShop.Destroy()
			self.wndCostumeShop = None

		if app.ENABLE_WARDROBE_SYSTEM:
			if self.wndWardrobe:
				self.wndWardrobe.Destroy()
			self.wndWardrobe = None
			if self.wardrobeController:
				self.wardrobeController.SetChangeEvent(None)
				self.wardrobeController.resultEvent = None
			self.wardrobeController = None


# Interface icinde ara:
			if self.wndRanking:
				self.wndRanking.Open()

# Altina ekle:
	if app.ENABLE_WARDROBE_SYSTEM:
		def GetWardrobeController(self):
			return self.wardrobeController

		def ToggleWardrobeWindow(self):
			if not self.wardrobeController:
				return
			if not self.wndWardrobe:
				self.wndWardrobe = uiwardrobe.WardrobeWindow(self.wardrobeController, self)
			if self.wndWardrobe.IsShow():
				self.wndWardrobe.Close()
			else:
				self.wndWardrobe.Open()

		def OpenWardrobeInventory(self, lookSlot = -1):
			if not self.wardrobeController:
				return
			if not self.wndWardrobe:
				self.wndWardrobe = uiwardrobe.WardrobeWindow(self.wardrobeController, self)
			self.wndWardrobe.OpenInventory(lookSlot)

		def __OnWardrobeChanged(self, what):
			if self.wndWardrobe and self.wndWardrobe.IsShow():
				self.wndWardrobe.OnControllerChanged(what)

		def __OnWardrobeResult(self, action, result):
			if self.wndWardrobe:
				self.wndWardrobe.OnResult(action, result)

	if app.ENABLE_COSTUME_SHOP:
		def __GetCostumeShop(self):
			if not self.wndCostumeShop:
				self.wndCostumeShop = uicostumeshop.CostumeShopWindow()
				self.wndCostumeShop.SetInterface(self)
			return self.wndCostumeShop

		def CostumeShopClear(self):
			self.__GetCostumeShop().ClearEntries()

		def CostumeShopAdd(self, data):
			self.__GetCostumeShop().AddEntries(data)

		def CostumeShopOpen(self, serverTime):
			self.__GetCostumeShop().Open(serverTime)

		def CostumeShopResult(self, result):
			if self.wndCostumeShop:
				self.wndCostumeShop.OnResult(result)

