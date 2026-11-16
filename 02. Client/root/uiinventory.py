# InventoryWindowButtons.__init__ icinde ara:
		self.GetChild("Button_Auto_Cape").SetEvent(ui.__mem_func__(self.OpenAutoCape))
		self.GetChild("Button_Quest_Book").SetEvent(ui.__mem_func__(self.OpenMissionBook))

# Altina ekle:
		if self.IsChild("Button_Wardrobe"):
			self.GetChild("Button_Wardrobe").SetEvent(ui.__mem_func__(self.OpenWardrobe))


# InventoryWindowButtons.__init__ icinde ara:
		names = (("Equipment_Tab_1", localeInfo.INVENTORY_TAB_EQUIPMENT), ("Equipment_Tab_2", localeInfo.INVENTORY_TAB_COSTUMES), ("Equipment_Tab_3", localeInfo.INVENTORY_TAB_PETS),

# Altina ekle:
			("Button_Auto_Cape", localeInfo.INVENTORY_BUTTON_AUTO_CAPE), ("Button_Quest_Book", localeInfo.INVENTORY_BUTTON_QUEST_BOOK), ("Button_Wardrobe", localeInfo.INVENTORY_BUTTON_WARDROBE))


# InventoryWindowButtons icinde ara:
		if self.inventory:
			self.inventory.ShowSoonMessage()

# Altina ekle:
	def OpenWardrobe(self):
		interface = self.inventory.interface if self.inventory else None
		if app.ENABLE_WARDROBE_SYSTEM and interface:
			interface.ToggleWardrobeWindow()
		elif self.inventory:
			self.inventory.ShowSoonMessage()


# InventoryWindow.__BindReferenceButtons icinde ara:
		self.GetChild("MallButton").SetEvent(ui.__mem_func__(self.ClickMallButton))
		self.GetChild("CostumeButton").Hide()

# Altina ekle:
		if app.ENABLE_COSTUME_SHOP:
			self.GetChild("CostumeShopButton").SetEvent(ui.__mem_func__(self.__ClickCostumeShopButton))
		else:
			self.GetChild("CostumeShopButton").SetEvent(ui.__mem_func__(self.ShowSoonMessage))


# InventoryWindow icinde ara:
			if self.shopButtonToolTip:
				self.shopButtonToolTip.HideToolTip()

# Altina ekle:
	def __ClickCostumeShopButton(self):
		net.SendChatPacket("/costume_shop _open")


# InventoryWindow.SelectEmptySlot icinde, ilgili if blogunun sonuna ekle:
				elif app.ENABLE_WARDROBE_ITEM_TRANSFER and player.SLOT_TYPE_WARDROBE == attachedSlotType:
					wardrobe = self.interface.GetWardrobeController() if self.interface else None
					if wardrobe:
						wardrobe.Withdraw(attachedSlotPos, selectedSlotPos)


# InventoryWindow.SelectEmptySlot icinde, ilgili if blogunun sonuna ekle:
				elif app.ENABLE_WARDROBE_ITEM_TRANSFER and player.SLOT_TYPE_WARDROBE == attachedSlotType:
					wardrobe = self.interface.GetWardrobeController() if self.interface else None
					if wardrobe:
						wardrobe.Withdraw(attachedSlotPos, selectedSlotPos)

