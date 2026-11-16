# Ara:
		lines.append(" ".join(line_tokens))
	return lines

# Altina ekle:
INLINE_MODEL_PREVIEW = app.ENABLE_COSTUME_SHOP


# ItemToolTip.AddItemData icinde ara:
					if isTimeItem:
						(timeText, timeColor) = self.__GetCostumeBonusTimeText(metinSlot[self.COSTUME_BONUS_EXPIRE_SOCKET])

# Altina ekle:
						self.__AppendCostumeBonusTimeAttributeLine(localeInfo.COSTUME_SHOP_NO_BONUS, EMPTY_COSTUME_BONUS_COLOR, timeText, timeColor)


# ItemToolTip.AddItemData icinde ara:
					else:

# Altina ekle:
						self.AppendTextLine(localeInfo.COSTUME_SHOP_NO_BONUS, EMPTY_COSTUME_BONUS_COLOR)


# ItemToolTip.__AppendCostumeTypeLine icinde ara:
		if item.ITEM_TYPE_COSTUME == itemType:
			key = {

# Altina ekle:
				item.COSTUME_TYPE_BODY : "WARDROBE_TOOLTIP_TYPE_BODY",
				item.COSTUME_TYPE_HAIR : "WARDROBE_TOOLTIP_TYPE_HAIR",
				item.COSTUME_TYPE_WEAPON : "WARDROBE_TOOLTIP_TYPE_WEAPON",
				item.COSTUME_TYPE_MOUNT : "WARDROBE_TOOLTIP_TYPE_MOUNT",
				item.COSTUME_TYPE_MOUNT_STANDING : "WARDROBE_TOOLTIP_TYPE_MOUNT",	# turbo surfboard
				item.COSTUME_TYPE_PET : "WARDROBE_TOOLTIP_TYPE_PET",
				item.COSTUME_TYPE_ACCE : "WARDROBE_TOOLTIP_TYPE_ACCE",
				item.COSTUME_TYPE_ACCE_SKIN : "WARDROBE_TOOLTIP_TYPE_ACCE",


# ItemToolTip.__AppendCostumeTypeLine icinde ara:
			}.get(itemSubType)
		elif item.ITEM_TYPE_PET == itemType:

# Altina ekle:
			key = "WARDROBE_TOOLTIP_TYPE_PET"


# ItemToolTip.__AppendCostumeTypeLine icinde ara:
		elif item.ITEM_TYPE_SHINING == itemType:

# Altina ekle:
			key = "WARDROBE_TOOLTIP_TYPE_SHINING"


# ItemToolTip.__AppendCostumeTypeLine icinde ara:
		typeText = localeInfo.GetText(key) if key else ""
		if typeText:

# Altina ekle:
			self.AppendTextLine(localeInfo.WARDROBE_TOOLTIP_TYPE % typeText, 0xffffc700)

