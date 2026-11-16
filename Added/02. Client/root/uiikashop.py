# cpython modules
import app
import re
import player
import item
import net
import dbg
import wndMgr
import ikashop
import chr

# m2 python modules
import localeInfo as locale
import mouseModule as mouse
import ui
import uiCommon as uicommon
from uiAutoCape import SliderBarNew
import uiToolTip as uitooltip

# python modules
import time
import types
import ime
from _weakref import proxy, ProxyType, CallableProxyType
from random import shuffle

AUCTION_MIN_RAISE_PERCENTAGE = 10
RESTORE_DURATION_COST = 1000000
MOVE_SHOP_ENTITY_COST = 100000
SLOT_SIZE = 32
MIN_OFFER_PCT = 30
YANG_PER_CHEQUE = 100000000

ENABLE_DEFAULT_UI_BOARD = 1
SEARCH_SHOP_RENEWAL = 1
OFFER_VIEWS = 4
SEARCH_HISTORY_ROWS = 7
MARKET_FEE_PCT = 3
MAX_MARKET_PRICE = 100000000000
MAX_NET_PRICE = MAX_MARKET_PRICE * (100 - MARKET_FEE_PCT) / 100	# 97.000.000.000 typed -> 100.000.000.000
SLOT_BASE_IMG = "d:/ymir work/ui/game/common/slots/slot_32x32.png"
TITLEBAR_REFRESH_IMG = "d:/ymir work/ui/game/common/button_titlebar_refresh_%s.png"
OFFLINESHOP_UI_PATH = "d:/ymir work/ui/game/offlineshop/"
LINKED_BOARD_GAP = 6
ENABLE_CHEQUE_SYSTEM = app.ENABLE_CHEQUE_SYSTEM

def debug(fmt, *args):
	if args:
		fmt = fmt.format(*args)
	dbg.Tracen(fmt)

def debugStack():
	import traceback
	s = traceback.format_stack()
	for line in s[:-1]:
		debug(line)

def RomeNumber(num):
	nums = {
		1 : "I",		2 : "II",		3 : "III",
		4 : "IV",		5 : "V",		6 : "VI",
		7 : "VII",		8 : "VIII",		9 : "IX",
	}
	return nums.get(num, "X")

def DatetimeFormat(timestamp):
	try:
		dts = time.localtime(timestamp)
		now = time.time()
		for (days, fmt) in ((0, locale.IKASHOP_DATETIME_TODAY), (-1, locale.IKASHOP_DATETIME_YESTERDAY), (1, locale.IKASHOP_DATETIME_TOMORROW)):
			day = time.localtime(now + days * 86400)
			if day[0:3] == dts[0:3]:
				return fmt.format(dts[3], dts[4])
		# formatting dd/mm/yy hh:mm
		return "{:02d}/{:02d}/{:02d} {:02d}:{:02d}".format(dts[2], dts[1], dts[0] % 100, dts[3], dts[4])
	except Exception as e:
		dbg.TraceError("{}: {}".format(e, timestamp))

class IkashopItemToolTip(uitooltip.ItemToolTip):
	PREVIEW_TYPES = (item.ITEM_TYPE_COSTUME, item.ITEM_TYPE_PET)

	def __init__(self):
		self.previewVnum = 0
		self.showEmptyCostumeBonus = False
		uitooltip.ItemToolTip.__init__(self)

	def AddItemData(self, itemVnum, *args, **kwargs):
		item.SelectItem(itemVnum)
		self.allowModelPreview = item.GetItemType() in self.PREVIEW_TYPES
		self.previewVnum = itemVnum if self.allowModelPreview else 0
		self.showEmptyCostumeBonus = item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() != item.COSTUME_TYPE_ACCE
		if self.previewVnum and self.toolTipWidth < 250:
			self.toolTipWidth = 250	# room for the "[Shift] - Kostumu Onizlemek icin Basili Tut" line
			self.ResizeToolTip()
		result = uitooltip.ItemToolTip.AddItemData(self, itemVnum, *args, **kwargs)
		if self.previewVnum:
			self.AppendSpace(5)
			self.AppendTextLine(locale.IKASHOP_PREVIEW_SHIFT_HINT, SEARCH_TEXT_COLOR)
		return result

	def HideToolTip(self):
		uitooltip.ItemToolTip.HideToolTip(self)
		self.previewVnum = 0

	def FitTextWidth(self, text):
		textLine = ui.TextLine()
		textLine.SetFontName(self.defFontName)
		textLine.SetText(text)
		(textWidth, textHeight) = textLine.GetTextSize()
		if self.toolTipWidth < textWidth + 40:
			self.toolTipWidth = textWidth + 40

	def AppendAntiFlagInformation(self):
		if self.showEmptyCostumeBonus:
			return
		return uitooltip.ItemToolTip.AppendAntiFlagInformation(self)

	def OnUpdate(self):
		uitooltip.ItemToolTip.OnUpdate(self)
		if self.previewVnum and self.IsShow():
			if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
				IkashopOpenRenderTarget(self.previewVnum)


IKASHOP_RENDER = {"window": None, "vnum": 0}


def IkashopOpenRenderTarget(vnum):
	window = IKASHOP_RENDER["window"]
	if not app.ENABLE_RENDER_TARGET or (window and window.IsShow() and IKASHOP_RENDER["vnum"] == vnum):
		return
	import uiRenderTarget
	if not IKASHOP_RENDER["window"]:
		IKASHOP_RENDER["window"] = uiRenderTarget.RenderTargetWindow()
	IKASHOP_RENDER["vnum"] = vnum
	IKASHOP_RENDER["window"].Open(0, vnum)


def IkashopCloseRenderTarget():
	if IKASHOP_RENDER["vnum"] and IKASHOP_RENDER["window"]:
		IKASHOP_RENDER["window"].Close()
	IKASHOP_RENDER["vnum"] = 0


def FitTextLine(textLine, text, maxWidth):
	textLine.SetText(text)
	if textLine.GetTextSize()[0] <= maxWidth:
		return
	while text and textLine.GetTextSize()[0] > maxWidth:
		text = text[:-1]
		textLine.SetText(text + "..")


def ApplyListFrame(board, image, pos, size, emptyPos):
	box = board.boardBox
	box.LoadImage(image)
	box.SetPosition(*pos)
	box.SetScale(float(size[0]) / max(1, box.GetWidth()), float(size[1]) / max(1, box.GetHeight()))
	board.elementScrollbar.SetPosition(pos[0] + size[0] - 10, pos[1] + 32)
	board.elementScrollbar.SetScrollBarSize(size[1] - 36)
	board.emptyHeader.SetFontName(locale.UI_DEF_FONT)
	board.emptyHeader.SetOutline(0)
	board.emptyHeader.SetPackedFontColor(0xFFCABDAB)
	board.emptyHeader.SetPosition(*emptyPos)


def ToMarketPrice(price):
	if isinstance(price, tuple):
		return (ToMarketPrice(price[0]),) + price[1:]
	if long(price) < 0:
		return -ToMarketPrice(-long(price))
	keep = 100 - MARKET_FEE_PCT
	return min(MAX_MARKET_PRICE, (long(price) * 100 + keep - 1) / keep)

def ToNetPrice(price):
	if long(price) < 0:
		return -ToNetPrice(-long(price))
	return long(price) * (100 - MARKET_FEE_PCT) / 100

def GetItemHeight(vnum):
	item.SelectItem(vnum)
	return item.GetItemSize()[1]

def GetScreenSize():
	return wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight()

def IsProxy(obj):
	return type(obj) in (ProxyType, CallableProxyType)

def SelfDestroyObject(instance):
	def DestroyValue(value):
		if IsProxy(value):
			return True
		if isinstance(value, ui.Window):
			if isinstance(value, IkarusShopWindow):
				value.Destroy()
			else:
				SelfDestroyObject(value)
			return True
		elif type(value) in (list, tuple, dict, set):
			values = value if type(value) != dict else value.values()
			ret = [DestroyValue(val) for val in values]
			return any(ret)
		elif isinstance(value, types.MethodType):
			return True
		return False

	def MakeEmptyValue(value):
		if type(value) in (list, tuple, dict, set):
			return type(value)()
		return None

	# skipping all non-window instances
	if not isinstance(instance, ui.Window):
		return

	# skipping all instances already destroyed
	if "_SelfDestroyed" in instance.__dict__:
		return

	# desroying the instance
	instance._SelfDestroyed = True
	for name, value in vars(instance).items():
		if value and DestroyValue(value):
			setattr(instance, name, MakeEmptyValue(value))

def IsPressingCTRL():
	return app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL)

def IsPressingSHIFT():
	return app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT)

def GetSellableSlotTypes():
	types = [player.SLOT_TYPE_DRAGON_SOUL_INVENTORY, player.SLOT_TYPE_INVENTORY]
	if app.ENABLE_WARDROBE_ITEM_TRANSFER:
		types.append(player.SLOT_TYPE_WARDROBE)
	return types

def GetInventoryItemHash(win, pos):
	vnum = player.GetItemIndex(win, pos)
	count = player.GetItemCount(win, pos)
	sockets = tuple(player.GetItemMetinSocket(win, pos, i) for i in xrange(player.METIN_SOCKET_MAX_NUM))
	attrs = tuple(player.GetItemAttribute(win, pos, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM))
	return ikashop.GetItemHash(vnum, count, sockets, attrs)

def GetAttributeSettings():
	def NoFormat(str):
		removingStrings = ["%", "0", "+", ":"]
		for value in removingStrings:
			str = str.replace(value, "")
		return str.strip()

	values = []
	attributeDict = uitooltip.ItemToolTip.AFFECT_DICT
	for apply, text in attributeDict.items():
		if callable(text):
			text = text(0)
		if not isinstance(text, str) or not text:
			continue
		values.append((apply, NoFormat(text)))
	values.sort(key = lambda t : t[1])
	values = [(0, locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT),] + values
	return values

def IsUsingFilter(filters):
	for filter in filters:
		if isinstance(filter, tuple):
			if IsUsingFilter(filter):
				return True
		elif filter:
			return True
	return False

def ExtractInputPrice(dialog):
	if ENABLE_CHEQUE_SYSTEM:
		cheque = dialog.GetCheque()
		cheque = cheque.lower().replace("k", "000")
		cheque = int(cheque) if cheque and cheque.isdigit() else 0

	# extracting value
	value = dialog.GetText()
	value = value.lower().replace("k", "000")
	value = long(value) if value and value.isdigit() else 0

	if isinstance(dialog, IkarusShopItemPriceDialog) and dialog.IsOfferOnly():
		return True, (-value, 0) if ENABLE_CHEQUE_SYSTEM else (-value,)

	if ENABLE_CHEQUE_SYSTEM:
		if cheque == 0 and value == 0:
			return False, None
		price = value, cheque
	else:
		if value == 0:
			return False, None
		price = value,
	return True, price

class IkashopQuestionDialog(ui.Board):
	LINE_STEP = 18

	def __init__(self):
		ui.Board.__init__(self)
		self.AddFlag("float")
		self.AddFlag("movable")
		self.lines = []
		self.acceptEvent = None
		self.cancelEvent = None
		self.thinBoard = ui.ThinBoard()
		self.thinBoard.SetParent(self)
		self.thinBoard.AddFlag("not_pick")
		self.thinBoard.SetPosition(8, 8)
		self.thinBoard.Show()
		self.textLine = ui.TextLine()	# measuring / compatibility (GetTextSize)
		self.acceptButton = self._Button("accept", self._OnAccept)
		self.cancelButton = self._Button("cancel", self._OnCancel)

	def _Button(self, name, event):
		btn = ui.Button()
		btn.SetParent(self)
		btn.SetUpVisual("d:/ymir work/ui/game/common/button_%s_norm.png" % name)
		btn.SetOverVisual("d:/ymir work/ui/game/common/button_%s_hover.png" % name)
		btn.SetDownVisual("d:/ymir work/ui/game/common/button_%s_down.png" % name)
		btn.SetEvent(event)
		btn.Show()
		return btn

	def SetText(self, text):
		parts = [p for p in re.split(r"(?<=[?])\s+", text) if p] if "?" in text[:-1] else [text]
		for line in self.lines:
			line.Hide()
		self.lines = []
		width = 0
		for part in parts:
			line = ui.TextLine()
			line.SetParent(self)
			line.SetHorizontalAlignCenter()
			line.SetVerticalAlignCenter()
			line.SetText(part)
			line.Show()
			self.lines.append(line)
			width = max(width, line.GetTextSize()[0])
		self.textLine.SetText(max(parts, key = len))
		self._Layout(width + 40)

	def SetWidth(self, width):
		pass

	def _Layout(self, width):
		width = max(230, width)
		height = 105
		self.SetSize(width, height)
		self.thinBoard.SetSize(width - 17, height - 17)
		ys = (38,) if len(self.lines) == 1 else (25, 47)
		for (i, line) in enumerate(self.lines[:2]):
			line.SetPosition(width / 2, ys[i])
		by = 63 if len(self.lines) == 1 else 64
		self.acceptButton.SetPosition(width / 2 - 57 - 12, by)
		self.cancelButton.SetPosition(width / 2 + 12, by)
		self.SetCenterPosition()

	def SetAcceptText(self, text):
		pass

	def SetCancelText(self, text):
		pass

	def SetAcceptEvent(self, event):
		self.acceptEvent = event

	def SetCancelEvent(self, event):
		self.cancelEvent = event

	def SAFE_SetAcceptEvent(self, event):
		self.acceptEvent = event

	def _OnAccept(self):
		if self.acceptEvent:
			self.acceptEvent()

	def _OnCancel(self):
		if self.cancelEvent:
			self.cancelEvent()
		else:
			self.Hide()

	def Open(self):
		self.Show()
		self.SetTop()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self._OnCancel()
		return True


class IkashopPriceCheckBox(ui.Window):
	def __init__(self, parent, x, y, text, event):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.SetPosition(x, y)
		self.checked = False
		self.event = event
		self.box = ui.ImageBox()
		self.box.SetParent(self)
		self.box.AddFlag("not_pick")
		self.box.LoadImage("d:/ymir work/ui/game/common/checkbox_new_unselected.png")
		self.box.Show()
		self.text = ui.TextLine()
		self.text.SetParent(self)
		self.text.AddFlag("not_pick")
		self.text.SetPosition(20, 0)
		self.text.SetPackedFontColor(0xFFCABDAB)
		self.text.SetText(text)
		self.text.Show()
		self.SetSize(20 + self.text.GetTextSize()[0], 16)
		self.Show()

	def SetChecked(self, checked):
		self.checked = checked
		self.box.LoadImage("d:/ymir work/ui/game/common/checkbox_new_%s.png" % ("selected" if checked else "unselected"))

	def OnMouseLeftButtonUp(self):
		self.SetChecked(not self.checked)
		if self.event:
			self.event(self.checked)
		return True


class IkarusShopItemPriceDialog(ui.BoardWithTitleBar):
	PATH = "d:/ymir work/ui/game/offline_shop/add_item/"
	SALE_ROWS = 3
	PRICE_SLIDER_RANGE = 0.5

	def __init__(self):
		self.settingValue = False
		ui.BoardWithTitleBar.__init__(self)
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetSize(198, 430)
		self.SetTitleName(locale.IKASHOP_ITEM_PRICE_DIALOG_TITLE)
		self.SetCloseEvent(self._OnCancel)
		self.acceptEvent = None
		self.cancelEvent = None
		self.average = -1
		self.sales = ()
		self.saleScroll = 0
		self.vnum = 0
		self.count = 1
		self.keep = []

		self._Img(self.PATH + "bg_item.png", 5, 21)
		self.itemIcon = ui.ExpandedImageBox()
		self.itemIcon.SetParent(self)
		self.itemIcon.AddFlag("not_pick")
		self.itemIcon.SetPosition(83, 55)
		self.itemIcon.Show()
		self.itemSockets = None
		self.itemAttrs = None
		self.itemToolTip = uitooltip.ItemToolTip()
		self.itemToolTip.HideToolTip()
		self.itemHover = SearchHoverArea()
		self.itemHover.SetParent(self)
		self.itemHover.SetPosition(83, 55)
		self.itemHover.SetSize(32, 32)
		self.itemHover.SetEvents(ui.__mem_func__(self._ShowItemToolTip), ui.__mem_func__(self._HideItemToolTip))
		self.itemHover.Show()

		# Piyasa Fiyati
		self._Img(self.PATH + "title_bg.png", 5, 107)
		self._Text(99, 112, locale.IKASHOP_ITEM_PRICE_MARKET_TITLE, center = True, bold = True)
		marketBg = self._Img(self.PATH + "bg_market_price.png", 5, 124)
		marketBg.SetMouseWheelEvent(self._OnSaleWheel)
		self.averageText = self._Text(15, 131, "", color = 0xFF8FD3FF)
		self._Text(14, 147, locale.IKASHOP_ITEM_PRICE_LAST_SALES)
		self._Img(self.PATH + "bg_last_selled.png", 11, 163)
		self.saleTexts = [self._Text(20, 169 + i * 19, "") for i in xrange(self.SALE_ROWS)]
		self.saleBar = ui.Bar()
		self.saleBar.SetParent(self)
		self.saleBar.SetColor(0xFF8A7A62)
		self.saleBar.SetPosition(181, 167)
		self.saleBar.SetSize(2, 22)
		self.saleBar.Hide()

		# Senin Fiyatin
		self._Img(self.PATH + "title_bg.png", 5, 234)
		self._Text(99, 239, locale.IKASHOP_ITEM_PRICE_YOUR_PRICE_TITLE, center = True, bold = True)
		self._Img(self.PATH + "bg_input_price.png", 5, 251)
		self._Img(self.PATH + "editline_bg.png", 13, 260)
		self.valueEdit = ui.EditLine()
		self.valueEdit.SetParent(self)
		self.valueEdit.SetPosition(18, 261)
		self.valueEdit.SetSize(156, 16)
		self.valueEdit.SetMax(14)
		self.valueEdit.SetNumberMode()
		self.valueEdit.SetReturnEvent(self._OnAccept)
		self.valueEdit.SetEscapeEvent(self._OnCancel)
		self.valueEdit.OnIMEUpdate = ui.__mem_func__(self._OnValueUpdate)
		self.valueEdit.Show()
		self.saleText = self._Text(99, 278, "", center = True)
		self.averageCheck = IkashopPriceCheckBox(self, 13, 299, locale.IKASHOP_ITEM_PRICE_SELL_AT_AVERAGE, self._OnCheckAverage)
		self.lastSoldCheck = IkashopPriceCheckBox(self, 13, 319, locale.IKASHOP_ITEM_PRICE_SELL_AT_LAST_SOLD, self._OnCheckLast)
		self.offerOnlyCheck = IkashopPriceCheckBox(self, 13, 339, locale.IKASHOP_OFFER_ONLY, None)
		self.offerOnlyCheck.text.SetPackedFontColor(0xFFFFC800)
		self.offerOnlyCheck.Hide()

		self.sliderBase = 0
		self.sliderMoving = False
		self.slider = SliderBarNew()
		self.slider.SetParent(self)
		self.slider.SetPosition((198 - self.slider.GetWidth()) / 2, 364)
		self.slider.SetSliderPos(0.5)
		self.slider.SetEvent(ui.__mem_func__(self._OnSliderMove))
		self.slider.Show()

		self.acceptButton = self._Button("accept", 31, 395, self._OnAccept)
		self.cancelButton = self._Button("cancel", 111, 395, self._OnCancel)

	def _Img(self, image, x, y):
		img = ui.ImageBox()
		img.SetParent(self)
		img.LoadImage(image)
		img.SetPosition(x, y)
		img.Show()
		self.keep.append(img)
		return img

	def _Text(self, x, y, text, center = False, bold = False, color = 0xFFCABDAB):
		line = ui.TextLine()
		line.SetParent(self)
		if bold:
			line.SetFontName("Tahoma:12b")
		if center:
			line.SetHorizontalAlignCenter()
		line.SetPosition(x, y)
		line.SetPackedFontColor(color)
		line.SetText(text)
		line.Show()
		self.keep.append(line)
		return line

	def _Button(self, name, x, y, event):
		btn = ui.Button()
		btn.SetParent(self)
		btn.SetPosition(x, y)
		btn.SetUpVisual("d:/ymir work/ui/game/common/button_%s_norm.png" % name)
		btn.SetOverVisual("d:/ymir work/ui/game/common/button_%s_hover.png" % name)
		btn.SetDownVisual("d:/ymir work/ui/game/common/button_%s_down.png" % name)
		btn.SetEvent(event)
		btn.Show()
		return btn

	# -------------------------------------------------- MoneyInputDialog interface
	def SetTitle(self, title):
		pass

	def IsOfferOnly(self):
		return self.offerOnlyCheck.IsShow() and self.offerOnlyCheck.checked

	def SetOfferOnly(self, offerOnly):
		self.offerOnlyCheck.SetChecked(bool(offerOnly) and self.offerOnlyCheck.IsShow())

	def SetItem(self, vnum, count, sockets = None, attrs = None):
		self.vnum = vnum
		self.count = max(1, count)
		self.itemSockets = sockets
		self.itemAttrs = attrs
		item.SelectItem(vnum)
		equipment = item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR)
		self.offerOnlyCheck.Show() if equipment else self.offerOnlyCheck.Hide()
		self.slider.Hide() if equipment else self.slider.Show()
		self.offerOnlyCheck.SetChecked(False)
		self.itemIcon.LoadImage(item.GetIconImageFileName())
		h = item.GetItemSize()[1]
		self.itemIcon.SetPosition(83, 64 - 16 * h + 7)
		self.itemHover.SetPosition(83, 64 - 16 * h + 7)
		self.itemHover.SetSize(32, 32 * h)

	def _ShowItemToolTip(self):
		if not self.vnum:
			return
		tip = self.itemToolTip
		tip.ClearToolTip()
		sockets = list(self.itemSockets) if self.itemSockets else [0] * player.METIN_SOCKET_MAX_NUM
		attrs = list(self.itemAttrs) if self.itemAttrs else [(0, 0)] * player.ATTRIBUTE_SLOT_MAX_NUM
		tip.AddItemData(self.vnum, sockets, attrs)
		tip.ShowToolTip()

	def _HideItemToolTip(self):
		self.itemToolTip.HideToolTip()

	def SetAcceptEvent(self, event):
		self.acceptEvent = event

	def SetCancelEvent(self, event):
		self.cancelEvent = event

	def SetValue(self, value):
		self.settingValue = True
		self.valueEdit.SetText(str(value))
		self.valueEdit.SetEndPosition()
		self._OnValueUpdate()
		self.settingValue = False
		if not self.sliderMoving:
			self._ResetSlider()

	def GetText(self):
		return self.valueEdit.GetText()

	def Open(self):
		self.averageCheck.SetChecked(False)
		self.lastSoldCheck.SetChecked(False)
		self.SetCenterPosition()
		self.Show()
		self.SetTop()
		self.valueEdit.SetFocus()

	def SoftClose(self):
		self.valueEdit.KillFocus()
		self.itemToolTip.HideToolTip()
		self.Hide()

	def Close(self):
		self.SoftClose()

	def SetPriceAverage(self, price, sales = ()):
		self.average = price
		if price == -1:
			self.averageText.SetText(locale.IKASHOP_ITEM_PRICE_AVERAGE_REQUESTING)
		elif price <= 0:
			self.averageText.SetText(locale.IKASHOP_ITEM_PRICE_AVERAGE_NOT_AVAILABLE)
		else:
			self.averageText.SetText(locale.IKASHOP_ITEM_PRICE_AVERAGE_VALUE.format(locale.NumberToMoneyString(price)))
		self.sales = tuple(sales)
		self.saleScroll = 0
		self._RefreshSales()
		# a checked option fills the price once the average / the sales arrive
		if self.averageCheck.checked and price > 0:
			self.SetValue(ToNetPrice(price))
		elif self.lastSoldCheck.checked and self.sales:
			self._OnCheckLast(True)

	# -------------------------------------------------- internals
	def _RefreshSales(self):
		for (i, line) in enumerate(self.saleTexts):
			idx = self.saleScroll + i
			if idx < len(self.sales):
				(count, price, stamp) = self.sales[idx]
				line.SetText("%s x%d (%s)" % (locale.NumberToMoneyString(price), count, DatetimeFormat(stamp)))
			else:
				line.SetText("")
		if len(self.sales) > self.SALE_ROWS:
			span = len(self.sales) - self.SALE_ROWS
			h = max(8, 63 * self.SALE_ROWS / len(self.sales))
			self.saleBar.SetSize(2, h)
			self.saleBar.SetPosition(181, 167 + (63 - h) * self.saleScroll / span)
			self.saleBar.Show()
		else:
			self.saleBar.Hide()

	def _OnSaleWheel(self, delta):
		span = max(0, len(self.sales) - self.SALE_ROWS)
		self.saleScroll = max(0, min(span, self.saleScroll + (-1 if delta > 0 else 1)))
		self._RefreshSales()
		return True

	def _GetInputValue(self):
		text = self.valueEdit.GetText().lower().replace("k", "000")
		return long(text) if text.isdigit() else 0

	def _ResetSlider(self):
		self.sliderBase = self._GetInputValue()
		self.slider.SetSliderPos(0.5)

	def _OnSliderMove(self):
		if self.sliderBase <= 0:
			self.sliderBase = self._GetInputValue() or (ToNetPrice(self.average) if self.average > 0 else 0)
		if self.sliderBase <= 0:
			return
		factor = 1.0 + (self.slider.GetSliderPos() - 0.5) * 2.0 * self.PRICE_SLIDER_RANGE
		self._UncheckOptions()
		self.sliderMoving = True
		self.SetValue(min(MAX_NET_PRICE, max(1, long(self.sliderBase * factor))))
		self.sliderMoving = False

	def _OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.valueEdit)
		value = self._GetInputValue()
		if value > MAX_NET_PRICE:
			value = MAX_NET_PRICE
			self.valueEdit.SetText(str(value))
			self.valueEdit.SetEndPosition()
		if not self.settingValue:
			self._UncheckOptions()
		if not self.sliderMoving:
			self.sliderBase = value
			self.slider.SetSliderPos(0.5)
		if value > 0:
			self.saleText.SetText(locale.NumberToMoneyString(ToMarketPrice(value)))
		else:
			self.saleText.SetText(locale.IKASHOP_ITEM_PRICE_SALES_PRICE_FORMAT.format(locale.NumberToMoneyString(0), MARKET_FEE_PCT))

	def _UncheckOptions(self):
		self.averageCheck.SetChecked(False)
		self.lastSoldCheck.SetChecked(False)

	def _OnCheckAverage(self, checked):
		if checked:
			self.lastSoldCheck.SetChecked(False)
			if self.average > 0:
				self.SetValue(ToNetPrice(self.average))

	def _OnCheckLast(self, checked):
		if checked:
			self.averageCheck.SetChecked(False)
			if self.sales:
				(count, price, stamp) = self.sales[0]
				self.SetValue(ToNetPrice(long(price) * self.count / max(1, count)))

	def _OnAccept(self):
		if self.acceptEvent:
			self.acceptEvent()
		return True

	def _OnCancel(self):
		if self.cancelEvent:
			self.cancelEvent()
		else:
			self.SoftClose()
		return True

	def OnPressEscapeKey(self):
		return self._OnCancel()


class IkarusShopWindow(ui.Window):

	HALIGN_SETTER = {
		"center" : ui.Window.SetWindowHorizontalAlignCenter,
		"right" : ui.Window.SetWindowHorizontalAlignRight,
	}

	VALIGN_SETTER = {
		"center" : ui.Window.SetWindowVerticalAlignCenter,
		"bottom" : ui.Window.SetWindowVerticalAlignBottom,
	}

	def __init__(self):
		self._dialogs = []
		self.questionDialog = None
		self.popupDialog = None
		self.moneyInputDialog = None
		self.itemToolTip = None
		self._ExclamationMark = None
		super(IkarusShopWindow, self).__init__()

	def _ApplyWidgetAlignments(self, child, halign, valign):
		if halign in self.HALIGN_SETTER:
			self.HALIGN_SETTER[halign](child)
		if valign in self.VALIGN_SETTER:
			self.VALIGN_SETTER(child)

	def _RegisterDialog(self, dialog):
		self._dialogs.append(dialog)

	def SetTop(self):
		super(IkarusShopWindow, self).SetTop()
		for dialog in self._dialogs:
			dialog.SetTop()

	def Hide(self):
		super(IkarusShopWindow, self).Hide()
		for window in self._dialogs:
			window.Hide()

	def CreateWidget(self, type, x = 0, y = 0, show = True, pos = None, size = None, parent = None, halign = None, valign = None):
		child = type()
		child.SetParent(parent if parent else self)
		if show:
			child.Show()
		if size:
			child.SetSize(*size)
		self._ApplyWidgetAlignments(child, halign, valign)
		if pos:
			x,y = pos
		child.SetPosition(x,y)
		return child

	def Destroy(self):
		super(IkarusShopWindow, self).Destroy()
		# cleaning shitty undestroyable widgets
		if self.questionDialog:
			SelfDestroyObject(self.questionDialog)
			self.questionDialog = None
		if self.popupDialog:
			SelfDestroyObject(self.popupDialog)
			self.popupDialog = None
		if self.moneyInputDialog:
			SelfDestroyObject(self.moneyInputDialog)
			self.moneyInputDialog = None
		if self.itemToolTip:
			SelfDestroyObject(self.itemToolTip)
			self.itemToolTip = None
		# cleaning itself
		SelfDestroyObject(self)

	def OpenQuestionDialog(self, question, acceptEvent, denyEvent = None):
		if not self.questionDialog:
			self.questionDialog = IkashopQuestionDialog()
			self._RegisterDialog(self.questionDialog)
		self.questionDialog.SetText(question)
		self.questionDialog.SetAcceptEvent(acceptEvent)
		self.questionDialog.SetCancelEvent(denyEvent if denyEvent else self.questionDialog.Hide)
		self.questionDialog.Open()

	def OpenPopupDialog(self, message, seconds = 6):
		if not self.popupDialog:
			self.popupDialog = uicommon.PopupDialog()
			self._RegisterDialog(self.popupDialog)
		self.popupDialog.SetText(message)
		self.popupDialog.SetWidth(self.popupDialog.message.GetTextSize()[0] + 40)
		self.popupDialog.Open()
		self.popupDialog.SetAutoClose(seconds)

	def OpenMoneyInputDialog(self, acceptEvent, denyEvent = None, value = 0, cheque = 0, nocheque = 0):
		if ENABLE_CHEQUE_SYSTEM:
			if not nocheque:
				yangmax = 2**31
				while yangmax <= value:
					cheque += 1
					value -= ikashop.YANG_PER_CHEQUE

		if not self.moneyInputDialog:
			self.moneyInputDialog = uicommon.MoneyInputDialog()
			self.moneyInputDialog.SetTitle(locale.IKASHOP_MONEY_INPUT_DIALOG_TITLE)
			self._RegisterDialog(self.moneyInputDialog)

		if ENABLE_CHEQUE_SYSTEM:
			self.moneyInputDialog.HideCheque() if nocheque \
				else self.moneyInputDialog.ShowCheque()

		self.moneyInputDialog.Open()
		self.moneyInputDialog.SetAcceptEvent(acceptEvent)
		self.moneyInputDialog.SetCancelEvent(denyEvent if denyEvent else self.moneyInputDialog.Hide)
		self.moneyInputDialog.SetValue(value if value != 0 else "")
		if ENABLE_CHEQUE_SYSTEM:
			self.moneyInputDialog.SetCheque(cheque if cheque != 0 else "")

	def GetToolTip(self):
		if not self.itemToolTip:
			self.itemToolTip = IkashopItemToolTip()
			self.itemToolTip.itemVnum = 1
			self._RegisterDialog(self.itemToolTip)
		return self.itemToolTip

	def Toggle(self):
		self.Close() if self.IsShow()\
			else self.Open()

	def ShowExclamationMark(self, pos = None):
		rpos = pos if pos else (self.GetWidth() - 14, 1)
		if not self._ExclamationMark:
			self._ExclamationMark = self.CreateWidget(ui.ImageBox, pos = rpos )
			self._ExclamationMark.LoadImage("ikashop/lite/mark.png")
		self._ExclamationMark.Show()

	def HideExclamationMark(self):
		if self._ExclamationMark:
			self._ExclamationMark.Hide()

if ENABLE_DEFAULT_UI_BOARD:
	class IkashopBoardWithTitleBar(IkarusShopWindow):
		def __init__(self):
			self._internalBoard = None
			super(IkashopBoardWithTitleBar, self).__init__()
			self._LoadIkashopBoardWithTitleBar()

		def _LoadIkashopBoardWithTitleBar(self):
			self._internalBoard = self.CreateWidget(ui.BoardWithTitleBar, pos = (-2, -2))
			self._internalBoard.SetSize(self.GetWidth()+6, self.GetHeight()+4)

		def _UpdateView(self):
			if self._internalBoard:
				self._internalBoard.SetSize(self.GetWidth()+6, self.GetHeight()+4)

		def SetSize(self, w, h):
			super(IkashopBoardWithTitleBar, self).SetSize(w,h)
			self._UpdateView()

		def SetTitleName(self, title):
			self._internalBoard.SetTitleName(title)

		def SetCloseEvent(self, event, *args):
			self._internalBoard.SetCloseEvent(ui.__mem_func__(event, *args))

		def OnPressEscapeKey(self):
			if self.IsShow():
				self.Close()
				return True
			return False

else:
	class IkashopBoardWithTitleBar(IkarusShopWindow):

		SIDE_MARGIN = 16

		def __init__(self):
			self.centerImage = None
			super(IkashopBoardWithTitleBar, self).__init__()
			self._LoadIkashopBoardWithTitleBar()

		def _LoadIkashopBoardWithTitleBar(self):
			# loading center
			self.centerImage = self.CreateWidget(ui.ExpandedImageBox, x = 3, y = 30)
			self.centerImage.LoadImage("ikashop/lite/common/board/center.png")
			self.centerImage.AddFlag("not_pick")

			# loading sides
			self.leftSide = self.CreateWidget(ui.ExpandedImageBox, y = self.SIDE_MARGIN)
			self.leftSide.LoadImage("ikashop/lite/common/board/left.png")
			self.leftSide.AddFlag("not_pick")

			self.rightSide = self.CreateWidget(ui.ExpandedImageBox, y = self.SIDE_MARGIN)
			self.rightSide.LoadImage("ikashop/lite/common/board/right.png")
			self.rightSide.AddFlag("not_pick")

			self.bottomSide = self.CreateWidget(ui.ExpandedImageBox, x = self.SIDE_MARGIN)
			self.bottomSide.LoadImage("ikashop/lite/common/board/bottom.png")
			self.bottomSide.AddFlag("not_pick")

			# loading corners
			self.leftBottomCorner = self.CreateWidget(ui.ImageBox)
			self.leftBottomCorner.LoadImage("ikashop/lite/common/board/lb_corner.png")
			self.leftBottomCorner.AddFlag("not_pick")

			self.rightBottomCorner = self.CreateWidget(ui.ImageBox)
			self.rightBottomCorner.LoadImage("ikashop/lite/common/board/rb_corner.png")
			self.rightBottomCorner.AddFlag("not_pick")

			# loading titlebar
			self.titleLeft = self.CreateWidget(ui.ImageBox)
			self.titleLeft.LoadImage("ikashop/lite/common/board/titlebar/left.png")
			self.titleLeft.AddFlag("not_pick")

			self.titleRight = self.CreateWidget(ui.ImageBox)
			self.titleRight.LoadImage("ikashop/lite/common/board/titlebar/right.png")
			self.titleRight.AddFlag("not_pick")

			self.titleCenter = self.CreateWidget(ui.ExpandedImageBox, x = self.titleLeft.GetWidth())
			self.titleCenter.LoadImage("ikashop/lite/common/board/titlebar/center.png")
			self.titleCenter.AddFlag("not_pick")

			self.closeButton = self.CreateWidget(ui.Button, y = 3)
			self.closeButton.SetUpVisual("ikashop/lite/common/board/titlebar/close/default.png")
			self.closeButton.SetDownVisual("ikashop/lite/common/board/titlebar/close/default.png")
			self.closeButton.SetOverVisual("ikashop/lite/common/board/titlebar/close/hover.png")

			self.titleText = self.CreateWidget(ui.TextLine)
			self.titleText.SetHorizontalAlignCenter()
			self.titleText.SetFontName("Tahoma:20")
			self.titleText.SetPackedFontColor(0xFFFFFFFF)
			self.titleText.SetOutline(1)
			self.titleText.AddFlag("not_pick")

		def _UpdateView(self):
			if self.centerImage == None:
				return

			width = float(self.GetWidth())
			height = float(self.GetHeight())

			# updating center
			centerWidth = width - 6
			centerHeight = height - 33
			centerHorizontalScale = centerWidth / self.centerImage.GetWidth()
			centerVerticalScale = centerHeight / self.centerImage.GetHeight()
			self.centerImage.SetRenderingRect(0.0, 0.0, centerHorizontalScale - 1.0, centerVerticalScale - 1.0)

			# updating sides
			sideVerticalScale = (height - self.SIDE_MARGIN*2) / self.leftSide.GetHeight()
			self.leftSide.SetRenderingRect(0.0, 0.0, 0.0, sideVerticalScale - 1.0)
			sideVerticalScale = (height - self.SIDE_MARGIN*2) / self.rightSide.GetHeight()
			self.rightSide.SetRenderingRect(0.0, 0.0, 0.0, sideVerticalScale - 1.0)
			self.rightSide.SetPosition(width - self.rightSide.GetWidth(), self.SIDE_MARGIN)
			sideHorizontalScale = (width - self.SIDE_MARGIN*2) / self.bottomSide.GetWidth()
			self.bottomSide.SetRenderingRect(0.0, 0.0, sideHorizontalScale - 1.0, 0.0)
			self.bottomSide.SetPosition(self.SIDE_MARGIN, height - self.bottomSide.GetHeight())

			# updating corner positions
			self.leftBottomCorner.SetPosition(0, height - self.leftBottomCorner.GetHeight())
			self.rightBottomCorner.SetPosition(width - self.rightBottomCorner.GetWidth(), height - self.rightBottomCorner.GetHeight())

			# updating titlebar
			titlebarCenterWidth = width - self.titleLeft.GetWidth() - self.titleRight.GetWidth()
			titlebarCenterWidth = max(10, titlebarCenterWidth)
			titlebarCenterScale = titlebarCenterWidth / self.titleCenter.GetWidth()
			self.titleCenter.SetScale(titlebarCenterScale, 1.0)
			self.titleRight.SetPosition(titlebarCenterWidth + self.titleLeft.GetWidth(), 0)
			self.closeButton.SetPosition(width - self.closeButton.GetWidth() - 6, self.closeButton.GetLocalPosition()[1])
			self.titleText.SetPosition(width/2, 3)

		def SetSize(self, w, h):
			super(IkashopBoardWithTitleBar, self).SetSize(w,h)
			self._UpdateView()

		def SetTitleName(self, title):
			self.titleText.SetText(title)

		def SetCloseEvent(self, event, *args):
			self.closeButton.SetEvent(event, *args)

		def OnPressEscapeKey(self):
			if self.IsShow():
				self.Close()
				return True
			return False


class IkarusShopSafeboxBoard(IkashopBoardWithTitleBar):

	GRID_COLUMNS = ikashop.SAFEBOX_GRID_WIDTH
	GRID_ROWS = ikashop.SAFEBOX_GRID_HEIGHT
	PAGE_COUNT = ikashop.SAFEBOX_PAGE_COUNT


	def __init__(self):
		self.pendingClaim = False
		super(IkarusShopSafeboxBoard, self).__init__()
		self.items = []
		self._SettingUpBoard()
		self._LoadIkarusShopSafeboxBoard()

	def _SettingUpBoard(self):
		sw, sh = GetScreenSize()
		self.SetSize(177, 387)
		self.SetTitleName(locale.IKASHOP_SAFEBOX_BOARD_TITLE)
		self.SetCloseEvent(self.Close)
		self.SetPosition(sw/2 - self.GetWidth(), sh / 2 - self.GetHeight()/2)
		self.AddFlag("movable")
		self.AddFlag("float")
		self.yang = 0
		self.silentRequest = False
		self.moneyEvent = None

	def _LoadIkarusShopSafeboxBoard(self):
		self.slotBox = self.CreateWidget(ui.ImageBox, pos = (6, 26))
		self.slotBox.LoadImage(OFFLINESHOP_UI_PATH + "bg_grid.png")

		self.slotWindow = self.CreateWidget(ui.GridSlotWindow, parent = self.slotBox, pos = (3,3))
		self.slotWindow.ArrangeSlot(0, self.GRID_COLUMNS, self.GRID_ROWS, SLOT_SIZE, SLOT_SIZE, 0, 0)
		self.slotWindow.SetSlotBaseImage(SLOT_BASE_IMG, 1.0, 1.0, 1.0, 1.0)
		self.slotWindow.SetOverInItemEvent(self._ShowToolTipOnItemSlot)
		self.slotWindow.SetOverOutItemEvent(self._HideToolTipOnItemSlot)
		self.slotWindow.SetSelectItemSlotEvent(self._OnClickItemSlot)

		self.moneyText = self.CreateWidget(ui.TextLine, pos = (0, 0), show = False)

		# page buttons (6,322) 166x24, buttons 39x20 at (9 + 40*i, 324)
		self.pageButtonsBg = self.CreateWidget(ui.ImageBox, pos = (6, 322))
		self.pageButtonsBg.LoadImage(OFFLINESHOP_UI_PATH + "bg_pagenumber.png")
		self.selectPageButtons = []
		for i in xrange(self.PAGE_COUNT):
			selectPageButton = self.CreateWidget(ui.Button, pos = (9 + i*40, 324))
			selectPageButton.SetUpVisual(OFFLINESHOP_UI_PATH + "btn_page.png")
			selectPageButton.SetOverVisual(OFFLINESHOP_UI_PATH + "btn_page_hover.png")
			selectPageButton.SetDownVisual(OFFLINESHOP_UI_PATH + "btn_page_clicked.png")
			selectPageButton.SetDisableVisual(OFFLINESHOP_UI_PATH + "btn_page_active.png")
			selectPageButton.SetText(RomeNumber(i+1))
			selectPageButton.SAFE_SetEvent(self._OnSelectPage, i)
			self.selectPageButtons.append(selectPageButton)

		# claim items (6,348) 166x30
		self.itemsClaimButton = self.CreateWidget(ui.Button, pos = (6, 348))
		self.itemsClaimButton.SetUpVisual(OFFLINESHOP_UI_PATH + "btn_collect.png")
		self.itemsClaimButton.SetOverVisual(OFFLINESHOP_UI_PATH + "btn_collect_hover.png")
		self.itemsClaimButton.SetDownVisual(OFFLINESHOP_UI_PATH + "btn_collect_clicked.png")
		self.itemsClaimButton.SetText(locale.IKASHOP_SAFEBOX_CLAIM_ITEMS_BUTTON_TEXT)
		self.itemsClaimButton.SAFE_SetEvent(self._OnClickClaimAllItemsButton)

		# default opening first page
		self._OnSelectPage(0)

	def _OnSelectPage(self, num):
		for button in self.selectPageButtons:
			button.Enable()
		self.selectPageButtons[num].Disable()
		self.currentPage = num
		self._RefreshPage()

	def _RefreshPage(self):
		cells = self.GRID_COLUMNS * self.GRID_ROWS
		srange = cells * self.currentPage
		erange = srange + cells

		for i in xrange(srange, erange):
			local = i - srange
			if not i in self.items:
				self.slotWindow.ClearSlot(local)
				continue
			data = self.items[i]
			count = data['count'] if data['count'] > 1 else 0
			self.slotWindow.SetItemSlot(local, data['vnum'], count)

		self.slotWindow.RefreshSlot()

	def _RefreshItems(self, items):
		self.items = {item['cell'] : item for item in items}
		self._RefreshPage()

	def _ShowToolTipOnItemSlot(self, slot):
		slot = slot + self.currentPage * (self.GRID_COLUMNS * self.GRID_ROWS)
		if slot in self.items:
			data = self.items[slot]
			tooltip = self.GetToolTip()
			tooltip.ClearToolTip()
			tooltip.AddItemData(data['vnum'], data['sockets'], data['attrs'])
			tooltip.AppendTextLine(locale.IKASHOP_SAFEBOX_CLAIM_ITEM_TOOLTIP)
			tooltip.ShowToolTip()

	def _HideToolTipOnItemSlot(self, slot=0):
		tooltip = self.GetToolTip()
		tooltip.ClearToolTip()
		tooltip.HideToolTip()

	def _OnClickItemSlot(self, cell):
		cell = cell + self.currentPage * (self.GRID_COLUMNS * self.GRID_ROWS)
		if cell in self.items:
			data = self.items[cell]
			ikashop.SendSafeboxGetItem(data['id'])

	def _OnClickClaimAllItemsButton(self):
		self.OpenQuestionDialog(
			locale.IKASHOP_SAFEBOX_CLAIM_ALL_ITEMS_QUESTION, self._OnAcceptClaimAllItemsQuestion)

	def _OnClickClaimMoneyButton(self):


		ikashop.SendSafeboxGetValutes()

	def _OnAcceptClaimAllItemsQuestion(self):
		self.questionDialog.Hide()
		for item in self.items.values():
			ikashop.SendSafeboxGetItem(item['id'])

	def Open(self):
		self.SetTop()
		if not self.IsShow():
			ikashop.SendSafeboxOpen()

	def Setup(self, yang, items):
		self.yang = yang
		self.moneyText.SetText(locale.NumberToString(yang))
		if self.moneyEvent:
			self.moneyEvent(yang)
		self._RefreshItems(items)
		if self.silentRequest:
			self.silentRequest = False
			if not self.IsShow():
				if self.pendingClaim:
					self.pendingClaim = False
					ikashop.SendSafeboxGetValutes()
					self.silentRequest = True
					return
				ikashop.SendSafeboxClose()
				return
		if not self.IsShow():
			self.Show()
			self.SetTop()

	def SetMoneyEvent(self, event):
		self.moneyEvent = event

	def RequestMoney(self):
		if self.IsShow():
			return
		self.silentRequest = True
		ikashop.SendSafeboxOpen()

	def ClaimMoney(self):
		if self.IsShow():
			ikashop.SendSafeboxGetValutes()
			return
		self.pendingClaim = True
		self.silentRequest = True
		ikashop.SendSafeboxOpen()

	def RemoveItem(self, itemid):
		items = [data for data in self.items.values() if data['id'] != itemid]
		self._RefreshItems(items)

	def AddItem(self, item):
		items = list(self.items.values()) + [item,]
		self._RefreshItems(items)

	def Destroy(self):
		super(IkarusShopSafeboxBoard, self).Destroy()

	def Close(self):
		ikashop.SendSafeboxClose()
		self.Hide()

class IkarusCreateAuctionDialog(IkashopBoardWithTitleBar):

	def __init__(self):
		super(IkarusCreateAuctionDialog, self).__init__()
		self._LoadIkarusCreateAuctionDialog()
		self._InsertedItem = None
		self._ItemInfo = None

	def _LoadIkarusCreateAuctionDialog(self):
		self._SettingUpBoard()

		# loading slot
		self.slot = self.CreateWidget(ui.GridSlotWindow, pos = (self.GetWidth()/2- 17, 45))
		self.slot.ArrangeSlot(0, 1, 3, SLOT_SIZE, SLOT_SIZE, 0, 0)
		self.slot.SetSlotBaseImage("ikashop/lite/common/slot/default.png", 1.0, 1.0, 1.0, 1.0)
		self.slot.SetSelectEmptySlotEvent(self._OnClickEmptySlot)
		self.slot.SetSelectItemSlotEvent(self._OnClickItemSlot)
		self.slot.SetOverInItemEvent(self._ShowToolTipOnItemSlot)
		self.slot.SetOverOutItemEvent(self._HideToolTipOnItemSlot)

		# loading continue button
		self.proceedButton = self.CreateWidget(ui.Button, pos = (self.GetWidth() / 2 - 53, self.GetHeight() - 40))
		self.proceedButton.SetUpVisual("ikashop/lite/auction/raise_button/default.png")
		self.proceedButton.SetDownVisual("ikashop/lite/auction/raise_button/default.png")
		self.proceedButton.SetOverVisual("ikashop/lite/auction/raise_button/hover.png")
		self.proceedButton.SetText(locale.IKASHOP_ACUTION_CREATE_CREATE_BUTTON)
		self.proceedButton.SAFE_SetEvent(self._OnClickCreateAuction)
		self.proceedButton.Show()
		self.proceedButton.ButtonText.SetPosition(self.proceedButton.GetWidth()/2 + 12, self.proceedButton.GetHeight()/2-1)

	def _SettingUpBoard(self):
		sw, sh = GetScreenSize()
		self.SetSize(145, 195)
		self.SetTitleName(locale.IKASHOP_AUCTION_CREATE_BOARD_TITLE)
		self.SetCloseEvent(self.Close)
		self.SetPosition(sw/2 - self.GetWidth()/2, sh / 2 - self.GetHeight()/2)
		self.AddFlag("movable")
		self.AddFlag("float")

	def _Reset(self):
		# reset slots
		for i in xrange(3):
			self.slot.ClearSlot(i)
		self.slot.RefreshSlot()

		if self.moneyInputDialog:
			self.moneyInputDialog.SoftClose()

		self._InsertedItem = None
		self._ItemInfo = None

	def _OnClickEmptySlot(self, slot):
		if self._InsertedItem != None:
			return
		if mouse.mouseController.isAttached():
			attachedType = mouse.mouseController.GetAttachedType()
			attachedItemIndex = mouse.mouseController.GetAttachedItemIndex()
			attachedItemSlotPos = mouse.mouseController.GetAttachedSlotNumber()
			mouse.mouseController.DeattachObject()
			# validating attached item
			if attachedType in GetSellableSlotTypes():
				win, pos = player.SlotTypeToInvenType(attachedType), attachedItemSlotPos
				if player.ITEM_MONEY != attachedItemIndex:
					self.InsertItemInSlot(win, pos)

	def _OnClickItemSlot(self, slot):
		if mouse.mouseController.isAttached():
			return
		self._Reset()

	def _ShowToolTipOnItemSlot(self, slot):
		win, pos = self._InsertedItem
		tooltip = self.GetToolTip()
		tooltip.SetInventoryItem(pos, win)
		tooltip.AppendTextLine(locale.IKASHOP_AUCTION_CREATE_REMOVE_ITEM)

	def _HideToolTipOnItemSlot(self, slot = 0):
		tooltip = self.GetToolTip()
		tooltip.ClearToolTip()
		tooltip.HideToolTip()

	def _OnClickCreateAuction(self):
		self.OpenMoneyInputDialog(self._OnAcceptStartingPriceInput, nocheque = 1)
		if app.EXTEND_IKASHOP_ULTIMATE:
			vnum, count, hash = self._ItemInfo
			ikashop.SendPriceAverageRequest(vnum, count)
			self.moneyInputDialog.SetPriceAverage(-1)

	def _OnAcceptStartingPriceInput(self):
		# extracting value
		value = self.moneyInputDialog.GetText()
		value = value.lower().replace("k", "000")
		self.moneyInputDialog.SoftClose()

		# validating value
		if not value or not value.isdigit():
			self.OpenPopupDialog(locale.IKASHOP_BUSINESS_INVALID_ITEM_PRICE)
			return

		if self._InsertedItem is None:
			return

		win, pos = self._InsertedItem

		self.Close()
		ikashop.SendAuctionCreate(win, pos, long(value))
		return True

	def InsertItemInSlot(self, win, pos):
		vnum = player.GetItemIndex(win, pos)
		count = player.GetItemCount(win, pos)

		# checking item antifalg
		item.SelectItem(vnum)
		if item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
			self.OpenPopupDialog(locale.IKASHOP_BUSINESS_CANNOT_SELL_ITEM)
			return

		self._InsertedItem = win, pos
		self._ItemInfo = vnum, count, GetInventoryItemHash(win, pos)

		self.slot.SetItemSlot(0, vnum, count if count > 1 else 0)
		self.slot.RefreshSlot()

	def Open(self):
		self._Reset()
		self.Show()
		self.SetTop()
		if app.EXTEND_IKASHOP_PRO:
			player.RefreshInventory()

	def Close(self):
		self.Hide()
		if app.EXTEND_IKASHOP_PRO:
			player.RefreshInventory()

	def OnUpdate(self):
		if self._ItemInfo != None:
			win, pos = self._InsertedItem
			vnum, count, hash = self._ItemInfo

			if vnum != player.GetItemIndex(win, pos):
				self._Reset()
			elif count != player.GetItemCount(win, pos):
				self._Reset()
			elif hash != GetInventoryItemHash(win, pos):
				self._Reset()


class IkarusShopAuctionOfferView(IkarusShopWindow):

	def __init__(self):
		super(IkarusShopAuctionOfferView, self).__init__()
		self._LoadIkarusShopAuctionOfferView()

	def _LoadIkarusShopAuctionOfferView(self):
		self.background = self.CreateWidget(ui.ImageBox, pos = ())
		self.background.LoadImage("ikashop/lite/auction/offer_box.png")
		self.SetSize(self.background.GetWidth(), self.background.GetHeight())

		# making name text
		self.nameText = self.CreateWidget(ui.TextLine, pos = (28, 5))
		self.nameText.SetPackedFontColor(0xFFFFFFFF)
		self.nameText.SetFontName("Tahoma:11")

		# making datetime
		self.datetimeText = self.CreateWidget(ui.TextLine, pos = (168 + 13, 5))
		self.datetimeText.SetPackedFontColor(0xFFFFFFFF)
		self.datetimeText.SetHorizontalAlignCenter()

		# making money text
		self.moneyText = self.CreateWidget(ui.TextLine, pos = (256 + 13, 5))
		self.moneyText.SetPackedFontColor(0xFFFFFFFF)

	def Setup(self, pos, data):
		name, datetime, price = data['buyername'], data['datetime'], data['price']
		self.nameText.SetText("{}. {}".format(pos, name))
		self.datetimeText.SetText(DatetimeFormat(datetime))
		self.moneyText.SetText(locale.NumberToString(price))
		self.Show()

class IkarusShopAuctionOwnerBoard(IkashopBoardWithTitleBar):
	OFFER_VIEW_COUNT = 6
	OFFER_VIEW_HEIGHT = 28
	RAISE_FACTOR = 1.0 + float(AUCTION_MIN_RAISE_PERCENTAGE) / 100.0

	def __init__(self):
		super(IkarusShopAuctionOwnerBoard, self).__init__()
		self._SettingUpBoard()
		self._LoadIkarusShopAuctionOwnerBoard()

	def _SettingUpBoard(self):
		sw, sh = GetScreenSize()
		self.SetSize(513 + 13, 249)
		self.SetTitleName(locale.IKASHOP_AUCTION_BOARD_TITLE)
		self.SetCloseEvent(self.Close)
		self.SetPosition(sw/2 - self.GetWidth(), sh / 2 - self.GetHeight()/2 + 100)
		self.AddFlag("movable")
		self.AddFlag("float")

	def _LoadIkarusShopAuctionOwnerBoard(self):
		# making info box
		self.infoBox = self.CreateWidget(ui.ImageBox, pos = (12, 36))
		self.infoBox.LoadImage("ikashop/lite/auction/info_box.png")
		self.infoBox.SetMouseWheelEvent(self._MouseWheelScrollOffers)

		self.minRaiseText = self.CreateWidget(ui.TextLine, pos = (458+13, 221-36), parent = self.infoBox)
		self.minRaiseText.SetPackedFontColor(0xFFFFFFFF)
		self.minRaiseText.SetHorizontalAlignRight()

		self.durationText = self.CreateWidget(ui.TextLine, pos = (141, 221-36), parent = self.infoBox)
		self.durationText.SetPackedFontColor(0xFFFFFFFF)

		# making slot
		self.slot = self.CreateWidget(ui.GridSlotWindow, pos = (36, 44), size = (32, 98), parent = self.infoBox)
		self.slot.ArrangeSlot(0, 1, 3, SLOT_SIZE, SLOT_SIZE, 0, 0)
		self.slot.SetSlotBaseImage("ikashop/lite/common/slot/default.png", 1.0, 1.0, 1.0, 1.0)
		self.slot.SetOverInItemEvent(self._OverInItem)
		self.slot.SetOverOutItemEvent(self._OverOutItem)

		# making scrollbar
		self.offerScrollbar = self.CreateWidget(ui.ScrollBar, pos = (470+13, 4), parent = self.infoBox)
		self.offerScrollbar.SetScrollBarSize(self.infoBox.GetHeight() - 35)
		self.offerScrollbar.SetScrollEvent(self._ScrollOffers)

		# making cancel auction button
		self.cancelAuctionButton = self.CreateWidget(ui.Button, pos = (12, self.GetHeight() - 33))
		self.cancelAuctionButton.SetUpVisual("ikashop/lite/auction/cancel_button/default.png")
		self.cancelAuctionButton.SetDownVisual("ikashop/lite/auction/cancel_button/default.png")
		self.cancelAuctionButton.SetOverVisual("ikashop/lite/auction/cancel_button/hover.png")
		self.cancelAuctionButton.SetText(locale.IKASHOP_ACUTION_CANCEL_AUCTION_BUTTON)
		self.cancelAuctionButton.SAFE_SetEvent(self._OnClickCancelAuction)
		self.cancelAuctionButton.Show()

		# making offers
		self.offerViews = []
		for i in xrange(self.OFFER_VIEW_COUNT):
			self.offerViews.append(self.CreateWidget(
				IkarusShopAuctionOfferView, pos = (115, 6 + i*self.OFFER_VIEW_HEIGHT), parent = self.infoBox))

	def _RefreshOffers(self):
		# calculating count difference
		diff = len(self.offers) - self.OFFER_VIEW_COUNT
		diff = max(diff, 0)

		# calculating ranges
		offset = self.offerScrollbar.GetPos()
		sindex = int(diff * offset)
		eindex = sindex + min(self.OFFER_VIEW_COUNT, len(self.offers))

		# iterating over views
		for i, view in enumerate(self.offerViews):
			ri = i + sindex
			view.Hide() if ri >= eindex \
				else view.Setup(ri+1, self.offers[ri])

		# updating scrollbar middlebar length
		viewHeight = self.OFFER_VIEW_HEIGHT
		self.offerScrollbar.UpdateScrollbarLenght(viewHeight * len(self.offers))

	def _MouseWheelScrollOffers(self, delta):
		if self.offerScrollbar.IsShow():
			self.offerScrollbar.OnDown() if delta < 0 \
				else self.offerScrollbar.OnUp()
		return True

	def _ScrollOffers(self):
		if self.offerScrollbar.IsShow():
			self._RefreshOffers()

	def _UpdateScrollbarState(self):
		self.offerScrollbar.SetPos(0)
		if len(self.offers) <= self.OFFER_VIEW_COUNT:
			self.offerScrollbar.Hide()
		else:
			self.offerScrollbar.Show()

	def _OverInItem(self, slot):
		data = self.auctionInfo
		tooltip = self.GetToolTip()
		tooltip.ClearToolTip()
		tooltip.AddItemData(data['vnum'], data['sockets'], data['attrs'])
		if app.EXTEND_IKASHOP_ULTIMATE:
			tooltip.AppendTextLine(locale.IKASHOP_ULTIMATE_PRICE_AVERAGE_NOT_AVAILABLE) if data['priceavg'] == 0 \
				else tooltip.AppendTextLine(locale.IKASHOP_ULTIMATE_PRICE_AVERAGE_VALUE.format(locale.NumberToMoneyString(data['priceavg'])))
		tooltip.ShowToolTip()

	def _OverOutItem(self, slot = 0):
		tooltip = self.GetToolTip()
		tooltip.ClearToolTip()
		tooltip.HideToolTip()

	def _OnClickCancelAuction(self):
		if self.auctionInfo['offers']:
			self.OpenPopupDialog(locale.IKASHOP_AUCTION_CANNOT_CANCEL)
			return

		self.OpenQuestionDialog(locale.IKASHOP_AUCTION_CANCEL_AUCTION_QUESTION, self._OnAcceptCancelAuction)

	def _OnAcceptCancelAuction(self):
		ikashop.SendMyAuctionCancel()
		self.questionDialog.Close()
		self.Close()

	def SetOffers(self, offers):
		self.offers = sorted(offers, key = lambda val : val['datetime'], reverse=True)
		self._UpdateScrollbarState()
		self._RefreshOffers()
		self.RefreshMinRaise()

	def SetDuration(self, duration):
		self.durationText.SetText(locale.SecondToDHM(duration*60))

	def _GetMinRaise(self):
		if not self.offers:
			return self.auctionInfo['price']

		minraise = max([val['price'] for val in self.offers])
		if minraise < 1000:
			return minraise + 1000

		return minraise * (100+AUCTION_MIN_RAISE_PERCENTAGE) / 100

	def RefreshMinRaise(self):
		self.minRaise = self._GetMinRaise()
		self.minRaiseText.SetText(locale.IKASHOP_AUCTION_MIN_BID + '  ' + locale.NumberToString(self.minRaise))

	def Open(self):
		ikashop.SendMyAuctionOpen()

	def Close(self):
		self.Hide()
		ikashop.SendMyAuctionClose()

	def Setup(self, data):
		# storing data
		self.auctionInfo = data

		# refreshing duration
		seconds = data['duration'] * 60
		self.durationText.SetText(locale.SecondToDHM(seconds))

		# refreshing item
		vnum = data['vnum']
		count = data['count'] if data['count'] > 1 else 0
		item.SelectItem(vnum)
		size = item.GetItemSize()[1]
		self.slot.ArrangeSlot(0, 1, size, SLOT_SIZE, SLOT_SIZE, 0, 0)
		self.slot.SetSlotBaseImage("ikashop/lite/common/slot/default.png", 1.0, 1.0, 1.0, 1.0)
		self.slot.SetItemSlot(0, vnum, count)

		# refreshing offers
		self.SetOffers(data['offers'])

		if not self.IsShow():
			self.Show()
			self.SetTop()

class IkarusShopListBoard(IkashopBoardWithTitleBar):

	DOCKED_TO_SHOP = False

	def __init__(self):
		self.elements = []
		super(IkarusShopListBoard, self).__init__()

	def _LoadIkarusShopListBoard(self):
		# making board box
		self.boardBox = self.CreateWidget(ui.ExpandedImageBox, pos = (11,36))
		self.boardBox.LoadImage("ikashop/lite/list_box.png")
		boardBoxHorizontalScale = float(self.GetWidth() - 22 - 16) / self.boardBox.GetWidth()
		boardBoxVerticalScale =  float(self.GetHeight() - 47) / self.boardBox.GetHeight()
		self.boardBox.SetScale(boardBoxHorizontalScale, boardBoxVerticalScale)
		self.boardBox.SetMouseWheelEvent(self._MouseWheelScrollElements)

		# making scrollbar
		self.elementScrollbar = self.CreateWidget(ui.ScrollBar, pos = (self.GetWidth() - 24, 36))
		self.elementScrollbar.SetScrollBarSize(self.boardBox.GetHeight())
		self.elementScrollbar.SetScrollEvent(self._ScrollElements)

		# making empty header
		self.emptyHeader = self.CreateWidget(ui.TextLine, pos = (self.GetWidth()/2, self.GetHeight()/2 - 10))
		self.emptyHeader.SetFontName("Tahoma:14")
		self.emptyHeader.SetPackedFontColor(0xFFFFFFFF)
		self.emptyHeader.SetOutline(1)
		self.emptyHeader.SetHorizontalAlignCenter()
		self.emptyHeader.SetVerticalAlignCenter()
		self.emptyHeader.SetText(locale.IKASHOP_GENERIC_LIST_EMPTY_HEADER)

	def _SettingUpBoard(self):
		sw, sh = GetScreenSize()
		self.SetCloseEvent(self.Close)
		self.SetPosition(sw/2 + 20 - (self.GetWidth() - 200), sh / 2 - self.GetHeight()/2)
		if not self.DOCKED_TO_SHOP:
			self.AddFlag("movable")
		self.AddFlag("float")

	def _MakeListElements(self, type, viewCount):
		self.viewCount = viewCount
		# making notifiction boxes
		self.views = []
		for i in xrange(self.viewCount):
			view = self.CreateWidget(type, parent = self.boardBox)
			space = view.GetHeight()+2
			view.SetPosition(9, 7 + i * space)
			self.views.append(view)

	def _ScrollElements(self):
		if self.elementScrollbar.IsShow():
			self._RefreshElements()

	def _MouseWheelScrollElements(self, delta):
		if self.elementScrollbar.IsShow():
			self.elementScrollbar.OnDown() if delta < 0 \
				else self.elementScrollbar.OnUp()
		return True

	def _UpdateScrollbarState(self):
		if len(self.elements) <= self.viewCount:
			self.elementScrollbar.SetPos(0)
			self.elementScrollbar.Hide()
		else:
			self.elementScrollbar.Show()

	def _RefreshElements(self):
		# calculating count difference
		diff = len(self.elements) - self.viewCount
		diff = max(diff, 0)

		# calculating ranges
		offset = self.elementScrollbar.GetPos()
		sindex = int(diff * offset)
		eindex = sindex + min(self.viewCount, len(self.elements))

		# iterating over views
		for i, view in enumerate(self.views):
			ri = i + sindex
			if ri >= eindex:
				view.Hide()
			else:
				view.Setup(self.elements[ri])
				view.Show()

		# updating scrollbar middlebar length
		viewHeight = self.views[0].GetHeight()+2
		self.elementScrollbar.UpdateScrollbarLenght(viewHeight * len(self.elements))

	def SetElements(self, elements):
		self.elements = elements
		self._UpdateScrollbarState()
		self._RefreshElements()

		self.emptyHeader.Show() if not elements \
			else self.emptyHeader.Hide()


class IkarusShopOfferView(IkarusShopWindow):

	def __init__(self):
		self.itemData = None
		super(IkarusShopOfferView, self).__init__()
		self._LoadIkarusShopOfferView()

	def _LoadIkarusShopOfferView(self):
		# making background
		self.background = self.CreateWidget(ui.ExpandedImageBox)
		self.background.LoadImage("ikashop/lite/search_shop/result_item_box.png")
		self.SetSize(self.background.GetWidth(), self.background.GetHeight())

		# making textlines
		self.itemName = self.CreateWidget(ui.TextLine, pos = (60, 17 - 6))
		self.itemName.SetPackedFontColor(0xFFFFFFFF)
		self.sellerName = self.CreateWidget(ui.TextLine, pos = (78, 41 - 6))
		self.duration = self.CreateWidget(ui.TextLine, pos = (226, 41 - 6))
		self.price = self.CreateWidget(ui.TextLine, pos = (78, 58))

		if app.EXTEND_IKASHOP_ULTIMATE:
			self.priceAverage = self.CreateWidget(ui.TextLine, pos = (330-8, 58))
			self.priceAverage.SetHorizontalAlignRight()

		# making buttons
		self.acceptOfferButton = self.CreateWidget(ui.Button, pos = (261, 84))
		self.acceptOfferButton.SetUpVisual("ikashop/lite/search_shop/buy_button/default.png")
		self.acceptOfferButton.SetDownVisual("ikashop/lite/search_shop/buy_button/default.png")
		self.acceptOfferButton.SetOverVisual("ikashop/lite/search_shop/buy_button/hover.png")
		self.acceptOfferButton.SAFE_SetEvent(self._OnClickAcceptOffer)
		self.acceptOfferButton.SetText(locale.IKASHOP_OFFER_LIST_ACCEPT_OFFER_BUTTON_TEXT)

		self.cancelOfferButton = self.CreateWidget(ui.Button, pos = (189, 84))
		self.cancelOfferButton.SetUpVisual("ikashop/lite/search_shop/offer_button/default.png")
		self.cancelOfferButton.SetDownVisual("ikashop/lite/search_shop/offer_button/default.png")
		self.cancelOfferButton.SetOverVisual("ikashop/lite/search_shop/offer_button/hover.png")
		self.cancelOfferButton.SAFE_SetEvent(self._OnClickCancelButton)
		self.cancelOfferButton.SetText(locale.IKASHOP_SEARCH_SHOP_OFFER_BUTTON_TEXT)

		# making slot item
		self.slot = self.CreateWidget(ui.GridSlotWindow, pos = (9, 7))
		self.slot.ArrangeSlot(0, 1, 3, SLOT_SIZE, SLOT_SIZE, 0, 0)
		self.slot.SetSlotBaseImage("ikashop/lite/common/slot/default.png", 1.0, 1.0, 1.0, 1.0)
		self.slot.SetOverInItemEvent(self._OverInItem)
		self.slot.SetOverOutItemEvent(self._OverOutItem)

	def _OverInItem(self, slot):
		tooltip = self.GetToolTip()
		tooltip.ClearToolTip()
		tooltip.AddItemData(self.itemData['vnum'], self.itemData['sockets'], self.itemData['attrs'])
		tooltip.ShowToolTip()

	def _OverOutItem(self):
		tooltip = self.GetToolTip()
		tooltip.HideToolTip()

	def _OnClickAcceptOffer(self):
		self.OpenQuestionDialog(locale.IKASHOP_OFFER_LIST_ACCEPT_OFFER_QUESTION, self._OnAcceptOffer)

	def _OnClickCancelButton(self):
		self.OpenQuestionDialog(locale.IKASHOP_OFFER_LIST_CANCEL_OFFER_QUESTION, self._OnCancelOffer)

	def _OnAcceptOffer(self):
		self.questionDialog.Hide()
		ikashop.SendOfferAccept(self.data['id'])

	def _OnCancelOffer(self):
		self.questionDialog.Hide()
		ikashop.SendOfferCancel(self.data['id'], self.data['ownerid'])

	def Setup(self, data):
		self.ShowExclamationMark() if data['incoming']\
			else self.HideExclamationMark()

		self.acceptOfferButton.Show() if data['incoming']\
			else self.acceptOfferButton.Hide()

		self.cancelOfferButton.SetText(locale.IKASHOP_OFFER_LIST_DENY_OFFER_BUTTON_TEXT) if data['incoming']\
			else self.cancelOfferButton.SetText(locale.IKASHOP_OFFER_LIST_CANCEL_OFFER_BUTTON_TEXT)

		self.cancelOfferButton.SetPosition(189, 84) if data['incoming']\
			else self.cancelOfferButton.SetPosition(261, 84)

		self.background.LoadImage("ikashop/lite/offer_list/incoming_offer.png") if data['incoming']\
			else self.background.LoadImage("ikashop/lite/offer_list/outcoming_offer.png")

		# setting itemname
		itemData = data['item']
		item.SelectItem(itemData['vnum'])
		itemName = item.GetItemName()
		self.itemName.SetText(itemName)

		# setting seller name
		self.sellerName.SetText(data['buyer_name']) if data['incoming']\
			else self.sellerName.SetText(data['name'])

		# setting duration
		self.duration.SetText(DatetimeFormat(data['datetime']))

		# setting price
		self.price.SetText(locale.NumberToString(data['price']))

		if app.EXTEND_IKASHOP_ULTIMATE:
			pa = locale.IKASHOP_ULTIMATE_PRICE_AVERAGE_NOT_AVAILABLE_EMOJI if itemData['priceavg'] == 0 \
				else locale.IKASHOP_ULTIMATE_PRICE_AVERAGE_EMOJI.format(locale.NumberToMoneyString(itemData['priceavg']))
			self.priceAverage.SetText(pa)


		# setting slot
		itemcount = itemData['count'] if itemData['count'] > 1 else 0
		self.slot.ArrangeSlot(0, 1, item.GetItemSize()[1], SLOT_SIZE, SLOT_SIZE, 0, 0)
		self.slot.SetSlotBaseImage("ikashop/lite/common/slot/default.png", 1.0, 1.0, 1.0, 1.0)
		self.slot.SetItemSlot(0, itemData['vnum'], itemcount)
		self.data = data
		self.itemData = itemData

	if SEARCH_SHOP_RENEWAL:
		def _LoadIkarusShopOfferView(self):
			self.background = self.CreateWidget(ui.ImageBox)
			self.background.LoadImage(OFFER_UI + "bg_offer.png")
			self.SetSize(156, 139)
			self.slot = self.CreateWidget(ui.GridSlotWindow, pos = (6, 6))
			self.slot.ArrangeSlot(0, 1, 3, SLOT_SIZE, SLOT_SIZE, 0, 1)
			self.slot.SetOverInItemEvent(self._OverInItem)
			self.slot.SetOverOutItemEvent(self._OverOutItem)
			self.offerTexts = []
			for y in (16, 41, 67, 93):
				line = self.CreateWidget(ui.TextLine, pos = (96, y))
				line.SetHorizontalAlignCenter()
				line.SetVerticalAlignCenter()
				line.SetPackedFontColor(SEARCH_TEXT_COLOR)
				self.offerTexts.append(line)
			(self.itemName, self.price, self.sellerName, self.duration) = self.offerTexts
			self.pmButton = self.CreateWidget(ui.Button, pos = (127, 57))
			self.pmButton.SetUpVisual(OFFER_UI + "btn_pm.png")
			self.pmButton.SetOverVisual(OFFER_UI + "btn_pm_hover.png")
			self.pmButton.SetDownVisual(OFFER_UI + "btn_pm_clicked.png")
			self.pmButton.SAFE_SetEvent(self._OnClickOfferPM)
			self.acceptOfferButton = self.CreateWidget(ui.Button, pos = (0, 112))
			self.acceptOfferButton.SetUpVisual(OFFER_UI + "btn_accept.png")
			self.acceptOfferButton.SetOverVisual(OFFER_UI + "btn_accept_hover.png")
			self.acceptOfferButton.SetDownVisual(OFFER_UI + "btn_accept_clicked.png")
			self.acceptOfferButton.SAFE_SetEvent(self._OnClickAcceptOffer)
			self.acceptOfferButton.SetToolTipText(locale.IKASHOP_OFFER_LIST_ACCEPT_OFFER_BUTTON_TEXT)
			self.cancelOfferButton = self.CreateWidget(ui.Button, pos = (78, 112))
			self.cancelOfferButton.SetUpVisual(OFFER_UI + "btn_decline.png")
			self.cancelOfferButton.SetOverVisual(OFFER_UI + "btn_decline_hover.png")
			self.cancelOfferButton.SetDownVisual(OFFER_UI + "btn_decline_clicked.png")
			self.cancelOfferButton.SAFE_SetEvent(self._OnClickCancelButton)
			self.cancelOfferButton.SetToolTipText(locale.IKASHOP_OFFER_LIST_DENY_OFFER_BUTTON_TEXT)
			self.statusBar = self.CreateWidget(ui.ImageBox, pos = (0, 112), show = False)
			self.statusBar.LoadImage(OFFER_UI + "bg_acceptedordeclined.png")
			self.statusText = self.CreateWidget(ui.TextLine, pos = (78, 13), parent = self.statusBar)
			self.statusText.SetHorizontalAlignCenter()
			self.statusText.SetVerticalAlignCenter()
			self.statusText.SetFontName("Tahoma:12b")
			self.statusText.SetText(locale.IKASHOP_OFFER_STATUS_ACCEPTED)

		def Setup(self, data):
			self.data = data
			itemData = data['item']
			self.itemData = itemData
			item.SelectItem(itemData['vnum'])
			self.itemName.SetText(item.GetItemName())
			self.price.SetText(SearchShortMoney(data['price']) + SEARCH_PRICE_COIN)
			self.sellerName.SetText(data['buyer_name'] if data['incoming'] else data['name'])
			self.sellerName.SetPosition(85, 67)
			self.pmButton.Show()
			self.duration.SetText(DatetimeFormat(data['datetime']) or "")
			count = itemData['count'] if itemData['count'] > 1 else 0
			self.slot.ArrangeSlot(0, 1, max(1, min(3, item.GetItemSize()[1])), SLOT_SIZE, SLOT_SIZE, 0, 1)
			self.slot.SetItemSlot(0, itemData['vnum'], count)
			accepted = data.get('accepted')
			self.statusBar.Show() if accepted else self.statusBar.Hide()
			if accepted:
				self.acceptOfferButton.Hide()
				self.cancelOfferButton.Hide()
			elif data['incoming']:
				self.acceptOfferButton.Show()
				self.cancelOfferButton.Show()
			else:
				self.acceptOfferButton.Hide()
				self.cancelOfferButton.Show()
			self.cancelOfferButton.SetPosition(78 if data['incoming'] else 39, 112)
			self.HideExclamationMark()

		def _OnClickOfferPM(self):
			name = self.data.get('buyer_name' if self.data.get('incoming') else 'name', '')
			board = SEARCH_SALES.get("board")
			if name and board and app.EXTEND_IKASHOP_PRO:
				try:
					board.OpenWhisper(name)
				except ReferenceError:
					pass

class IkarusShopOffersBoard(IkarusShopListBoard):

	OFFER_VIEW_COUNT = 3

	def __init__(self):
		self.lastOfferTab = None
		self.offerScroll = 0
		self.offerPeek = None
		super(IkarusShopOffersBoard, self).__init__()
		self._SettingUpBoard()
		self._LoadIkarusShopOffersBoard()

	def _SettingUpBoard(self):
		self.SetSize(177, 468)
		self.SetTitleName(locale.IKASHOP_OFFER_LIST_BOARD_TITLE)
		super(IkarusShopOffersBoard, self)._SettingUpBoard()

	def _LoadIkarusShopOffersBoard(self):
		self._LoadIkarusShopListBoard()
		ApplyListFrame(self, OFFLINESHOP_UI_PATH + "offer_list/bg.png", (5, 28), (166, 432), (83, 70))
		self.offerTab = "incoming"
		self.tabButtons = {}
		for (i, (name, text)) in enumerate((("incoming", locale.IKASHOP_OFFER_TAB_INCOMING_SHORT), ("outgoing", locale.IKASHOP_OFFER_TAB_OUTGOING_SHORT))):
			tab = self.CreateWidget(ui.RadioButton, pos = (7 + i * 81, 30))
			tab.SetUpVisual(OFFLINESHOP_UI_PATH + "offer_list/btn_tab.png")
			tab.SetOverVisual(OFFLINESHOP_UI_PATH + "offer_list/btn_tab_clicked.png")
			tab.SetDownVisual(OFFLINESHOP_UI_PATH + "offer_list/btn_tab_active.png")
			tab.SetText(text)
			tab.SAFE_SetEvent(self._OnSelectTab, name)
			self.tabButtons[name] = tab
		self.offers = []
		self._MakeListElements(IkarusShopOfferView, self.OFFER_VIEW_COUNT)
		self._OnSelectTab("incoming")

	def _OnSelectTab(self, name):
		self.offerTab = name
		for (key, tab) in self.tabButtons.items():
			tab.Down() if key == name else tab.SetUp()
		incoming = name == "incoming"
		if self.lastOfferTab and self.lastOfferTab != name:
			self.offerScroll = 0
			self.elementScrollbar.pos = 0.0
		self.lastOfferTab = name
		self.SetElements([offer for offer in self.offers if bool(offer.get('incoming', True)) == incoming])

	def SetOffers(self, offers):
		self.offers = sorted(offers, key = lambda val : val['datetime'], reverse=True)
		self._OnSelectTab(self.offerTab)
		self.Show()
		self.SetTop()

	def Open(self):
		ikashop.SendOfferListRequest()

	def Close(self):
		self.Hide()
		ikashop.SendOffersListClose()

	if SEARCH_SHOP_RENEWAL:
		DOCKED_TO_SHOP = True
		OFFER_VIEW_COUNT = OFFER_VIEWS
		_LoadIkarusShopOffersBoardDefault = _LoadIkarusShopOffersBoard

		def _LoadIkarusShopOffersBoard(self):
			self._LoadIkarusShopOffersBoardDefault()
			self.boardBox.SetInsideRender(True)
			self.elementScrollbar.Hide()
			self.elementScrollbar = self.CreateWidget(SearchThinScrollBar, pos = (165, 62), show = False)
			self.elementScrollbar.SetScrollBarSize(398)
			self.elementScrollbar.SetScrollEvent(self._ScrollElements)
			self.offerScroll = 0
			self.offerPeek = self.CreateWidget(ui.Window, pos = (2, 34), size = (158, self.boardBox.GetHeight() - 37), parent = self.boardBox)
			self.offerPeek.SetInsideRender(True)
			self.offerPeek.SetMouseWheelEvent(self._MouseWheelScrollElements)
			for (i, view) in enumerate(self.views):
				view.SetParent(self.offerPeek)
				view.SetPosition(0, i * OFFER_VIEW_STEP)
				view.offersBoard = proxy(self)
				view.SetMouseWheelEvent(self._MouseWheelScrollElements)
				SearchSetWheelDeep(view, self._MouseWheelScrollElements)
				if app.ENABLE_CLIP_MASKING:
					view.SetClippingMaskWindow(self.offerPeek)

		def _RefreshElements(self):
			visible = self._OfferVisible()
			maxScroll = self._OfferMaxScroll()
			self.offerScroll = max(0, min(maxScroll, self.offerScroll))
			first = self.offerScroll / OFFER_VIEW_STEP
			for (i, view) in enumerate(self.views):
				index = first + i
				y = index * OFFER_VIEW_STEP - self.offerScroll
				if index < len(self.elements) and y < visible:
					view.Setup(self.elements[index])
					view.SetPosition(0, y)
					view.Show()
				else:
					view.Hide()
			self.elementScrollbar.UpdateScrollbarLenght(OFFER_VIEW_STEP * len(self.elements))
			if app.ENABLE_CLIP_MASKING:
				return
			for view in self.views:
				(x, y) = view.GetLocalPosition()
				item.SelectItem(view.itemData['vnum']) if view.itemData else None
				size = max(1, min(3, item.GetItemSize()[1])) if view.itemData else 1
				view.slot.Show() if y + 6 + 33 * size <= self.boardBox.GetHeight() else view.slot.Hide()

		def _UpdateScrollbarState(self):
			if self._OfferMaxScroll() <= 0:
				self.offerScroll = 0
				self.elementScrollbar.pos = 0.0
				self.elementScrollbar.Hide()
			else:
				self.elementScrollbar.Show()

		def _OfferVisible(self):
			peek = self.offerPeek
			return peek.GetHeight() if peek else 392

		def _OfferMaxScroll(self):
			return max(0, OFFER_VIEW_STEP * len(self.elements) - self._OfferVisible())

		def _ScrollElements(self):
			self.offerScroll = int(self.elementScrollbar.GetPos() * self._OfferMaxScroll())
			self._RefreshElements()

		def _MouseWheelScrollElements(self, delta):
			maxScroll = self._OfferMaxScroll()
			if maxScroll > 0:
				self.offerScroll = max(0, min(maxScroll, self.offerScroll + (-OFFER_WHEEL_STEP if delta > 0 else OFFER_WHEEL_STEP)))
				self.elementScrollbar.pos = float(self.offerScroll) / maxScroll
				self.elementScrollbar._Refresh()
				self._RefreshElements()
			return True

if app.EXTEND_IKASHOP_PRO:
	class IkarusShopNotificationView(IkarusShopWindow):


		def __init__(self):
			super(IkarusShopNotificationView, self).__init__()
			self._LoadIkarusShopNotificationView()

		def _LoadIkarusShopNotificationView(self):
			self.background = self.CreateWidget(ui.ImageBox)
			self.background.LoadImage("ikashop/pro/notification/notification_box.png")
			self.SetSize(self.background.GetWidth(), self.background.GetHeight())

			# making what
			self.whatText = self.CreateWidget(ui.TextLine, pos = (9, 5))
			self.whatText.SetPackedFontColor(0xFFFFFFFF)

			# making datetime
			self.datetimeText = self.CreateWidget(ui.TextLine, pos = (405-11, 5))
			self.datetimeText.SetPackedFontColor(0xFFFFFFFF)
			self.datetimeText.SetHorizontalAlignCenter()

		def Setup(self, data):
			def GetItemName(what):
				if what == 0:
					return ""
				item.SelectItem(what)
				return item.GetItemName()

			def extractPriceString(format):
				if ENABLE_CHEQUE_SYSTEM:
					s = format.split("|")
					money = long(s[0])
					cheque = long(s[1]) if len(s) > 1 else 0
					price = ""
					if money != 0:
						price += locale.NumberToMoneyString(money)
					if cheque != 0:
						if price:
							price += ', '
						price += locale.NumberToCheque(cheque)
					return price
				return locale.NumberToMoneyString(long(format))

			self.data = data
			itemname = GetItemName(data['what'])
			if data['type'] == ikashop.NOTIFICATION_SELLER_SELLER_SOLD_ITEM:
				price = extractPriceString(data['format'])
				message = locale.IKASHOP_PRO_NOTIFICATION_SELLER_SOLD_ITEM.format(itemname, price)
				self.whatText.SetText(message)
			elif data['type'] == ikashop.NOTIFICATION_SELLER_NEW_OFFER_ON_ITEM:
				message = locale.IKASHOP_PRO_NOTIFICATION_SELLER_NEW_OFFER_ON_ITEM.format(itemname)
				self.whatText.SetText(message)
			elif data['type'] == ikashop.NOTIFICATION_SELLER_SHOP_EXPIRED:
				message = locale.IKASHOP_PRO_NOTIFICATION_SELLER_SHOP_EXPIRED
				self.whatText.SetText(message)
			elif data['type'] == ikashop.NOTIFICATION_SELLER_ITEM_EXPIRED:
				message = locale.IKASHOP_PRO_NOTIFICATION_SELLER_ITEM_EXPIRED.format(itemname)
				self.whatText.SetText(message)
			elif data['type'] == ikashop.NOTIFICATION_SELLER_AUCTION_NEW_OFFER:
				message = locale.IKASHOP_PRO_NOTIFICATION_SELLER_AUCTION_NEW_OFFER.format(itemname)
				self.whatText.SetText(message)
			elif data['type'] == ikashop.NOTIFICATION_SELLER_AUCTION_EXPIRED:
				message = locale.IKASHOP_PRO_NOTIFICATION_SELLER_AUCTION_EXPIRED.format(itemname)
				self.whatText.SetText(message)
			elif data['type'] == ikashop.NOTIFICATION_SELLER_AUCTION_SOLD:
				price = long(data['format'])
				message = locale.IKASHOP_PRO_NOTIFICATION_SELLER_AUCTION_SOLD.format(itemname, data['who'], locale.NumberToMoneyString(price))
				self.whatText.SetText(message)
			elif data['type'] == ikashop.NOTIFICATION_SELLER_OFFER_CANCELLED:
				message = locale.IKASHOP_PRO_NOTIFICATION_SELLER_OFFER_CANCELLED.format(itemname)
				self.whatText.SetText(message)
			elif data['type'] == ikashop.NOTIFICATION_BUYER_OFFER_DENIED:
				price = long(data['format'])
				message = locale.IKASHOP_PRO_NOTIFICATION_BUYER_OFFER_DENIED.format(locale.NumberToMoneyString(price), itemname)
				self.whatText.SetText(message)
			elif data['type'] == ikashop.NOTIFICATION_BUYER_OFFER_ACCEPTED:
				price = long(data['format'])
				message = locale.IKASHOP_PRO_NOTIFICATION_BUYER_OFFER_ACCEPTED.format(locale.NumberToMoneyString(price), itemname)
				self.whatText.SetText(message)
			elif data['type'] == ikashop.NOTIFICATION_BUYER_OFFER_EXPIRED:
				price = long(data['format'])
				message = locale.IKASHOP_PRO_NOTIFICATION_BUYER_OFFER_EXPIRED.format(locale.NumberToMoneyString(price), itemname)
				self.whatText.SetText(message)
			elif data['type'] == ikashop.NOTIFICATION_BUYER_AUCTION_BUY:
				price = long(data['format'])
				message = locale.IKASHOP_PRO_NOTIFICATION_BUYER_AUCTION_BUY.format(itemname, locale.NumberToMoneyString(price))
				self.whatText.SetText(message)
			elif data['type'] == ikashop.NOTIFICATION_BUYER_AUCTION_RAISE:
				message = locale.IKASHOP_PRO_NOTIFICATION_BUYER_AUCTION_RAISE.format(data['who'], itemname)
				self.whatText.SetText(message)
			elif data['type'] == ikashop.NOTIFICATION_BUYER_AUCTION_LOST:
				price = long(data['format'])
				message = locale.IKASHOP_PRO_NOTIFICATION_BUYER_AUCTION_LOST.format(data['who'], itemname, locale.NumberToMoneyString(price))
				self.whatText.SetText(message)

			if app.EXTEND_IKASHOP_ULTIMATE:
				if data['type'] == ikashop.NOTIFICATION_SELLER_DECORATION_EXPIRED:
					self.whatText.SetText(locale.IKASHOP_ULTIMATE_NOTIFICATION_SELLER_DECORATION_EXPIRED)

			self.datetimeText.SetText(DatetimeFormat(data['datetime']))
			self.ShowExclamationMark() if not data['seen']\
				else self.HideExclamationMark()


	class IkarusShopNotificationBoard(IkarusShopListBoard):

		NOTIFICATION_VIEW_COUNT = 10

		def __init__(self):
			super(IkarusShopNotificationBoard, self).__init__()
			ikashop.LoadNotifications()
			self._SettingUpBoard()
			self._LoadIkarusShopNotificationBoard()

		def _SettingUpBoard(self):
			self.SetSize(177, 387)
			self.SetTitleName(locale.IKASHOP_PRO_NOTIFICATION_BOARD_TITLE)
			super(IkarusShopNotificationBoard, self)._SettingUpBoard()

		def _LoadIkarusShopNotificationBoard(self):
			self._LoadIkarusShopListBoard()
			ApplyListFrame(self, OFFLINESHOP_UI_PATH + "notification/bg.png", (5, 25), (166, 354), (89, 213))
			self.headerBg = self.CreateWidget(ui.ImageBox, pos = (7, 27))
			self.headerBg.LoadImage(OFFLINESHOP_UI_PATH + "notification/header.png")
			self.headerText = self.CreateWidget(ui.TextLine, pos = (81, 10), parent = self.headerBg)
			self.headerText.SetHorizontalAlignCenter()
			self.headerText.SetVerticalAlignCenter()
			self.headerText.SetText(locale.IKASHOP_LAST_NOTIFICATIONS)
			self.emptyHeader.SetText(locale.IKASHOP_PRO_NOTIFICATION_BOARD_EMPTY)
			self._MakeListElements(IkarusShopNotificationView, self.NOTIFICATION_VIEW_COUNT)

		def SetNotifications(self, notifications):
			cached = ikashop.GetNotifications()
			for i, notification in enumerate(notifications):
				type = notification['type']
				who = notification['who']
				what = notification['what']
				format = notification['format']
				datetime = notification['datetime']
				save = i == len(notifications)-1
				ikashop.RegisterNotification(type, who, what, format, datetime, save)
			notifications = cached + notifications
			self.notifications = sorted(notifications, key = lambda val : val['datetime'], reverse=True)
			self.SetElements(self.notifications)
			self.Show()
			self.SetTop()

		def Open(self):
			ikashop.SendNotificationListRequest()

		def Close(self):
			self.Hide()
			ikashop.SendNotificationListClose()

		if SEARCH_SHOP_RENEWAL and app.EXTEND_IKASHOP_PRO:
			DOCKED_TO_SHOP = True
			_LoadIkarusShopNotificationBoardDefault = _LoadIkarusShopNotificationBoard

			def _LoadIkarusShopNotificationBoard(self):
				self._LoadIkarusShopNotificationBoardDefault()
				for view in self.views:
					SelfDestroyObject(view)
				self.listWindow = self.CreateWidget(ui.Window, pos = self.boardBox.GetLocalPosition(), size = (166, NOTIF_LIST_HEIGHT))
				self.listWindow.SetMouseWheelEvent(self._MouseWheelScrollElements)
				self.elementScrollbar.Hide()
				self.elementScrollbar = self.CreateWidget(SearchThinScrollBar, pos = (165, 50), show = False)
				self.elementScrollbar.SetScrollBarSize(326)
				self.openedKey = None
				self.rowOffset = 0
				self.views = []
				for i in xrange(NOTIF_VIEWS):
					view = self.CreateWidget(IkarusShopNotificationAccordionView, parent = self.listWindow, show = False)
					view.toggleEvent = ui.__mem_func__(self._NotifToggle)
					view.SetMouseWheelEvent(self._MouseWheelScrollElements)
					SearchSetWheelDeep(view, self._MouseWheelScrollElements)
					if app.ENABLE_CLIP_MASKING:
						view.SetClippingMaskWindow(self.listWindow)
					self.views.append(view)

			def _NotifToggle(self, data):
				key = _Notif_Key(data)
				self.openedKey = None if self.openedKey == key else key
				data['seen'] = True
				self._RefreshElements()

			def SetElements(self, elements):
				self.elements = elements
				self.rowOffset = 0
				self._RefreshElements()
				self.emptyHeader.Show() if not elements else self.emptyHeader.Hide()

			def _RefreshElements(self):
				elements = self.elements
				self.rowOffset = max(0, min(self.rowOffset, max(0, len(elements) - 1)))
				visible = NOTIF_LIST_HEIGHT
				y = 24
				for view in self.views:
					view.Hide()
				index = 0
				for i in xrange(self.rowOffset, len(elements)):
					if index >= len(self.views) or y >= visible:
						break
					data = elements[i]
					view = self.views[index]
					opened = _Notif_Key(data) == self.openedKey
					view.Setup(data, opened)
					view.SetPosition(2, y)
					view.Show()
					y += view.GetFullHeight(opened)
					index += 1
				total = len(elements)
				if total > 1:
					self.elementScrollbar.UpdateScrollbarLenght(total * NOTIF_ROW_STEP)
					self.elementScrollbar.pos = float(self.rowOffset) / max(1, total - 1)
					self.elementScrollbar._Refresh()
					self.elementScrollbar.Show() if total * NOTIF_ROW_STEP > visible - 24 else self.elementScrollbar.Hide()
				else:
					self.elementScrollbar.Hide()

			def _MouseWheelScrollElements(self, delta):
				self.rowOffset += -1 if delta > 0 else 1
				self._RefreshElements()
				return True

class IkarusShopCounter(IkarusShopWindow):
	def __init__(self):
		super(IkarusShopCounter, self).__init__()
		self._LoadIkarusShopCounter()

	def _LoadIkarusShopCounter(self):
		self.background = self.CreateWidget(ui.ImageBox)
		self.background.LoadImage("ikashop/lite/business/counter.png")

		self.counter = self.CreateWidget(ui.TextLine)
		self.counter.SetOutline(1)
		self.counter.SetPackedFontColor(0xFFFFFFFF)
		self.counter.SetPosition(self.background.GetWidth()/2, self.background.GetHeight()/2 - 1)
		self.counter.SetHorizontalAlignCenter()
		self.counter.SetVerticalAlignCenter()

	def SetCounter(self, count):
		if count == 0:
			self.Hide()
		else:
			self.counter.SetText(str(count) if count <= 9 else "9+")
			self.Show()

class IkarusShopBusinessBoard(IkashopBoardWithTitleBar):

	GRID_COLUMNS = ikashop.SHOP_GRID_WIDTH
	GRID_ROWS = ikashop.SHOP_GRID_HEIGHT
	PAGE_SIZE = GRID_COLUMNS * GRID_ROWS

	if app.EXTEND_IKASHOP_ULTIMATE:
		PAGE_COUNT = 4

	def __init__(self):
		self.insertingPriceInfo = None
		self.sortMoves = None
		self.moneyInputDialog = None
		self.notificationBoard = None
		self.createAuctionDialog = None
		self.lockToolTip = None
		self.lockedCells = []
		self.shopInfo = {}
		super(IkarusShopBusinessBoard, self).__init__()
		if app.EXTEND_IKASHOP_ULTIMATE:
			self.selectedPage = 0
		if app.EXTEND_IKASHOP_PRO:
			self.editedMarkedInfo = None
			self.editedMarkedTime = None
			self.editedMarkedColor = None
			self.removingItemList = []
		self._SettingUpBoard()
		self._LoadLinkedBoards()
		self._LoadShopBusinessWindow()
		ikashop.SetBusinessBoard(self)

	def __del__(self):
		super(IkarusShopBusinessBoard, self).__del__()
		ikashop.SetBusinessBoard(None)

	def _SettingUpBoard(self):
		self.SetSize(177, 468)
		self.SetTitleName(locale.IKASHOP_BUSINESS_BOARD_TITLE)
		self.SetCloseEvent(self.Close)
		self.SetCenterPosition()
		self.AddFlag("movable")
		self.AddFlag("float")

	def _LoadShopBusinessWindow(self):
		P = OFFLINESHOP_UI_PATH

		def Btn(pos, name, tooltip, event, *args):
			btn = self.CreateWidget(ui.Button, pos = pos)
			btn.SetUpVisual(P + name + ".png")
			btn.SetOverVisual(P + name + "_hover.png")
			btn.SetDownVisual(P + name + "_clicked.png")
			if tooltip:
				btn.SetToolTipText(tooltip)
				btn.ToolTipText.SetOutline(1)
			btn.SAFE_SetEvent(event, *args)
			return btn

		def Box(pos, image):
			box = self.CreateWidget(ui.ImageBox, pos = pos)
			box.LoadImage(P + image)
			return box

		# title bar "sort" button (6,5) 38x24
		self.sortShopButton = self.CreateWidget(ui.Button, pos = (6, 5))
		self.sortShopButton.SetUpVisual(TITLEBAR_REFRESH_IMG % "norm")
		self.sortShopButton.SetOverVisual(TITLEBAR_REFRESH_IMG % "hover")
		self.sortShopButton.SetDownVisual(TITLEBAR_REFRESH_IMG % "down")
		self.sortShopButton.SetToolTipText(locale.IKASHOP_BUSINESS_SORT_SHOP_BUTTON_TEXT)
		self.sortShopButton.ToolTipText.SetOutline(1)
		self.sortShopButton.SAFE_SetEvent(self._OnClickSortShopButton)

		# action buttons row (6,28) 166x35, buttons 28x25 at y 33
		self.actionButtonsBackground = Box((6, 28), "bg_btns.png")
		if app.EXTEND_IKASHOP_PRO:
			self.moveShopButton = Btn((11, 33), "btn_tp", locale.IKASHOP_PRO_BUSINESS_MOVE_SHOP_BUTTON_TEXT, self._OnClickMoveShopButton)
		self.safeboxOpenButton = Btn((43, 33), "btn_chest", locale.IKASHOP_BUSINESS_SAFEBOX_OPEN_BUTTON_TEXT, self._ToggleLinkedBoard, self.safeboxBoard)
		if app.EXTEND_IKASHOP_PRO:
			self.notificationOpenButton = Btn((75, 33), "btn_notif", locale.IKASHOP_PRO_BUSINESS_NOTIFICATION_OPEN_BUTTON_TEXT, self._ToggleLinkedBoard, self.notificationBoard)
		self.privateOfferOpenButton = Btn((107, 33), "btn_offer", locale.IKASHOP_BUSINESS_PRIVATE_OFFER_OPEN_BUTTON_TEXT, self._ToggleLinkedBoard, self.offersBoard)
		self.cancelShopButton = Btn((139, 33), "btn_closeshop", locale.IKASHOP_BUSINESS_CANCEL_SHOP_BUTTON_TEXT, self._OnClickCancelShopButton)
		self.auctionOpenButton = self.CreateWidget(ui.Button, pos = (139, 33), show = False)
		self.auctionOpenButton.SAFE_SetEvent(self._ToggleLinkedBoard, self.auctionBoard)

		# counters (button + 15, -5)
		self.safeboxItemCounter = self.CreateWidget(IkarusShopCounter, pos = (58, 28))
		self.privateOfferCounter = self.CreateWidget(IkarusShopCounter, pos = (122, 28))
		self.auctionOfferCounter = self.CreateWidget(IkarusShopCounter, pos = (154, 28), show = False)
		if app.EXTEND_IKASHOP_PRO:
			self.notificationCounter = self.CreateWidget(IkarusShopCounter, pos = (90, 28))

		# grid (6,65) 166x294, 5 x 9 slots at (9,68)
		self.slotBox = Box((6, 65), "bg_grid.png")
		if app.EXTEND_IKASHOP_ULTIMATE:
			self.slotBox.SetMouseWheelEvent(self._OnScrollMouseWheel)
		self.slotWindow = self.CreateWidget(ui.GridSlotWindow, parent = self.slotBox, pos = (3, 3))
		self.slotWindow.ArrangeSlot(0, self.GRID_COLUMNS, self.GRID_ROWS, SLOT_SIZE, SLOT_SIZE, 0, 0)
		self.slotWindow.SetSlotBaseImage(SLOT_BASE_IMG, 1.0, 1.0, 1.0, 1.0)
		self.slotWindow.SetSelectEmptySlotEvent(self._OnClickEmptySlot)
		self.slotWindow.SetSelectItemSlotEvent(self._OnClickItemSlot)
		self.slotWindow.SetOverInItemEvent(self._ShowToolTipOnItemSlot)
		self.slotWindow.SetOverOutItemEvent(self._HideToolTipOnItemSlot)
		self.slotWindow.SetUnselectItemSlotEvent(self._OnRightClickItemSlot)

		if app.EXTEND_IKASHOP_ULTIMATE:
			self.lockedCells = []
			for i in xrange(self.PAGE_SIZE):
				col, row = i % self.GRID_COLUMNS, i // self.GRID_COLUMNS
				lock = self.CreateWidget(ui.ImageBox, pos = (3 + 32*col, 3 + 32*row), parent = self.slotBox, show = 0)
				lock.LoadImage("ikashop/ultimate/lock_slot.png")
				self.lockedCells.append(lock)

			# page buttons (6,361) 166x24, buttons 39x20 at (10 + 40*i, 363)
			self.pageButtonsBackground = Box((6, 361), "bg_pagenumber.png")
			self.selectPageButtons = []
			for i in xrange(self.PAGE_COUNT):
				selectPageButton = self.CreateWidget(ui.Button, pos = (10 + i*40, 363))
				selectPageButton.SetUpVisual(P + "btn_page.png")
				selectPageButton.SetOverVisual(P + "btn_page_hover.png")
				selectPageButton.SetDownVisual(P + "btn_page_clicked.png")
				selectPageButton.SetDisableVisual(P + "btn_page_active.png")
				selectPageButton.SetText(RomeNumber(i+1))
				selectPageButton.SAFE_SetEvent(self._OnSelectPage, i)
				self.selectPageButtons.append(selectPageButton)

			self.decorationBox = self.CreateWidget(ui.Window, pos = (0, 0), show = False)
			self.decorationTime = self.CreateWidget(ui.TextLine, pos = (372, 42), show = False)

		# total (6,387): "Toplam" left (38) / sum right aligned (166)
		self.totalYangBox = Box((6, 387), "bg_totalyang.png")
		self.totalYangLabel = self.CreateWidget(ui.TextLine, pos = (38, 398))
		self.totalYangLabel.SetVerticalAlignCenter()
		self.totalYangLabel.SetPackedFontColor(0xFFCABDAB)
		self.totalYangLabel.SetText(locale.IKASHOP_BUSINESS_TOTAL_LABEL)
		self.totalYangText = self.CreateWidget(ui.TextLine, pos = (166, 398))
		self.totalYangText.SetHorizontalAlignRight()
		self.totalYangText.SetVerticalAlignCenter()
		self.totalYangText.SetPackedFontColor(0xFFC79E65)
		self.totalYangText.SetText(locale.NumberToMoneyString(0))

		# duration (6,412) + refresh duration (149,412)
		self.durationBox = Box((6, 412), "timerbg.png")
		self.durationText = self.CreateWidget(ui.TextLine, pos = (41, 424))
		self.durationText.SetVerticalAlignCenter()
		self.durationText.SetPackedFontColor(0xFFFFFFFF)
		self.durationExpiredIcon = self.CreateWidget(ui.Window, pos = (0, 0), show = False)
		self.durationIncreaseButton = Btn((149, 412), "btn_timer", None, self._OnClickDurationIncreaseButton)
		self.durationIncreaseButton.SetToolTipText(locale.IKASHOP_BUSINESS_DURATION_INCREASE_BUTTON_TEXT)
		self.durationIncreaseButton.ToolTipText.SetOutline(1)

		# shop safebox money (6,437) + claim (149,437)
		self.claimYangBox = Box((6, 437), "yangsmth.png")
		self.claimYangText = self.CreateWidget(ui.TextLine, pos = (41, 449))
		self.claimYangText.SetVerticalAlignCenter()
		self.claimYangText.SetPackedFontColor(0xFFCABDAB)
		self.claimYangText.SetText(locale.NumberToMoneyString(0))
		self.claimYangButton = Btn((149, 437), "btn_check", locale.IKASHOP_SAFEBOX_CLAIM_MONEY_BUTTON_TEXT, self._OnClickClaimYangButton)
		self.safeboxBoard.SetMoneyEvent(self._OnSafeboxMoney)

	def OpenMoneyInputDialog(self, acceptEvent, denyEvent = None, value = 0, cheque = 0, nocheque = 0):
		if self.moneyInputDialog == None:
			self.moneyInputDialog = IkarusShopItemPriceDialog()
			self._RegisterDialog(self.moneyInputDialog)
		info = self.insertingPriceInfo
		if isinstance(info, dict):
			self.moneyInputDialog.SetItem(info['vnum'], info['count'], info.get('sockets'), info.get('attrs'))
		elif info:
			(dest, win, pos) = info
			self.moneyInputDialog.SetItem(player.GetItemIndex(win, pos), player.GetItemCount(win, pos),
				[player.GetItemMetinSocket(win, pos, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)],
				[player.GetItemAttribute(win, pos, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)])
		self.moneyInputDialog.SetAcceptEvent(acceptEvent)
		self.moneyInputDialog.SetCancelEvent(denyEvent if denyEvent else self.moneyInputDialog.SoftClose)
		offerOnly = isinstance(info, dict) and info.get('price', 1) <= 0
		if isinstance(info, dict) and value and value == info.get('price'):
			value = abs(ToNetPrice(value))
		self.moneyInputDialog.SetValue(value if value != 0 else "")
		self.moneyInputDialog.SetPriceAverage(-1)
		self.moneyInputDialog.Open()
		self.moneyInputDialog.SetOfferOnly(offerOnly)
		if app.EXTEND_IKASHOP_ULTIMATE and self.moneyInputDialog.vnum:
			ikashop.SendPriceAverageRequest(self.moneyInputDialog.vnum, self.moneyInputDialog.count)

	def _ToggleLinkedBoard(self, board):
		if board.IsShow():
			board.Close()
			return
		self._PlaceLinkedBoard(board)
		board.Open()

	def _PlaceLinkedBoard(self, board):
		(x, y) = self.GetGlobalPosition()
		board.SetPosition(x - board.GetWidth() - LINKED_BOARD_GAP, y)

	def OnMoveWindow(self, x, y):
		for board in (self.safeboxBoard, self.offersBoard, self.auctionBoard, self.notificationBoard):
			if board and board.IsShow():
				self._PlaceLinkedBoard(board)

	def _RefreshTotal(self):
		total = sum(max(0, it.get('price', 0)) for it in self.shopInfo.get('items', {}).values())
		self.totalYangText.SetText(locale.NumberToMoneyString(total))

	def _OnSafeboxMoney(self, yang):
		self.claimYangText.SetText(locale.NumberToMoneyString(yang))

	def _OnClickClaimYangButton(self):
		self.safeboxBoard.ClaimMoney()

	def _OnClickSortShopButton(self):
		self.OpenQuestionDialog(locale.IKASHOP_BUSINESS_SORT_SHOP_QUESTION, self._OnAcceptSortShop)

	def _OnAcceptSortShop(self):
		self.questionDialog.Hide()
		items = sorted(self.shopInfo.get('items', {}).values(), key = lambda it: (-GetItemHeight(it['vnum']), it['vnum'], it['cell']))
		placed = []
		moves = []
		for it in items:
			item.SelectItem(it['vnum'])
			cell = ikashop.GetFirstEmptyCell(item.GetItemSize()[1], placed)
			if cell == None:
				return
			placed.append((it['vnum'], cell))
			if cell != it['cell']:
				moves.append((it['cell'], cell))
		self.sortMoves = moves
		self._SendNextSortMove()

	def _SendNextSortMove(self):
		while self.sortMoves:
			(src, dst) = self.sortMoves.pop(0)
			cells = dict((it['cell'], it) for it in self.shopInfo.get('items', {}).values())
			if src in cells and dst not in cells:
				ikashop.SendShopMoveItem(src, dst)
				return

	def _LoadLinkedBoards(self):
		self.safeboxBoard = IkarusShopSafeboxBoard()
		self.auctionBoard = IkarusShopAuctionOwnerBoard()
		self.offersBoard = IkarusShopOffersBoard()
		if app.EXTEND_IKASHOP_PRO:
			self.notificationBoard = IkarusShopNotificationBoard()

	# HANDLING DURATION RESTORE PROCESS
	def _OnClickDurationIncreaseButton(self):
		# checking cash
		if player.GetElk() < RESTORE_DURATION_COST:
			self.OpenPopupDialog(locale.IKASHOP_BUSINESS_INCREASE_DURATION_NO_MONEY)
			return

		# opening question
		question = locale.IKASHOP_BUSINESS_INCREASE_DURATION_QUESTION.format(locale.NumberToMoneyString(RESTORE_DURATION_COST))
		self.OpenQuestionDialog(question, self._OnIncreaseDurationQuestionAccept)

	def _OnIncreaseDurationQuestionAccept(self):
		ikashop.SendShopCreate()
		self.questionDialog.Hide()

	# HANDLING INSERT ITEM PROCESS
	def _OnClickEmptySlot(self, slot):
		if app.EXTEND_IKASHOP_ULTIMATE:
			slot = self._LocalToGlobalSlot(slot)

		if mouse.mouseController.isAttached():
			attachedType = mouse.mouseController.GetAttachedType()
			attachedItemIndex = mouse.mouseController.GetAttachedItemIndex()
			attachedItemSlotPos = mouse.mouseController.GetAttachedSlotNumber()
			mouse.mouseController.DeattachObject()

			if app.EXTEND_IKASHOP_ULTIMATE:
				if attachedType == player.SLOT_TYPE_OFFLINESHOP:
					ikashop.SendShopMoveItem(attachedItemSlotPos, slot)
					return

			# validating attached item
			if attachedType in GetSellableSlotTypes():
				win, pos = player.SlotTypeToInvenType(attachedType), attachedItemSlotPos
				if player.ITEM_MONEY != attachedItemIndex:
					self.InsertItemInSlot(win, pos, slot)

	def InsertItemInSlot(self, win, pos, slot = None):
		# checking shop isn't expired
		if self.shopInfo['duration'] <= 0:
			self.OpenPopupDialog(locale.IKASHOP_BUSINESS_CANNOT_SELL_ITEM_EXPIRED_SHOP)
			return

		# checking item antiflags
		itemIndex = player.GetItemIndex(win, pos)
		itemCount = player.GetItemCount(win, pos)

		if itemIndex != 0:
			item.SelectItem(itemIndex)
			# checking item antifalg
			if item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
				self.OpenPopupDialog(locale.IKASHOP_BUSINESS_CANNOT_SELL_ITEM)
				return

			# autodetecting price
			if app.EXTEND_IKASHOP_PRO:
				itemHash = GetInventoryItemHash(win, pos)
				detectedPrice = ikashop.GetItemPriceCache(itemIndex, itemHash, itemCount)
				isFastCall = slot == None

			# autodetecting empty slot
			items = [(sitem['vnum'], sitem['cell']) for sitem in self.shopInfo['items'].values()]
			if slot == None:
				slot = ikashop.GetFirstEmptyCell(item.GetItemSize()[1], items)

				if slot == None:
					self.OpenPopupDialog(locale.IKASHOP_BUSINESS_CANNOT_SELL_ITEM_NO_SPACE)

			# checking shop space
			else:
				if app.EXTEND_IKASHOP_ULTIMATE:
					if not ikashop.CheckShopSpace(items, itemIndex, slot, self.shopInfo['lock']):
						return
				else:
					if not ikashop.CheckShopSpace(items, itemIndex, slot):
						return

			# caching inserting item info
			self.insertingPriceInfo = slot, win, pos

			if app.EXTEND_IKASHOP_PRO:
				if isFastCall and detectedPrice:
					price = detectedPrice['value'],
					if ENABLE_CHEQUE_SYSTEM:
						price += detectedPrice['cheque'],
					ikashop.SendAddItem(win, pos, slot, *ToMarketPrice(price))
					return

				# opening money input dialog
				kargs = detectedPrice if detectedPrice else {}
				self.priceCacheInfo = itemIndex, itemHash, itemCount
				self.OpenMoneyInputDialog(self._OnAcceptInsertingItemPrice, **kargs)

			else:
				self.OpenMoneyInputDialog(self._OnAcceptInsertingItemPrice)

			if app.EXTEND_IKASHOP_ULTIMATE:
				ikashop.SendPriceAverageRequest(itemIndex, itemCount)
				self.moneyInputDialog.SetPriceAverage(-1)

	def _OnAcceptInsertingItemPrice(self):
		self.moneyInputDialog.SoftClose()

		ok, price = ExtractInputPrice(self.moneyInputDialog)
		if not ok:
			self.OpenPopupDialog(locale.IKASHOP_BUSINESS_INVALID_ITEM_PRICE)
			return

		# sending add item
		dest, win, slot = self.insertingPriceInfo
		ikashop.SendAddItem(win, slot, dest, *ToMarketPrice(price))
		if app.EXTEND_IKASHOP_PRO:
			vnum, hash, count = self.priceCacheInfo
			ikashop.RegisterItemPriceCache(vnum, hash, count, *price)
		return True

	# HANDLING EDIT PRICE/ REMOVE ITEM
	def _OnClickItemSlot(self, slot):
		if app.EXTEND_IKASHOP_ULTIMATE:
			if mouse.mouseController.isAttached():
				return
			slot = self._LocalToGlobalSlot(slot)

		if slot in self.shopInfo['items']:
			data = self.shopInfo['items'][slot]

			if IsPressingSHIFT():
				self.insertingPriceInfo = data
				if app.EXTEND_IKASHOP_PRO:
					self.insertingPriceAllSimilar = False
					detectPrice = ikashop.GetItemPriceCache(data['vnum'], data['hash'], data['count'])
					kargs = detectPrice if detectPrice else {}
					self.OpenMoneyInputDialog(self._OnAcceptEditingItemPrice, **kargs)
				else:
					self.OpenMoneyInputDialog(self._OnAcceptEditingItemPrice)
				if app.EXTEND_IKASHOP_ULTIMATE:
					self.moneyInputDialog.SetPriceAverage(data['priceavg'])
				return

			if app.EXTEND_IKASHOP_PRO:
				if IsPressingCTRL():
					self.insertingPriceInfo = data
					self.insertingPriceAllSimilar = True
					detectPrice = ikashop.GetItemPriceCache(data['vnum'], data['hash'], data['count'])
					kargs = detectPrice if detectPrice else {}
					self.OpenMoneyInputDialog(self._OnAcceptEditingItemPrice, **kargs)
					self.SetEditedMarkedSlotInfo(data['vnum'], data['count'], data['hash'], (0.7, 0.7, 0.7), infinite=1)
					if app.EXTEND_IKASHOP_ULTIMATE:
						self.moneyInputDialog.SetPriceAverage(data['priceavg'])
					return

			if app.EXTEND_IKASHOP_ULTIMATE:
				# attaching the item
				mouse.mouseController.AttachObject(self, player.SLOT_TYPE_OFFLINESHOP, slot, data['vnum'], data['count'])


	def _OnRightClickItemSlot(self, slot):
		if app.EXTEND_IKASHOP_ULTIMATE:
			slot = self._LocalToGlobalSlot(slot)
			if mouse.mouseController.isAttached():
				return

		if slot in self.shopInfo['items']:
			data = self.shopInfo['items'][slot]

			if app.EXTEND_IKASHOP_PRO:
				if IsPressingCTRL():
					self.removingVnum = data['vnum']
					item.SelectItem(self.removingVnum)
					question = locale.IKASHOP_PRO_BUSINESS_REMOVE_ALL_SIMILAR_ITEMS_QUESTION.format(item.GetItemName())
					self.OpenQuestionDialog(question, self._OnAcceptRemoveAllSimilarItems)

					# marking all removing items
					for slot, data in self.shopInfo['items'].items():
						if data['vnum'] == self.removingVnum:
							self.AppendRemovingItemSlot(slot)
					self._RefreshItems()
					return

			# starting edit item price process
			ikashop.SendRemoveItem(data['id'])

	def _OnAcceptRemoveAllSimilarItems(self):
		self.questionDialog.Hide()
		for item in self.shopInfo['items'].values():
			if item['vnum'] == self.removingVnum:
				ikashop.SendRemoveItem(item['id'])

	def _OnAcceptEditingItemPrice(self):
		self.moneyInputDialog.SoftClose()
		ok, price = ExtractInputPrice(self.moneyInputDialog)
		if not ok:
			self.OpenPopupDialog(locale.IKASHOP_BUSINESS_INVALID_ITEM_PRICE)
			return

		# sending edit item
		data = self.insertingPriceInfo

		if app.EXTEND_IKASHOP_PRO:
			ikashop.RegisterItemPriceCache(data['vnum'], data['hash'], data['count'], *price)
			price = ToMarketPrice(price)
			# editing all item prices
			if self.insertingPriceAllSimilar:
				for checkData in self.shopInfo['items'].values():
					if data['hash'] == checkData['hash'] and data['count'] == checkData['count'] and data['vnum'] == checkData['vnum']:
						if price[0] != checkData['price'] or (ENABLE_CHEQUE_SYSTEM and price[1] != checkData['cheque']):
							ikashop.SendEditItem(checkData['id'], *price)
				self.SetEditedMarkedSlotInfo(data['vnum'], data['count'], data['hash'], (0.5, 0.5, 0.1), price = price)
			else:
				ikashop.SendEditItem(data['id'], *price)

		else:
			ikashop.SendEditItem(data['id'], *price)

		return True

	# HANDLING TOOLTIP OVER IN OVER OUT
	def _ShowToolTipOnItemSlot(self, slot):
		if app.EXTEND_IKASHOP_ULTIMATE:
			slot = self._LocalToGlobalSlot(slot)

		if slot in self.shopInfo['items']:
			data = self.shopInfo['items'][slot]
			tooltip = self.GetToolTip()
			tooltip.ClearToolTip()
			rows = [(("mouse_left", "shift"), locale.IKASHOP_BUSINESS_SHORTCUT_EDIT)]
			if app.EXTEND_IKASHOP_PRO:
				rows.append((("mouse_left", "ctrl"), locale.IKASHOP_BUSINESS_SHORTCUT_EDIT_SIMILAR))
			rows.append((("mouse_right",), locale.IKASHOP_BUSINESS_SHORTCUT_REMOVE))
			if app.EXTEND_IKASHOP_PRO:
				rows.append((("mouse_right", "ctrl"), locale.IKASHOP_BUSINESS_SHORTCUT_REMOVE_SIMILAR))
			measure = ui.TextLine()
			measure.SetFontName(tooltip.defFontName)
			textWidth = 0
			for (keys, text) in rows:
				measure.SetText(text)
				textWidth = max(textWidth, measure.GetTextSize()[0])
			tooltip.toolTipWidth = max(310, 175 + textWidth)
			tooltip.ResizeToolTip()
			tooltip.AddItemData(data['vnum'], data['sockets'], data['attrs'])
			if data.get('price', 0) <= 0:
				tooltip.AppendTextLine(locale.IKASHOP_OFFER_ONLY, tooltip.SPECIAL_TITLE_COLOR)
			if data.get('price', 0) != 0:
				tooltip.AppendPrice(abs(data['price']))
			if app.EXTEND_IKASHOP_ULTIMATE:
				tooltip.AppendTextLine(locale.IKASHOP_ULTIMATE_PRICE_AVERAGE_NOT_AVAILABLE if data.get('priceavg', 0) == 0 					else locale.IKASHOP_ULTIMATE_PRICE_AVERAGE_VALUE.format(locale.NumberToMoneyString(data['priceavg'])))
			tooltip.AppendShortcutTable(rows)
			tooltip.ResizeToolTip()
			tooltip.ShowToolTip()

	def _HideToolTipOnItemSlot(self, slot=0):
		tooltip = self.GetToolTip()
		tooltip.ClearToolTip()
		tooltip.HideToolTip()

	# HANDLING CANCEL SHOP REQUEST
	def _OnClickCancelShopButton(self):
		self.OpenQuestionDialog(locale.IKASHOP_BUSINESS_CANCEL_SHOP_QUESTION, self._OnAcceptCancelShopQuestion)

	def _OnAcceptCancelShopQuestion(self):
		self.questionDialog.Hide()
		ikashop.SendForceCloseShop()

	if app.EXTEND_IKASHOP_PRO:
		# HANDLING MOVE SHOP REQUEST
		def _OnClickMoveShopButton(self):
			# checking money
			if player.GetElk() < MOVE_SHOP_ENTITY_COST:
				self.OpenPopupDialog(locale.IKASHOP_PRO_BUSINESS_MOVE_SHOP_NO_MONEY)
				return
			# sending question
			message = locale.IKASHOP_PRO_BUSINESS_MOVE_SHOP_QUESTION.format(locale.NumberToMoneyString(MOVE_SHOP_ENTITY_COST))
			self.OpenQuestionDialog(message, self._OnAcceptMoveShopQuestion)

		def _OnAcceptMoveShopQuestion(self):
			self.questionDialog.Hide()
			ikashop.SendMoveShopEntity()

	# HANDLING AUCTION CREATION
	def _OnAcceptCreateAuctionQuestion(self):
		self.questionDialog.Hide()

		if not self.createAuctionDialog:
			self.createAuctionDialog = IkarusCreateAuctionDialog()
			self._RegisterDialog(self.createAuctionDialog)

		self.createAuctionDialog.Open()

	if app.EXTEND_IKASHOP_ULTIMATE:
		def _LocalToGlobalSlot(self, pos):
			return self.selectedPage * self.PAGE_SIZE + pos

		def _GlobalToLocalSlot(self, pos):
			return pos % self.PAGE_SIZE

	def _RefreshItems(self):
		# resetting slots
		for i in xrange(self.GRID_COLUMNS*self.GRID_ROWS):
			self.slotWindow.ClearSlot(i)
			if app.EXTEND_IKASHOP_PRO:
				self.slotWindow.DeactivateSlot(i)

		if app.EXTEND_IKASHOP_ULTIMATE:
			for i in xrange(self.PAGE_SIZE):
				self.lockedCells[i].Hide()

			scell = self.PAGE_SIZE * self.selectedPage
			ecell = scell + self.PAGE_SIZE

			for cell in xrange(scell, ecell):
				if cell >= self.shopInfo['lock']:
					self.lockedCells[self._GlobalToLocalSlot(cell)].Show()

			for cell in xrange(scell, ecell):
				if cell in self.shopInfo['items']:
					item = self.shopInfo['items'][cell]
					pos = self._GlobalToLocalSlot(cell)
					self.slotWindow.SetItemSlot(pos, item['vnum'], item['count'] if item['count'] > 1 else 0)

		else:
			# setting up slots
			for item in self.shopInfo['items'].values():
				self.slotWindow.SetItemSlot(item['cell'], item['vnum'], item['count'] if item['count'] > 1 else 0)

		if app.EXTEND_IKASHOP_PRO:
			self._RefreshMarkedSlots()

		self.slotWindow.RefreshSlot()


	if app.EXTEND_IKASHOP_PRO:
		def _RefreshMarkedSlots(self):
			# marking edited items
			actualTime = app.GetTime()
			if self.editedMarkedInfo != None and self.editedMarkedTime != None:
				if self.editedMarkedTime > actualTime or self.editedMarkedTime == -1:
					vnum, count, hash, price = self.editedMarkedInfo
					for i in xrange(self.PAGE_SIZE):
						slot = i
						if app.EXTEND_IKASHOP_ULTIMATE:
							slot = self._LocalToGlobalSlot(i)

						if slot in self.shopInfo['items']:
							data = self.shopInfo['items'][slot]
							if (data['vnum'], data['count'], data['hash']) == (vnum, count, hash):
								if ENABLE_CHEQUE_SYSTEM:
									itemPrice = (data['price'], data['cheque'])
								else:
									itemPrice = data['price'],
								if price is None or itemPrice == price:
									self.slotWindow.ActivateSlot(i, *self.editedMarkedColor)

			# marking removing items
			if app.EXTEND_IKASHOP_ULTIMATE:
				shownCellStart = self.selectedPage * self.PAGE_SIZE
				shownCellEnd = shownCellStart + self.PAGE_SIZE
				for slot in self.removingItemList:
					if slot >= shownCellStart and slot < shownCellEnd:
						local = self._GlobalToLocalSlot(slot)
						self.slotWindow.ActivateSlot(local, 0.5, 0.1, 0.1)

			else:
				for slot in self.removingItemList:
					self.slotWindow.ActivateSlot(slot, 0.5, 0.1, 0.1)


	# PUBLIC INTERFACE
	def Open(self):
		ikashop.SendOpenShopOwner()
		if app.EXTEND_IKASHOP_PRO:
			player.RefreshInventory()

	def Close(self):
		self.Hide()
		ikashop.SendCloseMyShopBoard()
		if app.EXTEND_IKASHOP_PRO:
			player.RefreshInventory()

	if app.EXTEND_IKASHOP_PRO:
		def AppendRemovingItemSlot(self, slot):
			if not slot in self.removingItemList:
				self.removingItemList.append(slot)

		def SetEditedMarkedSlotInfo(self, vnum, count, hash, color, infinite = 0, price = None):
			self.editedMarkedInfo = vnum, count, hash, price
			self.editedMarkedTime = app.GetTime() + 20.0 if not infinite else -1
			self.editedMarkedColor = color
			self._RefreshItems()

		def OnUpdate(self):
			if self.editedMarkedTime != None and self.editedMarkedTime != -1 and self.editedMarkedTime < app.GetTime():
				self.editedMarkedTime = None
				self.editedMarkedInfo = None
				self._RefreshItems()

			if self.editedMarkedInfo != None and self.editedMarkedTime == -1 and not self.moneyInputDialog.IsShow():
				self.editedMarkedTime = None
				self.editedMarkedInfo = None
				self._RefreshItems()

			if self.removingItemList:
				if not self.questionDialog.IsShow():
					self.removingItemList = []
					self._RefreshItems()

	def IsCreatingAuction(self):
		return self.createAuctionDialog and self.createAuctionDialog.IsShow()

	# BINARY CALLS
	def OpenShopOwner(self, data):
		# refreshing duration
		if data['duration'] > 0:
			self.durationText.SetText(locale.SecondToDHM(data['duration']*60))
			self.durationExpiredIcon.Hide()
			if not app.EXTEND_IKASHOP_ULTIMATE:
				self.durationIncreaseButton.Hide()
		else:
			self.durationText.SetText(locale.IKASHOP_BUSINESS_SHOP_EXPIRED_DURATION)
			self.durationExpiredIcon.Show()
			self.durationIncreaseButton.Show()

		if app.EXTEND_IKASHOP_ULTIMATE:
			self.decorationBox.Show() if data['decoration'] != 0\
				else self.decorationBox.Hide()
			self.decorationTime.SetText(locale.SecondToDHM(data['decoration_time']*60))


		data['items'] = { item['cell'] : item for item in data['items'] }
		self.shopInfo = data

		self._RefreshItems()
		self._RefreshTotal()

		if not self.IsShow():
			self.Show()
			self.SetTop()
			if app.EXTEND_IKASHOP_ULTIMATE:
				self._OnSelectPage(0)
			self.safeboxBoard.RequestMoney()

		# "Pazari Duzenle": next move once the server answered the previous one
		self._SendNextSortMove()

		if app.EXTEND_IKASHOP_PRO:
			player.RefreshInventory()

	def OpenShopOwnerEmpty(self):
		# refreshing duration
		self.durationText.SetText(locale.IKASHOP_BUSINESS_SHOP_EXPIRED_DURATION)
		self.durationExpiredIcon.Show()
		self.durationIncreaseButton.Show()

		if app.EXTEND_IKASHOP_ULTIMATE:
			self.decorationBox.Hide()

		# resetting slots
		for i in xrange(self.GRID_COLUMNS*self.GRID_ROWS):
			self.slotWindow.ClearSlot(i)
		self.slotWindow.RefreshSlot()

		# making shop info data
		self.shopInfo = {'duration' : 0, 'items' : {}}
		if app.EXTEND_IKASHOP_ULTIMATE:
			self.shopInfo['lock'] = ikashop.OFFSHOP_LOCK_INDEX_INIT
		self._RefreshTotal()

		if not self.IsShow():
			self.Show()
			self.SetTop()
			if app.EXTEND_IKASHOP_ULTIMATE:
				self._OnSelectPage(0)
			self.safeboxBoard.RequestMoney()

		if app.EXTEND_IKASHOP_PRO:
			player.RefreshInventory()

	def ShopOwnerRemoveItem(self, itemid):
		if 'items' in self.shopInfo:
			self.shopInfo['items'] = {cell:item for cell,item in self.shopInfo['items'].items() if item['id'] != itemid}
			self._RefreshItems()
			self._RefreshTotal()

	def ShopOwnerEditItem(self, itemid, prices):
		if 'items' in self.shopInfo:
			for data in self.shopInfo['items'].values():
				if data['id'] == itemid:
					data['price'] = prices['price']
					if prices.has_key('cheque'):
						data['cheque'] = prices['cheque']
					self._RefreshItems()
					self._RefreshTotal()
					break

	def SetupSafebox(self, yang, items):
		self.safeboxBoard.Setup(yang, items)

	def SafeboxRemoveItem(self, itemid):
		self.safeboxBoard.RemoveItem(itemid)

	def SafeboxAddItem(self, item):
		self.safeboxBoard.AddItem(item)

	def SetupAcutionOwner(self, data):
		self.auctionBoard.Setup(data)

	def OpenCreateAuctionQuestion(self):
		question = locale.IKASHOP_BUSINESS_NO_AUCTION_CREATE_AUCTION_QUESTION
		self.OpenQuestionDialog(question, self._OnAcceptCreateAuctionQuestion)

	def AuctionInsertItemInSlot(self, win, pos):
		self.createAuctionDialog.InsertItemInSlot(win, pos)

	def SetOffers(self, offers):
		self.offersBoard.SetOffers(offers)

	def SetSafeboxCounter(self, count):
		self.safeboxItemCounter.SetCounter(count)

	def SetAuctionCounter(self, count):
		self.auctionOfferCounter.SetCounter(count)

	def SetOffersCounter(self, count):
		self.privateOfferCounter.SetCounter(count)

	if app.EXTEND_IKASHOP_PRO:
		def SetNotificationCounter(self, count):
			self.notificationCounter.SetCounter(count)

		def SetNotifications(self, notifications):
			self.notificationBoard.SetNotifications(notifications)

	if app.EXTEND_IKASHOP_ULTIMATE:
		def SetPriceAverage(self, price, sales = ()):
			if SEARCH_SHOP_RENEWAL and SearchOnPriceAverage(price, sales):
				return
			if self.moneyInputDialog:
				if isinstance(self.moneyInputDialog, IkarusShopItemPriceDialog):
					self.moneyInputDialog.SetPriceAverage(price, sales)
				else:
					self.moneyInputDialog.SetPriceAverage(price)
			if self.createAuctionDialog:
				if self.createAuctionDialog.moneyInputDialog:
					self.createAuctionDialog.moneyInputDialog.SetPriceAverage(price)

		def _OnSelectPage(self, page):
			self.selectedPage = page
			for idx, button in enumerate(self.selectPageButtons):
				button.Disable() if idx == page else button.Enable()
			self._RefreshItems()

		def _OnScrollMouseWheel(self, delta):
			if delta > 0:
				if self.selectedPage > 0:
					self._OnSelectPage(self.selectedPage-1)
			else:
				if self.selectedPage + 1 < self.PAGE_COUNT:
					self._OnSelectPage(self.selectedPage+1)
			return True

	def ServerPopupMessage(self, message):
		if SEARCH_SHOP_RENEWAL and message == "IKASHOP_SERVER_POPUP_MESSAGE_SEARCH_COOLDOWN_STILL_ACTIVED" and SearchOnCooldownPopup():
			return
		message = locale.GetText(message, message)
		self.OpenPopupDialog(message)

	if SEARCH_SHOP_RENEWAL and app.EXTEND_IKASHOP_ULTIMATE:
		_LoadShopBusinessWindowDefault = _LoadShopBusinessWindow

		def _LoadShopBusinessWindow(self):
			self._LoadShopBusinessWindowDefault()
			for lock in self.lockedCells:
				lock.SetOverInEvent(ui.__mem_func__(self._ShowLockToolTip))
				lock.SetOverOutEvent(ui.__mem_func__(self._HideLockToolTip))

		def _ShowLockToolTip(self):
			tip = self.lockToolTip
			if not tip:
				tip = self.lockToolTip = uitooltip.ToolTip(170)
			tip.ClearToolTip()
			item.SelectItem(SHOP_KEY_VNUM)
			icon = ui.ImageBox()
			icon.SetParent(tip)
			icon.LoadImage(item.GetIconImageFileName())
			icon.SetPosition(8, 10)
			icon.AddFlag("not_pick")
			icon.Show()
			tip.childrenList.append(icon)
			have = player.GetItemCountByVnum(SHOP_KEY_VNUM)
			left = max(0, self.PAGE_COUNT * self.PAGE_SIZE - self.shopInfo.get('lock', 0))
			for (y, text, color) in ((21, item.GetItemName(), LOCK_TIP_NAME_COLOR),
					(40, SearchLocale("IKASHOP_LOCK_TIP_REQUIRED").format(1), LOCK_TIP_TEXT_COLOR),
					(55, SearchLocale("IKASHOP_LOCK_TIP_HAVE").format(have), LOCK_TIP_MISSING_COLOR if have < 1 else LOCK_TIP_TEXT_COLOR),
					(71, SearchLocale("IKASHOP_LOCK_TIP_LEFT").format(left), LOCK_TIP_TEXT_COLOR)):
				line = ui.TextLine()
				line.SetParent(tip)
				line.SetFontName(tip.defFontName)
				line.SetVerticalAlignCenter()
				line.SetPosition(51, y)
				line.SetPackedFontColor(color)
				line.SetText(text)
				line.SetOutline()
				line.Show()
				tip.childrenList.append(line)
			tip.toolTipHeight = 86 - tip.TOOL_TIP_HEIGHT
			tip.ResizeToolTip()
			tip.ShowToolTip()

		def _HideLockToolTip(self):
			if self.lockToolTip:
				self.lockToolTip.HideToolTip()

class IkarusShopGuestBoard(IkashopBoardWithTitleBar):

	GRID_COLUMNS = ikashop.SHOP_GRID_WIDTH
	GRID_ROWS = ikashop.SHOP_GRID_HEIGHT

	if app.EXTEND_IKASHOP_ULTIMATE:
		PAGE_COUNT = 4
		PAGE_SIZE = GRID_COLUMNS * GRID_ROWS

	def __init__(self):
		super(IkarusShopGuestBoard, self).__init__()
		if app.EXTEND_IKASHOP_ULTIMATE:
			self.selectedPage = 0
			self.lockImages = []
		self.markedInfo = None
		self._SettingUpBoard()
		self._LoadIkarusShopGuestBoard()

	def _SettingUpBoard(self):
		self.SetSize(508, 404)
		self.SetCloseEvent(self.Close)
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetCenterPosition()
		x,y = self.GetLocalPosition()
		self.SetPosition(x+100,y)

	def _LoadIkarusShopGuestBoard(self):
		# making slot box
		self.slotBox = self.CreateWidget(ui.ImageBox, pos = (5,35 + 27))
		self.slotBox.LoadImage("ikashop/lite/business/slot_box.png")
		if app.EXTEND_IKASHOP_ULTIMATE:
			self.slotBox.SetMouseWheelEvent(self._OnScrollMouseWheel)

		self.slotWindow = self.CreateWidget(ui.GridSlotWindow, parent = self.slotBox, pos = (6,6))
		self.slotWindow.ArrangeSlot(0, self.GRID_COLUMNS, self.GRID_ROWS, SLOT_SIZE, SLOT_SIZE, 0, 0)
		self.slotWindow.SetSlotBaseImage("ikashop/lite/common/slot/default.png", 1.0, 1.0, 1.0, 1.0)
		self.slotWindow.SetSelectItemSlotEvent(self._OnClickItemSlot)
		self.slotWindow.SetOverInItemEvent(self._ShowToolTipOnItemSlot)
		self.slotWindow.SetOverOutItemEvent(self._HideToolTipOnItemSlot)

		# making duration box
		self.durationBox = self.CreateWidget(ui.ImageBox, pos = (5,35))
		self.durationBox.LoadImage("ikashop/lite/business/duration_box.png")

		self.durationText = self.CreateWidget(ui.TextLine, parent = self.durationBox, pos = (30, 4))
		self.durationText.SetPackedFontColor(0xFFFFFFFF)
		self.durationText.SetText("11d 22h 18m")

		if app.EXTEND_IKASHOP_ULTIMATE:
			self.lockedCells = []
			for i in xrange(self.PAGE_SIZE):
				col, row = i % self.GRID_COLUMNS, i // self.GRID_COLUMNS
				lock = self.CreateWidget(ui.ImageBox, pos = (6 + 32*col,6 + 32*row), parent = self.slotBox, show = 0)
				lock.LoadImage("ikashop/ultimate/lock_slot.png")
				self.lockedCells.append(lock)

			# making page selection box
			self.selectPageButtons = []
			for i in xrange(self.PAGE_COUNT):
				selectPageButton = self.CreateWidget(ui.Button, pos = (269 - 48 + i*41, 35))
				selectPageButton.SetUpVisual("ikashop/lite/safebox/buttons/select_page/default.png")
				selectPageButton.SetDownVisual("ikashop/lite/safebox/buttons/select_page/default.png")
				selectPageButton.SetOverVisual("ikashop/lite/safebox/buttons/select_page/hover.png")
				selectPageButton.SetDisableVisual("ikashop/lite/safebox/buttons/select_page/disabled.png")
				selectPageButton.SetText(RomeNumber(i+1))
				selectPageButton.SAFE_SetEvent(self._OnSelectPage, i)
				self.selectPageButtons.append(selectPageButton)

	def _OnClickItemSlot(self, slot):
		if app.EXTEND_IKASHOP_ULTIMATE:
			slot = self._LocalToGlobalSlot(slot)

		if slot in self.shopInfo['items']:
			data = self.shopInfo['items'][slot]

			# making item name
			item.SelectItem(data['vnum'])
			itemName = item.GetItemName()
			if data['count'] > 1:
				itemName += "({})".format(data['count'])

			# making item price
			if ENABLE_CHEQUE_SYSTEM:
				itemPrice = ""
				if data['price'] != 0:
					itemPrice += locale.NumberToMoneyString(data['price'])
				if data['cheque'] != 0:
					if itemPrice:
						itemPrice += ', '
					itemPrice += locale.NumberToCheque(data['cheque'])
			else:
				itemPrice = locale.NumberToMoneyString(data['price'])


			if app.EXTEND_IKASHOP_PRO:
				if IsPressingCTRL():
					item.SelectItem(data['vnum'])

					# making message
					message = locale.IKASHOP_PRO_SHOP_GUEST_BUY_ALL_ITEMS_QUESTION.format(itemName, itemPrice)
					self.buyAllInfo = data['vnum'], data['count'], data['price']
					self.OpenQuestionDialog(message, self._OnAcceptBuyAllQuestion)
					return

			if IsPressingSHIFT():
				# checking offer min price
				if 0 < data['price'] + data.get('cheque', 0) * YANG_PER_CHEQUE < 10000:
					self.OpenPopupDialog(locale.IKASHOP_SHOP_GUEST_MAKE_OFFER_ITEM_PRICE_TOO_LOW)
					return

				self.offerInfo = data['id'], data['price'], data.get('cheque', 0)
				self.OpenMoneyInputDialog(self._OnAcceptMakeOfferInput)
				if app.EXTEND_IKASHOP_ULTIMATE:
					self.moneyInputDialog.SetPriceAverage(data['priceavg'])
				return

			self.buyItemInfo = self.shopInfo['id'], data['id'], data['price'] + data.get('cheque', 0) * YANG_PER_CHEQUE
			message = locale.IKASHOP_SHOP_GUEST_BUY_ITEM_QUESTION.format(itemName, itemPrice)
			self.OpenQuestionDialog(message, self._OnAcceptBuyItemQuestion)

	if app.EXTEND_IKASHOP_PRO:
		def _OnAcceptBuyAllQuestion(self):
			self.questionDialog.Hide()
			for data in self.shopInfo['items'].values():
				if (data['vnum'], data['count'], data['price']) == self.buyAllInfo:
					ikashop.SendBuyItem(self.shopInfo['id'], data['id'], data['price'] + data.get('cheque', 0) * YANG_PER_CHEQUE)

	def _OnAcceptBuyItemQuestion(self):
		ikashop.SendBuyItem(*self.buyItemInfo)
		self.questionDialog.Hide()

	def _OnAcceptMakeOfferInput(self):
		self.moneyInputDialog.SoftClose()

		# validating value
		ok, value = ExtractInputPrice(self.moneyInputDialog)
		if not ok:
			self.OpenPopupDialog(locale.IKASHOP_BUSINESS_INVALID_ITEM_PRICE)
			return

		id, price, cheque = self.offerInfo

		if ENABLE_CHEQUE_SYSTEM:
			valueTotal = value[0] + value[1] * YANG_PER_CHEQUE
			priceTotal = price + cheque * YANG_PER_CHEQUE
			if valueTotal >= priceTotal:
				self.OpenPopupDialog(locale.IKASHOP_SHOP_GUEST_OFFER_MUST_BE_LOWER_THAN_PRICE)
				return True

			minoffer = priceTotal * MIN_OFFER_PCT / 100
			if valueTotal < minoffer:
				self.OpenPopupDialog(locale.IKASHOP_SHOP_GUEST_OFFER_MUST_BE_HIGHER_THAN_PCT_OF_PRICE.format(MIN_OFFER_PCT))
				return True

			# checking owned cash
			if value[0] > player.GetElk() or value[1] > player.GetCheque():
				self.OpenPopupDialog(locale.IKASHOP_SHOP_GUEST_OFFER_NOT_ENOUGH_MONEY)
				return True

		else:
			if price > 0 and value[0] >= price:
				self.OpenPopupDialog(locale.IKASHOP_SHOP_GUEST_OFFER_MUST_BE_LOWER_THAN_PRICE)
				return True

			minoffer = max(1, price * MIN_OFFER_PCT / 100)
			if value[0] < minoffer:
				self.OpenPopupDialog(locale.IKASHOP_SHOP_GUEST_OFFER_MUST_BE_HIGHER_THAN_PCT_OF_PRICE.format(MIN_OFFER_PCT))
				return True

			# checking owned cash
			if value[0] > player.GetElk():
				self.OpenPopupDialog(locale.IKASHOP_SHOP_GUEST_OFFER_NOT_ENOUGH_MONEY)
				return True

		ikashop.SendOfferCreate(self.shopInfo['id'], id, *value)
		return True

	def _ShowToolTipOnItemSlot(self, slot):
		if app.EXTEND_IKASHOP_ULTIMATE:
			slot = self._LocalToGlobalSlot(slot)

		if slot in self.shopInfo['items']:
			data = self.shopInfo['items'][slot]
			tooltip = self.GetToolTip()
			tooltip.ClearToolTip()
			if app.EXTEND_IKASHOP_PRO:
				tooltip.FitTextWidth(locale.IKASHOP_PRO_SHOP_GUEST_BUY_ALL_ITEM_TOOLTIP)
			tooltip.AddItemData(data['vnum'], data['sockets'], data['attrs'])
			if data.get('price', 0) <= 0:
				tooltip.AppendTextLine(locale.IKASHOP_OFFER_ONLY, tooltip.SPECIAL_TITLE_COLOR)
			if 'price' in data and data['price'] != 0:
				tooltip.AppendPrice(abs(data['price']))
			if 'cheque' in data and data['cheque'] != 0:
				tooltip.AppendCheque(data['cheque'])
			if app.EXTEND_IKASHOP_ULTIMATE:
				tooltip.AppendTextLine(locale.IKASHOP_ULTIMATE_PRICE_AVERAGE_NOT_AVAILABLE) if data['priceavg'] == 0 \
					else tooltip.AppendTextLine(locale.IKASHOP_ULTIMATE_PRICE_AVERAGE_VALUE.format(locale.NumberToMoneyString(data['priceavg'])))
			tooltip.AppendTextLine(locale.IKASHOP_SHOP_GUEST_BUY_ITEM_TOOLTIP)
			if app.EXTEND_IKASHOP_PRO:
				tooltip.AppendTextLine(locale.IKASHOP_PRO_SHOP_GUEST_BUY_ALL_ITEM_TOOLTIP)
			if not SEARCH_SHOP_RENEWAL:
				tooltip.AppendTextLine(locale.IKASHOP_SHOP_GUEST_OFFER_ITEM_TOOLTIP)
			tooltip.ShowToolTip()

	def _HideToolTipOnItemSlot(self, slot=0):
		tooltip = self.GetToolTip()
		tooltip.ClearToolTip()
		tooltip.HideToolTip()

	if app.EXTEND_IKASHOP_ULTIMATE:
		def _OnSelectPage(self, page):
			self.selectedPage = page
			for idx, button in enumerate(self.selectPageButtons):
				button.Disable() if idx == page else button.Enable()
			self._RefreshItems()

		def _LocalToGlobalSlot(self, pos):
			return self.selectedPage * self.PAGE_SIZE + pos

		def _GlobalToLocalSlot(self, pos):
			return pos % self.PAGE_SIZE

		def _OnScrollMouseWheel(self, delta):
			if delta > 0:
				if self.selectedPage > 0:
					self._OnSelectPage(self.selectedPage-1)
			else:
				if self.selectedPage + 1 < self.PAGE_COUNT:
					self._OnSelectPage(self.selectedPage+1)
			return True

	def _RefreshItems(self):
		# resetting slots
		for i in xrange(self.GRID_COLUMNS*self.GRID_ROWS):
			self.slotWindow.ClearSlot(i)
			self.slotWindow.DeactivateSlot(i)

		if app.EXTEND_IKASHOP_ULTIMATE:
			for i in xrange(self.PAGE_SIZE):
				self.lockedCells[i].Hide()

			scell = self.PAGE_SIZE * self.selectedPage
			ecell = scell + self.PAGE_SIZE

			for cell in xrange(scell, ecell):
				if cell >= self.shopInfo['lock']:
					self.lockedCells[self._GlobalToLocalSlot(cell)].Show()


				if cell in self.shopInfo['items']:
					item = self.shopInfo['items'][cell]
					pos = self._GlobalToLocalSlot(cell)
					self.slotWindow.SetItemSlot(pos, item['vnum'], item['count'] if item['count'] > 1 else 0)

		else:
			# setting up slots
			for item in self.shopInfo['items'].values():
				self.slotWindow.SetItemSlot(item['cell'], item['vnum'], item['count'] if item['count'] > 1 else 0)

		self.slotWindow.RefreshSlot()
		self._RefreshMarkedSlots()

	def _RefreshMarkedSlots(self):
		if not self.markedInfo:
			return

		if app.EXTEND_IKASHOP_ULTIMATE:
			scell = self.PAGE_SIZE * self.selectedPage
			ecell = scell + self.PAGE_SIZE
			shownCells = xrange(scell, ecell)

		vnum, count, price = self.markedInfo
		for cell, data in self.shopInfo['items'].items():
			if app.EXTEND_IKASHOP_ULTIMATE:
				if cell not in shownCells:
					continue
			if (data['vnum'], data['count'], data['price']) == (vnum, count, price):
				self.slotWindow.ActivateSlot(cell, 0.4, 0.4, 0.1)
		self.slotWindow.RefreshSlot()

	def Open(self, data):
		# refreshing duration & title
		self.durationText.SetText(locale.SecondToDHM(data['duration']*60))
		self.SetTitleName(locale.IKASHOP_SHOP_NAME_FORMAT.format(data['name']))

		data['items'] = { item['cell'] : item for item in data['items'] }
		self.shopInfo = data

		self._RefreshItems()

		if not self.IsShow():
			if app.EXTEND_IKASHOP_ULTIMATE:
				self._OnSelectPage(0)
			self.Show()
		self.SetTop()

	def Close(self):
		self.Hide()
		ikashop.SendCloseShopGuestBoard()

	def MarkItems(self, vnum, count, price):
		self.markedInfo = vnum, count, price
		self._RefreshMarkedSlots()

	def CheckExpiring(self, id):
		if self.shopInfo['id'] == id:
			self.Close()
			self.OpenPopupDialog(locale.IKASHOP_SHOP_GUEST_EXPIRED)

	def ShopGuestRemoveItem(self, itemid):
		if 'items' in self.shopInfo:
			self.shopInfo['items'] = { cell : data for cell, data in self.shopInfo['items'].items() if data['id'] != itemid}
			self._RefreshItems()

	def EditItem(self, itemid, prices):
		if 'items' in self.shopInfo:
			for data in self.shopInfo['items'].values():
				if data['id'] == itemid:
					data['price'] = prices['price']
					if 'cheque' in prices:
						data['cheque'] = prices['cheque']
					self._RefreshItems()
					break

	if SEARCH_SHOP_RENEWAL:
		def _SettingUpBoard(self):
			self.SetSize(177, 352)
			self.SetCloseEvent(self.Close)
			self.AddFlag("movable")
			self.AddFlag("float")
			self.SetCenterPosition()

		def _LoadIkarusShopGuestBoard(self):
			self.slotBox = self.CreateWidget(ui.ImageBox, pos = (6, 26))
			self.slotBox.LoadImage(OFFLINESHOP_UI_PATH + "bg_grid.png")
			if app.EXTEND_IKASHOP_ULTIMATE:
				self.slotBox.SetMouseWheelEvent(self._OnScrollMouseWheel)
			self.slotWindow = self.CreateWidget(ui.GridSlotWindow, parent = self.slotBox, pos = (3, 3))
			self.slotWindow.ArrangeSlot(0, self.GRID_COLUMNS, self.GRID_ROWS, SLOT_SIZE, SLOT_SIZE, 0, 0)
			self.slotWindow.SetSlotBaseImage(SLOT_BASE_IMG, 1.0, 1.0, 1.0, 1.0)
			self.slotWindow.SetSelectItemSlotEvent(self._OnClickItemSlot)
			self.slotWindow.SetOverInItemEvent(self._ShowToolTipOnItemSlot)
			self.slotWindow.SetOverOutItemEvent(self._HideToolTipOnItemSlot)
			if app.EXTEND_IKASHOP_ULTIMATE:
				self.slotWindow.SetMouseWheelEvent(self._OnScrollMouseWheel)

			self.durationBox = self.CreateWidget(ui.Window, show = False)
			self.durationText = self.CreateWidget(ui.TextLine, parent = self.durationBox, show = False)

			if app.EXTEND_IKASHOP_ULTIMATE:
				self.lockedCells = []
				for i in xrange(self.PAGE_SIZE):
					(col, row) = (i % self.GRID_COLUMNS, i // self.GRID_COLUMNS)
					lock = self.CreateWidget(ui.ImageBox, pos = (3 + 32 * col, 3 + 32 * row), parent = self.slotBox, show = 0)
					lock.LoadImage("ikashop/ultimate/lock_slot.png")
					self.lockedCells.append(lock)

				self.pageButtonsBg = self.CreateWidget(ui.ImageBox, pos = (6, 322))
				self.pageButtonsBg.LoadImage(OFFLINESHOP_UI_PATH + "bg_pagenumber.png")
				self.selectPageButtons = []
				for i in xrange(self.PAGE_COUNT):
					button = self.CreateWidget(ui.Button, pos = (9 + i * 40, 324))
					button.SetUpVisual(OFFLINESHOP_UI_PATH + "btn_page.png")
					button.SetOverVisual(OFFLINESHOP_UI_PATH + "btn_page_hover.png")
					button.SetDownVisual(OFFLINESHOP_UI_PATH + "btn_page_clicked.png")
					button.SetDisableVisual(OFFLINESHOP_UI_PATH + "btn_page_active.png")
					button.SetText(RomeNumber(i + 1))
					button.SAFE_SetEvent(self._OnSelectPage, i)
					self.selectPageButtons.append(button)


class IkarusAuctionGuestBoard(IkashopBoardWithTitleBar):

	OFFER_VIEW_COUNT = 6
	OFFER_VIEW_HEIGHT = 28

	def __init__(self):
		super(IkarusAuctionGuestBoard, self).__init__()
		self._SettingUpBoard()
		self._LoadIkarusShopAuctionGuestBoard()

	def _SettingUpBoard(self):
		sw, sh = GetScreenSize()
		self.SetSize(513 + 13, 249)
		self.SetCloseEvent(self.Close)
		self.SetPosition(sw/2 + self.GetWidth() - 600, sh / 2 - self.GetHeight()/2 + 100)
		self.AddFlag("movable")
		self.AddFlag("float")

	def _LoadIkarusShopAuctionGuestBoard(self):
		# making info box
		self.infoBox = self.CreateWidget(ui.ImageBox, pos = (12, 36))
		self.infoBox.LoadImage("ikashop/lite/auction/info_box.png")
		self.infoBox.SetMouseWheelEvent(self._MouseWheelScrollOffers)

		self.minRaiseText = self.CreateWidget(ui.TextLine, pos = (458+13, 221-36), parent = self.infoBox)
		self.minRaiseText.SetPackedFontColor(0xFFFFFFFF)
		self.minRaiseText.SetHorizontalAlignRight()

		self.durationText = self.CreateWidget(ui.TextLine, pos = (141, 221-36), parent = self.infoBox)
		self.durationText.SetPackedFontColor(0xFFFFFFFF)

		# making slot
		self.slot = self.CreateWidget(ui.GridSlotWindow, pos = (36, 44), size = (32, 98), parent = self.infoBox)
		self.slot.ArrangeSlot(0, 1, 3, SLOT_SIZE, SLOT_SIZE, 0, 0)
		self.slot.SetSlotBaseImage("ikashop/lite/common/slot/default.png", 1.0, 1.0, 1.0, 1.0)
		self.slot.SetOverInItemEvent(self._OverInItem)
		self.slot.SetOverOutItemEvent(self._OverOutItem)

		# making scrollbar
		self.offerScrollbar = self.CreateWidget(ui.ScrollBar, pos = (470+13, 4), parent = self.infoBox)
		self.offerScrollbar.SetScrollBarSize(self.infoBox.GetHeight() - 35)
		self.offerScrollbar.SetScrollEvent(self._ScrollOffers)

		# making cancel auction button
		self.raiseButton = self.CreateWidget(ui.Button, pos = (12, self.GetHeight() - 33))
		self.raiseButton.SetUpVisual("ikashop/lite/auction/raise_button/default.png")
		self.raiseButton.SetDownVisual("ikashop/lite/auction/raise_button/default.png")
		self.raiseButton.SetOverVisual("ikashop/lite/auction/raise_button/hover.png")
		self.raiseButton.SetText(locale.IKASHOP_ACUTION_GUEST_RAISE_AUCTION_BUTTON)
		self.raiseButton.SAFE_SetEvent(self._OnClickRaiseAuction)
		self.raiseButton.Show()

		# making offers
		self.offerViews = []
		for i in xrange(self.OFFER_VIEW_COUNT):
			self.offerViews.append(self.CreateWidget(
				IkarusShopAuctionOfferView, pos = (115, 6 + i*self.OFFER_VIEW_HEIGHT), parent = self.infoBox))

	def _RefreshOffers(self):
		# calculating count difference
		diff = len(self.offers) - self.OFFER_VIEW_COUNT
		diff = max(diff, 0)

		# calculating ranges
		offset = self.offerScrollbar.GetPos()
		sindex = int(diff * offset)
		eindex = sindex + min(self.OFFER_VIEW_COUNT, len(self.offers))

		# iterating over views
		for i, view in enumerate(self.offerViews):
			ri = i + sindex
			view.Hide() if ri >= eindex \
				else view.Setup(ri+1, self.offers[ri])

		# update scrollbar's middlebar height
		self.offerScrollbar.UpdateScrollbarLenght(self.OFFER_VIEW_HEIGHT * len(self.offers))

	def _MouseWheelScrollOffers(self, delta):
		if self.offerScrollbar.IsShow():
			self.offerScrollbar.OnDown() if delta < 0 \
				else self.offerScrollbar.OnUp()
		return True

	def _ScrollOffers(self):
		if self.offerScrollbar.IsShow():
			self._RefreshOffers()

	def _UpdateScrollbarState(self):
		self.offerScrollbar.SetPos(0)
		if len(self.offers) <= self.OFFER_VIEW_COUNT:
			self.offerScrollbar.Hide()
		else:
			self.offerScrollbar.Show()

	def _OverInItem(self, slot):
		data = self.auctionInfo
		tooltip = self.GetToolTip()
		tooltip.ClearToolTip()
		tooltip.AddItemData(data['vnum'], data['sockets'], data['attrs'])
		if app.EXTEND_IKASHOP_ULTIMATE:
			tooltip.AppendTextLine(locale.IKASHOP_ULTIMATE_PRICE_AVERAGE_NOT_AVAILABLE) if data['priceavg'] == 0 \
				else tooltip.AppendTextLine(locale.IKASHOP_ULTIMATE_PRICE_AVERAGE_VALUE.format(locale.NumberToMoneyString(data['priceavg'])))
		tooltip.ShowToolTip()

	def _OverOutItem(self, slot = 0):
		tooltip = self.GetToolTip()
		tooltip.ClearToolTip()
		tooltip.HideToolTip()

	def _OnClickRaiseAuction(self):
		self.OpenMoneyInputDialog(self._OnAcceptRaiseAuctionInput, value = self.minRaise)
		if app.EXTEND_IKASHOP_ULTIMATE:
			data = self.auctionInfo
			self.moneyInputDialog.SetPriceAverage(data['priceavg'])

	def _OnAcceptRaiseAuctionInput(self):
		self.moneyInputDialog.SoftClose()

		ok, value = ExtractInputPrice(self.moneyInputDialog)
		if not ok:
			self.OpenPopupDialog(locale.IKASHOP_BUSINESS_INVALID_ITEM_PRICE)
			return

		if ENABLE_CHEQUE_SYSTEM:
			valueTotal = value[0] + value[1] * YANG_PER_CHEQUE
			if self.minRaise > valueTotal:
				self.OpenPopupDialog(locale.IKASHOP_AUCTION_GUEST_MIN_RAISE_REQUIRED)
				return True

			if value[0] > player.GetElk() or value[1] > player.GetCheque():
				self.OpenPopupDialog(locale.IKASHOP_AUCTION_GUEST_NOT_ENOUGH_MONEY)
				return True

		else:
			if self.minRaise > value[0]:
				self.OpenPopupDialog(locale.IKASHOP_AUCTION_GUEST_MIN_RAISE_REQUIRED)
				return True

			if value[0] > player.GetElk():
				self.OpenPopupDialog(locale.IKASHOP_AUCTION_GUEST_NOT_ENOUGH_MONEY)
				return True

		ikashop.SendAuctionAddOffer(self.auctionInfo['owner'], *value)
		return True

	def SetOffers(self, offers):
		self.offers = sorted(offers, key = lambda val : val['datetime'], reverse=True)
		self._UpdateScrollbarState()
		self._RefreshOffers()
		self.RefreshMinRaise()

	def SetDuration(self, duration):
		self.durationText.SetText(locale.SecondToDHM(duration*60))

	def _GetMinRaise(self):
		if not self.offers:
			return self.auctionInfo['price']

		minraise = max([val['price'] for val in self.offers])
		if minraise < 1000:
			return minraise + 1000

		return minraise * (100+AUCTION_MIN_RAISE_PERCENTAGE) / 100

	def RefreshMinRaise(self):
		self.minRaise = self._GetMinRaise()
		self.minRaiseText.SetText(locale.IKASHOP_AUCTION_MIN_BID + '  ' + locale.NumberToString(self.minRaise))

	def Open(self, data):
		# storing data
		self.auctionInfo = data

		# refreshing duration & title
		seconds = data['duration'] * 60
		self.durationText.SetText(locale.SecondToDHM(seconds))
		self.SetTitleName(locale.IKASHOP_AUCTION_GUEST_NAME_FORMAT.format(data['ownername']))

		# refreshing item
		vnum = data['vnum']
		count = data['count'] if data['count'] > 1 else 0
		item.SelectItem(vnum)
		size = item.GetItemSize()[1]
		self.slot.ArrangeSlot(0, 1, size, SLOT_SIZE, SLOT_SIZE, 0, 0)
		self.slot.SetSlotBaseImage("ikashop/lite/common/slot/default.png", 1.0, 1.0, 1.0, 1.0)
		self.slot.SetItemSlot(0, vnum, count)

		# refreshing offers
		self.SetOffers(data['offers'])

		if not self.IsShow():
			self.Show()
			self.SetTop()

	def Close(self):
		self.Hide()
		ikashop.SendAuctionExitFrom(self.auctionInfo['owner'])


class IkarusAuctionListBoard(IkarusShopListBoard):

	AUCTION_VIEW_COUNT = 4

	def __init__(self):
		super(IkarusAuctionListBoard, self).__init__()
		self._SettingUpBoard()
		self._LoadIkarusAuctionListBoard()

	def _SettingUpBoard(self):
		self.SetSize(395, 510)
		self.SetTitleName(locale.IKASHOP_AUCTION_LIST_BOARD_TITLE)
		super(IkarusAuctionListBoard, self)._SettingUpBoard()

	def _LoadIkarusAuctionListBoard(self):
		self._LoadIkarusShopListBoard()
		self._MakeListElements(IkarusSearchShopItem, self.AUCTION_VIEW_COUNT)

	def SetAuctions(self, auctions):
		shuffle(auctions)
		self.auctions = auctions
		self.SetElements(self.auctions)
		self.Show()
		self.SetTop()

	def SetSearchShopBoard(self, board):
		for view in self.views:
			view.SetSearchShopBoard(board)

	def Open(self):
		ikashop.SendAuctionListRequest()

	def Close(self):
		self.Hide()

class IkarusShopHistoryFilterView(IkarusShopWindow):

	def __init__(self):
		super(IkarusShopHistoryFilterView, self).__init__()
		self._LoadIkarusShopHistoryFilterView()

	def _LoadIkarusShopHistoryFilterView(self):
		self.background = self.CreateWidget(ui.ImageBox)
		self.background.LoadImage("ikashop/lite/history_search/box.png")
		self.SetSize(self.background.GetWidth(), self.background.GetHeight())

		# making what
		self.whatText = self.CreateWidget(ui.TextLine, pos = (9, 5))
		self.whatText.SetPackedFontColor(0xFFFFFFFF)

		# making datetime
		self.datetimeText = self.CreateWidget(ui.TextLine, pos = (405-11, 5))
		self.datetimeText.SetPackedFontColor(0xFFFFFFFF)
		self.datetimeText.SetHorizontalAlignCenter()

		# info button
		self.infoButton = self.CreateWidget(ui.Button, pos = (294, 1))
		self.infoButton.SetUpVisual("ikashop/lite/history_search/info_button/default.png")
		self.infoButton.SetDownVisual("ikashop/lite/history_search/info_button/default.png")
		self.infoButton.SetOverVisual("ikashop/lite/history_search/info_button/hover.png")

		# search button
		self.searchButton = self.CreateWidget(ui.Button, pos = (294 + 27, 1))
		self.searchButton.SetUpVisual("ikashop/lite/search_shop/mini_search_button/default.png")
		self.searchButton.SetDownVisual("ikashop/lite/search_shop/mini_search_button/default.png")
		self.searchButton.SetOverVisual("ikashop/lite/search_shop/mini_search_button/hover.png")
		self.searchButton.SetToolTipText(locale.IKASHOP_SEARCH_SHOP_SEARCH_BUTTON_TEXT)

	def _ShowToolTip(self):
		tooltip = self.GetToolTip()
		tooltip.ClearToolTip()
		# adding item name
		tooltip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_HISTORY_WHAT_FORMAT.format(self.data['name'], self.data['count']))
		# adding type/subtype
		if self.data['type'] != 0:
			tooltip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_ITEM_TYPE_HEADER + ': ' + IkarusSearchShopBoard.ITEM_TYPES[self.data['type']])
			if self.data['subtype'] != 0:
				subtypes = IkarusSearchShopBoard.SUB_TYPES[self.data['type']]
				tooltip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_HEADER + ': ' + subtypes[self.data['subtype']])
		# adding price min/max
		if self.data['price_min'] != 0:
			tooltip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_ITEM_PRICE_MIN_HEADER + ': ' + locale.NumberToString(self.data['price_min']))
		if self.data['price_max'] != 0:
			tooltip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_ITEM_PRICE_MAX_HEADER + ': ' + locale.NumberToString(self.data['price_max']))
		# adding level min/max
		if self.data['level_min'] != 0:
			tooltip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_ITEM_LEVEL_MIN_HEADER + ': ' + locale.NumberToString(self.data['level_min']))
		if self.data['level_max'] != 0:
			tooltip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_ITEM_LEVEL_MAX_HEADER + ': ' + locale.NumberToString(self.data['level_max']))
		# adding attributes
		tooltip.AppendAttributes(self.data['attrs'])
		# adding special filters
		if self.data['sash'] != 0:
			tooltip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_SASH_ABSORB_HEADER + ': ' + IkarusSearchShopBoard.SASH_ABSORBS[self.data['sash']])
		if self.data['alchemy'] != 0:
			tooltip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_ALCHEMY_GRADE_HEADER + ': ' + IkarusSearchShopBoard.ALCHEMY_GRADES[self.data['alchemy']])
		tooltip.ResizeToolTip()
		tooltip.ShowToolTip()

	def _RefreshToolTip(self):
		tooltip = self.GetToolTip()
		if tooltip.IsShow():
			if not self.infoButton.IsIn():
				tooltip.HideToolTip()
		else:
			if self.infoButton.IsIn():
				self._ShowToolTip()

	def Setup(self, data):
		self.data = data
		self.datetimeText.SetText(DatetimeFormat(data['datetime']))
		self.whatText.SetText(locale.IKASHOP_SEARCH_SHOP_HISTORY_WHAT_FORMAT.format(data['name'], data['count']))

	def SetSearchEvent(self, event):
		self.searchButton.SAFE_SetEvent(event, proxy(self))

	def OnUpdate(self):
		self._RefreshToolTip()

	if SEARCH_SHOP_RENEWAL:
		def _LoadIkarusShopHistoryFilterView(self):
			self.background = self.CreateWidget(ui.ImageBox)
			self.background.LoadImage(SEARCH_HISTORY_UI + "bg2.png")
			self.SetSize(self.background.GetWidth(), self.background.GetHeight())
			self.whatText = self.CreateWidget(ui.TextLine, pos = (7, 10))
			self.whatText.SetPackedFontColor(0xFFFFFFFF)
			self.infoButton = self.CreateWidget(ui.Button, pos = (260, 5))
			self.infoButton.SetUpVisual(SEARCH_HISTORY_UI + "filter.png")
			self.infoButton.SetOverVisual(SEARCH_HISTORY_UI + "filter_hover.png")
			self.infoButton.SetDownVisual(SEARCH_HISTORY_UI + "filter_hover.png")
			self.searchButton = self.CreateWidget(ui.Button, pos = (286, 5))
			self.searchButton.SetUpVisual(SEARCH_HISTORY_UI + "btn_search.png")
			self.searchButton.SetOverVisual(SEARCH_HISTORY_UI + "btn_search_hover.png")
			self.searchButton.SetDownVisual(SEARCH_HISTORY_UI + "btn_search_clicked.png")
			self.searchButton.SetToolTipText(locale.IKASHOP_SEARCH_SHOP_SEARCH_BUTTON_TEXT)
			self.clockIcon = self.CreateWidget(ui.ImageBox, pos = (324, 9))
			self.clockIcon.LoadImage(SEARCH_HISTORY_UI + "clock_icon.png")
			self.datetimeText = self.CreateWidget(ui.TextLine, pos = (347, 10))
			self.datetimeText.SetPackedFontColor(0xFFFFFFFF)

		def Setup(self, data):
			self.data = data
			self.datetimeText.SetText(DatetimeFormat(data['datetime']))
			self.whatText.SetText(locale.IKASHOP_SEARCH_SHOP_HISTORY_NAME_FORMAT.format(SearchHistoryName(data['name'])))

		def _ShowToolTip(self):
			tooltip = self.GetToolTip()
			tooltip.ClearToolTip()
			tooltip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_HISTORY_WHAT_FORMAT.format(SearchHistoryName(self.data['name']), self.data['count']))
			category = SearchCategoryText(self.data['type'], self.data['subtype'])
			if category and self.data['type'] != 0:
				tooltip.AutoAppendTextLine(locale.IKASHOP_SEARCH_CATEGORIES + ': ' + category)
			if self.data['level_min'] != 0:
				tooltip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_ITEM_LEVEL_MIN_HEADER + ' ' + locale.NumberToString(self.data['level_min']))
			if self.data['level_max'] != 0:
				tooltip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_ITEM_LEVEL_MAX_HEADER + ' ' + locale.NumberToString(self.data['level_max']))
			tooltip.AppendAttributes(self.data['attrs'])
			sash = (locale.IKASHOP_SEARCH_SHOP_SASH_GRADE_VALUE0, locale.IKASHOP_SEARCH_SHOP_SASH_GRADE_VALUE1,
				locale.IKASHOP_SEARCH_SHOP_SASH_GRADE_VALUE2, locale.IKASHOP_SEARCH_SHOP_SASH_GRADE_VALUE3)
			if 0 < self.data['sash'] <= len(sash):
				tooltip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_SASH_ABSORB_HEADER + ' ' + sash[self.data['sash'] - 1])
			alchemy = (locale.IKASHOP_SEARCH_SHOP_ALCHEMY_GRADE_VALUE_MATTE, locale.IKASHOP_SEARCH_SHOP_ALCHEMY_GRADE_VALUE_CLEAR,
				locale.IKASHOP_SEARCH_SHOP_ALCHEMY_GRADE_VALUE_FLAWLESS, locale.IKASHOP_SEARCH_SHOP_ALCHEMY_GRADE_VALUE_BRILLIANT,
				locale.IKASHOP_SEARCH_SHOP_ALCHEMY_GRADE_VALUE_EXCELLENT)
			if 0 < self.data['alchemy'] <= len(alchemy):
				tooltip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_ALCHEMY_GRADE_HEADER + ' ' + alchemy[self.data['alchemy'] - 1])
			tooltip.ResizeToolTip()
			tooltip.ShowToolTip()

class IkarusHistoryFilterBoard(IkarusShopListBoard):

	HISTORY_FILTER_VIEW_COUNT = 10

	def __init__(self):
		super(IkarusHistoryFilterBoard, self).__init__()
		self._SettingUpBoard()
		self._LoadIkarusHistoryFilterBoard()

	def _SettingUpBoard(self):
		self.SetSize(494, 339)
		self.SetTitleName(locale.IKASHOP_HISTORY_FILTER_LIST_BOARD_TITLE)
		super(IkarusHistoryFilterBoard, self)._SettingUpBoard()

	def _LoadIkarusHistoryFilterBoard(self):
		self._LoadIkarusShopListBoard()
		self._MakeListElements(IkarusShopHistoryFilterView, self.HISTORY_FILTER_VIEW_COUNT)
		for view in self.views:
			view.SetSearchEvent(self._OnClickSearchOnHistoryElement)

	def _OnClickSearchOnHistoryElement(self, view):
		self.searchShopBoard.HistoryRedoSearch(view.data)
		self.Close()

	def SetSearchShopBoard(self, board):
		self.searchShopBoard = proxy(board)

	def SetFilters(self, filters):
		self.filters = sorted(filters, key = lambda elm : elm['datetime'], reverse=True)
		self.SetElements(self.filters)

	def Open(self):
		self.Show()
		self.SetTop()

	def Close(self):
		self.Hide()

	if SEARCH_SHOP_RENEWAL:
		HISTORY_FILTER_VIEW_COUNT = SEARCH_HISTORY_ROWS

		def _SettingUpBoard(self):
			self.SetSize(478, 310)
			self.SetTitleName(locale.IKASHOP_HISTORY_FILTER_LIST_BOARD_TITLE)
			IkarusShopListBoard._SettingUpBoard(self)

		def _LoadIkarusHistoryFilterBoard(self):
			self._LoadIkarusShopListBoard()
			box = self.boardBox
			box.LoadImage(SEARCH_HISTORY_UI + "bg.png")
			box.SetScale(1.0, 1.0)
			box.SetPosition(8, 30)
			self.elementScrollbar.Hide()
			self.elementScrollbar = self.CreateWidget(SearchThinScrollBar, pos = (465, 62), show = False)
			self.elementScrollbar.SetScrollBarSize(238)
			self.elementScrollbar.SetScrollEvent(self._ScrollElements)
			self.historyHeaders = []
			for (x, text) in ((166, locale.IKASHOP_SEARCH_SHOP_WHAT), (393, locale.IKASHOP_SEARCH_SHOP_DATE)):
				header = self.CreateWidget(ui.TextLine, pos = (x, 39))
				header.SetHorizontalAlignCenter()
				header.SetText(text)
				self.historyHeaders.append(header)
			self.emptyHeader.SetFontName(locale.UI_DEF_FONT)
			self.emptyHeader.SetOutline(0)
			self.emptyHeader.SetPackedFontColor(0xFFCABDAB)
			self.emptyHeader.SetPosition(239, 180)
			self._MakeListElements(IkarusShopHistoryFilterView, SEARCH_HISTORY_ROWS)
			for (i, view) in enumerate(self.views):
				view.SetPosition(3, 33 + i * 35)
				view.SetSearchEvent(self._OnClickSearchOnHistoryElement)
				view.SetMouseWheelEvent(self._MouseWheelScrollElements)

class IkarusShopComboBox(IkarusShopWindow):

	DEFAULT_VIEW_COUNT = 5
	ELEMENT_HEIGHT = 14

	class ComboBoxView(ui.Button):
		def Destroy(self):
			SelfDestroyObject(self)

	def __init__(self):
		super(IkarusShopComboBox, self).__init__()
		self.viewCount = self.DEFAULT_VIEW_COUNT
		self.elementWidth = 0
		self.selectItemEvent = None
		self.views = []
		self.items = []
		self.elementImages = (
			"ikashop/lite/search_shop/combo_box_element/default.png",
			"ikashop/lite/search_shop/combo_box_element/default.png",
			"ikashop/lite/search_shop/combo_box_element/hover.png")
		self.selectedItem = 0
		self._LoadIkarusShopComboBox()

	def _LoadIkarusShopComboBox(self):
		self.SetMouseWheelEvent(self._MouseWheelScrollView)

		self.background = self.CreateWidget(ui.Bar3D)
		self.background.SetColor(0xFF999999, 0xFF000000, 0xFF777777)

		self.scrollbar = self.CreateWidget(ui.ScrollBar, show = False, parent = self.background)
		self.scrollbar.SetScrollEvent(self._ScrollView)

	def _MakeViews(self):
		for view in self.views:
			SelfDestroyObject(view)

		self.views = []
		images = self.elementImages
		for i in xrange(self.viewCount):
			view = self.CreateWidget(self.ComboBoxView, pos = (0, i*self.ELEMENT_HEIGHT), parent = self.background)
			view.SetUpVisual(images[0])
			view.SetDownVisual(images[1])
			view.SetOverVisual(images[2])
			view.SetWindowName("cacca")
			self.elementWidth = max(self.elementWidth, view.GetWidth())
			self.views.append(view)

	def _MouseWheelScrollView(self, delta):
		if self.scrollbar.IsShow():
			self.scrollbar.OnDown() if delta < 0\
				else self.scrollbar.OnUp()
		return True

	def _ScrollView(self):
		if self.scrollbar.IsShow():
			self._RefreshView()

	def _RefreshView(self):
		if not self.views:
			self._MakeViews()

		# calculating sindex
		pos = self.scrollbar.GetPos() if self.scrollbar.IsShow() else 0.0
		diff = max(len(self.items) - self.viewCount, 0)
		sindex = int(diff * pos)
		eindex = sindex + min(len(self.items), self.viewCount)

		# hiding all views
		for view in self.views:
			view.Hide()

		for i in xrange(sindex, eindex):
			ri = i - sindex
			view = self.views[ri]
			view.SetText(self.items[i])
			view.ButtonText.SetPosition(view.GetWidth()/2, view.GetHeight() /2 -1)
			view.SAFE_SetEvent(self.SelectItem, i)
			view.Show()

			color = 0xFFFFFFFF if i != self.selectedItem else 0xFFFFFF88
			view.ButtonText.SetPackedFontColor(color)

		# updating scrollbar's middlebar length
		self.scrollbar.UpdateScrollbarLenght(len(self.items) * self.ELEMENT_HEIGHT)

	def _UpdateSize(self):
		viewHeight = self.ELEMENT_HEIGHT * min(len(self.items), self.viewCount)
		self.SetSize(self.GetWidth(), viewHeight)
		self.scrollbar.SetScrollBarSize(viewHeight)
		self.background.SetSize(self.GetWidth(), self.GetHeight())

	def _UpdateScrollbar(self):
		if len(self.items) > self.viewCount:
			self.scrollbar.Show()
			self.scrollbar.SetPos(0)
			self.scrollbar.SetPosition(self.elementWidth+1, 0)
			self.SetSize(self.elementWidth + 1 + self.scrollbar.GetWidth(), self.GetHeight())
			self.background.SetSize(self.GetWidth(), self.GetHeight())
		else:
			self.scrollbar.Hide()
			self.SetSize(self.elementWidth, self.GetHeight())
			self.background.SetSize(self.GetWidth(), self.GetHeight())

	def Open(self):
		self.Show()

	def Close(self):
		self.Hide()

	def GetSelectedItem(self):
		return self.selectedItem

	def SelectItem(self, index):
		self.selectedItem = index
		self._RefreshView()
		self.Close()
		if self.selectItemEvent:
			self.selectItemEvent(index, self.items[index])

	def SetSelectItemEvent(self, event):
		self.selectItemEvent = event

	def SetItems(self, items):
		self.items = items
		if not self.views:
			self._MakeViews()
		self._UpdateSize()
		self._UpdateScrollbar()
		self._RefreshView()

	def SetViewCount(self, count):
		self.viewCount = count
		self._UpdateSize()
		self._UpdateScrollbar()
		self._MakeViews()
		self._RefreshView()

	def ChangeElementImages(self, images):
		self.elementImages = images
		self._MakeViews()
		self._UpdateSize()
		self._UpdateScrollbar()
		self._RefreshView()

	def IsMe(self, combobox):
		return self is combobox


if app.EXTEND_IKASHOP_ULTIMATE:
	class IkashopCheckBox(IkarusShopWindow):

		def __init__(self):
			super(IkashopCheckBox, self).__init__()
			self.checkEvent = None
			self.isEnabled = False
			self._LoadIkashopCheckBox()

		def _LoadIkashopCheckBox(self):
			self.text = self.CreateWidget(ui.TextLine)
			self.text.SetPackedFontColor(0xFFFFFFFF)

			self.base = self.CreateWidget(ui.ImageBox)
			self.base.SetOnMouseLeftButtonUpEvent(self.Check)

			self.checked = self.CreateWidget(ui.ImageBox, show = False)
			self.checked.SetOnMouseLeftButtonUpEvent(self.Uncheck)

		def _Resize(self):
			w = self.text.GetWidth() + 5 + max(self.base.GetWidth(), self.checked.GetWidth())
			h = max([self.text.GetHeight(), self.base.GetHeight(), self.checked.GetHeight()])
			self.base.SetPosition(self.text.GetWidth() + 5, 0)
			self.checked.SetPosition(self.text.GetWidth() + 5, 0)
			self.SetSize(w, h)

		def SetImages(self, base, checked):
			self.base.LoadImage(base)
			self.checked.LoadImage(checked)
			self._Resize()

		def SetText(self, text):
			self.text.SetText(text)
			self.text.FitText()
			self._Resize()

		def SetCheckEvent(self, event):
			self.checkEvent = event

		def Check(self, callback = 1):
			if self.isEnabled:
				self.base.Hide()
				self.checked.Show()
			if callback and self.checkEvent:
				self.checkEvent()

		def Uncheck(self, callback = 1):
			self.base.Show()
			self.checked.Hide()
			if callback and self.checkEvent:
				self.checkEvent()

		def IsChecked(self):
			return self.checked.IsShow()

		def Enable(self):
			self.isEnabled = True

		def Disable(self):
			self.isEnabled = False

		def IsEnabled(self):
			return self.isEnabled

class IkarusSearchShopItem(IkarusShopWindow):

	def __init__(self):
		self.searchShopBoard = None
		super(IkarusSearchShopItem, self).__init__()
		self.data = {'id':-1}
		self._LoadIkarusSearchShopItem()

	def _LoadIkarusSearchShopItem(self):
		# making background
		self.background = self.CreateWidget(ui.ExpandedImageBox)
		self.background.LoadImage("ikashop/lite/search_shop/result_item_box.png")
		self.SetSize(self.background.GetWidth(), self.background.GetHeight())

		# making textlines
		self.itemName = self.CreateWidget(ui.TextLine, pos = (60, 17 - 6))
		self.sellerName = self.CreateWidget(ui.TextLine, pos = (78, 41 - 6))
		self.duration = self.CreateWidget(ui.TextLine, pos = (226, 41 - 6))
		self.price = self.CreateWidget(ui.TextLine, pos = (78, 58))

		if ENABLE_CHEQUE_SYSTEM:
			self.cheque = self.CreateWidget(ui.TextLine, pos = (128 + 70, 58))
			self.chequeIcon = self.CreateWidget(ui.ImageBox, pos = (110 + 70, 59))
			self.chequeIcon.LoadImage("d:/ymir work/ui/game/windows/cheque_icon.sub")

		if app.EXTEND_IKASHOP_ULTIMATE:
			self.priceAverage = self.CreateWidget(ui.TextLine, pos = (330-8, 58))
			self.priceAverage.SetHorizontalAlignRight()

		# making buttons
		self.buyButton = self.CreateWidget(ui.Button, pos = (261, 84))
		self.buyButton.SetUpVisual("ikashop/lite/search_shop/buy_button/default.png")
		self.buyButton.SetDownVisual("ikashop/lite/search_shop/buy_button/default.png")
		self.buyButton.SetOverVisual("ikashop/lite/search_shop/buy_button/hover.png")
		self.buyButton.SAFE_SetEvent(self._OnClickBuyButton)
		self.buyButton.SetText(locale.IKASHOP_SEARCH_SHOP_BUY_BUTTON_TEXT)

		self.offerButton = self.CreateWidget(ui.Button, pos = (189, 84))
		self.offerButton.SetUpVisual("ikashop/lite/search_shop/offer_button/default.png")
		self.offerButton.SetDownVisual("ikashop/lite/search_shop/offer_button/default.png")
		self.offerButton.SetOverVisual("ikashop/lite/search_shop/offer_button/hover.png")
		self.offerButton.SAFE_SetEvent(self._OnClickOfferButton)
		self.offerButton.SetText(locale.IKASHOP_SEARCH_SHOP_OFFER_BUTTON_TEXT)

		self.openSellingBoard = self.CreateWidget(ui.Button, pos = (50, 84), show = False)
		self.openSellingBoard.SetUpVisual("ikashop/lite/search_shop/offer_button/default.png")
		self.openSellingBoard.SetDownVisual("ikashop/lite/search_shop/offer_button/default.png")
		self.openSellingBoard.SetOverVisual("ikashop/lite/search_shop/offer_button/hover.png")
		self.openSellingBoard.SAFE_SetEvent(self._OnClickOpenSellingBoardButton)

		if app.EXTEND_IKASHOP_PRO:
			self.messageSellerButton = self.CreateWidget(ui.Button)
			self.messageSellerButton.SetUpVisual("ikashop/ultimate/seller_message/default.png")
			self.messageSellerButton.SetOverVisual("ikashop/ultimate/seller_message/hover.png")
			self.messageSellerButton.SetDownVisual("ikashop/ultimate/seller_message/default.png")
			self.messageSellerButton.SAFE_SetEvent(self._OnClickMessageSeller)

		# making slot item
		self.slot = self.CreateWidget(ui.GridSlotWindow, pos = (9, 7))
		self.slot.ArrangeSlot(0, 1, 3, SLOT_SIZE, SLOT_SIZE, 0, 0)
		self.slot.SetSlotBaseImage("ikashop/lite/common/slot/default.png", 1.0, 1.0, 1.0, 1.0)
		self.slot.SetOverInItemEvent(self._OverInItem)
		self.slot.SetOverOutItemEvent(self._OverOutItem)

	def _OnClickBuyButton(self):
		item.SelectItem(self.data['vnum'])
		# making item name
		itemName = item.GetItemName()
		if self.data['count'] > 1:
			itemName += "({})".format(self.data['count'])

		# making item price
		if ENABLE_CHEQUE_SYSTEM:
			itemPrice = ""
			if self.data['price'] != 0:
				itemPrice += locale.NumberToMoneyString(self.data['price'])
			if self.data['cheque'] != 0:
				if itemPrice:
					itemPrice += ', '
				itemPrice += locale.NumberToCheque(self.data['cheque'])
		else:
			itemPrice = locale.NumberToMoneyString(self.data['price'])

		self.buyItemInfo = self.data['owner'], self.data['id'], self.data['price'] + self.data.get('cheque', 0) * YANG_PER_CHEQUE
		message = locale.IKASHOP_SHOP_GUEST_BUY_ITEM_QUESTION.format(itemName, itemPrice)
		self.OpenQuestionDialog(message, self._OnAcceptBuyItemQuestion)

	def _OnClickOfferButton(self):
		# checking offer min price
		if 0 < self.data['price'] + self.data.get('cheque', 0) * YANG_PER_CHEQUE < 10000:
			self.OpenPopupDialog(locale.IKASHOP_SHOP_GUEST_MAKE_OFFER_ITEM_PRICE_TOO_LOW)
			return

		self.offerInfo = self.data['id'], self.data['price'], self.data.get('cheque', 0)
		self.OpenMoneyInputDialog(self._OnAcceptMakeOfferInput)
		if app.EXTEND_IKASHOP_ULTIMATE:
			self.moneyInputDialog.SetPriceAverage(self.data['priceavg'])
		return

	def _OnAcceptBuyItemQuestion(self):
		ikashop.SendBuyItem(*self.buyItemInfo)
		self.questionDialog.Hide()

	def _OnAcceptMakeOfferInput(self):
		self.moneyInputDialog.SoftClose()

		# validating value
		ok, value = ExtractInputPrice(self.moneyInputDialog)
		if not ok:
			self.OpenPopupDialog(locale.IKASHOP_BUSINESS_INVALID_ITEM_PRICE)
			return

		id, price, cheque = self.offerInfo

		if ENABLE_CHEQUE_SYSTEM:
			valueTotal = value[0] + value[1] * YANG_PER_CHEQUE
			priceTotal = price + cheque * YANG_PER_CHEQUE
			if valueTotal >= priceTotal:
				self.OpenPopupDialog(locale.IKASHOP_SHOP_GUEST_OFFER_MUST_BE_LOWER_THAN_PRICE)
				return True

			minoffer = priceTotal * MIN_OFFER_PCT / 100
			if valueTotal < minoffer:
				self.OpenPopupDialog(locale.IKASHOP_SHOP_GUEST_OFFER_MUST_BE_HIGHER_THAN_PCT_OF_PRICE.format(MIN_OFFER_PCT))
				return True

			# checking owned cash
			if value[0] > player.GetElk() or value[1] > player.GetCheque():
				self.OpenPopupDialog(locale.IKASHOP_SHOP_GUEST_OFFER_NOT_ENOUGH_MONEY)
				return True

		else:
			if price > 0 and value[0] >= price:
				self.OpenPopupDialog(locale.IKASHOP_SHOP_GUEST_OFFER_MUST_BE_LOWER_THAN_PRICE)
				return True

			minoffer = max(1, price * MIN_OFFER_PCT / 100)
			if value[0] < minoffer:
				self.OpenPopupDialog(locale.IKASHOP_SHOP_GUEST_OFFER_MUST_BE_HIGHER_THAN_PCT_OF_PRICE.format(MIN_OFFER_PCT))
				return True

			# checking owned cash
			if value[0] > player.GetElk():
				self.OpenPopupDialog(locale.IKASHOP_SHOP_GUEST_OFFER_NOT_ENOUGH_MONEY)
				return True

		ikashop.SendOfferCreate(self.data['owner'], id, *value)
		return True

	def _OnClickOpenSellingBoardButton(self):
		if self.data['is_auction']:
			ikashop.SendAuctionOpenAuction(self.data['owner'])
		if app.EXTEND_IKASHOP_ULTIMATE:
			if not self.data['is_auction']:
				self.searchShopBoard.RequestOpenSellerShop(
					self.data['owner'], self.data['vnum'], self.data['count'], self.data['price'])

	def _OverInItem(self, slot):
		tooltip = self.GetToolTip()
		tooltip.ClearToolTip()
		tooltip.AddItemData(self.data['vnum'], self.data['sockets'], self.data['attrs'])
		tooltip.ShowToolTip()

	def _OverOutItem(self):
		tooltip = self.GetToolTip()
		tooltip.HideToolTip()

	if app.EXTEND_IKASHOP_PRO:
		def _OnClickMessageSeller(self):
			self.searchShopBoard.OpenWhisper(self.sellerName.GetText())

	def SetSearchShopBoard(self, board):
		self.searchShopBoard = proxy(board)

	def GetId(self):
		return self.data['id']

	def SetNotAvailable(self):
		if not self.data['is_auction']:
			self.slot.DisableSlot(0)
			self.itemName.SetPackedFontColor(0xFFFF8888)
			self.buyButton.Hide()
			self.offerButton.Hide()

	def SetAvailable(self):
		if not self.data['is_auction']:
			self.slot.EnableSlot(0)
			self.itemName.SetPackedFontColor(0xFFFFFFFF)
			self.buyButton.Show()
			self.offerButton.Show()

	def Setup(self, data):
		if data['is_auction']:
			self.buyButton.Hide()
			self.offerButton.Hide()
			self.background.LoadImage("ikashop/lite/search_shop/result_item_auction_box.png")
			self.openSellingBoard.SetText(locale.IKASHOP_SEARCH_SHOP_OPEN_AUCTION_BUTTON_TEXT)
			self.openSellingBoard.Show()
		else:
			self.buyButton.Show()
			self.offerButton.Show()
			self.background.LoadImage("ikashop/lite/search_shop/result_item_box.png")
			if app.EXTEND_IKASHOP_ULTIMATE:
				self.openSellingBoard.SetText(locale.IKASHOP_SEARCH_SHOP_OPEN_SHOP_BUTTON_TEXT)
				self.openSellingBoard.Show()
			else:
				self.openSellingBoard.Hide()

		# setting itemname
		item.SelectItem(data['vnum'])
		itemName = item.GetItemName()
		if data['is_auction']:
			itemName += ' ' + locale.IKASHOP_SEARCH_SHOP_ITEM_NAME_AUCTION
		self.itemName.SetText(itemName)

		# setting seller name
		self.sellerName.SetText(data['seller_name'])

		if app.EXTEND_IKASHOP_PRO:
			sx, sy = self.sellerName.GetLocalPosition()
			self.messageSellerButton.SetPosition(sx + self.sellerName.GetTextSize()[0] + 10, sy)

		# setting duration
		self.duration.SetText(locale.SecondToDHM(data['duration']*60))

		# setting price
		self.price.SetText(locale.NumberToString(data['price']))

		if ENABLE_CHEQUE_SYSTEM:
			self.cheque.Show() if data['cheque'] != 0 else self.cheque.Hide()
			self.chequeIcon.Show() if data['cheque'] != 0 else self.chequeIcon.Hide()
			self.cheque.SetText(locale.NumberToString(data['cheque']))

		if app.EXTEND_IKASHOP_ULTIMATE:
			pa = locale.IKASHOP_ULTIMATE_PRICE_AVERAGE_NOT_AVAILABLE_EMOJI if data['priceavg'] == 0 \
				else locale.IKASHOP_ULTIMATE_PRICE_AVERAGE_EMOJI.format(locale.NumberToMoneyString(data['priceavg']))
			self.priceAverage.SetText(pa)

		# setting slot
		itemcount = data['count'] if data['count'] > 1 else 0
		self.slot.ArrangeSlot(0, 1, item.GetItemSize()[1], SLOT_SIZE, SLOT_SIZE, 0, 0)
		self.slot.SetSlotBaseImage("ikashop/lite/common/slot/default.png", 1.0, 1.0, 1.0, 1.0)
		self.slot.SetItemSlot(0, data['vnum'], itemcount)
		self.data = data


class IkarusSearchShopBoard(IkashopBoardWithTitleBar):

	RESULT_ITEM_VIEW_COUNT = 4

	ITEM_TYPES = (
		locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,
		locale.IKASHOP_SEARCH_SHOP_ITEM_TYPE_WEAPON,
		locale.IKASHOP_SEARCH_SHOP_ITEM_TYPE_ARMOR,
		locale.IKASHOP_SEARCH_SHOP_ITEM_TYPE_JEWEL,
		locale.IKASHOP_SEARCH_SHOP_ITEM_TYPE_COSTUME,
		locale.IKASHOP_SEARCH_SHOP_ITEM_TYPE_PET,
		locale.IKASHOP_SEARCH_SHOP_ITEM_TYPE_MOUNT,
		locale.IKASHOP_SEARCH_SHOP_ITEM_TYPE_ALCHEMY,
		locale.IKASHOP_SEARCH_SHOP_ITEM_TYPE_BOOK,
		locale.IKASHOP_SEARCH_SHOP_ITEM_TYPE_STONE,
		locale.IKASHOP_SEARCH_SHOP_ITEM_TYPE_MINERALS,
		locale.IKASHOP_SEARCH_SHOP_ITEM_TYPE_FISH,
	)

	SUBTYPE_WEAPON = (
		locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_WEAPON_SWORD,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_WEAPON_TWOHANDED,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_WEAPON_BLADE,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_WEAPON_DAGGER,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_WEAPON_BOW,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_WEAPON_BELL,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_WEAPON_FAN,
	)

	if app.ENABLE_WOLFMAN_CHARACTER:
		SUBTYPE_WEAPON += (locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_WEAPON_CLAW,)

	SUBTYPE_ARMOR = (
		locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_ARMOR_WARRIOR,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_ARMOR_SURA,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_ARMOR_ASSASSIN,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_ARMOR_SHAMAN,
	)

	if app.ENABLE_WOLFMAN_CHARACTER:
		SUBTYPE_ARMOR += (locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_ARMOR_WOLFMAN,)

	SUBTYPE_JEWEL = (
		locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_JEWEL_HELM,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_JEWEL_SHIELD,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_JEWEL_EAR,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_JEWEL_NECK,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_JEWEL_WRIST,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_JEWEL_SHOES,
	)

	SUBTYPE_COSTUME = (
		locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_COSTUME_BODY,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_COSTUME_WEAPON,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_COSTUME_HAIR,
	)

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		SUBTYPE_COSTUME += (locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_COSTUME_SASH,)

	SUBTYPE_PET = (
		locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_PET_EGGS,
		locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_PET_SEALS,
	)

	SUBTYPE_MOUNT = (locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,)
	SUBTYPE_ALCHEMY = (locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,)
	SUBTYPE_BOOKS = (locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,)
	SUBTYPE_STONE = (locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,)
	SUBTYPE_MINERAL = (locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,)
	SUBTYPE_FISH = (locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,)

	SUB_TYPES = (
		(locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,),
		SUBTYPE_WEAPON,
		SUBTYPE_ARMOR,
		SUBTYPE_JEWEL,
		SUBTYPE_COSTUME,
		SUBTYPE_PET,
		SUBTYPE_MOUNT,
		SUBTYPE_ALCHEMY,
		SUBTYPE_BOOKS,
		SUBTYPE_STONE,
		SUBTYPE_MINERAL,
		SUBTYPE_FISH,
	)

	SASH_ABSORBS = (
		locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,
		locale.IKASHOP_SEARCH_SHOP_SASH_GRADE_VALUE0,
		locale.IKASHOP_SEARCH_SHOP_SASH_GRADE_VALUE1,
		locale.IKASHOP_SEARCH_SHOP_SASH_GRADE_VALUE2,
		locale.IKASHOP_SEARCH_SHOP_SASH_GRADE_VALUE3,
	)

	ALCHEMY_GRADES = (
		locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,
		locale.IKASHOP_SEARCH_SHOP_DRAGON_SOUL_GRADE_NORMAL,
		locale.IKASHOP_SEARCH_SHOP_DRAGON_SOUL_GRADE_BRILLIANT,
		locale.IKASHOP_SEARCH_SHOP_DRAGON_SOUL_GRADE_RARE,
		locale.IKASHOP_SEARCH_SHOP_DRAGON_SOUL_GRADE_ANCIENT,
		locale.IKASHOP_SEARCH_SHOP_DRAGON_SOUL_GRADE_LEGENDARY,
	)

	def __init__(self):
		self.openWhisperTextEvent = None
		if SEARCH_SHOP_RENEWAL:
			self.pendingSearch = None
			self.lastSearch = None
			self.lastSearchSent = -100.0
			self.lastCategory = None
			self.overpricedDialog = None
			self.numericEdits = []
			self.searchLoading = None
			self.searchLoadingStart = None
			self.inputNamePlaceHolder = None
		super(IkarusSearchShopBoard, self).__init__()
		ikashop.SetSearchShopBoard(self)
		self.items = []
		self.lastOpen = 0
		self.markItemInfo = None
		if app.EXTEND_IKASHOP_ULTIMATE:
			self.shuffleItem = None
		self._MakeItemNameContainers()
		self._SettingUpBoard()
		self._LoadSearchShopWindow()

	def __del__(self):
		super(IkarusSearchShopBoard, self).__del__()
		ikashop.SetSearchShopBoard(None)

	def _MakeItemNameContainers(self):
		names = ikashop.GetItemNames()
		self.itemNames = set()

		for name in names:
			f = name.find("+")
			if f != -1 and len(name)-1 != f and name[f+1:].isdigit():
				name = name[:f]
			self.itemNames.add(name.lower())

	def _SettingUpBoard(self):
		self.SetSize(604, 519)
		self.SetTitleName(locale.IKASHOP_SEARCH_SHOP_BOARD_TITLE)
		self.SetCloseEvent(self.Close)
		self.SetCenterPosition()
		self.AddFlag("movable")
		self.AddFlag("float")

	def _LoadLinkedBoard(self):
		self.shopGuestBoard = IkarusShopGuestBoard()
		self.auctionGuestBoard = IkarusAuctionGuestBoard()
		self.auctionListBoard = IkarusAuctionListBoard()
		self.historyFilterBoard = IkarusHistoryFilterBoard()

		self.auctionListBoard.SetSearchShopBoard(self)
		self.historyFilterBoard.SetSearchShopBoard(self)
		self.historyFilterBoard.SetFilters(ikashop.GetFilterHistory())

	def _LoadSearchShopWindow(self):
		self._LoadLinkedBoard()
		getBottom = lambda win : win.GetLocalPosition()[1] + win.GetHeight()
		getRight = lambda win : win.GetLocalPosition()[0] + win.GetWidth()

		largerComboBoxImages = (
			"ikashop/lite/search_shop/attribute_element/default.png",
			"ikashop/lite/search_shop/attribute_element/default.png",
			"ikashop/lite/search_shop/attribute_element/hover.png",
		)

		self.inputNameBox = self.CreateWidget(ui.ExpandedImageBox, pos = (14,40))
		self.inputNameBox.LoadImage("ikashop/lite/search_shop/input_name.png")
		self.inputNameBox.SetScale(155.0 / self.inputNameBox.GetWidth(), 1.0)

		self.searchButton = self.CreateWidget(ui.Button, pos = (14 + self.inputNameBox.GetWidth() + 2, 42))
		self.searchButton.SetUpVisual("ikashop/lite/search_shop/mini_search_button/default.png")
		self.searchButton.SetDownVisual("ikashop/lite/search_shop/mini_search_button/default.png")
		self.searchButton.SetOverVisual("ikashop/lite/search_shop/mini_search_button/hover.png")
		self.searchButton.SAFE_SetEvent(self._OnClickSearchButton)
		self.searchButton.SetToolTipText(locale.IKASHOP_SEARCH_SHOP_SEARCH_BUTTON_TEXT)

		iw = self.inputNameBox.GetWidth() - self.searchButton.GetWidth() - 6
		ih = self.inputNameBox.GetHeight() - 6
		self.inputNameEdit = self.CreateWidget(ui.EditLine, pos = (6, 6), size = (iw, ih), parent=self.inputNameBox)
		self.inputNameEdit.SetMax(ikashop.FILTER_NAME_MAX_LEN)
		self.inputNameEdit.SetEscapeEvent(ui.__mem_func__(self.inputNameEdit.KillFocus))
		self.inputNameEdit.SetFocusUpdateEvent(self._OnUpdateInputName)
		self.inputNameBox.SetOnMouseLeftButtonUpEvent(self.inputNameEdit.SetFocus)

		self.inputNameSuggestion = self.CreateWidget(IkarusShopComboBox, pos = (14, getBottom(self.inputNameBox)+2))
		self.inputNameSuggestion.SetSelectItemEvent(self._OnSelectSuggestedItemName)
		self.inputNameSuggestion.ChangeElementImages(largerComboBoxImages)
		self.inputNameSuggestion.SetViewCount(6)
		self.inputNameSuggestion.SetItems(["",])

		self.resetFilterButton = self.CreateWidget(ui.Button, pos = (getRight(self.searchButton) + 3, 42))
		self.resetFilterButton.SetUpVisual("ikashop/lite/search_shop/reset_filter_button/default.png")
		self.resetFilterButton.SetDownVisual("ikashop/lite/search_shop/reset_filter_button/default.png")
		self.resetFilterButton.SetOverVisual("ikashop/lite/search_shop/reset_filter_button/hover.png")
		self.resetFilterButton.SAFE_SetEvent(self._OnClickResetFilters)
		self.resetFilterButton.SetToolTipText(locale.IKASHOP_SEARCH_SHOP_RESET_FILTER_BUTTON_TEXT)

		# item type filter
		self.itemTypeFilterBox = self.CreateWidget(ui.ExpandedImageBox, pos = (14, 72))
		self.itemTypeFilterBox.LoadImage("ikashop/lite/search_shop/filter_box.png")

		self.itemTypeHeader = self.CreateWidget(ui.TextLine, pos = (6, 13), parent = self.itemTypeFilterBox)
		self.itemTypeHeader.SetText(locale.IKASHOP_SEARCH_SHOP_ITEM_TYPE_HEADER)

		self.itemTypeSelectButton = self.CreateWidget(ui.Button, pos = (85, 8), parent = self.itemTypeFilterBox)
		self.itemTypeSelectButton.SetUpVisual("ikashop/lite/search_shop/combo_box_button/default.png")
		self.itemTypeSelectButton.SetDownVisual("ikashop/lite/search_shop/combo_box_button/default.png")
		self.itemTypeSelectButton.SetOverVisual("ikashop/lite/search_shop/combo_box_button/hover.png")
		self.itemTypeSelectButton.SAFE_SetEvent(self._OnClickItemTypeSelectButton)

		self.itemTypeSelectComboBox = self.CreateWidget(IkarusShopComboBox, pos = (14 + 85, 72 + 28))
		self.itemTypeSelectComboBox.SetItems(self.ITEM_TYPES)
		self.itemTypeSelectComboBox.SetSelectItemEvent(self._OnSelectItemType)

		# item subtype filter
		self.itemSubTypeHeader = self.CreateWidget(ui.TextLine, pos = (6, 39), parent = self.itemTypeFilterBox)
		self.itemSubTypeHeader.SetText(locale.IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_HEADER)

		self.itemSubTypeSelectButton = self.CreateWidget(ui.Button, pos = (85, 8+26), parent = self.itemTypeFilterBox)
		self.itemSubTypeSelectButton.SetUpVisual("ikashop/lite/search_shop/combo_box_button/default.png")
		self.itemSubTypeSelectButton.SetDownVisual("ikashop/lite/search_shop/combo_box_button/default.png")
		self.itemSubTypeSelectButton.SetOverVisual("ikashop/lite/search_shop/combo_box_button/hover.png")
		self.itemSubTypeSelectButton.SAFE_SetEvent(self._OnClickItemSubTypeSelectButton)

		self.itemSubTypeSelectComboBox = self.CreateWidget(IkarusShopComboBox, pos = (14 + 86, 72 + 8 + 26 + 20))
		self.itemSubTypeSelectComboBox.SetSelectItemEvent(self._OnSelectItemSubType)
		self.itemSubTypeSelectComboBox.SetItems([locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT,])

		# item price filter
		self.itemPriceFilterBox = self.CreateWidget(ui.ExpandedImageBox, pos = (14, getBottom(self.itemTypeFilterBox) + 5))
		self.itemPriceFilterBox.LoadImage("ikashop/lite/search_shop/filter_box.png")

		self.itemPriceMinHeader = self.CreateWidget(ui.TextLine, pos = (6, 13), parent = self.itemPriceFilterBox)
		self.itemPriceMinHeader.SetText(locale.IKASHOP_SEARCH_SHOP_ITEM_PRICE_MIN_HEADER)

		self.itemPriceMaxHeader = self.CreateWidget(ui.TextLine, pos = (6, 39), parent = self.itemPriceFilterBox)
		self.itemPriceMaxHeader.SetText(locale.IKASHOP_SEARCH_SHOP_ITEM_PRICE_MAX_HEADER)

		self.itemPriceMinBox = self.CreateWidget(ui.ImageBox, pos = (64, 8), parent = self.itemPriceFilterBox)
		self.itemPriceMinBox.LoadImage("ikashop/lite/search_shop/input_box.png")

		self.itemPriceMaxBox = self.CreateWidget(ui.ImageBox, pos = (64, 8+26), parent = self.itemPriceFilterBox)
		self.itemPriceMaxBox.LoadImage("ikashop/lite/search_shop/input_box.png")

		self.itemPriceMinEdit = self.CreateWidget(ui.EditLine, pos = (6, 6), parent = self.itemPriceMinBox)
		self.itemPriceMinEdit.SetMax(12)
		self.itemPriceMinEdit.SetEscapeEvent(ui.__mem_func__(self.itemPriceMinEdit.KillFocus))
		self.itemPriceMinEdit.SetNumberMode()
		self.itemPriceMinBox.SetOnMouseLeftButtonUpEvent(self.itemPriceMinEdit.SetFocus)

		self.itemPriceMaxEdit = self.CreateWidget(ui.EditLine, pos = (6, 6), parent = self.itemPriceMaxBox)
		self.itemPriceMaxEdit.SetMax(12)
		self.itemPriceMaxEdit.SetEscapeEvent(ui.__mem_func__(self.itemPriceMaxEdit.KillFocus))
		self.itemPriceMaxEdit.SetNumberMode()
		self.itemPriceMaxBox.SetOnMouseLeftButtonUpEvent(self.itemPriceMaxEdit.SetFocus)

		# item level filter
		self.itemLevelFilterBox = self.CreateWidget(ui.ExpandedImageBox, pos = (14, getBottom(self.itemPriceFilterBox) + 5))
		self.itemLevelFilterBox.LoadImage("ikashop/lite/search_shop/filter_box.png")

		self.itemLevelMinHeader = self.CreateWidget(ui.TextLine, pos = (6, 13), parent = self.itemLevelFilterBox)
		self.itemLevelMinHeader.SetText(locale.IKASHOP_SEARCH_SHOP_ITEM_LEVEL_MIN_HEADER)

		self.itemLevelMaxHeader = self.CreateWidget(ui.TextLine, pos = (6, 39), parent = self.itemLevelFilterBox)
		self.itemLevelMaxHeader.SetText(locale.IKASHOP_SEARCH_SHOP_ITEM_LEVEL_MAX_HEADER)

		self.itemLevelMinBox = self.CreateWidget(ui.ImageBox, pos = (64, 8), parent = self.itemLevelFilterBox)
		self.itemLevelMinBox.LoadImage("ikashop/lite/search_shop/input_box.png")

		self.itemLevelMaxBox = self.CreateWidget(ui.ImageBox, pos = (64, 8+26), parent = self.itemLevelFilterBox)
		self.itemLevelMaxBox.LoadImage("ikashop/lite/search_shop/input_box.png")

		self.itemLevelMinEdit = self.CreateWidget(ui.EditLine, pos = (6, 6), parent = self.itemLevelMinBox)
		self.itemLevelMinEdit.SetMax(12)
		self.itemLevelMinEdit.SetEscapeEvent(ui.__mem_func__(self.itemLevelMinEdit.KillFocus))
		self.itemLevelMinEdit.SetNumberMode()
		self.itemLevelMinBox.SetOnMouseLeftButtonUpEvent(self.itemLevelMinEdit.SetFocus)

		self.itemLevelMaxEdit = self.CreateWidget(ui.EditLine, pos = (6, 6), parent = self.itemLevelMaxBox)
		self.itemLevelMaxEdit.SetMax(12)
		self.itemLevelMaxEdit.SetEscapeEvent(ui.__mem_func__(self.itemLevelMaxEdit.KillFocus))
		self.itemLevelMaxEdit.SetNumberMode()
		self.itemLevelMaxBox.SetOnMouseLeftButtonUpEvent(self.itemLevelMaxEdit.SetFocus)

		# item attributes filter
		self.attributeSettings = GetAttributeSettings()
		self.attributeBonusToItem = {bonus[0]:index for index, bonus in enumerate(self.attributeSettings)}

		self.itemAttrsFilterBox = self.CreateWidget(ui.ExpandedImageBox, pos = (14, getBottom(self.itemLevelFilterBox) + 5))
		self.itemAttrsFilterBox.LoadImage("ikashop/lite/search_shop/filter_box.png")
		self.itemAttrsFilterBox.SetScale(1.0, 126.0 / self.itemAttrsFilterBox.GetHeight())

		self.attrSelectButtons = []
		self.attrComboBoxes = []
		self.attrValueBoxes = []
		self.attrValueEdits = []

		for i in xrange(ikashop.FILTER_ATTRIBUTE_NUM):
			# select button
			attrSelectButton = self.CreateWidget(ui.Button, pos = (6, 6 + i*23), parent = self.itemAttrsFilterBox)
			attrSelectButton.SetUpVisual("ikashop/lite/search_shop/attribute_select_button/default.png")
			attrSelectButton.SetDownVisual("ikashop/lite/search_shop/attribute_select_button/default.png")
			attrSelectButton.SetOverVisual("ikashop/lite/search_shop/attribute_select_button/hover.png")
			attrSelectButton.SAFE_SetEvent(self._OnClickAttributeSelectButton, i)
			attrSelectButton.SetText("")
			bx, by = attrSelectButton.ButtonText.GetLocalPosition()
			attrSelectButton.ButtonText.SetPosition(bx - 10, by)
			self.attrSelectButtons.append(attrSelectButton)

			attrComboBox = self.CreateWidget(IkarusShopComboBox, pos = (14 + 6, self.itemAttrsFilterBox.GetLocalPosition()[1] + 5 + i*23 + 20))
			attrComboBox.SetSelectItemEvent(lambda id, text, _self = proxy(self), _num = i : _self._OnSelectAttributeItem(_num, id, text))
			attrComboBox.ChangeElementImages(largerComboBoxImages)
			attrComboBox.SetViewCount(7)
			attrComboBox.SetItems([text for apply, text in self.attributeSettings])
			self.attrComboBoxes.append(attrComboBox)

			attrValueBox = self.CreateWidget(ui.ImageBox, pos = (148, 6 + i*23), parent = self.itemAttrsFilterBox)
			attrValueBox.LoadImage("ikashop/lite/search_shop/attribute_value_box.png")
			self.attrValueBoxes.append(attrValueBox)

			attrValueEdit = self.CreateWidget(ui.EditLine, pos = (9, 6), parent = attrValueBox)
			attrValueEdit.SetMax(4)
			attrValueEdit.SetEscapeEvent(ui.__mem_func__(attrValueEdit.KillFocus))
			attrValueEdit.SetNumberMode()
			attrValueBox.SetOnMouseLeftButtonUpEvent(attrValueEdit.SetFocus)
			self.attrValueEdits.append(attrValueEdit)

		# special filters
		self.itemSpecialFilterBox = self.CreateWidget(ui.ExpandedImageBox, pos = (14, getBottom(self.itemAttrsFilterBox) + 5))
		self.itemSpecialFilterBox.LoadImage("ikashop/lite/search_shop/filter_box.png")

		self.itemAlchemyGradeHeader = self.CreateWidget(ui.TextLine, pos = (6, 13), parent = self.itemSpecialFilterBox)
		self.itemAlchemyGradeHeader.SetText(locale.IKASHOP_SEARCH_SHOP_ALCHEMY_GRADE_HEADER)

		self.itemAlchemyGradeSelectButton = self.CreateWidget(ui.Button, pos = (85, 8), parent = self.itemSpecialFilterBox)
		self.itemAlchemyGradeSelectButton.SetUpVisual("ikashop/lite/search_shop/combo_box_button/default.png")
		self.itemAlchemyGradeSelectButton.SetDownVisual("ikashop/lite/search_shop/combo_box_button/default.png")
		self.itemAlchemyGradeSelectButton.SetOverVisual("ikashop/lite/search_shop/combo_box_button/hover.png")
		self.itemAlchemyGradeSelectButton.SAFE_SetEvent(self._OnClickAlchemyGradeSelectButton)

		self.itemAlchemyGradeSelectComboBox = self.CreateWidget(IkarusShopComboBox, pos = (14 + 85, getBottom(self.itemAttrsFilterBox) + 5 + 8 + 20))
		self.itemAlchemyGradeSelectComboBox.SetSelectItemEvent(self._OnSelectAlchemyGradeType)
		self.itemAlchemyGradeSelectComboBox.SetItems(self.ALCHEMY_GRADES)

		self.itemSashAbsHeader = self.CreateWidget(ui.TextLine, pos = (6, 39), parent = self.itemSpecialFilterBox)
		self.itemSashAbsHeader.SetText(locale.IKASHOP_SEARCH_SHOP_SASH_ABSORB_HEADER)

		self.itemSashAbsSelectButton = self.CreateWidget(ui.Button, pos = (85, 8+26), parent = self.itemSpecialFilterBox)
		self.itemSashAbsSelectButton.SetUpVisual("ikashop/lite/search_shop/combo_box_button/default.png")
		self.itemSashAbsSelectButton.SetDownVisual("ikashop/lite/search_shop/combo_box_button/default.png")
		self.itemSashAbsSelectButton.SetOverVisual("ikashop/lite/search_shop/combo_box_button/hover.png")
		self.itemSashAbsSelectButton.SAFE_SetEvent(self._OnClickSashGradeSelectButton)

		self.itemSashAbsSelectComboBox = self.CreateWidget(IkarusShopComboBox, pos = (14 + 86, getBottom(self.itemAttrsFilterBox) + 5 + 8 + 26 + 20))
		self.itemSashAbsSelectComboBox.SetItems(self.SASH_ABSORBS)
		self.itemSashAbsSelectComboBox.SetSelectItemEvent(self._OnSelectSashGrade)
		self.itemSashAbsSelectComboBox.SetViewCount(4)

		self.auctionListButton = self.CreateWidget(ui.Button, pos = (14, getBottom(self.itemSpecialFilterBox) + 6))
		self.auctionListButton.SetUpVisual("ikashop/lite/search_shop/auction_list_button/default.png")
		self.auctionListButton.SetDownVisual("ikashop/lite/search_shop/auction_list_button/default.png")
		self.auctionListButton.SetOverVisual("ikashop/lite/search_shop/auction_list_button/hover.png")
		self.auctionListButton.SAFE_SetEvent(self._OnClickAuctionListButton)
		self.auctionListButton.SetText(locale.IKASHOP_SEARCH_SHOP_AUCTION_LIST_BUTTON_TEXT)
		tx, ty = self.auctionListButton.ButtonText.GetLocalPosition()
		self.auctionListButton.ButtonText.SetPosition(tx + 5, ty)
		self.auctionListButton.ButtonText.SetPackedFontColor(0xFFFFFFFF)

		hpos = (14 + self.itemSpecialFilterBox.GetWidth() - self.auctionListButton.GetWidth(), getBottom(self.itemSpecialFilterBox) + 6)
		self.historyButton = self.CreateWidget(ui.Button, pos = hpos)
		self.historyButton.SetUpVisual("ikashop/lite/search_shop/history_button/default.png")
		self.historyButton.SetDownVisual("ikashop/lite/search_shop/history_button/default.png")
		self.historyButton.SetOverVisual("ikashop/lite/search_shop/history_button/hover.png")
		self.historyButton.SAFE_SetEvent(self._OnClickHistoryButton)
		self.historyButton.SetText(locale.IKASHOP_SEARCH_SHOP_HISTORY_BUTTON_TEXT)
		tx, ty = self.historyButton.ButtonText.GetLocalPosition()
		self.historyButton.ButtonText.SetPosition(tx + 5, ty)
		self.historyButton.ButtonText.SetPackedFontColor(0xFFFFFFFF)

		self.resultBox = self.CreateWidget(ui.ExpandedImageBox, pos = (227, 40))
		self.resultBox.LoadImage("ikashop/lite/search_shop/result_box.png")
		self.resultBox.SetMouseWheelEvent(self._OnScrollMouseWheelResultItems)
		hs = float(self.resultBox.GetWidth() - 10) / self.resultBox.GetWidth()
		vs = 469.0 / self.resultBox.GetHeight()
		self.resultBox.SetScale(hs, vs)

		# making result items
		self.resultItems = []
		for i in xrange(self.RESULT_ITEM_VIEW_COUNT):
			item = self.CreateWidget(IkarusSearchShopItem, pos = (5, 4 + 116*i), parent = self.resultBox)
			item.SetSearchShopBoard(self)
			self.resultItems.append(item)

		# making result item scrollbar
		self.resultItemScrollBar = self.CreateWidget(ui.ScrollBar, pos = (self.resultBox.GetWidth() - 19, 3), parent = self.resultBox)
		self.resultItemScrollBar.SetScrollEvent(self._OnScrollResultItems)
		self.resultItemScrollBar.SetScrollBarSize(self.resultBox.GetHeight() - 6)

		self.comboBoxes = []
		for value in vars(self).values() + self.attrComboBoxes:
			if isinstance(value, IkarusShopComboBox):
				value.AddFlag("float")
				value.SetTop()
				value.SelectItem(0)
				self._RegisterDialog(value)
				self.comboBoxes.append(proxy(value))

		if app.EXTEND_IKASHOP_ULTIMATE:
			self.sortByPriceCheckbox = self.CreateWidget(IkashopCheckBox)
			self.sortByPriceCheckbox.SetImages("ikashop/ultimate/sort_checkbox/base.png", "ikashop/ultimate/sort_checkbox/checked.png")
			self.sortByPriceCheckbox.SetText(locale.IKASHOP_ULTIMATE_SORT_BY_PRICE_CHECKBOX)
			self.sortByPriceCheckbox.SetPosition(self.GetWidth() - 40 - self.sortByPriceCheckbox.GetWidth(), 7)
			self.sortByPriceCheckbox.SetCheckEvent(self._OnCheckSortByPriceCheckBox)

	def _ExtractFilterTypes(self):
		return \
			self.itemTypeSelectComboBox.GetSelectedItem(),\
			self.itemSubTypeSelectComboBox.GetSelectedItem()

	def _ExtractFilterPrice(self):
		minPrice = self.itemPriceMinEdit.GetText()
		minPrice = minPrice.lower().replace("k", "000")
		minPrice = long(minPrice) if minPrice and minPrice.isdigit() else long(0)
		maxPrice = self.itemPriceMaxEdit.GetText()
		maxPrice = maxPrice.lower().replace("k", "000")
		maxPrice = long(maxPrice) if maxPrice and maxPrice.isdigit() else long(0)
		return minPrice, maxPrice

	def _ExtractFilterLevel(self):
		minLevel = self.itemLevelMinEdit.GetText()
		minLevel = int(minLevel) if minLevel and minLevel.isdigit() else 0
		maxLevel = self.itemLevelMaxEdit.GetText()
		maxLevel = int(maxLevel) if maxLevel and maxLevel.isdigit() else 0
		return minLevel, maxLevel

	def _ExtractFilterAttributes(self):
		def extractOne(combo, edit):
			if combo.GetSelectedItem() == 0:
				return 0,0
			bonus = self.attributeSettings[combo.GetSelectedItem()][0]
			value = edit.GetText()
			value = int(value) if value and value.isdigit() else 0
			return bonus, value

		ret = tuple(extractOne(self.attrComboBoxes[i], self.attrValueEdits[i]) for i in xrange(ikashop.FILTER_ATTRIBUTE_NUM))
		return ret

	def _ExtractFilterSpecial(self):
		sashAbs = self.itemSashAbsSelectComboBox.GetSelectedItem()
		dssGrade = self.itemAlchemyGradeSelectComboBox.GetSelectedItem()
		return sashAbs, dssGrade

	def _ExtractFilterSettings(self):
		# getting values
		inputName = self.inputNameEdit.GetText()
		type, subtype = self._ExtractFilterTypes()
		prices = self._ExtractFilterPrice()
		levels = self._ExtractFilterLevel()
		attributes = self._ExtractFilterAttributes()
		specials = self._ExtractFilterSpecial()
		# making arg tuple
		args = (inputName, type, subtype, prices, levels, attributes, specials)
		if not IsUsingFilter(args):
			return None
		return args

	def _OnClickSearchButton(self):
		self.inputNameEdit.KillFocus()
		filters = self._ExtractFilterSettings()
		if filters is None:
			self.OpenPopupDialog(locale.IKASHOP_SEARCH_SHOP_NO_FILTER_USED)
			return
		ikashop.SendFilterRequest(*filters)

	def _OnClickAuctionListButton(self):
		self.auctionListBoard.Toggle()

	def _OnClickItemTypeSelectButton(self):
		for combo in self.comboBoxes:
			if not combo.IsMe(self.itemTypeSelectComboBox) and combo.IsShow():
				combo.Close()
		self.itemTypeSelectComboBox.Toggle()

	def _OnClickItemSubTypeSelectButton(self):
		for combo in self.comboBoxes:
			if not combo.IsMe(self.itemSubTypeSelectComboBox) and combo.IsShow():
				combo.Close()
		self.itemSubTypeSelectComboBox.Toggle()

	def _OnSelectItemType(self, index, text):
		self.itemTypeSelectButton.SetText(text)
		self.itemSubTypeSelectComboBox.SetItems(self.SUB_TYPES[index])
		self.itemSubTypeSelectComboBox.SelectItem(0)

	def _OnSelectItemSubType(self, index, text):
		self.itemSubTypeSelectButton.SetText(text)

	def _OnSelectAttributeItem(self, num, index, text):
		usingButton = self.attrSelectButtons[num]
		for i in xrange(100):
			btext = text[:-i] if i > 0 else text
			if i != 0:
				btext += ".."
			usingButton.SetText(btext)
			if usingButton.ButtonText.GetTextSize()[0] + 35 < usingButton.GetWidth():
				break

	def _OnClickAttributeSelectButton(self, num):
		usingComboBox = self.attrComboBoxes[num]
		for combo in self.comboBoxes:
			if not combo.IsMe(usingComboBox) and combo.IsShow():
				combo.Close()
		usingComboBox.Toggle()

	def _OnClickSashGradeSelectButton(self):
		for combo in self.comboBoxes:
			if not combo.IsMe(self.itemSashAbsSelectComboBox) and combo.IsShow():
				combo.Close()
		self.itemSashAbsSelectComboBox.Toggle()

	def _OnSelectSashGrade(self, index, text):
		self.itemSashAbsSelectButton.SetText(text)

	def _OnClickAlchemyGradeSelectButton(self):
		for combo in self.comboBoxes:
			if not combo.IsMe(self.itemAlchemyGradeSelectComboBox) and combo.IsShow():
				combo.Close()
		self.itemAlchemyGradeSelectComboBox.Toggle()

	def _OnSelectAlchemyGradeType(self, index, text):
		self.itemAlchemyGradeSelectButton.SetText(text)

	def _OnUpdateInputName(self, isFocus):
		if not isFocus or len(self.inputNameEdit.GetText()) < 3:
			self.inputNameSuggestion.Close()
			return

		text = self.inputNameEdit.GetText().lower()
		most_relevant = []
		less_relevant = []

		for name in self.itemNames:
			if name.startswith(text):
				most_relevant.append(name)
			elif text in name:
				less_relevant.append(name)

		most_relevant = sorted(most_relevant)
		less_relevant = sorted(less_relevant)
		suggestions = most_relevant + less_relevant

		self.inputNameSuggestion.SetItems(suggestions)
		if suggestions:
			self.inputNameSuggestion.Open()
		else:
			self.inputNameSuggestion.Close()

	def _OnSelectSuggestedItemName(self, index, name):
		self.inputNameEdit.SetText(name)
		self.inputNameEdit.KillFocus()

	def _OnClickResetFilters(self):
		for combo in self.comboBoxes:
			if not combo.IsMe(self.inputNameSuggestion):
				combo.SelectItem(0)
		# resetting edit line values
		self.itemPriceMinEdit.SetText("")
		self.itemPriceMaxEdit.SetText("")
		self.itemLevelMinEdit.SetText("")
		self.itemLevelMaxEdit.SetText("")
		self.inputNameEdit.SetText("")
		for edit in self.attrValueEdits:
			edit.SetText("")

	def _OnClickHistoryButton(self):
		self.historyFilterBoard.Toggle()

	def _OnScrollResultItems(self):
		self._RefreshResultItem()

	def _OnScrollMouseWheelResultItems(self, delta):
		self.resultItemScrollBar.OnDown() if delta < 0\
			else self.resultItemScrollBar.OnUp()
		return True

	def _RefreshResultItem(self):
		# calculating sindex
		pos = self.resultItemScrollBar.GetPos() if self.resultItemScrollBar.IsShow() else 0.0
		diff = max(len(self.items) - self.RESULT_ITEM_VIEW_COUNT, 0)
		sindex = int(diff * pos)
		eindex = sindex + min(len(self.items), self.RESULT_ITEM_VIEW_COUNT)

		# hiding all views
		for view in self.resultItems:
			view.Hide()

		for i in xrange(sindex, eindex):
			ri = i - sindex
			data = self.items[i]
			view = self.resultItems[ri]
			view.Setup(data)
			view.Show()
			view.SetAvailable() if data.get('deleted', 0) == 0 \
				else view.SetNotAvailable()

		# updating scrollbar's middlebar length
		self.resultItemScrollBar.UpdateScrollbarLenght(4 + 116*len(self.items))

	def _UpdateScrollbarState(self):
		self.resultItemScrollBar.Show() if self.RESULT_ITEM_VIEW_COUNT < len(self.items)\
			else self.resultItemScrollBar.Hide()
		self.resultItemScrollBar.SetPos(0)

	def _ApplySearchFilterSettings(self, settings):
		# setting up name
		self.inputNameEdit.SetText(settings['name'])
		# setting up prices
		self.itemPriceMaxEdit.SetText(str(settings['price_max']) if settings['price_max'] != 0 else "")
		self.itemPriceMinEdit.SetText(str(settings['price_min']) if settings['price_min'] != 0 else "")
		# setting up levels
		self.itemLevelMaxEdit.SetText(str(settings['level_max']) if settings['level_max'] != 0 else "")
		self.itemLevelMinEdit.SetText(str(settings['level_min']) if settings['level_min'] != 0 else "")
		# setting up comboboxes
		self.itemTypeSelectComboBox.SelectItem(settings['type'])
		self.itemSubTypeSelectComboBox.SelectItem(settings['subtype'])
		self.itemSashAbsSelectComboBox.SelectItem(settings['sash'])
		self.itemAlchemyGradeSelectComboBox.SelectItem(settings['alchemy'])
		# setting up attributes
		for attrComboBox, attrEdit, sett in zip(self.attrComboBoxes, self.attrValueEdits, settings['attrs']):
			type, value = sett
			attrEdit.SetText(str(value) if value != 0 else "")
			attrComboBox.SelectItem(self.attributeBonusToItem[type])

	def HistoryRedoSearch(self, settings):
		self._ApplySearchFilterSettings(settings)
		self._OnClickSearchButton()

	def Open(self):
		now = app.GetTime()
		if self.lastOpen == 0 or now - self.lastOpen > 60 or len(self.items) == 0:
			ikashop.SendRandomSearchFillRequest()
			self._IsRandomFilling = True
			return

		self.lastOpen = now
		self.Show()
		self.SetTop()

	def Close(self):
		self.Hide()
		self.inputNameEdit.KillFocus()

	def DeleteSearchResultItem(self, id):
		for item in self.items:
			if item['id'] == id:
				item['deleted'] = 1

		for view in self.resultItems:
			if view.GetId() == id:
				view.SetNotAvailable()

	if app.EXTEND_IKASHOP_ULTIMATE:
		def RequestOpenSellerShop(self, owner, vnum, count, price):
			if not self.sortByPriceCheckbox.IsEnabled():
				self.OpenPopupDialog(locale.IKASHOP_ULTIMATE_SORT_BY_PRICE_PREMIUM_FEATURE)
				return
			self.markItemInfo = vnum, count, price
			ikashop.SendOpenShop(owner)

		def _OnSortByPrice(self):
			priceGetter = lambda item : item['price'] + item.get('cheque', 0) * YANG_PER_CHEQUE
			self.items = sorted(self.items, key = priceGetter) if self.sortByPriceCheckbox.IsChecked() \
				else self.shuffleItem
			self._RefreshResultItem()

		def _OnCheckSortByPriceCheckBox(self):
			if not self.sortByPriceCheckbox.IsEnabled():
				self.OpenPopupDialog(locale.IKASHOP_ULTIMATE_SORT_BY_PRICE_PREMIUM_FEATURE)
				return
			self._OnSortByPrice()

		def ActiveSortByPriceFeature(self):
			self.sortByPriceCheckbox.Enable()
			self.sortByPriceCheckbox.Check(callback=0)

		def DeactiveSortByPriceFeature(self):
			self.sortByPriceCheckbox.Disable()
			self.sortByPriceCheckbox.Uncheck(callback=1)

	# BINARY CALLS
	def SetSearchResultItems(self, items):
		shuffle(items)
		self.items = items
		if app.EXTEND_IKASHOP_ULTIMATE:
			self.shuffleItem = items
		self._UpdateScrollbarState()
		if self.IsShow() == False:
			self.Show()
			self.SetTop()
			self.lastOpen = app.GetTime()
		if not self._IsRandomFilling:
			self.RegisterHistoryFilter()
		self._IsRandomFilling = False

	def OpenShopGuest(self, data):
		self.shopGuestBoard.Open(data)
		if self.markItemInfo:
			vnum, count, price = self.markItemInfo
			self.shopGuestBoard.MarkItems(vnum, count, price)

	def ShopExpiredGuesting(self, id):
		self.shopGuestBoard.CheckExpiring(id)

	def ShopGuestRemoveItem(self, itemid):
		self.shopGuestBoard.ShopGuestRemoveItem(itemid)

	def ShopGuestEditItem(self, itemid, price):
		self.shopGuestBoard.EditItem(itemid, price)

	def OpenAuctionGuest(self, data):
		self.auctionGuestBoard.Open(data)

	def SetAuctionList(self, auctions):
		self.auctionListBoard.SetAuctions(auctions)

	def RegisterHistoryFilter(self):
		filter = self._ExtractFilterSettings()
		ikashop.RegisterFilterHistory(len(self.items), *filter)
		self.historyFilterBoard.SetFilters(ikashop.GetFilterHistory())

	if app.EXTEND_IKASHOP_PRO:
		def SetOpenWhisper(self, event):
			self.openWhisperEvent = event

		def OpenWhisper(self, name):
			self.openWhisperEvent(name)

		def SetOpenWhisperText(self, event):
			self.openWhisperTextEvent = event

		def OpenWhisperText(self, name, text):
			if self.openWhisperTextEvent:
				self.openWhisperTextEvent(name, text)
			else:
				self.openWhisperEvent(name)

	if SEARCH_SHOP_RENEWAL:
		_OpenDefault = Open

		def _SettingUpBoard(self):
			self.SetSize(780, 558)
			ui.Window.SetSize(self, 780, 596)
			self.SetTitleName(locale.IKASHOP_SEARCH_SHOP_BOARD_TITLE)
			self.SetCloseEvent(self.Close)
			self.SetCenterPosition()
			self.AddFlag("movable")
			self.AddFlag("float")

		def _LoadSearchShopWindow(self):
			self._LoadLinkedBoard()
			self._IsRandomFilling = False
			SEARCH_SALES["board"] = proxy(self)	# offer rows open whispers through the search board
			self.page = 0
			self.rowOffset = 0
			self.cart = []
			self.allItems = []
			self.countSort = 0

			# --- search bar: name (8, 30) 149x24, history (156, 30), reset (179, 30), search (202, 30)
			self.inputNameBox = self.CreateWidget(ui.ImageBox, pos = (8, 30))
			self.inputNameBox.LoadImage(SEARCH_UI + "search_bg.png")
			self.inputNameEdit = self.CreateWidget(ui.EditLine, pos = (6, 6), size = (137, 16), parent = self.inputNameBox)
			self.inputNameEdit.SetMax(ikashop.FILTER_NAME_MAX_LEN)
			self.inputNameEdit.SetEscapeEvent(ui.__mem_func__(self.inputNameEdit.KillFocus))
			self.inputNameEdit.SetReturnEvent(ui.__mem_func__(self._OnClickSearchButton))
			self.inputNameEdit.SetFocusUpdateEvent(self._OnUpdateInputName)
			self.inputNameBox.SetOnMouseLeftButtonUpEvent(self.inputNameEdit.SetFocus)
			SearchEscapeOnlyWhenFocused(self.inputNameEdit)
			self.inputNamePlaceHolder = self.CreateWidget(ui.TextLine, pos = (6, 6), parent = self.inputNameBox)
			self.inputNamePlaceHolder.SetText(locale.IKASHOP_SEARCH_ITEM_NAME)
			self.inputNamePlaceHolder.SetPackedFontColor(0xFF8A8079)
			self.inputNamePlaceHolder.AddFlag("not_pick")

			self.inputNameSuggestion = self.CreateWidget(IkarusShopComboBox, pos = (8, 54))
			self.inputNameSuggestion.SetSelectItemEvent(self._OnSelectSuggestedItemName)
			self.inputNameSuggestion.SetViewCount(6)
			self.inputNameSuggestion.SetItems(["",])

			self.historyButton = SearchButton(self, "btn_history", 156, 30, self._OnClickHistoryButton)
			self.historyButton.SetToolTipText(locale.IKASHOP_SEARCH_SHOP_HISTORY_BUTTON_TEXT)
			self.resetFilterButton = SearchButton(self, "btn_delsearch", 179, 30, self._OnClickResetFilters)
			self.resetFilterButton.SetToolTipText(locale.IKASHOP_SEARCH_SHOP_RESET_FILTER_BUTTON_TEXT)
			self.searchButton = SearchButton(self, "btn_search", 202, 30, self._OnClickSearchButton)
			self.searchButton.SetToolTipText(locale.IKASHOP_SEARCH_SHOP_SEARCH_BUTTON_TEXT)

			# --- options: exact search / player name (8, 54) 218x58
			self.exactSearchBackground = self.CreateWidget(ui.ImageBox, pos = (8, 54))
			self.exactSearchBackground.LoadImage(SEARCH_UI + "bg_exactsearch.png")
			self.exactSearchCheckbox = self.CreateWidget(SearchShopCheckBox, pos = (13, 59))
			self.exactSearchCheckbox.SetChecked(False)
			self.exactSearchCheckbox.SetEvent(lambda checked, s = proxy(self): s.playerNameSearchCheckbox.SetChecked(False) if checked else None)
			self.playerNameSearchCheckbox = self.CreateWidget(SearchShopCheckBox, pos = (13, 85))
			self.playerNameSearchCheckbox.SetChecked(False)
			self.playerNameSearchCheckbox.SetEvent(lambda checked, s = proxy(self): s.exactSearchCheckbox.SetChecked(False) if checked else None)
			self.searchOptionLabels = []
			for (y, text) in ((63, locale.IKASHOP_SEARCH_SHOP_EXACT_SEARCH), (89, locale.IKASHOP_SEARCH_SHOP_SEARCH_PLAYER_NAME)):
				label = self.CreateWidget(ui.TextLine, pos = (41, y))
				label.SetText(text)
				self.searchOptionLabels.append(label)

			# --- tabs (8, 112) 110x30 / (118, 112) 109x30
			self.tabButtons = []
			for (i, (image, text)) in enumerate((("tab_categ_list", locale.IKASHOP_SEARCH_CATEGORIES), ("tab_filter_list", locale.IKASHOP_SEARCH_FILTERS))):
				tab = ui.RadioButton()
				tab.SetParent(self)
				tab.SetUpVisual(SEARCH_UI + image + ".png")
				tab.SetOverVisual(SEARCH_UI + image + "_hover.png")
				tab.SetDownVisual(SEARCH_UI + image + "_active.png")
				tab.SetPosition(8 + 110 * i, 112)
				tab.SetText(text)
				tab.SAFE_SetEvent(self._SearchSelectTab, i)
				tab.Show()
				self.tabButtons.append(tab)

			# --- left panel (8, 142) 218x410: category list / filter window
			self.leftPanelBackground = self.CreateWidget(ui.ImageBox, pos = (8, 142))
			self.leftPanelBackground.LoadImage(SEARCH_UI + "bg_categ_filters.png")
			self.category_list = self.CreateWidget(SearchShopCategoryList, pos = (8, 142))
			self.category_list.SetEvent(self._SearchOnSelectCategory)
			self.category_list.changeEvent = ui.__mem_func__(self._SearchClearCart)
			self.filterSearchWindow = self.CreateWidget(ui.Window, pos = (0, 0), size = (230, 560), show = False)
			self.filterSearchWindow.AddFlag("not_pick")
			self._SearchLoadFilterWindow()

			self.itemTypeSelectComboBox = self.CreateWidget(IkarusShopComboBox, show = False)
			self.itemTypeSelectComboBox.SetItems([""] * 64)
			self.itemSubTypeSelectComboBox = self.CreateWidget(IkarusShopComboBox, show = False)
			self.itemSubTypeSelectComboBox.SetItems([""] * 16)
			self.itemPriceMinEdit = self.CreateWidget(ui.EditLine, show = False)
			self.itemPriceMaxEdit = self.CreateWidget(ui.EditLine, show = False)

			# --- result header (227, 29) 548x31: Adet / Esya adi / Fiyat / Fiyat Degerlendirmesi / Islem, count sort
			self.resultHeader = self.CreateWidget(ui.ImageBox, pos = (227, 29))
			self.resultHeader.LoadImage(SEARCH_UI + "header_big.png")
			self.result_headers = []
			for (x, text) in ((263, locale.IKASHOP_SEARCH_COUNT), (352, locale.IKASHOP_SEARCH_ITEM_NAME), (524, locale.IKASHOP_SEARCH_SHOP_PRICE_TITLE),
					(644, locale.IKASHOP_SEARCH_SHOP_PRICE_RATING_HEADER), (732, locale.IKASHOP_SEARCH_ACTION)):
				header = self.CreateWidget(ui.TextLine, pos = (x, 38))
				header.SetHorizontalAlignCenter()
				header.SetText(text)
				header.SetPackedFontColor(0xFFFFFFFF)
				self.result_headers.append(header)
			self.countSortUpButton = SearchButton(self, "btn_count_up", 229, 31, lambda s = proxy(self): s._SearchSortCount(1))
			self.countSortDownButton = SearchButton(self, "btn_count_down", 229, 44, lambda s = proxy(self): s._SearchSortCount(-1))
			self.priceRatingInfoButton = self.CreateWidget(SearchHoverArea, pos = (592, 29), size = (105, 30))
			self.priceRatingInfoButton.SetEvents(self._SearchShowRatingInfo, self._SearchHideRatingInfo)
			self.ratingInfoToolTip = uitooltip.ToolTip()
			self.ratingInfoToolTip.HideToolTip()

			# --- result area (227, 60) 542x492, rows, thin scrollbar (770, 61)
			self.boardBox = self.CreateWidget(ui.ExpandedImageBox, pos = (227, 60))
			self.boardBox.LoadImage(SEARCH_UI + "bg_main1.png")
			self.boardBox.SetMouseWheelEvent(self._OnScrollMouseWheelResultItems)
			self.no_results_text = self.CreateWidget(ui.TextLine, pos = (271, 238), parent = self.boardBox)
			self.no_results_text.SetHorizontalAlignCenter()
			self.no_results_text.SetFontName("Tahoma:14b")
			self.no_results_text.SetPackedFontColor(SEARCH_TEXT_COLOR)
			self.no_results_text.SetText(locale.IKASHOP_NO_ITEMS_FOUNDS)
			self.no_results_text.Hide()
			self.searchLoading = self.CreateWidget(ui.ExpandedImageBox, pos = (473, 277), show = False)
			self.searchLoading.LoadImage("d:/ymir work/ui/game/common/loading_image.tga")
			self.searchLoading.SetOrigin(25, 28)
			self.searchLoading.AddFlag("not_pick")
			self.searchLoadingStart = None
			self.searchLoadingReady = False
			self.searchLoadingRotation = 0.0
			self.searchLoadingTick = 0.0
			self.peekWindow = self.CreateWidget(ui.Window, pos = (227, 60), size = (542, SEARCH_RESULT_HEIGHT))
			self.peekWindow.SetInsideRender(True)
			self.peekWindow.SetMouseWheelEvent(self._OnScrollMouseWheelResultItems)
			self.resultItems = []
			for i in xrange(SEARCH_PAGE_SIZE):
				row = self.CreateWidget(IkarusSearchShopRow, pos = (0, 0), parent = self.peekWindow, show = False)
				row.SetSearchShopBoard(self)
				row.SetCartEvent(self._SearchOnCartChange)
				row.SetMouseWheelEvent(self._OnScrollMouseWheelResultItems)
				if app.ENABLE_CLIP_MASKING:
					row.SetClippingMaskWindow(self.peekWindow)
				self.resultItems.append(row)
			self.scrollTrack = self.CreateWidget(ui.Bar, pos = (770, 61), size = (1, 489))
			self.scrollTrack.SetColor(0xFF3B3328)
			self.scrollThumb = self.CreateWidget(ui.Bar, pos = (771, 61), size = (3, 40), show = False)
			self.scrollThumb.SetColor(0xFF8C7A5E)
			self.resultItemScrollBar = self.CreateWidget(ui.ScrollBar, show = False)	# compatibility

			# --- cart (231, 489): two columns of bg_itemcart_1slot_noitemicon 223x22, total (689, 486), buy (689, 530)
			self.cartRows = []
			self.cartScroll = 0
			self.cartView = self.CreateWidget(ui.Window, pos = (229, 489), size = (449, SEARCH_CART_VIEW), show = False)
			self.cartView.SetInsideRender(True)
			self.cartView.SetMouseWheelEvent(self._SearchCartWheel)
			self.cartScrollFrame = self.CreateWidget(ui.Bar, pos = (678, 490), size = (7, 59), show = False)
			self.cartScrollFrame.SetColor(0xFF565656)
			self.cartScrollTrack = self.CreateWidget(ui.Bar, pos = (1, 1), size = (5, 57), parent = self.cartScrollFrame)
			self.cartScrollTrack.SetColor(0xFF000000)
			self.cartScrollThumb = self.CreateWidget(ui.Bar, pos = (0, 0), size = (5, 20), parent = self.cartScrollTrack)
			self.cartScrollThumb.SetColor(0xFF49443C)
			self.cartScrollFrame.SetMouseWheelEvent(self._SearchCartWheel)
			self.cartOffset = 0
			self.totalYangInput = self.CreateWidget(ui.ImageBox, pos = (687, 486), show = False)
			self.totalYangInput.LoadImage(SEARCH_UI + "yang_total_leftside.png")
			self.totalYangLabel = self.CreateWidget(ui.TextLine, pos = (43, 4), parent = self.totalYangInput)
			self.totalYangLabel.SetHorizontalAlignCenter()
			self.totalYangLabel.SetText(locale.IKASHOP_SEARCH_TOTAL_YANG)
			self.totalYangLabel.SetPackedFontColor(0xFFC7C7C7)
			self.totalYangLabel.SetFontName("Tahoma:12b")
			self.totalYangLabel.SetText(locale.IKASHOP_SEARCH_TOTAL_YANG)
			self.totalYangText = self.CreateWidget(ui.TextLine, pos = (43, 27), parent = self.totalYangInput)
			self.totalYangText.SetHorizontalAlignCenter()
			self.totalYangText.SetText("0")
			self.buy_selected_button = SearchButton(self, "btn_buy", 687, 530, self._SearchOnClickBuySelected, text = locale.IKASHOP_SEARCH_BUY)
			self.buy_selected_button.SetToolTipText(locale.IKASHOP_SEARCH_SHOP_BUY_SELECTED_TOOLTIP)
			self.buy_selected_button.Hide()

			# --- pages: bottom lip (391, 542) 394x48, first (466, 561), prev (488, 561), 6 numbers (506 + 37i, 556), next (736), last (754)
			self.bottomLip = self.CreateWidget(ui.ExpandedImageBox, pos = (391, 540))
			self.bottomLip.LoadImage(SEARCH_UI + "bottom_lip.png")
			self.bottomLip.SetRenderingRect(0.0, -float(SEARCH_LIP_HIDDEN) / self.bottomLip.GetHeight(), 0.0, 0.0)
			self.bottomLip.AddFlag("not_pick")
			PS = "ikashop/sama/private_search/"
			self.pageNavButtons = []
			for (name, x, w, event) in (("btn_first_left", 466, 14, lambda s = proxy(self): s._SearchGoPage(0)),
					("btn_next_left", 488, 10, lambda s = proxy(self): s._SearchGoPage(s.page - 1)),
					("btn_next_right", 736, 10, lambda s = proxy(self): s._SearchGoPage(s.page + 1)),
					("btn_first_right", 754, 14, lambda s = proxy(self): s._SearchGoPage(s._SearchPageCount() - 1))):
				btn = ui.Button()
				btn.SetParent(self)
				btn.SetUpVisual(PS + name + "_normal.png")
				btn.SetOverVisual(PS + name + "_over.png")
				btn.SetDownVisual(PS + name + "_down.png")
				btn.SetPosition(x, 561)
				btn.SetEvent(event)
				btn.Show()
				self.pageNavButtons.append(btn)
			self.page_buttons = []
			for i in xrange(6):
				btn = ui.Button()
				btn.SetParent(self)
				btn.SetUpVisual(SEARCH_UI + "btn_pagenumber.png")
				btn.SetOverVisual(SEARCH_UI + "btn_pagenumber_hover.png")
				btn.SetDownVisual(SEARCH_UI + "btn_pagenumber_clicked.png")
				btn.SetPosition(506 + 37 * i, 556)
				btn.SetText(str(i + 1))
				btn.Show()
				self.page_buttons.append(btn)

			self.comboBoxes = []
			for value in vars(self).values() + self.attrComboBoxes:
				if isinstance(value, (IkarusShopComboBox, SearchDropdown)) and not any(value is c for c in (self.itemTypeSelectComboBox, self.itemSubTypeSelectComboBox)):
					value.AddFlag("float")
					value.SetTop()
					value.SelectItem(0)
					self._RegisterDialog(value)
					self.comboBoxes.append(proxy(value))
			for combo in self.comboBoxes:
				combo.Close()

			if app.EXTEND_IKASHOP_ULTIMATE:
				self.sortByPriceCheckbox = self.CreateWidget(IkashopCheckBox, show = False)
				self.sortByPriceCheckbox.SetImages("ikashop/ultimate/sort_checkbox/base.png", "ikashop/ultimate/sort_checkbox/checked.png")
				self.sortByPriceCheckbox.Check(0)

			self._SearchSelectTab(0)
			self._SearchRefreshPages()

		def _SearchLoadFilterWindow(self):
			self.filterWidgets = []
			self.filterKeep = []

			def add(widget):
				self.filterWidgets.append(widget)
				return widget

			def keep(widget):
				self.filterKeep.append(widget)
				return widget

			def header(y, text):
				box = add(self.CreateWidget(ui.ImageBox, pos = (8, y)))
				box.LoadImage(SEARCH_UI + "bg_filtertitle.png")
				line = keep(self.CreateWidget(ui.TextLine, pos = (109, 8), parent = box))
				line.SetFontName("Tahoma:12b")
				line.SetHorizontalAlignCenter()
				line.SetText(text)
				line.SetPackedFontColor(0xFFFFFFFF)

			header(142, locale.IKASHOP_SEARCH_SHOP_FILTER_SETTINGS)
			self.numericEdits = []
			for (x, y, placeholder, maxLen) in (
					(12, 174, locale.IKASHOP_SEARCH_SHOP_ITEM_LEVEL_MIN_HEADER, 3), (118, 174, locale.IKASHOP_SEARCH_SHOP_ITEM_LEVEL_MAX_HEADER, 3),
					(12, 201, locale.IKASHOP_SEARCH_SHOP_ITEM_COUNT_MIN_HEADER, 4), (118, 201, locale.IKASHOP_SEARCH_SHOP_ITEM_COUNT_MAX_HEADER, 4),
					(12, 228, locale.IKASHOP_SEARCH_SHOP_REFINE_MIN_HEADER, 2), (118, 228, locale.IKASHOP_SEARCH_SHOP_REFINE_MAX_HEADER, 2)):
				box = add(self.CreateWidget(ui.ExpandedImageBox, pos = (x, y)))
				box.LoadImage(SEARCH_UI + "bg_settings1.png")
				edit = self.CreateWidget(ui.EditLine, pos = (5, 6), size = (94, 16), parent = box)
				edit.SetMax(maxLen)
				edit.SetNumberMode()
				edit.SetEscapeEvent(ui.__mem_func__(edit.KillFocus))
				SearchEscapeOnlyWhenFocused(edit)
				box.SetOnMouseLeftButtonUpEvent(edit.SetFocus)
				hint = self.CreateWidget(ui.TextLine, pos = (5, 6), parent = box)
				hint.SetText(placeholder)
				hint.SetPackedFontColor(0xFF8A8079)
				hint.AddFlag("not_pick")
				self.numericEdits.append((edit, hint))
			self.itemLevelMinEdit = self.numericEdits[0][0]
			self.itemLevelMaxEdit = self.numericEdits[1][0]
			self.itemCountMinEdit = self.numericEdits[2][0]
			self.itemCountMaxEdit = self.numericEdits[3][0]
			self.itemRefineMinEdit = self.numericEdits[4][0]
			self.itemRefineMaxEdit = self.numericEdits[5][0]

			def selectButton(x, y, width, text, event):
				btn = add(ui.Button())
				btn.SetParent(self)
				image = SEARCH_UI + ("bg_settings1.png" if width == 104 else "bg_bonusfilter.png")
				btn.SetUpVisual(image)
				btn.SetOverVisual(image)
				btn.SetDownVisual(image)
				btn.SetPosition(x, y)
				btn.SetText(text)
				btn.ButtonText.SetHorizontalAlignLeft()
				btn.ButtonText.SetPosition(5, 12)
				SearchSetEvent(btn, event)
				btn.Show()
				if width == 104:
					arrow = keep(self.CreateWidget(ui.ImageBox, pos = (88, 9), parent = btn))
					arrow.LoadImage("ikashop/sama/private_search/categories/arrow_down.png")
					arrow.AddFlag("not_pick")
				return btn

			def dropdown(x, y, width, items, event, viewCount = 5, searchable = False):
				combo = SearchDropdown(width, viewCount, searchable)
				combo.SetParent(self)
				combo.SetPosition(x, y)
				combo.SetItems(items)
				combo.SetSelectItemEvent(event)
				combo.Hide()
				return combo

			alchemy = (locale.IKASHOP_SEARCH_SHOP_ALCHEMY_GRADE_HEADER, locale.IKASHOP_SEARCH_SHOP_ALCHEMY_GRADE_VALUE_MATTE,
				locale.IKASHOP_SEARCH_SHOP_ALCHEMY_GRADE_VALUE_CLEAR, locale.IKASHOP_SEARCH_SHOP_ALCHEMY_GRADE_VALUE_FLAWLESS,
				locale.IKASHOP_SEARCH_SHOP_ALCHEMY_GRADE_VALUE_BRILLIANT, locale.IKASHOP_SEARCH_SHOP_ALCHEMY_GRADE_VALUE_EXCELLENT)
			self.itemAlchemyGradeSelectButton = selectButton(12, 255, 104, alchemy[0], lambda s = proxy(self): s._SearchToggleCombo(s.itemAlchemyGradeSelectComboBox))
			self.itemAlchemyGradeSelectComboBox = dropdown(12, 279, 104, alchemy, lambda i, t, s = proxy(self): s._SearchOnSelectCombo(s.itemAlchemyGradeSelectButton, t))
			sash = (locale.IKASHOP_SEARCH_SHOP_SASH_ABSORB_HEADER, locale.IKASHOP_SEARCH_SHOP_SASH_GRADE_VALUE0, locale.IKASHOP_SEARCH_SHOP_SASH_GRADE_VALUE1,
				locale.IKASHOP_SEARCH_SHOP_SASH_GRADE_VALUE2, locale.IKASHOP_SEARCH_SHOP_SASH_GRADE_VALUE3)
			self.itemSashAbsSelectButton = selectButton(118, 255, 104, sash[0], lambda s = proxy(self): s._SearchToggleCombo(s.itemSashAbsSelectComboBox))
			self.itemSashAbsSelectComboBox = dropdown(118, 279, 104, sash, lambda i, t, s = proxy(self): s._SearchOnSelectCombo(s.itemSashAbsSelectButton, t))
			rare = (locale.IKASHOP_FILTER_RARE_TITLE, locale.IKASHOP_FILTER_RARE_NONE, locale.IKASHOP_FILTER_RARE_ONE, locale.IKASHOP_FILTER_RARE_TWO)
			self.SEARCH_TIME_DAYS = (0, 2, 7, 14, 30)
			times = (locale.IKASHOP_FILTER_TIME_TITLE,) + tuple(locale.IKASHOP_FILTER_TIME_DAYS.format(d) for d in self.SEARCH_TIME_DAYS[1:])
			self.rareBonusSelectButton = selectButton(12, 282, 104, rare[0], lambda s = proxy(self): s._SearchToggleCombo(s.rareBonusComboBox))
			self.rareBonusComboBox = dropdown(12, 306, 104, rare, lambda i, t, s = proxy(self): s._SearchOnSelectCombo(s.rareBonusSelectButton, t))
			self.timeItemSelectButton = selectButton(118, 282, 104, times[0], lambda s = proxy(self): s._SearchToggleCombo(s.timeItemComboBox))
			self.timeItemComboBox = dropdown(118, 306, 104, times, lambda i, t, s = proxy(self): s._SearchOnSelectCombo(s.timeItemSelectButton, t))

			# Bonus: rows (12, 342 + 27i) 188x24, value (146, 6) inside, clear (200)
			header(309, locale.IKASHOP_SEARCH_SHOP_FILTER_BONUS)
			self.attributeSettings = GetAttributeSettings()
			self.attributeBonusToItem = {bonus[0]: index for index, bonus in enumerate(self.attributeSettings)}
			names = [locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT] + [text for apply, text in self.attributeSettings][1:]
			self.attrSelectButtons = []
			self.attrComboBoxes = []
			self.attrValueEdits = []
			self.attrClearButtons = []
			for i in xrange(ikashop.FILTER_ATTRIBUTE_NUM):
				y = 342 + 27 * i
				btn = selectButton(12, y, 188, locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT, lambda s = proxy(self), n = i: s._OnClickAttributeSelectButton(n))
				combo = dropdown(12, y + 24, 198, names, lambda idx, text, s = proxy(self), n = i: s._OnSelectAttributeItem(n, idx, text), 5, True)
				edit = self.CreateWidget(ui.EditLine, pos = (146, 6), size = (36, 16), parent = btn)
				edit.SetMax(4)
				edit.SetNumberMode()
				edit.SetEscapeEvent(ui.__mem_func__(edit.KillFocus))
				SearchEscapeOnlyWhenFocused(edit)
				clear = add(SearchButton(self, "btn_delfilters", 200, y, lambda s = proxy(self), n = i: s._SearchClearAttribute(n)))
				clear.SetToolTipText(locale.IKASHOP_SEARCH_CLEAR_BONUS)
				if i >= SEARCH_BONUS_ROWS:
					btn.Hide()
					clear.Hide()
				self.attrSelectButtons.append(btn)
				self.attrComboBoxes.append(combo)
				self.attrValueEdits.append(edit)
				self.attrClearButtons.append(clear)

			# class + sex icons (12 + 37i, 478) 30x30, *_on.png while selected
			self.filterRace = 0
			self.filterSex = 0
			self.classButtons = []
			for (i, (name, kind, value)) in enumerate((("filter_war", "race", 1), ("filter_sura", "race", 2), ("filter_ninja", "race", 3),
					("filter_shaman", "race", 4), ("filter_male", "sex", 1), ("filter_female", "sex", 2))):
				btn = add(ui.Button())
				btn.SetParent(self)
				btn.SetUpVisual(SEARCH_UI + name + ".png")
				btn.SetOverVisual(SEARCH_UI + name + "_on.png")
				btn.SetDownVisual(SEARCH_UI + name + "_on.png")
				btn.SetPosition(12 + 37 * i, 478)
				btn.SAFE_SetEvent(self._SearchToggleClass, kind, value)
				btn.Show()
				self.classButtons.append((btn, name, kind, value))

			reset = add(SearchButton(self, "btn_reset_filters", 12, 513, self._OnClickResetFilters, text = locale.IKASHOP_SEARCH_RESET_FILTERS))
			icon = keep(self.CreateWidget(ui.ImageBox, pos = (54, 7), parent = reset))
			icon.LoadImage(SEARCH_UI + "reset_filter_icon.png")
			icon.AddFlag("not_pick")

		def _SearchSelectTab(self, index):
			self.searchTab = index
			for (i, tab) in enumerate(self.tabButtons):
				tab.Down() if i == index else tab.SetUp()
			for combo in self.comboBoxes:
				combo.Close()
			if index == 0:
				self.category_list.Show()
				for widget in self.filterWidgets:
					widget.Hide()
			else:
				self.category_list.Hide()
				for widget in self.filterWidgets:
					widget.Show()
				for (i, (btn, clear)) in enumerate(zip(self.attrSelectButtons, self.attrClearButtons)):
					if i >= SEARCH_BONUS_ROWS:
						btn.Hide()
						clear.Hide()

		def _SearchToggleClass(self, kind, value):
			if kind == "race":
				self.filterRace = 0 if self.filterRace == value else value
			else:
				self.filterSex = 0 if self.filterSex == value else value
			self._SearchRefreshClassButtons()

		def _SearchRefreshClassButtons(self):
			for (btn, name, kind, value) in self.classButtons:
				active = (self.filterRace if kind == "race" else self.filterSex) == value
				btn.SetUpVisual(SEARCH_UI + name + ("_on.png" if active else ".png"))

		def _SearchRefreshCategoryFilters(self):
			pass

		def _SearchToggleCombo(self, combo):
			for other in self.comboBoxes:
				if not other.IsMe(combo) and other.IsShow():
					other.Close()
			combo.Close() if combo.IsShow() else combo.Open()

		def _SearchOnSelectCombo(self, button, text):
			button.SetText(text)
			button.ButtonText.SetHorizontalAlignLeft()
			button.ButtonText.SetPosition(5, 12)

		def _OnClickAttributeSelectButton(self, num):
			self._SearchToggleCombo(self.attrComboBoxes[num])

		def _OnSelectAttributeItem(self, num, index, text):
			btn = self.attrSelectButtons[num]
			btn.SetText(text if index != 0 else locale.IKASHOP_SEARCH_SHOP_SELECT_AN_ELEMENT)
			btn.ButtonText.SetHorizontalAlignLeft()
			btn.ButtonText.SetPosition(5, 12)
			if index == 0:
				self.attrValueEdits[num].SetText("")

		def _SearchClearAttribute(self, num):
			self.attrComboBoxes[num].SelectItem(0)

		def _SearchOnSelectCategory(self):
			(category, sub) = self.category_list.GetSelection()
			if self.lastCategory and (category, sub) != self.lastCategory and self.cart:
				self.cart = []
				self._RefreshResultItem()
			self.lastCategory = (category, sub)
			self.itemTypeSelectComboBox.selectedItem = category
			self.itemSubTypeSelectComboBox.selectedItem = sub
			if category == 0 and self._ExtractFilterSettings() is None:
				self._SearchQueue(ikashop.SendRandomSearchFillRequest, True)
				return
			self._OnClickSearchButton()

		def _SearchQueue(self, send, random = False):
			self.pendingSearch = (send, random)
			self._SearchFlushQueue()

		def Open(self):
			self._IsRandomFilling = False
			self._OpenDefault()
			if self._IsRandomFilling:
				self.lastSearchSent = app.GetTime()
				self.lastSearch = (ikashop.SendRandomSearchFillRequest, True)
				self._SearchStartLoading()

		def _SearchCartRow(self, index):
			while len(self.cartRows) <= index:
				row = self.CreateWidget(ui.ImageBox, parent = self.cartView, show = False)
				row.LoadImage(SEARCH_UI + "bg_itemcart_1slot_noitemicon.png")
				text = self.CreateWidget(ui.TextLine, pos = (6, 4), parent = row)
				text.SetPackedFontColor(SEARCH_TEXT_COLOR)
				remove = SearchButton(row, "btn_delitemcart", 203, 4)
				remove.SetToolTipText(locale.IKASHOP_SEARCH_REMOVE_CART)
				row.SetMouseWheelEvent(self._SearchCartWheel)
				text.SetMouseWheelEvent(self._SearchCartWheel)
				remove.SetMouseWheelEvent(self._SearchCartWheel)
				if app.ENABLE_CLIP_MASKING:
					row.SetClippingMaskWindow(self.cartView)
				self.cartRows.append((row, text, remove))
			return self.cartRows[index]

		def _SearchCartWheel(self, delta):
			self.cartScroll += -SEARCH_CART_STEP if delta > 0 else SEARCH_CART_STEP
			self._SearchRefreshCart()
			return True

		def _SearchClearCart(self):
			if self.cart:
				self.cart = []
				self._RefreshResultItem()

		def SearchSeller(self, name):
			if not self.IsShow():
				self.Show()
			self.SetTop()
			self.inputNameEdit.SetText(name)
			self.exactSearchCheckbox.SetChecked(False)
			self.playerNameSearchCheckbox.SetChecked(True)
			self.category_list.Select(0, 0)
			self._OnClickSearchButton()

		def _SearchIsLoading(self):
			return self.searchLoadingStart is not None

		def _SearchStartLoading(self):
			if not self.searchLoading:
				return
			self.searchLoadingStart = app.GetTime()
			self.searchLoadingReady = False
			self.searchLoading.Show()
			self.searchLoading.SetTop()
			self._RefreshResultItem()

		def _SearchUpdateLoading(self):
			now = app.GetTime()
			if not self._SearchIsLoading():
				self.searchLoadingTick = now
				return
			self.searchLoadingRotation = (self.searchLoadingRotation + SEARCH_LOADING_SPEED * max(0.0, now - self.searchLoadingTick)) % 360.0
			self.searchLoadingTick = now
			self.searchLoading.SetRotation(self.searchLoadingRotation)
			elapsed = now - self.searchLoadingStart
			if (self.searchLoadingReady and elapsed >= SEARCH_LOADING_MIN) or elapsed >= SEARCH_LOADING_TIMEOUT:
				self.searchLoadingStart = None
				self.searchLoading.Hide()
				self._RefreshResultItem()

		def _SearchFlushQueue(self):
			pending = self.pendingSearch
			if not pending:
				return
			now = app.GetTime()
			if now - self.lastSearchSent < SEARCH_MIN_INTERVAL:
				return
			(send, random) = pending
			self.pendingSearch = None
			self.lastSearch = pending
			self.lastSearchSent = now
			self._IsRandomFilling = random
			send()
			self._SearchStartLoading()

		def _OnClickSearchButton(self):
			self.inputNameEdit.KillFocus()
			filters = self._ExtractFilterSettings()
			if filters is None:
				self.OpenPopupDialog(locale.IKASHOP_SEARCH_SHOP_NO_FILTER_USED)
				return
			self._SearchQueue(lambda f = filters: ikashop.SendFilterRequest(*f))

		def _ExtractFilterTypes(self):
			return self.category_list.GetSelection()

		def _ExtractFilterSettings(self):
			name = self.inputNameEdit.GetText()
			if name and self.playerNameSearchCheckbox.IsChecked():
				name = "@" + name
			elif name and self.exactSearchCheckbox.IsChecked():
				name = "=" + name
			(type, subtype) = self._ExtractFilterTypes()
			args = (name, type, subtype, self._ExtractFilterPrice(), self._ExtractFilterLevel(), self._ExtractFilterAttributes(), self._ExtractFilterSpecial())
			if not IsUsingFilter(args):
				return None
			return args

		def _OnClickResetFilters(self):
			self.inputNameEdit.SetText("")
			self.exactSearchCheckbox.SetChecked(False)
			self.playerNameSearchCheckbox.SetChecked(False)
			self.category_list.Select(0, 0)
			self.itemTypeSelectComboBox.selectedItem = 0
			self.itemSubTypeSelectComboBox.selectedItem = 0
			for (edit, hint) in self.numericEdits:
				edit.SetText("")
			for combo in (self.itemAlchemyGradeSelectComboBox, self.itemSashAbsSelectComboBox, self.rareBonusComboBox, self.timeItemComboBox):
				combo.SelectItem(0)
			for i in xrange(len(self.attrComboBoxes)):
				self.attrComboBoxes[i].SelectItem(0)
				self.attrValueEdits[i].SetText("")
			self.filterRace = 0
			self.filterSex = 0
			self._SearchRefreshClassButtons()

		def _ApplySearchFilterSettings(self, settings):
			name = settings['name']
			self.exactSearchCheckbox.SetChecked(name.startswith("="))
			self.playerNameSearchCheckbox.SetChecked(name.startswith("@"))
			self.inputNameEdit.SetText(name[1:] if name[:1] in ("=", "@") else name)
			self.itemLevelMaxEdit.SetText(str(settings['level_max']) if settings['level_max'] != 0 else "")
			self.itemLevelMinEdit.SetText(str(settings['level_min']) if settings['level_min'] != 0 else "")
			self.category_list.Select(settings['type'], settings['subtype'])
			self.itemTypeSelectComboBox.selectedItem = settings['type']
			self.itemSubTypeSelectComboBox.selectedItem = settings['subtype']
			self.itemSashAbsSelectComboBox.SelectItem(settings['sash'])
			self.itemAlchemyGradeSelectComboBox.SelectItem(settings['alchemy'])
			for (attrComboBox, attrEdit, sett) in zip(self.attrComboBoxes, self.attrValueEdits, settings['attrs']):
				(type, value) = sett
				attrComboBox.SelectItem(self.attributeBonusToItem.get(type, 0))
				attrEdit.SetText(str(value) if value != 0 else "")

		def _SearchPassClientFilters(self, data):
			def number(edit):
				text = edit.GetText()
				return int(text) if text.isdigit() else 0
			(cmin, cmax) = (number(self.itemCountMinEdit), number(self.itemCountMaxEdit))
			if (cmin and data['count'] < cmin) or (cmax and data['count'] > cmax):
				return False
			item.SelectItem(data['vnum'])
			(rmin, rmax) = (number(self.itemRefineMinEdit), number(self.itemRefineMaxEdit))
			if rmin or rmax:
				if item.GetItemType() not in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
					return False
				refine = data['vnum'] % 10
				if (rmin and refine < rmin) or (rmax and refine > rmax):
					return False
			flags = (None, item.ITEM_ANTIFLAG_WARRIOR, item.ITEM_ANTIFLAG_SURA, item.ITEM_ANTIFLAG_ASSASSIN, item.ITEM_ANTIFLAG_SHAMAN)
			if self.filterRace and item.IsAntiFlag(flags[self.filterRace]):
				return False
			if self.filterSex == 1 and item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
				return False
			if self.filterSex == 2 and item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
				return False
			rare = self.rareBonusComboBox.GetSelectedItem()
			if rare:
				attrs = data.get('attrs', ())
				count = len([1 for (t, v) in attrs[5:7] if t != 0]) if len(attrs) >= 7 else 0
				if count != rare - 1:
					return False
			days = self.SEARCH_TIME_DAYS[self.timeItemComboBox.GetSelectedItem()]
			if days and data.get('duration', 0) < days * 24 * 60:
				return False
			return True

		def SetSearchResultItems(self, items):
			shuffle(items)
			self.allItems = [data for data in items if self._SearchPassClientFilters(data)]
			if self.countSort:
				self.allItems.sort(key = lambda d: d['count'], reverse = self.countSort < 0)
			self.items = self.allItems
			if app.EXTEND_IKASHOP_ULTIMATE:
				self.shuffleItem = items
			self.page = 0
			self.rowOffset = 0
			self.searchLoadingReady = True
			self._RefreshResultItem()
			if self.IsShow() == False:
				self.Show()
				self.SetTop()
				self.lastOpen = app.GetTime()
			if not self._IsRandomFilling:
				self.RegisterHistoryFilter()
			self._IsRandomFilling = False

		def _SearchSortCount(self, direction):
			self.countSort = direction
			self.allItems.sort(key = lambda d: d['count'], reverse = direction < 0)
			self.items = self.allItems
			self.rowOffset = 0
			self._RefreshResultItem()

		def _SearchPageCount(self):
			return max(1, (len(self.allItems) + SEARCH_PAGE_SIZE - 1) / SEARCH_PAGE_SIZE)

		def _SearchGoPage(self, page):
			page = max(0, min(page, self._SearchPageCount() - 1))
			if page == self.page:
				return
			self.page = page
			self.rowOffset = 0
			self._RefreshResultItem()

		def _SearchRefreshPages(self):
			count = self._SearchPageCount()
			first = max(0, min(self.page - 2, count - len(self.page_buttons)))
			for (i, btn) in enumerate(self.page_buttons):
				number = first + i
				if number >= count:
					btn.Hide()
					continue
				btn.SetText(str(number + 1))
				btn.SetUpVisual(SEARCH_UI + ("btn_pagenumber_active.png" if number == self.page else "btn_pagenumber.png"))
				btn.SAFE_SetEvent(self._SearchGoPage, number)
				btn.Show()

		def _SearchPageHeights(self):
			heights = []
			for data in self.allItems[self.page * SEARCH_PAGE_SIZE:(self.page + 1) * SEARCH_PAGE_SIZE]:
				item.SelectItem(data['vnum'])
				heights.append(SEARCH_ROW_HEIGHTS[max(1, min(3, item.GetItemSize()[1]))] + 1)
			return heights

		def _RefreshResultItem(self):
			pageItems = self.allItems[self.page * SEARCH_PAGE_SIZE:(self.page + 1) * SEARCH_PAGE_SIZE]
			visible = SEARCH_RESULT_HEIGHT_CART if self.cart else SEARCH_RESULT_HEIGHT
			self.peekWindow.SetSize(542, visible)
			heights = self._SearchPageHeights()
			total = sum(heights)
			self.rowOffset = max(0, min(self.rowOffset, max(0, total - visible)))
			cartIds = set(entry['id'] for entry in self.cart)
			y = 0
			for (i, row) in enumerate(self.resultItems):
				if i >= len(pageItems):
					row.Hide()
					continue
				top = y - self.rowOffset
				y += heights[i]
				if top + heights[i] <= 0 or top >= visible:
					row.Hide()
					continue
				data = pageItems[i]
				row.Setup(data)
				row.SetInCart(data['id'] in cartIds)
				row.SetPosition(0, top)
				row.SetAvailable() if data.get('deleted', 0) == 0 else row.SetNotAvailable()
				if not app.ENABLE_CLIP_MASKING:
					slotTop = top + 10
					slotBottom = slotTop + 32 * row.slotHeight
					row.slot.Hide() if (slotTop < 0 or slotBottom > visible) else row.slot.Show()
				row.Show()
			self.no_results_text.Show() if not pageItems else self.no_results_text.Hide()
			if self._SearchIsLoading():
				for row in self.resultItems:
					row.Hide()
				self.no_results_text.Hide()
			# thin scrollbar
			if total > visible and pageItems:
				trackHeight = visible - 2
				size = max(12, trackHeight * visible / total)
				self.scrollThumb.SetSize(3, size)
				self.scrollThumb.SetPosition(771, 61 + (trackHeight - size) * self.rowOffset / max(1, total - visible))
				self.scrollThumb.Show()
			else:
				self.scrollThumb.Hide()
			self.scrollTrack.SetSize(1, visible - 2)
			self._SearchRefreshPages()
			self._SearchRefreshCart()

		def _OnScrollMouseWheelResultItems(self, delta):
			self.rowOffset += -SEARCH_WHEEL_STEP if delta > 0 else SEARCH_WHEEL_STEP
			self._RefreshResultItem()
			return True

		def _UpdateScrollbarState(self):
			self.rowOffset = 0

		def _SearchOnCartChange(self, data, checked):
			self.cart = [entry for entry in self.cart if entry['id'] != data['id']]
			value = data['price'] + data.get('cheque', 0) * YANG_PER_CHEQUE
			if checked and data.get('deleted', 0) == 0 and value > 0:
				self.cart.append(data)
				if SearchPriceRating(value, data.get('priceavg', 0)) == 1:
					if not self.overpricedDialog:
						self.overpricedDialog = SearchOverpricedDialog()
					board = SearchWeak(self)
					self.overpricedDialog.Open([data], data['count'], value, None, set([data['id']]), board,
						lambda b = board, i = data['id']: b._SearchRemoveFromCart(i))
			self._RefreshResultItem()

		def _SearchRefreshCart(self):
			show = bool(self.cart)
			content = ((len(self.cart) + 1) / 2) * SEARCH_CART_STEP + 2
			maxScroll = max(0, content - SEARCH_CART_VIEW)
			self.cartScroll = max(0, min(self.cartScroll, maxScroll))
			for (i, data) in enumerate(self.cart):
				(row, text, remove) = self._SearchCartRow(i)
				y = (i / 2) * SEARCH_CART_STEP - self.cartScroll
				row.SetPosition((i % 2) * 224, y)
				item.SelectItem(data['vnum'])
				text.SetText("%dx %s" % (max(1, data['count']), item.GetItemName()))
				remove.SAFE_SetEvent(self._SearchRemoveFromCart, data['id'])
				row.Show() if (y + 22 > 0 and y < SEARCH_CART_VIEW) else row.Hide()
			for (row, text, remove) in self.cartRows[len(self.cart):]:
				row.Hide()
			self.cartView.Show() if show else self.cartView.Hide()
			if show and maxScroll > 0:
				size = max(6, 57 * SEARCH_CART_VIEW / content)
				self.cartScrollThumb.SetSize(5, size)
				self.cartScrollThumb.SetPosition(0, (57 - size) * self.cartScroll / maxScroll)
				self.cartScrollFrame.Show()
			else:
				self.cartScrollFrame.Hide()
			total = sum(entry['price'] + entry.get('cheque', 0) * YANG_PER_CHEQUE for entry in self.cart)
			self.totalYangText.SetText(locale.NumberToString(total))
			self.totalYangText.SetPackedFontColor(SEARCH_TOTAL_COLOR)
			for widget in (self.totalYangInput, self.buy_selected_button):
				widget.Show() if show else widget.Hide()

		def _SearchRemoveFromCart(self, id):
			self.cart = [entry for entry in self.cart if entry['id'] != id]
			self._RefreshResultItem()

		def _SearchOnClickBuySelected(self):
			if not self.cart:
				self.OpenPopupDialog(locale.IKASHOP_SEARCH_SHOP_MULTIBUY_SELECT_AT_LEAST_ONE)
				return
			total = sum(entry['price'] + entry.get('cheque', 0) * YANG_PER_CHEQUE for entry in self.cart)
			overpriced = set(entry['id'] for entry in self.cart
				if SearchPriceRating(abs(entry['price'] + entry.get('cheque', 0) * YANG_PER_CHEQUE), entry.get('priceavg', 0)) == 1)
			if not self.overpricedDialog:
				self.overpricedDialog = SearchOverpricedDialog()
			self.overpricedDialog.Open(self.cart, len(self.cart), total, self._SearchOnAcceptBuySelected, overpriced or None, SearchWeak(self))

		def _SearchOnAcceptBuySelected(self):
			for entry in self.cart:
				ikashop.SendBuyItem(entry['owner'], entry['id'], entry['price'] + entry.get('cheque', 0) * YANG_PER_CHEQUE)
			self.cart = []
			if self.questionDialog:
				self.questionDialog.Hide()
			if self.overpricedDialog:
				self.overpricedDialog.Close()
			self._RefreshResultItem()

		def _SearchShowRatingInfo(self):
			tip = self.ratingInfoToolTip
			tip.ClearToolTip()
			tip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_PRICE_RATING_HEADER, SEARCH_HEADER_COLOR)
			tip.AutoAppendTextLine(locale.IKASHOP_PRICE_RATING_INFO_DESC)
			tip.AppendSpace(4)
			for rating in (5, 4, 3, 2, 1):
				tip.AutoAppendTextLine(SearchLocale(SEARCH_RATING_TEXTS[rating]))
			tip.AlignHorizonalCenter()
			tip.ShowToolTip()

		def _SearchHideRatingInfo(self):
			self.ratingInfoToolTip.HideToolTip()

		def DeleteSearchResultItem(self, id):
			self.allItems = [data for data in self.allItems if data['id'] != id]
			self.items = self.allItems
			self.page = min(self.page, self._SearchPageCount() - 1)
			self.cart = [entry for entry in self.cart if entry['id'] != id]
			self._RefreshResultItem()

		def _SearchOnUpdatePlaceHolder(self):
			self.inputNamePlaceHolder.Hide() if (self.inputNameEdit.GetText() or self.inputNameEdit.IsFocus()) else self.inputNamePlaceHolder.Show()
			for (edit, hint) in self.numericEdits:
				hint.Hide() if (edit.GetText() or edit.IsFocus()) else hint.Show()

		def OnUpdate(self):
			self._SearchFlushQueue()
			self._SearchUpdateLoading()
			if self.inputNamePlaceHolder:
				self._SearchOnUpdatePlaceHolder()

if app.EXTEND_IKASHOP_ULTIMATE:
	class IkarusShopSkinListView(IkarusShopWindow):
		def __init__(self):
			super(IkarusShopSkinListView, self).__init__()
			self._LoadIkarusShopSkinListView()

		def _LoadIkarusShopSkinListView(self):
			self.button = self.CreateWidget(ui.Button)
			self.button.SetUpVisual("ikashop/ultimate/skin_select_button/default.png")
			self.button.SetOverVisual("ikashop/ultimate/skin_select_button/hover.png")
			self.button.SetDownVisual("ikashop/ultimate/skin_select_button/default.png")
			self.button.SetText("")
			self.button.ButtonText.SetPackedFontColor(0xFFFFFFFF)
			self.button.ButtonText.SetHorizontalAlignLeft()
			self.button.ButtonText.SetPosition(20, self.button.GetHeight()/2)
			self.SetSize(self.button.GetWidth(), self.button.GetHeight())

		def Setup(self, data):
			index, name = data
			self.button.SetText(name)
			self.index = index

		def SetOnClick(self, event):
			self.button.SAFE_SetEvent(event, proxy(self))


	class IkarusShopSkinBoard(IkarusShopListBoard):

		SKIN_VIEW_COUNT = 6
		SHOP_SKIN_COUNT = 7

		def __init__(self):
			self.selected = None
			super(IkarusShopSkinBoard, self).__init__()
			ikashop.SetShopSkinBoard(self)
			self._SettingUpBoard()
			self._LoadIkarusShopSkinBoard()

		def _SettingUpBoard(self):
			# setting list board
			self.SetSize(500, 260)
			super(IkarusShopSkinBoard, self)._SettingUpBoard()
			self.SetTitleName(locale.IKASHOP_ULTIMATE_SHOP_SKIN_BOARD_TITLE)

		def Destroy(self):
			ikashop.SetShopSkinBoard(None)
			super(IkarusShopSkinBoard, self).Destroy()

		def _LoadIkarusShopSkinBoard(self):
			ui.Window.SetSize(self, 500, 220)
			super(IkarusShopSkinBoard, self)._LoadIkarusShopListBoard()
			ui.Window.SetSize(self, 500, 260)

			self._MakeListElements(IkarusShopSkinListView, self.SKIN_VIEW_COUNT)
			for view in self.views:
				view.SetPosition(196, view.GetLocalPosition()[1])
				view.SetOnClick(self._OnClickView)

			self.skinImage = self.CreateWidget(ui.ImageBox, x = 10, y = 37)

			self.acceptButton = self.CreateWidget(ui.Button, pos = (346 - 65 - 5, 225))
			self.acceptButton.SetUpVisual("ikashop/lite/search_shop/buy_button/default.png")
			self.acceptButton.SetDownVisual("ikashop/lite/search_shop/buy_button/default.png")
			self.acceptButton.SetOverVisual("ikashop/lite/search_shop/buy_button/hover.png")
			self.acceptButton.SAFE_SetEvent(self._OnClickAcceptButton)
			self.acceptButton.SetText(locale.IKASHOP_OFFER_LIST_ACCEPT_OFFER_BUTTON_TEXT)

			self.cancelButton = self.CreateWidget(ui.Button, pos = (346 + 4 + self.acceptButton.GetWidth() - 65 + 5, 225))
			self.cancelButton.SetUpVisual("ikashop/lite/search_shop/offer_button/default.png")
			self.cancelButton.SetDownVisual("ikashop/lite/search_shop/offer_button/default.png")
			self.cancelButton.SetOverVisual("ikashop/lite/search_shop/offer_button/hover.png")
			self.cancelButton.SAFE_SetEvent(self._OnClickCancelButton)
			self.cancelButton.SetText(locale.IKASHOP_OFFER_LIST_CANCEL_OFFER_BUTTON_TEXT)

		def Open(self):
			images = ["ikashop/ultimate/decoration/{}.png".format(i+1) for i in xrange(self.SHOP_SKIN_COUNT)]
			names = [locale.IKASHOP_ULTIMATE_SHOP_SKIN_NAME.format(i+1) for i in xrange(self.SHOP_SKIN_COUNT)]
			self.data = [{'name' : name, 'image' : image} for name, image in zip(names,images)]

			self.Show()
			self.SetTop()
			self.SetElements([(index, name) for index, name in enumerate(names)])
			self._SelectElement(0)
			self.elementScrollbar.SetPos(0)

		def Close(self):
			self.Hide()

		def _OnClickView(self, view):
			self._SelectElement(view.index)
			self._RefreshElements()

		def _SelectElement(self, index):
			image = self.data[index]['image']
			name = "|cFFFFFF99|h"+self.data[index]['name']+"|r"

			if self.selected != None:
				self.elements[self.selected] = (self.selected, self.data[self.selected]['name'])

			self.skinImage.LoadImage(image)
			self.elements[index] = (index,name)
			self.selected = index

		def _OnClickAcceptButton(self):
			message = locale.IKASHOP_ULTIMATE_SHOP_SKIN_USAGE_QUESTION
			self.OpenQuestionDialog(message, self._OnAcceptSkinUsageQuestion)

		def _OnClickCancelButton(self):
			self.Close()

		def _OnAcceptSkinUsageQuestion(self):
			self.questionDialog.Hide()
			self.Close()
			ikashop.SendShopDecorationUse(self.selected+1)


#######################################################################################################################
# board 780x558: search bar, exact / player name options, Kategoriler | Filtreler tabs, category list, filter window,
#######################################################################################################################
SEARCH_UI = "d:/ymir work/ui/game/searchshop/"
SEARCH_PAGE_SIZE = 10
SEARCH_RESULT_TOP = 60
SEARCH_RESULT_HEIGHT = 491
SEARCH_RESULT_HEIGHT_CART = 425
SEARCH_ROW_HEIGHTS = {1: 52, 2: 84, 3: 120}
SEARCH_BONUS_ROWS = 5
SEARCH_MIN_INTERVAL = 1.1
SEARCH_WHEEL_STEP = 26
SEARCH_LIP_HIDDEN = 14
SEARCH_PRICE_COIN = " |Eemoji/gold|e"
SEARCH_OVERPRICED_COLOR = 0xFFFF7777
SEARCH_TEXT_COLOR = 0xFFCABDAB
SEARCH_TOTAL_COLOR = 0xFFFFD600
SEARCH_WARN_ORANGE = 0xFFFFAA55
SEARCH_WARN_GOLD = 0xFFC79E65
SEARCH_CART_STEP = 20
SEARCH_LOADING_MIN = 0.5
SEARCH_LOADING_TIMEOUT = 5.0
SEARCH_LOADING_SPEED = 360.0			# degrees per second
SEARCH_CART_VIEW = 59
SEARCH_HEADER_COLOR = 0xFFE8D5B5
SEARCH_CATEGORY_FIRST = 32

SEARCH_CATEGORIES = (
	("IKASHOP_SEARCH_ALL_ITEMS", "all_1.png", 0, ()),
	("IKASHOP_SEARCH_SHOP_ITEM_TYPE_WEAPON", "sword_1.png", 32, (
		"IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_WEAPON_SWORD", "IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_WEAPON_TWOHANDED",
		"IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_WEAPON_DAGGER", "IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_WEAPON_BOW",
		"IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_WEAPON_BELL", "IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_WEAPON_FAN")),
	("IKASHOP_SEARCH_SHOP_ITEM_TYPE_EQUIPEMENT", "armor_1.png", 33, (
		"IKASHOP_SEARCH_SHOP_ITEM_TYPE_ARMOR", "IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_JEWEL_HELM",
		"IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_JEWEL_SHIELD", "IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_JEWEL_EAR",
		"IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_JEWEL_NECK", "IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_JEWEL_WRIST",
		"IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_JEWEL_SHOES", "IKASHOP_SEARCH_SHOP_ITEM_TYPE_BELT",
		"IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_COSTUME_SASH")),
	("IKASHOP_SEARCH_SHOP_ITEM_TYPE_COSTUME", "costumes_1.png", 34, (
		"IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_COSTUME_BODY", "IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_COSTUME_WEAPON",
		"IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_COSTUME_HAIR", "IKASHOP_SEARCH_SHOP_ITEM_SUBTYPE_COSTUME_SASH",
		"IKASHOP_SEARCH_SHOP_ITEM_TYPE_MOUNT", "IKASHOP_SEARCH_SHOP_ITEM_TYPE_PET")),
	("IKASHOP_SEARCH_SHOP_ITEM_TYPE_ALCHEMY", "potion_1.png", 35, (
		"IKASHOP_SEARCH_SHOP_DRAGON_SOUL_GRADE_NORMAL", "IKASHOP_SEARCH_SHOP_DRAGON_SOUL_GRADE_BRILLIANT",
		"IKASHOP_SEARCH_SHOP_DRAGON_SOUL_GRADE_RARE", "IKASHOP_SEARCH_SHOP_DRAGON_SOUL_GRADE_ANCIENT",
		"IKASHOP_SEARCH_SHOP_DRAGON_SOUL_GRADE_LEGENDARY", "IKASHOP_SEARCH_SHOP_DRAGON_SOUL_GRADE_MYTH")),
	("IKASHOP_SEARCH_SHOP_ITEM_TYPE_BOOK", "book_1.png", 36, ()),
	("IKASHOP_SEARCH_SHOP_ITEM_TYPE_STONE", "stone_1.png", 37, ()),
	("IKASHOP_SEARCH_SHOP_ITEM_TYPE_MINERALS", "piackaxe_1.png", 38, ()),
	("IKASHOP_SEARCH_SHOP_ITEM_TYPE_FISH", "fish_1.png", 39, ()),
	("IKASHOP_SEARCH_SHOP_ITEM_TYPE_UPGRADE", "craft_1.png", 40, ()),
)
SEARCH_CATEGORY_HAS_EQUIP_FILTERS = (32, 33)	# weapon / equipment: 6/7 bonus + remaining time, others: character + sex


def SearchLocale(key):
	return locale.GetText(key, key)


def SearchPriceRating(price, average):
	if price <= 0 or average <= 0:
		return 0
	ratio = float(price) / float(average)
	if ratio <= 0.95:
		return 5
	if ratio <= 1.10:
		return 4
	if ratio < 1.15:
		return 3
	if ratio < 1.20:
		return 2
	return 1


SEARCH_RATING_TEXTS = {
	5: "IKASHOP_PRICE_RATING_GREAT_DEAL", 4: "IKASHOP_PRICE_RATING_GOOD_DEAL", 3: "IKASHOP_PRICE_RATING_FAIR_PRICE",
	2: "IKASHOP_PRICE_RATING_ABOVE_AVERAGE", 1: "IKASHOP_PRICE_RATING_OVERPRICED", 0: "IKASHOP_PRICE_RATING_NO_DATA",
}


MULTIBUY_UI = "d:/ymir work/ui/game/offline_shop/search_shop/"


class SearchOverpricedDialog(ui.Board):
	PANEL = (10, 39, 329, 103)
	WARN_STEP = 54
	CONFIRM_STEP = 42
	WHEEL = 21
	BODY_COLOR = 0xFF241F19
	BORDER_COLOR = 0xFF433930
	STRIP_COLOR = 0xFF2A251D
	WARN_COLOR = 0xFF2B1713

	def __init__(self):
		ui.Board.__init__(self)
		self.AddFlag("float")
		self.owner = None
		self.listings = []
		self.itemToolTip = uitooltip.ItemToolTip()
		self.itemToolTip.HideToolTip()
		self.acceptEvent = None
		self.keep = []
		self.entries = []
		self.heights = []
		self.scroll = 0
		self.count = 0
		self.background = ui.ImageBox()
		self.background.SetParent(self)
		self.background.AddFlag("not_pick")
		self.background.LoadImage(MULTIBUY_UI + "background_multibuy.png")
		self.background.SetPosition(5, 4)
		self.background.Show()
		self.title = self._Text(177, 24, "", SEARCH_TEXT_COLOR, center = True, bold = True)
		(x, y, w, h) = self.PANEL
		self.listBackground = ui.ImageBox()
		self.listBackground.SetParent(self)
		self.listBackground.LoadImage(MULTIBUY_UI + "multibuy_background_list.png")
		self.listBackground.SetPosition(x, y)
		self.listBackground.Show()
		self.panel = ui.Window()
		self.panel.SetParent(self.listBackground)
		self.panel.SetPosition(1, 1)
		self.panel.SetSize(w - 2, h - 2)
		self.panel.SetMouseWheelEvent(self._OnWheel)
		self.panel.Show()
		self.listBackground.SetMouseWheelEvent(self._OnWheel)
		self.viewHeight = h - 2
		self.view = ui.Window()
		self.view.SetParent(self.panel)
		self.view.SetPosition(0, 0)
		self.view.SetSize(w - 2, self.viewHeight)
		self.view.SetInsideRender(True)
		self.view.SetMouseWheelEvent(self._OnWheel)
		self.view.Show()
		self.scrollFrame = self._Bar(320, 3, 4, self.viewHeight - 6, 0xFF565656, parent = self.panel)
		self.scrollTrack = self._Bar(1, 1, 2, self.viewHeight - 8, 0xFF000000, parent = self.scrollFrame)
		self.scrollThumb = self._Bar(0, 0, 2, 20, 0xFF49443C, parent = self.scrollTrack)
		self.total = self._Text(177, 162, "", SEARCH_TEXT_COLOR, center = True, bold = True)
		self.acceptButton = self._Button("accept", 104, 178, self._OnAccept)
		self.cancelButton = self._Button("cancel", 194, 178, self._OnCancel)
		self.cancelEvent = None
		self.SetSize(355, 214)

	def __del__(self):
		ui.Board.__del__(self)

	def _Bar(self, x, y, w, h, color, parent = None):
		bar = ui.Bar()
		bar.SetParent(parent if parent else self)
		bar.SetPosition(x, y)
		bar.SetSize(w, h)
		bar.SetColor(color)
		bar.Show()
		self.keep.append(bar)
		return bar

	def _Text(self, x, y, text, color, center = False, bold = False, parent = None):
		line = ui.TextLine()
		line.SetParent(parent if parent else self)
		if bold:
			line.SetFontName("Tahoma:12b")
		if center:
			line.SetHorizontalAlignCenter()
		line.SetVerticalAlignCenter()
		line.SetPosition(x, y)
		line.SetPackedFontColor(color)
		line.SetText(text)
		line.Show()
		self.keep.append(line)
		return line

	def _Button(self, name, x, y, event):
		btn = ui.Button()
		btn.SetParent(self)
		btn.SetPosition(x, y)
		btn.SetUpVisual("d:/ymir work/ui/game/common/button_%s_norm.png" % name)
		btn.SetOverVisual("d:/ymir work/ui/game/common/button_%s_hover.png" % name)
		btn.SetDownVisual("d:/ymir work/ui/game/common/button_%s_down.png" % name)
		btn.SetEvent(ui.__mem_func__(event))
		btn.Show()
		return btn

	def _Entry(self, index):
		while len(self.entries) <= index:
			bg = self._Bar(0, 0, 316, 2, self.STRIP_COLOR, parent = self.view)
			bg.SetMouseWheelEvent(self._OnWheel)
			box = ui.Window()
			box.SetParent(self.view)
			box.SetSize(316, self.CONFIRM_STEP)
			box.SetMouseWheelEvent(self._OnWheel)
			box.SetOverInEvent(ui.__mem_func__(self._ShowItemToolTip), index)
			box.SetOverOutEvent(ui.__mem_func__(self._HideItemToolTip))
			box.Show()
			self.keep.append(box)
			icon = ui.ExpandedImageBox()
			icon.SetParent(box)
			icon.AddFlag("not_pick")
			icon.Show()
			self.keep.append(icon)
			name = self._Text(46, 21, "", SEARCH_TEXT_COLOR, parent = box)
			price = self._Text(300, 21, "", SEARCH_TEXT_COLOR, parent = box)
			unit = self._Text(8, 36, "", SEARCH_WARN_ORANGE, parent = box)
			self.entries.append({"box": box, "icon": icon, "name": name, "price": price, "unit": unit, "bg": bg, "warn": False, "cells": 1})
		return self.entries[index]

	def Open(self, listings, count, total, acceptEvent, overpricedIds = None, owner = None, cancelEvent = None):
		self.acceptEvent = acceptEvent
		self.cancelEvent = cancelEvent
		self.owner = owner
		overpricedIds = overpricedIds or set()
		listings = [d for d in listings if d['id'] in overpricedIds] + [d for d in listings if d['id'] not in overpricedIds]
		self.listings = listings
		self.count = len(listings)
		self.heights = [self.WARN_STEP if d['id'] in overpricedIds else self.CONFIRM_STEP for d in listings]
		self.scroll = 0
		if overpricedIds:
			self.title.SetText(SearchLocale("IKASHOP_SEARCH_OVERPRICED_TITLE").format(len(overpricedIds)))
			self.title.SetPackedFontColor(SEARCH_OVERPRICED_COLOR)
		else:
			self.title.SetText(SearchLocale("IKASHOP_SEARCH_BUY_CONFIRM_TITLE"))
			self.title.SetPackedFontColor(SEARCH_TEXT_COLOR)
		yang = SearchLocale("IKASHOP_SEARCH_YANG_FORMAT")
		scrolling = self._MaxScroll() > 0
		width = 316 if scrolling else 325
		for (i, data) in enumerate(listings):
			entry = self._Entry(i)
			warn = data['id'] in overpricedIds
			step = self.heights[i]
			value = abs(data['price'] + data.get('cheque', 0) * YANG_PER_CHEQUE)
			each = value / max(1, data['count'])
			average = data.get('priceavg', 0)
			item.SelectItem(data['vnum'])
			cells = max(1, min(3, item.GetItemSize()[1]))
			entry["icon"].LoadImage(item.GetIconImageFileName())
			entry["icon"].SetScale(1.0 / cells, 1.0 / cells)
			entry["cells"] = cells
			entry["warn"] = warn
			entry["name"].SetText(item.GetItemName() + (" x%d" % data['count'] if data['count'] > 1 else ""))
			entry["price"].SetText(yang.format(locale.NumberToString(value)))
			entry["box"].SetSize(width, step)
			if warn:
				entry["bg"].SetColor(self.WARN_COLOR)
				textY = 16
				entry["unit"].SetText(SearchLocale("IKASHOP_SEARCH_OVERPRICED_UNIT").format(locale.NumberToString(each),
					locale.NumberToString(average), "%.1f" % (float(each) / max(1, average))))
				entry["unit"].SetPosition(13, 36)
				entry["unit"].Show()
				color = SEARCH_OVERPRICED_COLOR
				priceColor = SEARCH_OVERPRICED_COLOR
			else:
				entry["bg"].SetColor(self.STRIP_COLOR)
				textY = step / 2
				entry["unit"].Hide()
				color = SEARCH_TEXT_COLOR
				priceColor = 0xFFCEBB98
			entry["icon"].SetPosition(8 + (32 - 32 / cells) / 2, (step - 32) / 2 if not warn else 4)
			entry["name"].SetPosition(47, textY)
			entry["name"].SetPackedFontColor(color)
			entry["price"].SetPackedFontColor(priceColor)
			entry["price"].SetPosition(309 - (325 - width) - entry["price"].GetTextSize()[0], textY)
		for entry in self.entries[len(listings):]:
			entry["box"].Hide()
			entry["bg"].Hide()
		items = sum(max(1, d['count']) for d in listings)
		self.total.SetText(SearchLocale("IKASHOP_SEARCH_OVERPRICED_TOTAL").format(items) + "|c%08X" % SEARCH_WARN_GOLD
			+ yang.format(locale.NumberToString(total)) + "|r")
		self._Layout()
		self.SetCenterPosition()
		self.Show()
		self.SetTop()

	def _MaxScroll(self):
		return max(0, 1 + sum(self.heights[:self.count]) - self.viewHeight)

	def _Layout(self):
		maxScroll = self._MaxScroll()
		self.scroll = max(0, min(self.scroll, maxScroll))
		y = 1 - self.scroll
		for (i, entry) in enumerate(self.entries[:self.count]):
			step = self.heights[i]
			box = entry["box"]
			box.SetPosition(0, y)
			inside = y + step > 0 and y < self.viewHeight
			box.Show() if inside else box.Hide()
			full = y >= 0 and y + step <= self.viewHeight
			entry["icon"].Show() if (entry["cells"] == 1 or full) else entry["icon"].Hide()
			(barTop, barHeight) = (y + 1, step - 3) if entry["warn"] else (y, 2)
			top = max(barTop, 0)
			bottom = min(barTop + barHeight, self.viewHeight)
			if bottom > top:
				entry["bg"].SetPosition(4 if entry["warn"] else 0, top)
				entry["bg"].SetSize(box.GetWidth() - (8 if entry["warn"] else 0), bottom - top)
				entry["bg"].Show()
			else:
				entry["bg"].Hide()
			y += step
		if maxScroll > 0:
			track = self.viewHeight - 8
			size = max(8, track * self.viewHeight / (maxScroll + self.viewHeight))
			self.scrollThumb.SetSize(2, size)
			self.scrollThumb.SetPosition(0, (track - size) * self.scroll / maxScroll)
			self.scrollFrame.Show()
		else:
			self.scrollFrame.Hide()

	def _OnWheel(self, delta):
		self.scroll += -self.WHEEL if delta > 0 else self.WHEEL
		self._Layout()
		return True

	def _ShowItemToolTip(self, index):
		if index < len(self.listings):
			data = self.listings[index]
			self.itemToolTip.ClearToolTip()
			self.itemToolTip.AddItemData(data['vnum'], data.get('sockets', [0] * player.METIN_SOCKET_MAX_NUM), data.get('attrs', [(0, 0)] * player.ATTRIBUTE_SLOT_MAX_NUM))
			self.itemToolTip.ShowToolTip()

	def _HideItemToolTip(self):
		self.itemToolTip.HideToolTip()

	def OnUpdate(self):
		try:
			if self.owner and not self.owner.IsShow():
				self.Close()
		except ReferenceError:
			self.Close()

	def Close(self):
		self._OnCancel()

	def _OnCancel(self):
		event = self.cancelEvent
		self.cancelEvent = None
		self.itemToolTip.HideToolTip()
		self.Hide()
		if event:
			event()

	def _OnAccept(self):
		self.cancelEvent = None
		event = self.acceptEvent
		self.itemToolTip.HideToolTip()
		self.Hide()
		if event:
			event()

	def OnPressEscapeKey(self):
		self._OnCancel()
		return True


_SEARCH_USE_PUT_INTO_ACCESSORY_SOCKET = 21
_SEARCH_USE_PUT_INTO_BELT_SOCKET = 29
_SEARCH_ITEM_TYPE_SKILLFORGET = 22


def SearchIsMessageOnlyItem(vnum):
	item.SelectItem(vnum)
	type = item.GetItemType()
	if type in (item.ITEM_TYPE_SKILLBOOK, _SEARCH_ITEM_TYPE_SKILLFORGET, item.ITEM_TYPE_METIN, item.ITEM_TYPE_FISH, item.ITEM_TYPE_MATERIAL):
		return True
	return type == item.ITEM_TYPE_USE and item.GetItemSubType() in (_SEARCH_USE_PUT_INTO_ACCESSORY_SOCKET, _SEARCH_USE_PUT_INTO_BELT_SOCKET)


def SearchItemLink(data):
	sockets = list(data.get('sockets', ())) + [0, 0, 0]
	link = "item:%x:%x:%x:%x:%x" % (data['vnum'], 0, sockets[0], sockets[1], sockets[2])
	link += ":%x" % 0
	for attr in data.get('attrs', ()):
		(type, value) = attr[0], attr[1]
		if type:
			link += ":%x:%d" % (type, value)
	item.SelectItem(data['vnum'])
	name = item.GetItemName() + (" x%d" % data['count'] if data.get('count', 1) > 1 else "")
	return "|cffffc700|H%s|h[%s]|h|r" % (link, name)


def SearchSetEvent(btn, event, *args):
	if type(event) == types.MethodType:
		btn.SAFE_SetEvent(event, *args)
	else:
		btn.SetEvent(event, *args)


def SearchButton(parent, name, x, y, event = None, text = None, hover = "_hover", down = "_clicked"):
	btn = ui.Button()
	btn.SetParent(parent)
	btn.SetUpVisual(SEARCH_UI + name + ".png")
	btn.SetOverVisual(SEARCH_UI + name + hover + ".png")
	btn.SetDownVisual(SEARCH_UI + name + down + ".png")
	btn.SetPosition(x, y)
	if text is not None:
		btn.SetText(text)
	if event:
		SearchSetEvent(btn, event)
	btn.Show()
	return btn


class SearchShopCheckBox(ui.Window):

	def __init__(self):
		ui.Window.__init__(self)
		self.SetSize(20, 20)
		self.checked = False
		self.event = None
		self.tick = ui.ImageBox()
		self.tick.SetParent(self)
		self.tick.AddFlag("not_pick")
		self.tick.LoadImage(SEARCH_UI + "check.png")
		self.tick.SetPosition(2, 3)

	def __del__(self):
		ui.Window.__del__(self)

	def SetEvent(self, event):
		self.event = event

	def SetChecked(self, checked, callback = False):
		self.checked = bool(checked)
		self.tick.Show() if self.checked else self.tick.Hide()
		if callback and self.event:
			self.event(self.checked)

	def IsChecked(self):
		return self.checked

	def OnMouseLeftButtonUp(self):
		self.SetChecked(not self.checked, True)
		return True


class SearchShopDropdown(IkarusShopComboBox):
	ELEMENT_HEIGHT = 24


class SearchDropdown(ui.Window):
	ROW = 24
	BG_COLOR = 0xFF1C1611
	LINE_COLOR = 0xFF3A3129
	BORDER_COLOR = 0xFF5A4A3A
	HOVER_COLOR = 0xFF2E241B
	SELECTED_COLOR = 0xFFFFFF88

	class Row(ui.Window):
		def __init__(self, width, height):
			ui.Window.__init__(self)
			self.SetSize(width, height)
			self.index = 0
			self.event = None
			self.bar = ui.Bar()
			self.bar.SetParent(self)
			self.bar.AddFlag("not_pick")
			self.bar.SetSize(width, height - 1)
			self.bar.SetColor(SearchDropdown.BG_COLOR)
			self.bar.Show()
			self.line = ui.Bar()
			self.line.SetParent(self)
			self.line.AddFlag("not_pick")
			self.line.SetPosition(0, height - 1)
			self.line.SetSize(width, 1)
			self.line.SetColor(SearchDropdown.LINE_COLOR)
			self.line.Show()
			self.text = ui.TextLine()
			self.text.SetParent(self)
			self.text.AddFlag("not_pick")
			self.text.SetHorizontalAlignCenter()
			self.text.SetVerticalAlignCenter()
			self.text.SetPosition(width / 2, height / 2 - 1)
			self.text.Show()

		def __del__(self):
			ui.Window.__del__(self)

		def OnMouseOverIn(self):
			self.bar.SetColor(SearchDropdown.HOVER_COLOR)

		def OnMouseOverOut(self):
			self.bar.SetColor(SearchDropdown.BG_COLOR)

		def OnMouseLeftButtonUp(self):
			if self.event:
				self.event(self.index)
			return True

	def __init__(self, width, viewCount = 5, searchable = False):
		ui.Window.__init__(self)
		self.width = width
		self.viewCount = viewCount
		self.searchable = searchable
		self.items = []				# (original index, text)
		self.shown = []
		self.offset = 0
		self.selectedItem = 0
		self.selectItemEvent = None
		self.lastFilter = None
		top = 24 if searchable else 0
		self.top = top
		self.SetSize(width, top + viewCount * self.ROW + 2)
		self.border = ui.Bar()
		self.border.SetParent(self)
		self.border.AddFlag("not_pick")
		self.border.SetColor(self.BORDER_COLOR)
		self.border.Show()
		self.inner = ui.Bar()
		self.inner.SetParent(self)
		self.inner.AddFlag("not_pick")
		self.inner.SetPosition(1, 1)
		self.inner.SetColor(self.BG_COLOR)
		self.inner.Show()
		self.searchEdit = None
		if searchable:
			self.searchBar = ui.Bar()
			self.searchBar.SetParent(self)
			self.searchBar.SetPosition(4, 3)
			self.searchBar.SetSize(width - 8, 18)
			self.searchBar.SetColor(0xFF000000)
			self.searchBar.Show()
			self.searchFrame = ui.Bar()
			self.searchFrame.SetParent(self)
			self.searchFrame.AddFlag("not_pick")
			self.searchFrame.SetPosition(4, 21)
			self.searchFrame.SetSize(width - 8, 1)
			self.searchFrame.SetColor(self.BORDER_COLOR)
			self.searchFrame.Show()
			self.searchEdit = ui.EditLine()
			self.searchEdit.SetParent(self.searchBar)
			self.searchEdit.SetPosition(4, 2)
			self.searchEdit.SetSize(width - 16, 16)
			self.searchEdit.SetMax(24)
			self.searchEdit.Show()
			SearchEscapeOnlyWhenFocused(self.searchEdit)
			self.searchBar.SetOnMouseLeftButtonUpEvent(self.searchEdit.SetFocus)
			self.searchHint = ui.TextLine()
			self.searchHint.SetParent(self.searchBar)
			self.searchHint.AddFlag("not_pick")
			self.searchHint.SetPosition(4, 2)
			self.searchHint.SetPackedFontColor(0xFF8A8079)
			self.searchHint.SetText(locale.IKASHOP_SEARCH_SHOP_SEARCH_BUTTON_TEXT)
			self.searchHint.Show()
		self.rows = []
		for i in xrange(viewCount):
			row = self.Row(width - 2, self.ROW)
			row.SetParent(self)
			row.SetPosition(1, top + 1 + i * self.ROW)
			row.event = ui.__mem_func__(self._OnClickRow)
			row.SetMouseWheelEvent(ui.__mem_func__(self.OnMouseWheel))
			self.rows.append(row)
		self.thumb = ui.Bar()
		self.thumb.SetParent(self)
		self.thumb.AddFlag("not_pick")
		self.thumb.SetColor(0xFF8C7A5E)
		self.SetMouseWheelEvent(ui.__mem_func__(self.OnMouseWheel))
		self.Hide()

	def __del__(self):
		ui.Window.__del__(self)

	def SetItems(self, texts):
		items = list(enumerate(texts))
		if self.searchable and len(items) > 1:
			items = items[:1] + sorted(items[1:], key = lambda e: e[1].lower())
		self.items = items
		self.offset = 0
		self._Filter()

	def _Filter(self):
		key = self.searchEdit.GetText().lower() if self.searchEdit else ""
		self.lastFilter = key
		self.shown = [e for e in self.items if not key or key in e[1].lower() or e[0] == 0]
		self.offset = 0
		self._Refresh()

	def _Refresh(self):
		count = min(self.viewCount, len(self.shown))
		height = self.top + max(1, count) * self.ROW + 2
		self.SetSize(self.width, height)
		self.border.SetSize(self.width, height)
		self.inner.SetSize(self.width - 2, height - 2)
		self.offset = max(0, min(self.offset, max(0, len(self.shown) - self.viewCount)))
		for (i, row) in enumerate(self.rows):
			index = self.offset + i
			if index >= len(self.shown):
				row.Hide()
				continue
			(original, text) = self.shown[index]
			row.index = original
			FitTextLine(row.text, text, self.width - 24)
			row.text.SetPackedFontColor(self.SELECTED_COLOR if original == self.selectedItem else 0xFFFFFFFF)
			row.Show()
		if len(self.shown) > self.viewCount:
			area = count * self.ROW
			size = max(10, area * self.viewCount / len(self.shown))
			pos = (area - size) * self.offset / max(1, len(self.shown) - self.viewCount)
			self.thumb.SetPosition(self.width - 5, self.top + 1 + pos)
			self.thumb.SetSize(3, size)
			self.thumb.Show()
		else:
			self.thumb.Hide()

	def OnMouseWheel(self, delta):
		self.offset += -1 if delta > 0 else 1
		self._Refresh()
		return True

	def OnUpdate(self):
		if self.searchEdit:
			text = self.searchEdit.GetText()
			self.searchHint.Hide() if (text or self.searchEdit.IsFocus()) else self.searchHint.Show()
			if text.lower() != self.lastFilter:
				self._Filter()

	def _OnClickRow(self, index):
		self.SelectItem(index)

	def SelectItem(self, index):
		self.selectedItem = index
		text = ""
		for (original, t) in self.items:
			if original == index:
				text = t
				break
		self.Close()
		self._Refresh()
		if self.selectItemEvent:
			self.selectItemEvent(index, text)

	def GetSelectedItem(self):
		return self.selectedItem

	def SetSelectItemEvent(self, event):
		self.selectItemEvent = event

	def Open(self):
		if self.searchEdit:
			self.searchEdit.SetText("")
			self._Filter()
		self.Show()
		self.SetTop()

	def Close(self):
		if self.searchEdit:
			self.searchEdit.KillFocus()
		self.Hide()

	def IsMe(self, other):
		return self is other


class SearchSubCategoryEntry(ui.Window):
	PATH = "d:/ymir work/ui/game/wiki/category/"
	WIDTH = 201
	HEIGHT = 26

	def __init__(self):
		ui.Window.__init__(self)
		self.SetSize(self.WIDTH, self.HEIGHT)
		self.selected = False
		self.hover = False
		self.event = None
		self.image = ui.ExpandedImageBox()
		self.image.SetParent(self)
		self.image.AddFlag("not_pick")
		self.image.Show()
		self.text = ui.TextLine()
		self.text.SetParent(self)
		self.text.AddFlag("not_pick")
		self.text.SetHorizontalAlignCenter()
		self.text.SetVerticalAlignCenter()
		self.text.SetPosition(self.WIDTH / 2, self.HEIGHT / 2 - 1)
		self.text.Show()
		self._Refresh()

	def __del__(self):
		ui.Window.__del__(self)

	def SetText(self, text):
		self.text.SetText(text)

	def SetSelected(self, selected):
		self.selected = selected
		self._Refresh()

	def _Refresh(self):
		name = "sub_select.png" if self.selected else ("sub_hover.png" if self.hover else "sub_norm.png")
		self.image.LoadImage(self.PATH + name)
		self.image.SetScale(float(self.WIDTH) / max(1, self.image.GetWidth()), float(self.HEIGHT) / max(1, self.image.GetHeight()))

	def OnMouseOverIn(self):
		self.hover = True
		self._Refresh()

	def OnMouseOverOut(self):
		self.hover = False
		self._Refresh()

	def OnMouseLeftButtonUp(self):
		if self.event:
			self.event()
		return True


class SearchShopCategoryList(ui.Window):
	VIEW_HEIGHT = 404
	VIEW_WIDTH = 204
	MAIN_STEP = 40
	SUB_STEP = 23
	WHEEL_STEP = 23

	def __init__(self):
		self.changeEvent = None
		ui.Window.__init__(self)
		self.SetSize(218, 410)
		self.entries = []
		self.opened = -1
		self.selected = (0, 0)
		self.scroll = 0
		self.event = None
		self.track = ui.ImageBox()
		self.track.SetParent(self)
		self.track.LoadImage(SEARCH_UI + "scroll_bg_category.png")
		self.track.SetPosition(208, 3)
		self.track.Show()
		self.thumb = ui.Bar()
		self.thumb.SetParent(self.track)
		self.thumb.SetColor(0xFF8C7A5E)
		self.thumb.Hide()
		self.view = ui.Window()
		self.view.SetParent(self)
		self.view.SetPosition(7, 3)
		self.view.SetSize(self.VIEW_WIDTH, self.VIEW_HEIGHT)
		self.view.SetInsideRender(True)
		self.view.Show()
		wheel = ui.__mem_func__(self.OnMouseWheel)
		self.view.SetMouseWheelEvent(wheel)
		self.SetMouseWheelEvent(wheel)
		for (i, (key, icon, category, subs)) in enumerate(SEARCH_CATEGORIES):
			main = ui.Button()
			main.SetParent(self.view)
			main.SetUpVisual(SEARCH_UI + "norm.png")
			main.SetOverVisual(SEARCH_UI + "hover.png")
			main.SetDownVisual(SEARCH_UI + "active.png")
			main.SetText(SearchLocale(key))
			main.ButtonText.SetHorizontalAlignLeft()
			main.ButtonText.SetPosition(50, 19)
			main.SAFE_SetEvent(self._OnClickMain, i)
			main.SetMouseWheelEvent(wheel)
			main.Show()
			image = ui.ExpandedImageBox()
			image.SetParent(main)
			image.AddFlag("not_pick")
			image.LoadImage(SEARCH_UI + "icons/" + icon)
			image.SetPosition(3, 4)
			image.Show()
			circle = arrow = None
			if subs:
				circle = ui.ImageBox()
				circle.SetParent(main)
				circle.AddFlag("not_pick")
				circle.LoadImage(SEARCH_UI + "circle.png")
				circle.SetPosition(179, 9)
				circle.Show()
				arrow = ui.ExpandedImageBox()
				arrow.SetParent(main)
				arrow.AddFlag("not_pick")
				arrow.LoadImage(SEARCH_UI + "down.png")
				arrow.SetPosition(182, 14)
				arrow.Show()
			subEntries = []
			for (j, subKey) in enumerate(subs):
				sub = SearchSubCategoryEntry()
				sub.SetParent(self.view)
				sub.SetText(SearchLocale(subKey))
				sub.event = lambda s = proxy(self), a = i, b = j + 1: s._OnClickSub(a, b)
				sub.SetMouseWheelEvent(wheel)
				sub.Hide()
				subEntries.append(sub)
			self.entries.append({"main": main, "icon": image, "circle": circle, "arrow": arrow, "subs": subEntries, "category": category})
			if app.ENABLE_CLIP_MASKING:
				for widget in [main] + subEntries:
					widget.SetClippingMaskWindow(self.view)
		self._Layout()

	def __del__(self):
		ui.Window.__del__(self)

	def SetEvent(self, event):
		self.event = event

	def GetSelection(self):
		(index, sub) = self.selected
		return (self.entries[index]["category"], sub)

	def Select(self, category, sub):
		for (i, entry) in enumerate(self.entries):
			if entry["category"] == category:
				self.selected = (i, sub if sub <= len(entry["subs"]) else 0)
				self.opened = i if entry["subs"] else self.opened
				break
		self._Layout()

	def _ContentHeight(self):
		h = len(self.entries) * self.MAIN_STEP
		if self.opened >= 0:
			h += len(self.entries[self.opened]["subs"]) * self.SUB_STEP
		return h

	def _Layout(self):
		maxScroll = max(0, self._ContentHeight() - self.VIEW_HEIGHT)
		self.scroll = max(0, min(self.scroll, maxScroll))
		y = -self.scroll
		(si, sj) = self.selected
		for (i, entry) in enumerate(self.entries):
			main = entry["main"]
			main.SetPosition(0, y)
			main.Show() if (y + 38 > 0 and y < self.VIEW_HEIGHT) else main.Hide()
			main.SetUpVisual(SEARCH_UI + ("active.png" if si == i else "norm.png"))
			if entry["arrow"]:
				entry["arrow"].LoadImage(SEARCH_UI + ("up.png" if self.opened == i else "down.png"))
			y += self.MAIN_STEP
			for (j, sub) in enumerate(entry["subs"]):
				if self.opened != i:
					sub.Hide()
					continue
				sub.SetPosition(1, y)
				sub.SetSelected(si == i and sj == j + 1)
				sub.Show() if (y + 26 > 0 and y < self.VIEW_HEIGHT) else sub.Hide()
				y += self.SUB_STEP
		total = self._ContentHeight()
		if total > self.VIEW_HEIGHT:
			size = max(12, self.VIEW_HEIGHT * self.VIEW_HEIGHT / total)
			pos = (self.VIEW_HEIGHT - size) * self.scroll / max(1, total - self.VIEW_HEIGHT)
			self.thumb.SetPosition(2, pos)
			self.thumb.SetSize(3, size)
			self.thumb.Show()
		else:
			self.thumb.Hide()

	def _OnClickMain(self, index):
		entry = self.entries[index]
		if index != self.selected[0] and self.changeEvent:
			self.changeEvent()
		if entry["subs"]:
			self.opened = -1 if self.opened == index else index
			self._Layout()
			return
		self.selected = (index, 0)
		self._Layout()
		if self.event:
			self.event()

	def _OnClickSub(self, index, sub):
		self.selected = (index, sub)
		self._Layout()
		if self.event:
			self.event()

	def OnMouseWheel(self, delta):
		self.scroll += -self.WHEEL_STEP if delta > 0 else self.WHEEL_STEP
		self._Layout()
		return True


class SearchShopPriceRating(ui.ImageBox):

	def __init__(self):
		ui.ImageBox.__init__(self)
		self.LoadImage(SEARCH_UI + "bg_pricerating.png")
		self.bars = []
		for i in xrange(5):
			bar = ui.ImageBox()
			bar.SetParent(self)
			bar.AddFlag("not_pick")
			bar.LoadImage(SEARCH_UI + "price_rating%d.png" % (i + 1))
			bar.SetPosition(3 + i * 21, 3)
			bar.Hide()
			self.bars.append(bar)

	def __del__(self):
		ui.ImageBox.__del__(self)

	def SetRating(self, rating):
		for (i, bar) in enumerate(self.bars):
			bar.Show() if i < rating else bar.Hide()


class SearchHoverArea(ui.Window):

	def __init__(self):
		ui.Window.__init__(self)
		self.overIn = None
		self.overOut = None

	def __del__(self):
		ui.Window.__del__(self)

	def SetEvents(self, overIn, overOut):
		self.overIn = overIn
		self.overOut = overOut

	def OnMouseOverIn(self):
		if self.overIn:
			self.overIn()

	def OnMouseOverOut(self):
		if self.overOut:
			self.overOut()


SEARCH_TIP_ORANGE = 0xFFF5A64A
SEARCH_TIP_BLUE = 0xFF8FD3FF
SEARCH_TIP_RED = 0xFFFF7070				# overpriced: price / average / unit price
SEARCH_TIP_WIDTH = 336
SEARCH_SALES_ROWS = 5
SEARCH_SALES_CACHE_SECONDS = 60
SEARCH_SALES = {"cache": {}, "pending": None}	# (vnum, count) -> (time, average, sales); pending = (vnum, count, row proxy, sent)


def SearchEscapeOnlyWhenFocused(edit):
	def onEscape(e = proxy(edit)):
		if e.IsFocus():
			e.KillFocus()
			return True
		return False
	edit.OnPressEscapeKey = onEscape


def SearchAppendSalesTable(tip, sales):
	widths = (128, 66, 128)
	width = sum(widths)
	left = (tip.toolTipWidth - width) / 2
	top = tip.toolTipHeight
	headerColor = 0xFF2D1C11
	borderColor = 0xFF42392F
	rowColor = 0xFF1F1511
	lineColor = 0xFF756657

	def bar(x, y, w, h, color):
		b = ui.Bar()
		b.SetParent(tip)
		b.SetPosition(x, y)
		b.SetSize(w, h)
		b.SetColor(color)
		b.Show()
		tip.childrenList.append(b)

	def text(value, x, y, color, bold = False):
		line = ui.TextLine()
		line.SetParent(tip)
		line.SetFontName("Tahoma:12b" if bold else tip.defFontName)
		line.SetPackedFontColor(color)
		line.SetOutline()
		line.SetHorizontalAlignCenter()
		line.SetText(value)
		line.SetPosition(x, y)
		line.Show()
		tip.childrenList.append(line)

	bar(left, top, width, 21, headerColor)
	bar(left, top, width, 1, borderColor)
	bar(left, top + 20, width, 1, borderColor)
	x = left
	for (w, key) in zip(widths, ("IKASHOP_SEARCH_TIP_COL_PRICE", "IKASHOP_SEARCH_TIP_COL_COUNT", "IKASHOP_SEARCH_TIP_COL_DATE")):
		text(SearchLocale(key), x + w / 2, top + 4, 0xFFCABDAB, True)
		x += w
	rows = list(sales)[:SEARCH_SALES_ROWS]
	for (i, (count, price, stamp)) in enumerate(rows):
		y = top + 21 + i * 18
		bar(left, y, width, 17, 0xFF231A14 if i % 2 == 0 else 0xFF1C120F)
		bar(left + widths[0], y, 1, 17, lineColor)
		bar(left + widths[0] + widths[1], y, 1, 17, lineColor)
		if i + 1 < len(rows):
			bar(left, y + 17, width, 1, lineColor)
		text(locale.IKASHOP_SEARCH_TIP_SALE_PRICE.format(locale.NumberToString(price)), left + widths[0] / 2, y + 2, 0xFFC7C7C7)
		text(locale.IKASHOP_SEARCH_TIP_SALE_COUNT.format(count), left + widths[0] + widths[1] / 2, y + 2, 0xFFC7C7C7)
		text(DatetimeFormat(stamp) or "", left + widths[0] + widths[1] + widths[2] / 2, y + 2, 0xFFC7C7C7)
	tip.toolTipHeight += 21 + len(rows) * 18 + 6
	tip.ResizeToolTip()


def SearchSalesFor(vnum, count):
	entry = SEARCH_SALES["cache"].get((vnum, count))
	if entry and app.GetTime() - entry[0] < SEARCH_SALES_CACHE_SECONDS:
		return entry
	return None


def SearchOnPriceAverage(price, sales):
	pending = SEARCH_SALES["pending"]
	if not pending:
		return False
	(vnum, count, row, sent) = pending
	SEARCH_SALES["pending"] = None
	SEARCH_SALES["cache"][(vnum, count)] = (app.GetTime(), price, tuple(sales))
	try:
		row._OnSalesArrived(vnum, count)
	except ReferenceError:
		pass
	return True


class IkarusSearchShopRow(IkarusSearchShopItem):

	def _LoadIkarusSearchShopItem(self):
		self.cartEvent = None
		self.priceHovered = False
		self.background = self.CreateWidget(ui.ExpandedImageBox)
		self.background.LoadImage(SEARCH_UI + "bg_1slot.png")
		self.SetSize(542, 52)

		self.checkbox = self.CreateWidget(SearchShopCheckBox, pos = (9, 16))
		self.checkbox.SetEvent(self._OnCheck)
		self.checkbox.SetChecked(False)

		self.slot = self.CreateWidget(ui.GridSlotWindow, pos = (41, 10))
		self.slot.ArrangeSlot(0, 1, 1, SLOT_SIZE, SLOT_SIZE, 0, 0)
		self.slot.SetSlotBaseImage("ikashop/lite/common/slot/default.png", 1.0, 1.0, 1.0, 1.0)
		self.slot.SetOverInItemEvent(self._OverInItem)
		self.slot.SetOverOutItemEvent(self._OverOutItem)

		self.itemName = self.CreateWidget(ui.TextLine, pos = (80, 19))
		self.price = self.CreateWidget(ui.TextLine, pos = (294, 19))
		self.price.SetHorizontalAlignCenter()
		self.sellerName = self.CreateWidget(ui.TextLine, show = False)
		self.duration = self.CreateWidget(ui.TextLine, show = False)

		self.priceHover = self.CreateWidget(SearchHoverArea, pos = (245, 14), size = (105, 22))
		self.priceHover.SetEvents(self._ShowPriceToolTip, self._HideTextToolTip)
		self.priceToolTip = uitooltip.ToolTip(SEARCH_TIP_WIDTH)
		self.priceToolTip.HideToolTip()

		self.rating = self.CreateWidget(SearchShopPriceRating, pos = (364, 19))
		self.ratingHover = self.CreateWidget(SearchHoverArea, pos = (364, 17), size = (106, 18))
		self.ratingHover.SetEvents(self._ShowRatingToolTip, self._HideTextToolTip)

		self.actionBackground = self.CreateWidget(ui.ImageBox, pos = (479, 12))
		self.actionBackground.LoadImage(SEARCH_UI + "bg_buttons.png")
		self.messageSellerButton = SearchButton(self, "btn_message", 482, 15, self._OnClickMessageSeller)
		self.messageSellerButton.SetShowToolTipEvent(ui.__mem_func__(self._ShowSellerToolTip))
		self.messageSellerButton.SetHideToolTipEvent(ui.__mem_func__(self._HideTextToolTip))
		self.offerButton = SearchButton(self, "btn_offer", 505, 15, self._OnClickOfferButton, hover = "_hover", down = "_hover_clicked")
		self.offerButton.SetToolTipText(locale.IKASHOP_SEARCH_SHOP_OFFER_BUTTON_TEXT)
		self.sendMessageButton = SearchButton(self, "btn_sendmsg", 482, 15, self._OnClickSendItemMessage)
		self.sendMessageButton.SetShowToolTipEvent(ui.__mem_func__(self._ShowSellerToolTip))
		self.sendMessageButton.SetHideToolTipEvent(ui.__mem_func__(self._HideTextToolTip))
		self.sendMessageButton.Hide()
		self.messageOnly = False
		self.soldCover = self.CreateWidget(ui.Bar, pos = (41, 10), size = (32, 32), show = False)
		self.soldCover.SetColor(0x4DFF0000)
		self.soldCover.AddFlag("not_pick")
		rightClick = ui.__mem_func__(self._OnRightClickOffer)
		for widget in (self, self.background, self.priceHover, self.ratingHover, self.actionBackground):
			widget.SetMouseRightButtonUpEvent(rightClick)
		self.slot.SetUnselectItemSlotEvent(ui.__mem_func__(self._OnRightClickOfferSlot))

		self.buyButton = self.CreateWidget(ui.Button, show = False)
		self.openSellingBoard = self.CreateWidget(ui.Button, show = False)

		self.textToolTip = uitooltip.ToolTip()
		self.textToolTip.HideToolTip()

	def SetMouseWheelEvent(self, event):
		IkarusSearchShopItem.SetMouseWheelEvent(self, event)
		for widget in (self.background, self.slot, self.checkbox, self.priceHover, self.ratingHover, self.actionBackground,
				self.messageSellerButton, self.offerButton, self.sendMessageButton):
			widget.SetMouseWheelEvent(event)

	def _OnCheck(self, checked):
		self._RefreshBackground()
		if self.cartEvent:
			self.cartEvent(self.data, checked)

	def SetCartEvent(self, event):
		self.cartEvent = event

	def SetInCart(self, inCart):
		self.checkbox.SetChecked(inCart)
		self._RefreshBackground()

	def _RefreshBackground(self):
		size = max(1, min(3, self.slotHeight))
		self.background.LoadImage(SEARCH_UI + "bg_%dslot%s.png" % (size, "_selected" if self.checkbox.IsChecked() else ""))

	def _TotalPrice(self):
		return abs(self.data['price'] + self.data.get('cheque', 0) * YANG_PER_CHEQUE)

	def _ShowPriceToolTip(self):
		self.priceHovered = True
		vnum, count = self.data['vnum'], self.data['count']
		entry = SearchSalesFor(vnum, count)
		pending = SEARCH_SALES["pending"]
		if not entry and (not pending or app.GetTime() - pending[3] > 3):
			SEARCH_SALES["pending"] = (vnum, count, proxy(self), app.GetTime())
			ikashop.SendPriceAverageRequest(vnum, count)
		self._BuildPriceToolTip(entry)

	def _BuildPriceToolTip(self, entry):
		tip = self.priceToolTip
		tip.ClearToolTip()
		total = self._TotalPrice()
		average = entry[1] if entry and entry[1] > 0 else self.data.get('priceavg', 0)
		overpriced = self.ratingValue == 1
		tip.AutoAppendTextLine(locale.IKASHOP_SEARCH_TIP_PRICE.format(locale.NumberToString(total)), SEARCH_TIP_RED if overpriced else SEARCH_TIP_ORANGE)
		if average > 0:
			tip.AutoAppendTextLine(locale.IKASHOP_ITEM_PRICE_AVERAGE_VALUE.format(locale.NumberToMoneyString(average)), SEARCH_TIP_RED if overpriced else SEARCH_TIP_BLUE)
		else:
			tip.AutoAppendTextLine(locale.IKASHOP_SEARCH_TIP_AVERAGE_NA, 0xFFFFFFFF)
		if self.data['count'] > 1 and total > 0:
			tip.AutoAppendTextLine(locale.IKASHOP_SEARCH_TIP_UNIT_PRICE.format(locale.NumberToString(total / self.data['count'])), SEARCH_TIP_RED if overpriced else SEARCH_TIP_ORANGE)
		tip.AppendSpace(5)
		sales = entry[2] if entry else ()
		if sales:
			tip.AutoAppendTextLine(locale.IKASHOP_SEARCH_TIP_RECENT_SALES, SEARCH_TIP_ORANGE)
			tip.AppendSpace(3)
			SearchAppendSalesTable(tip, sales)
		elif entry:
			tip.AutoAppendTextLine(locale.IKASHOP_SEARCH_TIP_RECENT_SALES_NONE, 0xFFFFFFFF)
		tip.ResizeToolTip()
		tip.ShowToolTip()

	def _OnSalesArrived(self, vnum, count):
		if self.priceHovered and self.data.get('vnum') == vnum and self.data.get('count') == count:
			self._BuildPriceToolTip(SearchSalesFor(vnum, count))

	def _ShowRatingToolTip(self):
		tip = self.textToolTip
		tip.ClearToolTip()
		tip.AutoAppendTextLine(locale.IKASHOP_PRICE_RATING_TOOLTIP_FORMAT.format(SearchLocale(SEARCH_RATING_TEXTS[self.ratingValue])), SEARCH_TIP_ORANGE)
		average = self.data.get('priceavg', 0)
		if average > 0:
			tip.AutoAppendTextLine(locale.IKASHOP_ITEM_PRICE_AVERAGE_VALUE.format(locale.NumberToMoneyString(average)), SEARCH_TIP_BLUE)
		else:
			tip.AutoAppendTextLine(locale.IKASHOP_ITEM_PRICE_AVERAGE_NOT_AVAILABLE, 0xFFFFFFFF)
		tip.AlignHorizonalCenter()
		tip.ShowToolTip()

	def _ShowSellerToolTip(self):
		tip = self.textToolTip
		tip.ClearToolTip()
		tip.AutoAppendTextLine(locale.IKASHOP_SEARCH_SHOP_SELLER_TOOLTIP_FORMAT.format(self.data.get('seller_name', '')))
		tip.AlignHorizonalCenter()
		tip.ShowToolTip()

	def _HideTextToolTip(self):
		self.priceHovered = False
		self.textToolTip.HideToolTip()
		self.priceToolTip.HideToolTip()

	def _OnClickMessageSeller(self):
		if app.EXTEND_IKASHOP_PRO and self.searchShopBoard:
			self.searchShopBoard.OpenWhisper(self.data.get('seller_name', ''))

	def _OnRightClickOffer(self):
		if self.messageOnly or not self.offerButton.IsShow() or self.data.get('deleted', 0):
			return
		self._HideTextToolTip()
		self._OnClickOfferButton()

	def _OnRightClickOfferSlot(self, slot = 0, *args):
		self._OnRightClickOffer()

	def _OnClickSendItemMessage(self):
		if app.EXTEND_IKASHOP_PRO and self.searchShopBoard:
			self.searchShopBoard.OpenWhisperText(self.data.get('seller_name', ''), SearchItemLink(self.data))

	def SetNotAvailable(self):
		self.slot.EnableSlot(0)
		self.soldCover.SetPosition(41, 10)
		self.soldCover.SetSize(32, 32 * self.slotHeight)
		self.soldCover.Show()
		self.itemName.SetPackedFontColor(0xFFFF8888)
		self.offerButton.Hide()
		self.checkbox.Hide()

	def SetAvailable(self):
		self.soldCover.Hide()
		self.slot.EnableSlot(0)
		self.itemName.SetPackedFontColor(SEARCH_TEXT_COLOR)
		self.offerButton.Hide() if self.messageOnly else self.offerButton.Show()
		self.checkbox.Show()

	def Setup(self, data):
		self.data = data
		item.SelectItem(data['vnum'])
		self.slotHeight = max(1, min(3, item.GetItemSize()[1]))
		height = SEARCH_ROW_HEIGHTS[self.slotHeight]
		self.SetSize(542, height)
		mid = height / 2

		name = item.GetItemName()
		if data.get('is_auction'):
			name += ' ' + locale.IKASHOP_SEARCH_SHOP_ITEM_NAME_AUCTION
		if data['count'] > 1:
			name += " x%d" % data['count']
		self.itemName.SetText(name)
		self.itemName.SetPackedFontColor(SEARCH_TEXT_COLOR)
		self.itemName.SetPosition(80, mid - 7)
		self.sellerName.SetText(data.get('seller_name', ''))

		raw = data['price'] + data.get('cheque', 0) * YANG_PER_CHEQUE
		total = abs(raw)
		self.ratingValue = SearchPriceRating(total, data.get('priceavg', 0))
		if raw <= 0:
			self.price.SetText(locale.IKASHOP_OFFER_ONLY)
		else:
			self.price.SetText(locale.NumberToString(total) + SEARCH_PRICE_COIN)
		self.price.SetPackedFontColor(SEARCH_OVERPRICED_COLOR if self.ratingValue == 1 else SEARCH_TEXT_COLOR)
		self.price.SetPosition(294, mid - 7)
		self.priceHover.SetPosition(245, mid - 12)
		self.rating.SetRating(self.ratingValue)
		self.rating.SetPosition(364, mid - 7)
		self.ratingHover.SetPosition(364, mid - 9)

		self.checkbox.SetPosition(9, mid - 10)
		self.actionBackground.SetPosition(479, mid - 14)
		self.messageSellerButton.SetPosition(482, mid - 11)
		self.offerButton.SetPosition(505, mid - 11)
		self.sendMessageButton.SetPosition(482, mid - 11)
		self.messageOnly = SearchIsMessageOnlyItem(data['vnum'])
		for widget in (self.messageSellerButton, self.offerButton):
			widget.Hide() if self.messageOnly else widget.Show()
		self.sendMessageButton.Show() if self.messageOnly else self.sendMessageButton.Hide()

		count = data['count'] if data['count'] > 1 else 0
		self.slot.ArrangeSlot(0, 1, self.slotHeight, SLOT_SIZE, SLOT_SIZE, 0, 0)
		self.slot.SetSlotBaseImage("ikashop/lite/common/slot/default.png", 1.0, 1.0, 1.0, 1.0)
		self.slot.SetItemSlot(0, data['vnum'], count)
		self._RefreshBackground()


def SearchOnCooldownPopup():
	board = SEARCH_SALES.get("board")
	if not board:
		return False
	try:
		if board.lastSearch and not board.pendingSearch:
			board.pendingSearch = board.lastSearch
		board.lastSearchSent = app.GetTime()
	except ReferenceError:
		return False
	return True


def SearchWeak(obj):
	return obj if type(obj) in (ProxyType, CallableProxyType) else proxy(obj)


#######################################################################################################################
# clock (324, 9), date (347, 10), thin scrollbar (465, 62)
#######################################################################################################################
SEARCH_HISTORY_UI = SEARCH_UI + "history/"


def SearchHistoryName(name):
	name = name[1:] if name[:1] in ("=", "@") else name
	return name if name else locale.IKASHOP_SEARCH_SHOP_HISTORY_EMPTY_NAME


def SearchCategoryText(type, subtype):
	for (key, icon, category, subs) in SEARCH_CATEGORIES:
		if category == type:
			text = SearchLocale(key)
			if 0 < subtype <= len(subs):
				text += " - " + SearchLocale(subs[subtype - 1])
			return text
	return ""


class SearchThinScrollBar(ui.Window):
	WIDTH = 4

	def __init__(self):
		ui.Window.__init__(self)
		self.pos = 0.0
		self.event = None
		self.content = 0
		self.dragging = False
		self.SetSize(self.WIDTH, 100)
		self.track = ui.Bar()
		self.track.SetParent(self)
		self.track.AddFlag("not_pick")
		self.track.SetColor(0xFF3B3328)
		self.track.SetPosition(0, 0)
		self.track.Show()
		self.thumb = ui.Bar()
		self.thumb.SetParent(self)
		self.thumb.AddFlag("not_pick")
		self.thumb.SetColor(0xFF8C7A5E)
		self.thumb.Show()
		self._Refresh()

	def __del__(self):
		ui.Window.__del__(self)

	def SetScrollBarSize(self, height):
		self.SetSize(self.WIDTH, height)
		self.track.SetSize(1, height)
		self._Refresh()

	def SetScrollEvent(self, event):
		self.event = event

	def UpdateScrollbarLenght(self, length):
		self.content = max(0, length)
		self._Refresh()

	def _ThumbHeight(self):
		h = self.GetHeight()
		if self.content <= h:
			return h
		return max(12, h * h / self.content)

	def _Refresh(self):
		h = self.GetHeight()
		size = self._ThumbHeight()
		self.thumb.SetSize(3, size)
		self.thumb.SetPosition(1, int((h - size) * self.pos))

	def GetPos(self):
		return self.pos

	def SetPos(self, pos):
		self.pos = max(0.0, min(1.0, float(pos)))
		self._Refresh()
		if self.event:
			self.event()

	def _Step(self):
		over = self.content - self.GetHeight()
		return 1.0 if over <= 0 else min(1.0, 35.0 / over)

	def OnUp(self):
		self.SetPos(self.pos - self._Step())

	def OnDown(self):
		self.SetPos(self.pos + self._Step())

	def _PosFromMouse(self):
		(x, y) = self.GetMouseLocalPosition()
		size = self._ThumbHeight()
		free = max(1, self.GetHeight() - size)
		self.SetPos(float(y - size / 2) / free)

	def OnMouseLeftButtonDown(self):
		self._PosFromMouse()
		return True


#######################################################################################################################
#######################################################################################################################
OFFER_UI = OFFLINESHOP_UI_PATH + "offer_list/"
OFFER_VIEW_STEP = 139


def SearchShortMoney(value):
	value = long(value)
	if value >= 1000 and value % 1000 == 0:
		return locale.NumberToString(value / 1000) + "k"
	return locale.NumberToString(value)


def SearchSetWheelDeep(widget, event, seen = None):
	seen = seen if seen is not None else set()
	if id(widget) in seen:
		return
	seen.add(id(widget))
	values = widget.__dict__.values() if isinstance(widget, ui.Window) else widget
	for value in values:
		if type(value) in (ProxyType, CallableProxyType):
			continue
		if isinstance(value, (list, tuple)):
			SearchSetWheelDeep(value, event, seen)
		elif isinstance(value, ui.Window) and not isinstance(value, uitooltip.ToolTip):
			value.SetMouseWheelEvent(event)
			SearchSetWheelDeep(value, event, seen)


OFFER_WHEEL_STEP = 46


#######################################################################################################################
#######################################################################################################################
NOTIF_UI = OFFLINESHOP_UI_PATH + "notification/"
NOTIF_ROW_STEP = 31
NOTIF_SECTION_STEP = 46
NOTIF_VIEWS = 12
NOTIF_NAME_WIDTH = 80
NOTIF_LIST_HEIGHT = 354


def _NotifKinds():
	K = {}
	def add(value, label, icon, price):
		K[value] = (label, icon, price)
	add(ikashop.NOTIFICATION_SELLER_SELLER_SOLD_ITEM, "IKASHOP_PRO_NOTIFICATION_TYPE_SOLD_ITEM", "icon_price.png", True)
	add(ikashop.NOTIFICATION_SELLER_NEW_OFFER_ON_ITEM, "IKASHOP_PRO_NOTIFICATION_TYPE_NEW_OFFER_ON_ITEM", "icon_received.png", False)
	add(ikashop.NOTIFICATION_SELLER_SHOP_EXPIRED, "IKASHOP_PRO_NOTIFICATION_TYPE_SHOP_EXPIRED", "icon_clock.png", False)
	add(ikashop.NOTIFICATION_SELLER_ITEM_EXPIRED, "IKASHOP_NOTIFICATION_ITEM_REMOVED_EXPIRED", "icon_clock.png", False)
	add(ikashop.NOTIFICATION_SELLER_AUCTION_NEW_OFFER, "IKASHOP_PRO_NOTIFICATION_TYPE_AUCTION_NEW_OFFER", "icon_received.png", False)
	add(ikashop.NOTIFICATION_SELLER_AUCTION_EXPIRED, "IKASHOP_PRO_NOTIFICATION_TYPE_AUCTION_EXPIRED", "icon_clock.png", False)
	add(ikashop.NOTIFICATION_SELLER_AUCTION_SOLD, "IKASHOP_PRO_NOTIFICATION_TYPE_AUCTION_SOLD", "icon_price.png", True)
	add(ikashop.NOTIFICATION_SELLER_OFFER_CANCELLED, "IKASHOP_PRO_NOTIFICATION_TYPE_OFFER_CANCELLED", "icon_sent.png", False)
	add(ikashop.NOTIFICATION_BUYER_OFFER_DENIED, "IKASHOP_PRO_NOTIFICATION_TYPE_OFFER_DENIED", "icon_sent.png", True)
	add(ikashop.NOTIFICATION_BUYER_OFFER_ACCEPTED, "IKASHOP_PRO_NOTIFICATION_TYPE_OFFER_ACCEPTED", "icon_sent.png", True)
	add(ikashop.NOTIFICATION_BUYER_OFFER_EXPIRED, "IKASHOP_PRO_NOTIFICATION_TYPE_OFFER_EXPIRED", "icon_clock.png", True)
	add(ikashop.NOTIFICATION_BUYER_AUCTION_BUY, "IKASHOP_PRO_NOTIFICATION_TYPE_AUCTION_BUY", "icon_price.png", True)
	add(ikashop.NOTIFICATION_BUYER_AUCTION_RAISE, "IKASHOP_PRO_NOTIFICATION_TYPE_AUCTION_RAISE", "icon_received.png", False)
	add(ikashop.NOTIFICATION_BUYER_AUCTION_LOST, "IKASHOP_PRO_NOTIFICATION_TYPE_AUCTION_LOST", "icon_sent.png", True)
	add(ikashop.NOTIFICATION_SELLER_DECORATION_EXPIRED, "IKASHOP_ULTIMATE_NOTIFICATION_SELLER_DECORATION_EXPIRED", "icon_clock.png", False)
	return K


class IkarusShopNotificationAccordionView(IkarusShopWindow):

	def __init__(self):
		super(IkarusShopNotificationAccordionView, self).__init__()
		self.data = None
		self.opened = False
		self.toggleEvent = None
		self.background = self.CreateWidget(ui.ImageBox)
		self.background.LoadImage(NOTIF_UI + "notification_bg.png")
		self.background.SetOnMouseLeftButtonUpEvent(self._OnToggle)
		self.icon = self.CreateWidget(ui.ImageBox, pos = (4, 6))
		self.icon.AddFlag("not_pick")
		self.unread = self.CreateWidget(ui.ImageBox, pos = (29, 2))
		self.unread.LoadImage(NOTIF_UI + "unreadicon.png")
		self.unread.AddFlag("not_pick")
		self.name = self.CreateWidget(ui.TextLine, pos = (50, 15))
		self.name.SetVerticalAlignCenter()
		self.name.SetPackedFontColor(0xFFCABDAB)
		self.name.AddFlag("not_pick")
		self.nameHover = self.CreateWidget(SearchHoverArea, pos = (40, 4), size = (90, 23))
		self.nameHover.SetEvents(ui.__mem_func__(self._ShowItemTip), ui.__mem_func__(self._HideItemTip))
		self.nameHover.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self._OnToggle))
		self.arrow = self.CreateWidget(ui.Button, pos = (134, 13))
		self.arrow.SAFE_SetEvent(self._OnToggle)
		self.openedBg = self.CreateWidget(ui.ExpandedImageBox, pos = (0, 31), show = False)
		self.openedBg.LoadImage(NOTIF_UI + "expanded_bg.png")
		self.sections = []
		for i in xrange(3):
			box = self.CreateWidget(ui.ImageBox, pos = (4, NOTIF_ROW_STEP + 4 + NOTIF_SECTION_STEP * i), show = False)
			box.LoadImage(NOTIF_UI + "expanded.png")
			label = self.CreateWidget(ui.TextLine, pos = (7, 11), parent = box)
			label.SetVerticalAlignCenter()
			label.SetPackedFontColor(0xFFCABDAB)
			value = self.CreateWidget(ui.TextLine, pos = (7, 33), parent = box)
			value.SetVerticalAlignCenter()
			value.SetPackedFontColor(0xFFCABDAB)
			self.sections.append((box, label, value))
		self.SetSize(156, NOTIF_ROW_STEP)

	def _OnToggle(self):
		self._HideItemTip()
		if self.toggleEvent and self.data:
			self.toggleEvent(self.data)

	def _ShowItemTip(self):
		vnum = self.data.get('what', 0) if self.data else 0
		if not vnum:
			return
		tip = NotifItemToolTip()
		tip.ClearToolTip()
		tip.AddItemData(vnum, [0] * player.METIN_SOCKET_MAX_NUM, [(0, 0)] * player.ATTRIBUTE_SLOT_MAX_NUM)
		tip.ShowToolTip()

	def _HideItemTip(self):
		if NOTIF_TOOLTIP[0]:
			NOTIF_TOOLTIP[0].HideToolTip()

	def GetFullHeight(self, opened):
		if not opened or not self.data:
			return NOTIF_ROW_STEP
		return NOTIF_ROW_STEP + 7 + NOTIF_SECTION_STEP * self._SectionCount()

	def _SectionCount(self):
		(label, icon, price) = _NOTIF_KINDS.get(self.data['type'], ("", "placeholder_icon.png", False))
		return 3 if price else 2

	def Setup(self, data, opened):
		self.data = data
		self.opened = opened
		(label, icon, hasPrice) = _NOTIF_KINDS.get(data['type'], ("", "placeholder_icon.png", False))
		self.icon.LoadImage(NOTIF_UI + icon)
		self.unread.Show() if not data.get('seen', True) and not opened else self.unread.Hide()
		name = ""
		if data.get('what'):
			item.SelectItem(data['what'])
			name = item.GetItemName()
		FitTextLine(self.name, name if name else SearchLocale(label), NOTIF_NAME_WIDTH)
		image = "btn_up" if opened else "btn_down"
		self.arrow.SetUpVisual(NOTIF_UI + image + ".png")
		self.arrow.SetOverVisual(NOTIF_UI + image + ".png")
		self.arrow.SetDownVisual(NOTIF_UI + image + "_clicked.png")
		rows = [(locale.IKASHOP_SEARCH_ACTION, SearchLocale(label))]
		if hasPrice:
			try:
				price = long(str(data.get('format', '0')).split("|")[0])
			except ValueError:
				price = 0
			rows.append((locale.IKASHOP_NOTIFICATION_PRICE_LABEL, locale.NumberToMoneyString(price)))
		rows.append((locale.IKASHOP_NOTIFICATION_DATE_LABEL, DatetimeFormat(data['datetime']) or ""))
		self.SetSize(156, self.GetFullHeight(opened))
		if opened:
			self.openedBg.SetScale(1.0, float(7 + NOTIF_SECTION_STEP * len(rows)) / 145.0)
			self.openedBg.SetPosition(0, NOTIF_ROW_STEP)
			self.openedBg.Show()
		else:
			self.openedBg.Hide()
		for (i, (box, labelLine, valueLine)) in enumerate(self.sections):
			if opened and i < len(rows):
				box.SetPosition(4, NOTIF_ROW_STEP + 4 + NOTIF_SECTION_STEP * i)
				labelLine.SetText(rows[i][0])
				valueLine.SetText(rows[i][1])
				box.Show()
			else:
				box.Hide()


NOTIF_TOOLTIP = [None]


def NotifItemToolTip():
	if not NOTIF_TOOLTIP[0]:
		NOTIF_TOOLTIP[0] = uitooltip.ItemToolTip()
		NOTIF_TOOLTIP[0].HideToolTip()
	return NOTIF_TOOLTIP[0]


def _Notif_Key(data):
	return (data['type'], data.get('what'), data.get('who'), data['datetime'], str(data.get('format')))


if SEARCH_SHOP_RENEWAL and app.EXTEND_IKASHOP_PRO:
	_NOTIF_KINDS = _NotifKinds()
else:
	_NOTIF_KINDS = {}


#######################################################################################################################
#######################################################################################################################


#######################################################################################################################
#######################################################################################################################
SHOP_KEY_VNUM = 51998
LOCK_TIP_NAME_COLOR = 0xFFFFD36A		# measured
LOCK_TIP_TEXT_COLOR = 0xFFCABDAB
LOCK_TIP_MISSING_COLOR = 0xFFFF5F5F


