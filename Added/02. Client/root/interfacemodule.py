if __USE_DYNAMIC_MODULE__:
	import pyapi

app = __import__(pyapi.GetModuleName("app"))
chr = __import__(pyapi.GetModuleName("chr"))
player = __import__(pyapi.GetModuleName("player"))
net = __import__(pyapi.GetModuleName("net"))

import constInfo
import systemSetting
import wndMgr
import chat
import ime
import uiTaskBar
import uiCharacter
import uiInventory
if app.ENABLE_DRAGON_SOUL_SYSTEM:
	import uiDragonSoul
import uiChat
import uiMessenger
import guild

import ui
import uiWhisper
if app.ENABLE_WHISPER_MESSENGER:
	import uiWhisperMessenger

if app.ENABLE_GUILD_APPLICATION:
	import uiGuildApplication
import uiPointReset
import uiShop
import uiExchange
import uiSystem
import uiRestart
import uiToolTip
import uidropinfo
import uishopsoldnotice
import uienergycrystal
import uishootingstars
import uiMiniMap
import uiParty
import uiSafebox
import uiGuild
import uiQuest
import uiPrivateShopBuilder
import uiCommon
import uiRefine
if app.ENABLE_REFINE_SEAL_RENEWAL:
	import uiRefineRenewal
import uiYinAndYangAttr
import uiEquipmentDialog
import uiGameButton
import uiTip
import uiCube
import miniMap
import uiNameReinforce
import uiselectitem
import uiScriptLocale
import shop
import event
import localeInfo

if app.ENABLE_GUILD_RANK_SYSTEM:
	import uiGuildRanking

if app.ENABLE_RENEWAL_SWITCHBOT:
	import uiSwitchbot

if app.ENABLE_ACCE_COSTUME_SYSTEM:
	import uiAcce

if app.ENABLE_VIEW_CHEST_DROP:
	import uiChestDrop

if app.ENABLE_SPECIAL_INVENTORY:
	import uiSpecialInventory



if app.ENABLE_RENDER_TARGET:
	import uiRenderTarget

if app.ENABLE_IKASHOP_RENEWAL:
	import uiikashop

if app.ENABLE_WIKI_SYSTEM:
	import uiWiki

if app.ENABLE_RENEWAL_SKILL_SELECT:
	import uiSkillSelect

if app.ENABLE_NEW_DUNGEON_LIB:
	import uiDungeonTimer

if app.ENABLE_TRACK_WINDOW:
	import uiTrack

if app.ENABLE_ITEMSHOP:
	import uiItemShopNew

if app.ENABLE_AURA_COSTUME_SYSTEM:
	import uiAura

	

if app.ENABLE_GROWTH_PET_SYSTEM:
	import uiPetInfo
import uiCompanion
import uiSkillUpgrade
import uiAutoCape

if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
	import uiTeleport

if app.ENABLE_SUNG_MAHI_TOWER:
	import uiSungMahi

if app.LINK_IN_CHAT:
	import os

if app.ENABLE_DUNGEON_INFO:
	import uiDungeonInfo
	import uitabledungeon

if app.__DUNGEON_INFO__:
	import uiDungeonTrack
	if app.ENABLE_DUNGEON_INFO_WINDOW:
		import uiDungeonWindow

if app.ENABLE_RENEWAL_SPECIAL_CHAT:
	import uiSpecialChat

if app.ENABLE_CHANGE_LOOK_SYSTEM:
	import uiChangeLook

if app.ENABLE_MOVE_COSTUME_ACCE_ATTR:
	import uiItemCombination

if app.ENABLE_HUNTING_SYSTEM:
	import uiHunting


if app.__AUTO_HUNT__:
	import uiAutoHunt


if app.ENABLE_BIOLOG_RENEWAL:
	import uibiologist

if app.ENABLE_BATTLEPASS_RENEWAL:
	import uibattlepass

if app.ENABLE_ZODIAC_MISSION:
	import ui12zi

import uiitemfinder










if app.ENABLE_GAYA_SYSTEM:
	import uiGemShop
	import uiselectitemEx

if app.ENABLE_GAYA_TICKET_SYSTEM:
	import uiGemTicket


if app.ENABLE_RANKING:
	import uiranking

if app.ENABLE_GLOBAL_RANKING:
	import uiglobalranking

if app.ENABLE_COSTUME_SHOP:
	import uicostumeshop

if app.ENABLE_WARDROBE_SYSTEM:
	import uiwardrobe

IsQBHide = 0
class Interface(object):
	CHARACTER_STATUS_TAB = 1
	CHARACTER_SKILL_TAB = 2

	def __init__(self):
		self.wndInventoryNew = None
		self.wndShop = None
		self.wndEnergyCrystal = None
		self.wndEnergyBar = None
		self.wndShopSoldNotice = None
		self._dropInfoGold = None
		self.wndWhisperMessenger = None
		self.wndMessengerButton = None
		self.wndGuildApplication = None
		self.wndGuildJoinNotification = None
		self.messengerQuickCloseTip = None
		systemSetting.SetInterfaceHandler(self)

		if app.__DUNGEON_INFO__:
			self.wndDungeonTrack = None
			self.wndDungeonManager = None

		if app.ENABLE_TRACK_WINDOW:
			self.wndTrackWindow = None

		self.windowOpenPosition = 0
		self.dlgWhisperWithoutTarget = None
		self.uiAffectshower = None
		self.uitargetBoard = None
		self.inputDialog = None
		self.tipBoard = None
		self.bigBoard = None

		if app.ENABLE_ZODIAC_MISSION:
			self.wnd12ziReward = None
			self.wnd12ziTimer = None

		if app.ENABLE_DUNGEON_INFO:
			self.wndDungeonInfo = None

		if app.ENABLE_WIKI_SYSTEM:
			self.wndWiki = None

		if app.ENABLE_ITEMSHOP:
			self.wndItemShop=None

		if app.ENABLE_RENEWAL_OX_EVENT:
			self.bigBoardControl = None


		# ITEM_MALL
		self.mallPageDlg = None
		# END_OF_ITEM_MALL

		self.wndWeb = None
		self.wndTaskBar = None
		self.wndCharacter = None
		self.wndInventory = None
		self.wndDragonSoul = None
		self.wndDragonSoulRefine = None
		self.DRAGON_SOUL_IS_QUALIFIED = FALSE
		self.wndExpandedMoney = None
		self.wndExpandedTaskBar = None
		self.wndCompanion = None
		self.wndSkillUpgrade = None
		self.wndBraveCape = None
		self.wndChat = None
		self.wndAutoChat = None
		self.wndMessenger = None
		self.wndMiniMap = None
		self.wndGuild = None
		self.wndGuildBuilding = None






		if app.ENABLE_RENEWAL_SWITCHBOT:
			self.wndSwitchbot = None

		if app.ENABLE_YIN_AND_YANG_ATTR:
			self.wndYinAndYangInventory = None
			self.wndYinAndYangHarmony = None

		if app.ENABLE_SUNG_MAHI_TOWER:
			self.wndSungMahiWindow = None

		if app.ENABLE_RENEWAL_CUBE:
			self.wndCubeRenewal = None

		if app.ENABLE_VIEW_CHEST_DROP:
			self.dlgChestDrop = None

		self.dlgDropInfo = None
		self._dropInfoSnapshot = None
		self.dlgShootingStars = None

		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory = None

		if app.ENABLE_RENDER_TARGET:
			self.wndRenderTarget = None

		if app.ENABLE_NEW_DUNGEON_LIB:
			self.wndDungeonTimer = None

		if app.ENABLE_SLOT_MARKING_SYSTEM:
			self.OnTopWindow = None
			self.dlgShop = None
			self.dlgExchange = None
			self.privateShopBuilder = None
			self.wndSafebox = None
			self.dlgRefineNew = None



		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			self.wndWarpWindow = None

		if app.ENABLE_RENEWAL_SPECIAL_CHAT:
			self.wndSpecialChat = None

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			self.wndChangeLook = None
		if app.ENABLE_MOVE_COSTUME_ACCE_ATTR:
			self.wndItemCombination = None

		if app.ENABLE_HUNTING_SYSTEM:
			self.wndHunting = None
			self.wndHuntingSelect = None
			self.wndHuntingReward = None

		if app.__AUTO_HUNT__:
			self.wndAutoHunt = None

		if app.ENABLE_BIOLOG_RENEWAL:
			self.wndBiologist = None

		if app.ENABLE_BATTLEPASS_RENEWAL:
			self.wndBattlePass = None

		if app.ENABLE_GAYA_TICKET_SYSTEM:
			self.wndImproveGemTicket = None

		if app.ENABLE_RANKING:
			self.wndRanking = None

		if app.ENABLE_COSTUME_SHOP:
			self.wndCostumeShop = None

		if app.ENABLE_WARDROBE_SYSTEM:
			self.wndWardrobe = None
			self.wardrobeController = uiwardrobe.WardrobeController()
			self.wardrobeController.SetChangeEvent(self.__OnWardrobeChanged)
			self.wardrobeController.resultEvent = self.__OnWardrobeResult

		self.listGMName = {}
		self.wndQuestWindow = {}
		self.wndQuestWindowNewKey = 0
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}

		if app.ENABLE_IKASHOP_RENEWAL:
			self.wndIkashopBusiness = None
			self.wndIkashopSearchShop = None
			if app.EXTEND_IKASHOP_ULTIMATE:
				self.wndIkashopShopSkin = None

		if app.LINK_IN_CHAT:
			self.OpenLinkQuestionDialog = None

		self.wndExpandedMoneyTaskBar = None

		event.SetInterfaceWindow(self)

	def __del__(self):
		systemSetting.DestroyInterfaceHandler()
		event.SetInterfaceWindow(None)

	################################
	## Make Windows & Dialogs
	def __MakeUICurtain(self):
		wndUICurtain = ui.Bar("TOP_MOST")
		wndUICurtain.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		wndUICurtain.SetColor(0x77000000)
		wndUICurtain.Hide()
		self.wndUICurtain = wndUICurtain

	def __MakeExpandMoney(self):
		if self.wndExpandedMoneyTaskBar:
			self.wndExpandedMoney = self.wndExpandedMoneyTaskBar
		else:
			self.wndExpandedMoney = uiTaskBar.ExpandedMoneyTaskBar()
	
	def __MakeMessengerWindow(self):
		if app.ENABLE_MESSENGER_DETAILS:
			import uiMessengerRenewal
			self.wndMessenger = uiMessengerRenewal.MessengerWindow()
		else:
			self.wndMessenger = uiMessenger.MessengerWindow()

		from _weakref import proxy
		self.wndMessenger.SetWhisperButtonEvent(lambda n,i=proxy(self):i.OpenWhisperDialog(n))
		self.wndMessenger.SetGuildButtonEvent(ui.__mem_func__(self.ToggleGuildWindow))

	def __MakeGuildWindow(self):
		if app.ENABLE_GUILD_WINDOW_RENEWAL:
			import uiGuildRenewal
			self.wndGuild = uiGuildRenewal.GuildWindow()
		else:
			self.wndGuild = uiGuild.GuildWindow()

	def __MakeChatWindow(self):
		wndChat = uiChat.ChatWindow()
		wndChat.SetSize(wndChat.CHAT_WINDOW_WIDTH, 0)
		wndChat.SetPosition(wndMgr.GetScreenWidth()/2 - wndChat.CHAT_WINDOW_WIDTH/2, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT - 37)
		wndChat.SetHeight(200)
		wndChat.Refresh()
		wndChat.Show()

		self.wndChat = wndChat
		self.wndChat.BindInterface(self)
		self.wndChat.SetSendWhisperEvent(ui.__mem_func__(self.OpenWhisperDialogWithoutTarget))
		self.wndChat.SetOpenChatLogEvent(ui.__mem_func__(self.ToggleChatLogWindow))

	def __MakeTaskBar(self):
		wndTaskBar = uiTaskBar.TaskBar()
		wndTaskBar.BindInterfaceClass(self)
		wndTaskBar.LoadWindow()
		self.wndTaskBar = wndTaskBar
		self.wndEnergyBar = None
		if app.ENABLE_ENERGY_SYSTEM:
			wndEnergyBar = uiTaskBar.EnergyBar()
			wndEnergyBar.LoadWindow()
			self.wndEnergyBar = wndEnergyBar
		self.wndEnergyCrystal = None
		if app.ENABLE_ENERGY_CRYSTAL:
			self.wndEnergyCrystal = uienergycrystal.EnergyCrystalWindow()
			self.wndEnergyCrystal.SetInterface(self)
			if self.wndEnergyBar:
				self.wndEnergyBar.SetEnergyButtonEvent(ui.__mem_func__(self.ToggleEnergyCrystalWindow))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHARACTER, ui.__mem_func__(self.ToggleCharacterWindowStatusPage))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_INVENTORY, ui.__mem_func__(self.ToggleInventoryWindow))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_MESSENGER, ui.__mem_func__(self.ToggleMessenger))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_SYSTEM, ui.__mem_func__(self.ToggleSystemDialog))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND_MONEY, ui.__mem_func__(self.ToggleExpandedMoneyButton))
		self.wndExpandedMoneyTaskBar = uiTaskBar.ExpandedMoneyTaskBar()
		if uiTaskBar.TaskBar.IS_EXPANDED:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND, ui.__mem_func__(self.ToggleExpandedButton))
			self.wndExpandedTaskBar = uiTaskBar.ExpandedTaskBar()
			self.wndExpandedTaskBar.LoadWindow()
			# Interface class'?n? ba?la
			self.wndExpandedTaskBar.BindInterfaceClass(self)

			if app.ENABLE_GROWTH_PET_SYSTEM:
				self.PetInformationActivate()
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_PET_INFO, ui.__mem_func__(self.TogglePetInformationWindow))

			if app.ENABLE_WIKI_SYSTEM:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_WIKI, ui.__mem_func__(self.OpenWikiWindow))

			if app.ENABLE_HUNTING_SYSTEM:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_HUNTING, ui.__mem_func__(self.ToggleHuntingWindow))

			if app.__AUTO_HUNT__:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_AUTO_WINDOW, ui.__mem_func__(self.ToggleAutoHuntWindow))
		else:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHAT, ui.__mem_func__(self.ToggleChat))

	def __MakeParty(self):
		wndParty = uiParty.PartyWindow()
		wndParty.Hide()
		self.wndParty = wndParty

	def __MakeGameButtonWindow(self):
		wndGameButton = uiGameButton.GameButtonWindow()
		wndGameButton.SetTop()
		wndGameButton.Show()
		wndGameButton.SetButtonEvent("STATUS", ui.__mem_func__(self.__OnClickStatusPlusButton))
		wndGameButton.SetButtonEvent("SKILL", ui.__mem_func__(self.__OnClickSkillPlusButton))
		wndGameButton.SetButtonEvent("QUEST", ui.__mem_func__(self.__OnClickQuestButton))
		wndGameButton.SetButtonEvent("BUILD", ui.__mem_func__(self.__OnClickBuildButton))
		wndGameButton.SetButtonEvent("GUIDE", ui.__mem_func__(self.__OnClickGuideButton))
		wndGameButton.SetButtonEvent("NOTIFICATION_HISTORY", ui.__mem_func__(self.__OnClickNotificationHistoryButton))
		wndGameButton.SetButtonEvent("BUFFI", ui.__mem_func__(self.ToggleCompanionBuffiWnd))
		import advanced_option_notifications
		advanced_option_notifications.BindButton(wndGameButton.gameButtonDict["NOTIFICATION_HISTORY"])

		self.wndGameButton = wndGameButton

	def __OnClickGuideButton(self):
		if app.ENABLE_WIKI_SYSTEM:
			self.OpenWikiWindow()

	def __OnClickNotificationHistoryButton(self):
		import advanced_option_notifications
		advanced_option_notifications.OpenHistory()

	def __IsChatOpen(self):
		return TRUE

	if app.ENABLE_AUTO_REFINE:
		def CheckRefineDialog(self, isFail):
			self.dlgRefineNew.CheckRefine(isFail)

	def __MakeWindows(self):
		if app.ENABLE_WHISPER_MESSENGER:
			try:
				self.wndWhisperMessenger = uiWhisperMessenger.WhisperMessenger()
				self.wndWhisperMessenger.BindInterface(self)
				self.wndWhisperMessenger.Hide()
				self.wndMessengerButton = uiWhisper.WhisperButton()
				self.wndMessengerButton.SetUpVisual("d:/ymir work/ui/game/whisper/mp_close.png")
				self.wndMessengerButton.SetOverVisual("d:/ymir work/ui/game/whisper/mp_open.png")
				self.wndMessengerButton.SetDownVisual("d:/ymir work/ui/game/whisper/mp_open.png")
				self.wndMessengerButton.SetToolTipText(localeInfo.WHISPER_MESSENGER_ENVELOPE)
				self.wndMessengerButton.ToolTipText.SetHorizontalAlignCenter()
				self.wndMessengerButton.SetEvent(ui.__mem_func__(self.__OnClickMessengerButton))
				self.messengerQuickCloseTip = uiToolTip.ToolTip()
				self.messengerQuickCloseTip.SetIconTextLine(localeInfo.WHISPER_TOOLTIP_CLOSE_SHORTCUT)
				self.messengerQuickCloseTip.Hide()
				self.wndMessengerButton.SetHoverEvent(ui.__mem_func__(self.ShowMessengerQuickCloseTip), ui.__mem_func__(self.HideMessengerQuickCloseTip))
				self.wndMessengerButton.badge = uiWhisperMessenger.UnreadBadge(self.wndMessengerButton)
				if not constInfo.MESSENGER_BUTTON_CLOSED:
					self.wndMessengerButton.Show()
			except:
				import dbg, traceback
				dbg.TraceError("WhisperMessenger init failed: " + traceback.format_exc())
				self.wndWhisperMessenger = None

		if app.ENABLE_GUILD_APPLICATION:
			try:
				self.wndGuildApplication = uiGuildApplication.GuildApplicationWindow()
				self.wndGuildJoinNotification = uiGuildApplication.GuildJoinNotification()
				uiGuildApplication.g_interface = self
			except:
				import dbg, traceback
				dbg.TraceError("GuildApplication init failed: " + traceback.format_exc())
				self.wndGuildApplication = None
				self.wndGuildJoinNotification = None

		wndCharacter = uiCharacter.CharacterWindow()

		wndInventory = uiInventory.InventoryWindow()
		wndInventory.BindInterfaceClass(self)

		# Sidebar butonlari artik ExpandedTaskBar'da, bu satirlar kaldirildi

		wndMiniMap = uiMiniMap.MiniMap()
		wndMiniMap.BindInterfaceClass(self)


		if not app.ENABLE_SPECIAL_INVENTORY:
			wndSafebox = uiSafebox.SafeboxWindow()
			if app.ENABLE_SLOT_MARKING_SYSTEM:
				wndSafebox.BindInterface(self)

			wndMall = uiSafebox.MallWindow()
			self.wndMall = wndMall

		wndChatLog = uiChat.ChatLogWindow()
		wndChatLog.BindInterface(self)



		self.wndCharacter = wndCharacter
		self.wndInventory = wndInventory
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul = uiDragonSoul.DragonSoulWindow()
			self.wndDragonSoul.BindInterfaceClass(self)
			self.wndDragonSoulRefine = uiDragonSoul.DragonSoulRefineWindow()
			self.wndDragonSoul.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)
			self.wndDragonSoulRefine.SetInventoryWindows(self.wndInventory, self.wndDragonSoul)
			self.wndInventory.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)
		self.wndMiniMap = wndMiniMap

		if not app.ENABLE_SPECIAL_INVENTORY:
			self.wndSafebox = wndSafebox

		self.wndChatLog = wndChatLog

		if app.ENABLE_IKASHOP_RENEWAL:
			self.wndIkashopBusiness = uiikashop.IkarusShopBusinessBoard()
			self.wndIkashopSearchShop = uiikashop.IkarusSearchShopBoard()
			if app.EXTEND_IKASHOP_PRO:
				from _weakref import proxy
				self.wndIkashopSearchShop.SetOpenWhisper(lambda name, _s = proxy(self) : _s.OpenWhisperDialog(name))
				self.wndIkashopSearchShop.SetOpenWhisperText(lambda name, text, _s = proxy(self) : _s.OpenWhisperWithText(name, text))
			if app.EXTEND_IKASHOP_ULTIMATE:
				self.wndIkashopShopSkin = uiikashop.IkarusShopSkinBoard()

		if app.ENABLE_SUNG_MAHI_TOWER:
			self.wndSungMahiWindow = uiSungMahi.SungMahiWindow()


		if app.ENABLE_GUILD_RANK_SYSTEM:
			self.wndGuildRanking = uiGuildRanking.GuildRankingDialog()

		if app.ENABLE_RENEWAL_SWITCHBOT:
			self.wndSwitchbot = uiSwitchbot.SwitchbotWindow()

		if app.ENABLE_VIEW_CHEST_DROP:
			self.dlgChestDrop = uiChestDrop.ChestDropWindow()

		self.dlgDropInfo = uidropinfo.DropInfoWindow()
		self.wndShopSoldNotice = uishopsoldnotice.ShopSoldNotice()
		self.dlgShootingStars = uishootingstars.ShootingStarLayer()

		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory = uiSpecialInventory.SpecialInventoryWindow()
			self.wndSpecialInventory.BindInterfaceClass(self)
			self.wndSafebox = uiSafebox.SafeboxWindow(self.wndSpecialInventory)
			self.wndMall = uiSafebox.MallWindow(self.wndSpecialInventory)
			self.wndSpecialInventory.BindSafeboxAndMallClass(self.wndSafebox, self.wndMall)

		if app.ENABLE_AURA_COSTUME_SYSTEM:
			wndAura = uiAura.AuraWindow()
			self.wndAura = wndAura

		if app.ENABLE_YIN_AND_YANG_ATTR:
			self.wndYinAndYangInventory = uiYinAndYangAttr.YinAndYangInventory()
			self.wndYinAndYangInventory.BindInventory(self.wndInventory)
			self.wndYinAndYangInventory.Hide()

			self.wndYinAndYangHarmony = uiYinAndYangAttr.YinAndYangHarmony()
			self.wndYinAndYangHarmony.BindInventory(self.wndInventory)
			self.wndYinAndYangHarmony.Hide()

		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.wndPetInfoWindow = uiPetInfo.PetInformationWindow()
			self.wndPetInfoWindow.BindInterfaceClass(self)
			self.wndInventory.SetPetHatchingWindow(self.wndPetInfoWindow.GetPetHatchingWindow())
			self.wndInventory.SetPetFeedWindow(self.wndPetInfoWindow.GetPetFeedWindow())
			self.wndInventory.SetPetNameChangeWindow(self.wndPetInfoWindow.GetPetNameChangeWindow())

		self.wndCompanion = uiCompanion.CompanionWindow()
		self.wndCompanion.BindInterface(self)
		self.wndCompanion.Hide()

		if app.ENABLE_SKILL_UPGRADE:
			self.wndSkillUpgrade = uiSkillUpgrade.SkillUpgradeWindow()
			self.wndSkillUpgrade.BindInterface(self)
			self.wndSkillUpgrade.Hide()

		if app.ENABLE_BRAVE_CAPE_RENEWAL:
			self.wndBraveCape = uiAutoCape.BraveCapeWindow()
			self.wndBraveCape.BindInterface(self)
			self.wndBraveCape.Hide()

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			self.wndWarpWindow = uiTeleport.TeleportWindow()

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			self.wndChangeLook = uiChangeLook.ChangeLookWindow()
		if app.ENABLE_MOVE_COSTUME_ACCE_ATTR:
			self.wndItemCombination = uiItemCombination.ItemCombinationWindow()

		if app.ENABLE_BIOLOG_RENEWAL:
			self.wndBiologist = uibiologist.BiologistWindow()
			self.wndBiologist.BindInterface(self)

		if app.ENABLE_BATTLEPASS_RENEWAL:
			self.wndBattlePass = uibattlepass.BattlePassWindow()
			self.wndBattlePass.BindInterface(self)

		if app.ENABLE_GLOBAL_RANKING:
			self.wndRanking = uiglobalranking.RankingWindow()

		elif app.ENABLE_RANKING:
			self.wndRanking = uiranking.RankingWindow()

	def __MakeDialogs(self):
		self.dlgExchange = uiExchange.ExchangeDialog()
		self.dlgExchange.LoadDialog()
		self.dlgExchange.SetCenterPosition()
		if app.ENABLE_SLOT_MARKING_SYSTEM:
			self.dlgExchange.BindInterface(self)
		self.dlgExchange.Hide()

		self.dlgPointReset = uiPointReset.PointResetDialog()
		self.dlgPointReset.LoadDialog()
		self.dlgPointReset.Hide()

		self.dlgShop = uiShop.ShopDialog()
		self.dlgShop.LoadDialog()
		if app.ENABLE_SLOT_MARKING_SYSTEM:
			self.dlgShop.BindInterface(self)
		self.dlgShop.Hide()

		if app.ENABLE_GAYA_TICKET_SYSTEM:
			self.wndImproveGemTicket = uiGemTicket.GemTicketWindow()

		self.dlgRestart = uiRestart.RestartDialog()
		self.dlgRestart.LoadDialog()
		self.dlgRestart.Hide()

		self.dlgSystem = uiSystem.SystemDialog()
		self.dlgSystem.BindInterfaceClass(self)
		self.dlgSystem.LoadDialog()
		self.dlgSystem.Hide()

		self.dlgPassword = uiSafebox.PasswordDialog()
		self.dlgPassword.Hide()

		self.hyperlinkItemTooltip = uiToolTip.HyperlinkItemToolTip()
		self.hyperlinkItemTooltip.Hide()

		self.tooltipItem = uiToolTip.ItemToolTip()
		if app.ENABLE_SLOT_MARKING_SYSTEM:
			self.tooltipItem.BindInterface(self)
		self.tooltipItem.Hide()

		self.tooltipSkill = uiToolTip.SkillToolTip()
		self.tooltipSkill.Hide()

		self.whisper_tooltip = None
		if app.ENABLE_WHISPER_CLOSE_SHORTCUT:
			self.whisper_tooltip = uiToolTip.ToolTip()
			self.whisper_tooltip.SetIconTextLine(localeInfo.WHISPER_TOOLTIP_CLOSE_SHORTCUT)
			self.whisper_tooltip.Hide()

		self.privateShopBuilder = uiPrivateShopBuilder.PrivateShopBuilder()
		if app.ENABLE_SLOT_MARKING_SYSTEM:
			self.privateShopBuilder.BindInterface(self)
		self.privateShopBuilder.Hide()

		if app.ENABLE_REFINE_SEAL_RENEWAL:
			self.dlgRefineNew = uiRefineRenewal.RefineDialogRenewal()
			self.dlgRefineNew.SetInven(self.wndInventory)
			self.dlgRefineNew.BindInterface(self)
		else:
			self.dlgRefineNew = uiRefine.RefineDialogNew()
			if app.ENABLE_SLOT_MARKING_SYSTEM:
				self.dlgRefineNew.SetInven(self.wndInventory)

			if constInfo.SHOW_REFINE_ITEM_DESC:
				self.dlgRefineNew.BindInterface(self)

		self.dlgRefineNew.Hide()


		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.tooltipPetSkill = uiToolTip.PetSkillToolTip()
			self.tooltipPetSkill.Hide()

		if app.ENABLE_RENEWAL_SPECIAL_CHAT:
			self.wndSpecialChat = uiSpecialChat.SpecialChat()
			self.wndSpecialChat.Hide()

		if app.ENABLE_HUNTING_SYSTEM:
			self.wndHunting = uiHunting.HuntingWindow()
			self.wndHuntingSelect = uiHunting.HuntingSelectWindow()
			self.wndHuntingReward = uiHunting.HuntingRewardWindow()

	def __MakeTipBoard(self):
		self.tipBoard = uiTip.TipBoardNew()
		self.tipBoard.Hide()

		self.bigBoard = uiTip.BigBoard()
		self.bigBoard.Hide()

		if app.ENABLE_RENEWAL_OX_EVENT:
			self.bigBoardControl = uiTip.BigBoardControl()
			self.bigBoardControl.Hide()

	def __MakeWebWindow(self):
		if constInfo.IN_GAME_SHOP_ENABLE:
			import uiWeb
			self.wndWeb = uiWeb.WebWindow()
			self.wndWeb.LoadWindow()
			self.wndWeb.Hide()

	def __MakeCubeWindow(self):
		self.wndCube = uiCube.CubeWindow()
		self.wndCube.LoadWindow()
		self.wndCube.Hide()

	def __MakeCubeResultWindow(self):
		self.wndCubeResult = uiCube.CubeResultWindow()
		self.wndCubeResult.LoadWindow()
		self.wndCubeResult.Hide()

	def __MakeItemFinder(self):
		self.wndItemFinder = uiitemfinder.ItemFinder()
		self.wndItemFinder.LoadWindow()
		self.wndItemFinder.Hide()

	def __MakeItemSelectWindow(self):
		self.wndItemSelect = uiselectitem.SelectItemWindow()
		self.wndItemSelect.Hide()

	if app.ENABLE_DUNGEON_INFO:
		def __MakeTableDungeonInfo(self):
			self.wndTableDungeonInfo = uitabledungeon.TableDungeonWindows()
			self.wndTableDungeonInfo.Hide()

	if app.ENABLE_RENEWAL_CUBE:
		def __MakeCubeRenewal(self):
			import uicuberenewal
			self.wndCubeRenewal = uicuberenewal.CubeRenewalWindows()
			self.wndCubeRenewal.Hide()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def __MakeAcceWindow(self):
			self.wndAcceCombine = uiAcce.CombineWindow()
			self.wndAcceCombine.LoadWindow()
			if app.ENABLE_SLOT_MARKING_SYSTEM:
				self.wndAcceCombine.BindInterface(self)
				if self.wndInventory:
					self.wndAcceCombine.SetInven(self.wndInventory)
			self.wndAcceCombine.Hide()

			self.wndAcceAbsorption = uiAcce.AbsorbWindow()
			self.wndAcceAbsorption.LoadWindow()
			if app.ENABLE_SLOT_MARKING_SYSTEM:
				self.wndAcceAbsorption.BindInterface(self)
				if self.wndInventory:
					self.wndAcceAbsorption.SetInven(self.wndInventory)
			self.wndAcceAbsorption.Hide()

			if self.wndInventory:
				self.wndInventory.SetAcceWindow(self.wndAcceCombine, self.wndAcceAbsorption)

	if app.ENABLE_RENEWAL_SKILL_SELECT:
		def __MakeSkillSelectWindow(self):
			self.wndSkillSelect = uiSkillSelect.SkillSelectWindow()
			self.wndSkillSelect.LoadWindow()
			self.wndSkillSelect.Hide()

	if app.ENABLE_GAYA_SYSTEM:
		def __MakeItemSelectWindowEx(self):
			self.wndItemSelectEx = uiselectitemEx.SelectItemWindowEx()
			self.wndItemSelectEx.Hide()

		def __MakeGemGui(self):
			self.wndGemG = uiGemShop.SelectGems()
			self.wndGemG.LoadWindow()
			self.wndGemG.Hide()

			self.wndGemM = uiGemShop.SelectGemsShop()
			self.wndGemM.LoadWindow()
			self.wndGemM.Hide()

	def MakeInterface(self):
		self.__MakeMessengerWindow()
		self.__MakeGuildWindow()
		self.__MakeChatWindow()
		if app.ENABLE_AUTO_CHAT:
			import uiautochat
			self.wndAutoChat = uiautochat.AutoChatWindow()
			self.wndAutoChat.BindInterface(self)
		self.__MakeParty()
		self.__MakeWindows()
		self.__MakeDialogs()

		self.__MakeUICurtain()
		self.__MakeTaskBar()
		self.__MakeGameButtonWindow()
		self.__MakeTipBoard()
		self.__MakeWebWindow()
		self.__MakeCubeWindow()
		self.__MakeCubeResultWindow()
		self.__MakeExpandMoney()
		self.__MakeItemFinder()
		self.__MakeItemSelectWindow()

		if app.ENABLE_RENEWAL_CUBE:
			self.__MakeCubeRenewal()

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.__MakeAcceWindow()

		if app.ENABLE_GAYA_SYSTEM:
			self.__MakeGemGui()

		if app.ENABLE_RENEWAL_SKILL_SELECT:
			self.__MakeSkillSelectWindow()

		if app.ENABLE_DUNGEON_INFO:
			self.__MakeTableDungeonInfo()

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		if app.ENABLE_WHISPER_MESSENGER:
			self.__ArrangeWhisperButton()

		if app.ENABLE_ZODIAC_MISSION:
			self.__Make12ziTimerWindow()
			self.__Make12ziRewardWindow()


		if app.ENABLE_GAYA_SYSTEM:
			self.__MakeItemSelectWindowEx()

		self.privateShopAdvertisementBoardDict = {}

		if app.ENABLE_BIOLOG_RENEWAL:
			self.wndBiologist.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_BATTLEPASS_RENEWAL:
			self.wndBattlePass.SetItemToolTip(self.tooltipItem)

		self.wndInventory.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_DRAGON_SOUL_SYSTEM and self.wndDragonSoul:
			self.wndDragonSoul.SetItemToolTip(self.tooltipItem)
			self.wndDragonSoulRefine.SetItemToolTip(self.tooltipItem)
		if self.wndEnergyCrystal:
			self.wndEnergyCrystal.SetItemToolTip(self.tooltipItem)
		self.wndSafebox.SetItemToolTip(self.tooltipItem)
		self.wndCube.SetItemToolTip(self.tooltipItem)
		self.wndCubeResult.SetItemToolTip(self.tooltipItem)



		# ITEM_MALL
		self.wndMall.SetItemToolTip(self.tooltipItem)
		# END_OF_ITEM_MALL
		if app.ENABLE_SUNG_MAHI_TOWER:
			self.wndSungMahiWindow.SetItemToolTip(self.tooltipItem)
		self.wndCharacter.SetSkillToolTip(self.tooltipSkill)
		self.wndTaskBar.SetItemToolTip(self.tooltipItem)
		self.wndTaskBar.SetSkillToolTip(self.tooltipSkill)
		self.wndGuild.SetSkillToolTip(self.tooltipSkill)
		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.wndItemSelect.SetItemToolTip(self.tooltipItem)
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		if app.ENABLE_GAYA_SYSTEM:
			self.wndGemM.SetItemToolTip(self.tooltipItem)

		self.dlgShop.SetItemToolTip(self.tooltipItem)
		self.dlgExchange.SetItemToolTip(self.tooltipItem)
		self.privateShopBuilder.SetItemToolTip(self.tooltipItem)



		if app.ENABLE_RENEWAL_SWITCHBOT:
			self.wndSwitchbot.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.wndAcceCombine.SetItemToolTip(self.tooltipItem)
			self.wndAcceAbsorption.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_VIEW_CHEST_DROP:
			self.dlgChestDrop.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_AURA_COSTUME_SYSTEM:
			self.wndAura.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_LOCK_SLOT_WHEN_SHOP_BUILDING:
			self.privateShopBuilder.SetInven(player.INVENTORY, self.wndInventory)
		elif app.ENABLE_SLOT_MARKING_SYSTEM:
			self.privateShopBuilder.SetInven(self.wndInventory)
			if app.ENABLE_SPECIAL_INVENTORY:
				self.privateShopBuilder.SetSpecialInven(self.wndSpecialInventory)

		if app.ENABLE_SLOT_MARKING_SYSTEM:
			self.dlgExchange.SetInven(self.wndInventory)
			if app.ENABLE_SPECIAL_INVENTORY:
				self.dlgExchange.SetSpecialInven(self.wndSpecialInventory)


		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.wndPetInfoWindow.SetItemToolTip(self.tooltipItem)
			self.wndPetInfoWindow.SetInven(self.wndInventory)
			self.wndPetInfoWindow.SetPetSkillToolTip(self.tooltipPetSkill)

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			self.wndChangeLook.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_MOVE_COSTUME_ACCE_ATTR:
			self.wndItemCombination.SetItemToolTip(self.tooltipItem)
			self.wndItemCombination.SetInven(self.wndInventory)

		if app.ENABLE_GAYA_SYSTEM:
			self.wndItemSelectEx.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_YIN_AND_YANG_ATTR:
			self.wndYinAndYangInventory.SetItemToolTip(self.tooltipItem)

		self.__InitWhisper()

	if app.LINK_IN_CHAT:
		def AnswerOpenLink(self, answer):
			if not self.OpenLinkQuestionDialog:
				return

			self.OpenLinkQuestionDialog.Close()
			self.OpenLinkQuestionDialog = None

			if not answer:
				return

			link = constInfo.link
			os.system(link)


	def MakeHyperlinkTooltip(self, hyperlink):
		tokens = hyperlink.split(":")
		if tokens and len(tokens):
			type = tokens[0]
			if "item" == type:
				self.hyperlinkItemTooltip.SetHyperlinkItem(tokens)
			elif "pm" == type and str(tokens[1]) != player.GetMainCharacterName():
				self.OpenWhisperDialog(str(tokens[1]))
			elif "web" == type and tokens[1].startswith("httpXxX") or "web" == type and tokens[1].startswith("httpsXxX"):
					OpenLinkQuestionDialog = uiCommon.QuestionDialog2()
					OpenLinkQuestionDialog.SetText1(localeInfo.CHAT_OPEN_LINK_DANGER)
					OpenLinkQuestionDialog.SetText2(localeInfo.CHAT_OPEN_LINK)
					OpenLinkQuestionDialog.SetAcceptEvent(lambda arg=TRUE: self.AnswerOpenLink(arg))
					OpenLinkQuestionDialog.SetCancelEvent(lambda arg=FALSE: self.AnswerOpenLink(arg))
					constInfo.link = "start " + tokens[1].replace("XxX", "://").replace("&","^&")
					OpenLinkQuestionDialog.Open()
					self.OpenLinkQuestionDialog = OpenLinkQuestionDialog
			elif "sysweb" == type:
				os.system("start " + tokens[1].replace("XxX", "://"))
			elif "petitem" == type and app.ENABLE_GROWTH_PET_SYSTEM:
				self.hyperlinkItemTooltip.SetHyperlinkPetItem(tokens)
			elif "wiki" == type:
				self.OpenWikiWindow()
				self.wndWiki.OpenRules()
			elif "ikashop" == type and app.ENABLE_IKASHOP_RENEWAL:
				if len(tokens) > 1 and self.wndIkashopSearchShop and uiikashop.SEARCH_SHOP_RENEWAL:
					self.wndIkashopSearchShop.SearchSeller(":".join(tokens[1:]))
			elif "shop" == type and app.ENABLE_AUTO_CHAT:
				if len(tokens) > 1 and str(tokens[1]) != player.GetMainCharacterName():
					self.OpenWhisperDialog(str(tokens[1]))

	## Make Windows & Dialogs
	################################

	def Close(self):
		import window_status
		window_status.Save()

		if app.__DUNGEON_INFO__:
			if self.wndDungeonTrack:
				self.wndDungeonTrack.Close()
				self.wndDungeonTrack.Destroy()
				self.wndDungeonTrack = None
			if self.wndDungeonManager:
				self.wndDungeonManager.Destroy()
				self.wndDungeonManager = None

		if app.ENABLE_TRACK_WINDOW:
			if self.wndTrackWindow:
				self.wndTrackWindow.Close()
				self.wndTrackWindow.Destroy()
				self.wndTrackWindow=None
		if self.dlgWhisperWithoutTarget:
			self.dlgWhisperWithoutTarget.Destroy()
			del self.dlgWhisperWithoutTarget

		if app.ENABLE_ZODIAC_MISSION:
			if self.wnd12ziTimer:
				self.wnd12ziTimer.Hide()
				self.wnd12ziTimer=None
			if self.wnd12ziReward:
				self.wnd12ziReward.Hide()
				self.wnd12ziReward=None

		if uiQuest.QuestDialog.__dict__.has_key("QuestCurtain"):
			uiQuest.QuestDialog.QuestCurtain.Close()

		if self.wndQuestWindow:
			for key, eachQuestWindow in self.wndQuestWindow.items():
				eachQuestWindow.nextCurtainMode = -1
				eachQuestWindow.CloseSelf()
				eachQuestWindow = None
		self.wndQuestWindow = {}

		if app.ENABLE_WIKI_SYSTEM:
			if self.wndWiki:
				self.wndWiki.Close()
				self.wndWiki.Destroy()
				self.wndWiki=None

		if app.ENABLE_ITEMSHOP:
			if self.wndItemShop:
				self.wndItemShop.Hide()
				self.wndItemShop.Destroy()
				self.wndItemShop = None

		if app.ENABLE_DUNGEON_INFO:
			if self.wndDungeonInfo:
				self.wndDungeonInfo.Close()
				self.wndDungeonInfo.Destroy()
				self.wndDungeonInfo = None

		if self.uiAffectshower:
			self.uiAffectshower = None

		if self.wndChat:
			self.wndChat.Destroy()

		if self.wndAutoChat:
			self.wndAutoChat.Destroy()
			self.wndAutoChat = None

		if self.wndTaskBar:
			self.wndTaskBar.Destroy()

		if self.wndEnergyBar:
			self.wndEnergyBar.Destroy()
			self.wndEnergyBar = None
		if self.wndEnergyCrystal:
			self.wndEnergyCrystal.Destroy()
			self.wndEnergyCrystal = None

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Destroy()

		if self.wndCharacter:
			self.wndCharacter.Destroy()

		if self.wndInventory:
			self.wndInventory.Hide()
			self.wndInventory.Destroy()

		if self.wndDragonSoul:
			self.wndDragonSoul.CancelDlgQuestion()
			self.wndDragonSoul.Destroy()
			self.wndDragonSoul = None
		if self.wndDragonSoulRefine:
			self.wndDragonSoulRefine.Destroy()
			self.wndDragonSoulRefine = None

		if self.wndExpandedMoney:
			self.wndExpandedMoney.Destroy()


		if app.ENABLE_GAYA_TICKET_SYSTEM:
			if (self.wndImproveGemTicket):
				del self.wndImproveGemTicket

		if self.dlgExchange:
			self.dlgExchange.Destroy()

		if self.dlgPointReset:
			self.dlgPointReset.Destroy()

		if self.dlgShop:
			self.dlgShop.Destroy()

		if self.dlgRestart:
			self.dlgRestart.Destroy()

		if self.dlgSystem:
			self.dlgSystem.Destroy()

		if self.dlgPassword:
			self.dlgPassword.Destroy()

		if self.wndMiniMap:
			self.wndMiniMap.Destroy()

		if self.wndSafebox:
			self.wndSafebox.Destroy()

		if self.wndWeb:
			self.wndWeb.Destroy()
			self.wndWeb = None

		if self.wndMall:
			self.wndMall.Destroy()

		if self.wndParty:
			self.wndParty.Destroy()


		if self.wndCube:
			self.wndCube.Destroy()

		if app.ENABLE_IKASHOP_RENEWAL:
			if self.wndIkashopBusiness:
				self.wndIkashopBusiness.Destroy()
				self.wndIkashopBusiness = None
			if self.wndIkashopSearchShop:
				self.wndIkashopSearchShop.Destroy()
				self.wndIkashopSearchShop = None
			if app.EXTEND_IKASHOP_ULTIMATE:
				if self.wndIkashopShopSkin:
					self.wndIkashopShopSkin.Destroy()
					self.wndIkashopShopSkin = None

		if self.wndCubeResult:
			self.wndCubeResult.Destroy()

		if app.ENABLE_DUNGEON_INFO:
			if self.wndTableDungeonInfo:
				self.wndTableDungeonInfo.Hide()
				self.wndTableDungeonInfo.Close()
				self.wndTableDungeonInfo.Destroy()

		if self.wndMessenger:
			self.wndMessenger.Destroy()

		if self.wndItemFinder:
			self.wndItemFinder.Destroy()

		if self.wndGuild:
			self.wndGuild.Destroy()

		if self.privateShopBuilder:
			self.privateShopBuilder.Destroy()

		if self.dlgRefineNew:
			self.dlgRefineNew.Destroy()


		if self.wndGuildBuilding:
			self.wndGuildBuilding.Destroy()

		if self.wndGameButton:
			self.wndGameButton.Destroy()


		if app.ENABLE_HUNTING_SYSTEM:
			if self.wndHunting:
				self.wndHunting.Destroy()
				del self.wndHunting
			if self.wndHuntingSelect:
				self.wndHuntingSelect.Destroy()
				del self.wndHuntingSelect
			if self.wndHuntingReward:
				self.wndHuntingReward.Destroy()
				del self.wndHuntingReward

		if app.__AUTO_HUNT__:
			if self.wndAutoHunt:
				self.wndAutoHunt.Close()
				self.wndAutoHunt.Destroy()
				self.wndAutoHunt = None

		if app.ENABLE_BIOLOG_RENEWAL:
			if self.wndBiologist:
				self.wndBiologist.Destroy()

		if app.ENABLE_BATTLEPASS_RENEWAL:
			if self.wndBattlePass:
				self.wndBattlePass.Destroy()

		# ITEM_MALL
		if self.mallPageDlg:
			self.mallPageDlg.Destroy()
		# END_OF_ITEM_MALL

		# ACCESSORY_REFINE_ADD_METIN_STONE
		if self.wndItemSelect:
			self.wndItemSelect.Destroy()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE


		if app.ENABLE_SUNG_MAHI_TOWER:
			if self.wndSungMahiWindow:
				self.wndSungMahiWindow.Destroy()

		if app.ENABLE_GUILD_RANK_SYSTEM:
			if self.wndGuildRanking:
				self.wndGuildRanking.Destory()

		if app.ENABLE_RENEWAL_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Hide()
				self.wndSwitchbot.Destroy()

		if app.ENABLE_GAYA_SYSTEM:
			if self.wndItemSelectEx:
				self.wndItemSelectEx.Destroy()

			if self.wndGemG:
				self.wndGemG.Destroy()

			if self.wndGemM:
				self.wndGemM.Destroy()


		if app.ENABLE_RENEWAL_CUBE:
			if self.wndCubeRenewal:
				self.wndCubeRenewal.Destroy()
				self.wndCubeRenewal.Close()

		if app.ENABLE_RANKING:
			if self.wndRanking:
				self.wndRanking.Destroy()
				del self.wndRanking

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


		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if self.wndAcceCombine:
				self.wndAcceCombine.Destroy()

			if self.wndAcceAbsorption:
				self.wndAcceAbsorption.Destroy()


		if app.ENABLE_VIEW_CHEST_DROP:
			if self.dlgChestDrop:
				self.dlgChestDrop.Destroy()

		if self.dlgDropInfo:
			self.dlgDropInfo.Destroy()
		if self.wndShopSoldNotice:
			self.wndShopSoldNotice.Destroy()
			self.wndShopSoldNotice = None

		if self.dlgShootingStars:
			self.dlgShootingStars.Destroy()

		if app.ENABLE_SPECIAL_INVENTORY:
			if self.wndSpecialInventory:
				self.wndSpecialInventory.Hide()
				self.wndSpecialInventory.Destroy()

		if app.ENABLE_RENDER_TARGET:
			if self.wndRenderTarget:
				self.wndRenderTarget.Close()
				self.wndRenderTarget.Destroy()
				self.wndRenderTarget = None

		if app.ENABLE_RENEWAL_SKILL_SELECT:
			if self.wndSkillSelect:
				self.wndSkillSelect.Destroy()

		if app.ENABLE_AURA_COSTUME_SYSTEM:
			if self.wndAura:
				self.wndAura.Destroy()
			del self.wndAura

		if app.ENABLE_YIN_AND_YANG_ATTR:
			if self.wndYinAndYangInventory:
				self.wndYinAndYangInventory.Destroy()
				self.wndYinAndYangInventory = None

			if self.wndYinAndYangHarmony:
				self.wndYinAndYangHarmony.Destroy()
				self.wndYinAndYangHarmony = None


		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.Destroy()

		if self.wndCompanion:
			self.wndCompanion.Destroy()
			self.wndCompanion = None

		if self.wndSkillUpgrade:
			self.wndSkillUpgrade.Destroy()
			self.wndSkillUpgrade = None

		if self.wndBraveCape:
			self.wndBraveCape.Destroy()
			self.wndBraveCape = None

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			if self.wndWarpWindow:
				self.wndWarpWindow.Destroy()

		if app.ENABLE_RENEWAL_SPECIAL_CHAT:
			if self.wndSpecialChat:
				self.wndSpecialChat.Destroy()

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if self.wndChangeLook:
				del self.wndChangeLook

		if app.ENABLE_MOVE_COSTUME_ACCE_ATTR:
			if self.wndItemCombination:
				self.wndItemCombination.Destroy()
				del self.wndItemCombination
				self.wndItemCombination = None

		self.wndChatLog.Destroy()
		for btn in self.questButtonList:
			btn.SetEvent(0)
		for btn in self.whisperButtonList:
			btn.SetEvent(0)
		for dlg in self.whisperDialogDict.itervalues():
			dlg.Destroy()
		if app.ENABLE_WHISPER_MESSENGER and self.wndWhisperMessenger:
			self.wndWhisperMessenger.Destroy()
			self.wndWhisperMessenger.Hide()
			self.wndWhisperMessenger = None
		if app.ENABLE_WHISPER_MESSENGER and self.wndMessengerButton:
			self.wndMessengerButton.SetEvent(0)
			self.wndMessengerButton.Hide()
			self.wndMessengerButton = None
		if app.ENABLE_GUILD_APPLICATION:
			if self.wndGuildApplication:
				self.wndGuildApplication.Destroy()
				self.wndGuildApplication = None
			if self.wndGuildJoinNotification:
				self.wndGuildJoinNotification.Hide()
				self.wndGuildJoinNotification = None
			uiGuildApplication.g_interface = None
		for brd in self.guildScoreBoardDict.itervalues():
			brd.Destroy()
		for dlg in self.equipmentDialogDict.itervalues():
			dlg.Destroy()

		# ITEM_MALL
		del self.mallPageDlg
		# END_OF_ITEM_MALL

		del self.wndGuild
		del self.wndMessenger
		del self.wndUICurtain
		del self.wndChat

		del self.wndTaskBar
		if self.wndExpandedTaskBar:
			del self.wndExpandedTaskBar

		del self.wndCharacter
		del self.wndInventory
		del self.wndExpandedMoney
		del self.dlgExchange
		del self.dlgPointReset
		del self.dlgShop
		del self.dlgRestart
		del self.dlgSystem
		del self.dlgPassword
		del self.hyperlinkItemTooltip
		del self.tooltipItem
		del self.tooltipSkill
		del self.wndMiniMap
		del self.wndSafebox
		del self.wndMall
		del self.wndParty
		del self.wndCube
		del self.wndCubeResult
		del self.privateShopBuilder
		del self.inputDialog
		del self.wndItemFinder
		del self.wndChatLog
		del self.dlgRefineNew
		del self.wndGuildBuilding
		del self.wndGameButton
		del self.tipBoard
		del self.bigBoard
		del self.wndItemSelect

		if app.ENABLE_SUNG_MAHI_TOWER:
			del self.wndSungMahiWindow

		if app.ENABLE_GUILD_RANK_SYSTEM:
			del self.wndGuildRanking

		if app.ENABLE_RENEWAL_SWITCHBOT:
			del self.wndSwitchbot

		if app.ENABLE_RENEWAL_CUBE:
			del self.wndCubeRenewal

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			del self.wndAcceCombine
			del self.wndAcceAbsorption

		if app.ENABLE_VIEW_CHEST_DROP:
			if self.dlgChestDrop:
				del self.dlgChestDrop

		if self.dlgDropInfo:
			del self.dlgDropInfo

		if self.dlgShootingStars:
			del self.dlgShootingStars

		if app.ENABLE_SPECIAL_INVENTORY:
			if self.wndSpecialInventory:
				del self.wndSpecialInventory

		if app.ENABLE_GAYA_SYSTEM:
			del self.wndGemG
			del self.wndGemM

		if app.ENABLE_RENEWAL_OX_EVENT:
			del self.bigBoardControl

		if app.ENABLE_GAYA_SYSTEM:
			del self.wndItemSelectEx

		if app.ENABLE_RENEWAL_SKILL_SELECT:
			del self.wndSkillSelect

		if app.ENABLE_NEW_DUNGEON_LIB:
			if self.wndDungeonTimer:
				self.wndDungeonTimer.Hide()
				self.wndDungeonTimer = 0

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				del self.wndPetInfoWindow
			self.wndPetInfoWindow = None
			del self.tooltipPetSkill

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			del self.wndWarpWindow

		if app.ENABLE_RENEWAL_SPECIAL_CHAT:
			del self.wndSpecialChat

		if app.ENABLE_BIOLOG_RENEWAL:
			if self.wndBiologist:
				del self.wndBiologist

		if app.ENABLE_BATTLEPASS_RENEWAL:
			if self.wndBattlePass:
				del self.wndBattlePass

		if app.ENABLE_DUNGEON_INFO:
			del self.wndTableDungeonInfo


		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}

		uiChat.DestroyChatInputSetWindow()


	## Skill
	def OnUseSkill(self, slotIndex, coolTime):
		self.wndCharacter.OnUseSkill(slotIndex, coolTime)
		self.wndTaskBar.OnUseSkill(slotIndex, coolTime)
		self.wndGuild.OnUseSkill(slotIndex, coolTime)

	def OnActivateSkill(self, slotIndex):
		self.wndCharacter.OnActivateSkill(slotIndex)
		self.wndTaskBar.OnActivateSkill(slotIndex)

	def OnDeactivateSkill(self, slotIndex):
		self.wndCharacter.OnDeactivateSkill(slotIndex)
		self.wndTaskBar.OnDeactivateSkill(slotIndex)

	def OnChangeCurrentSkill(self, skillSlotNumber):
		self.wndTaskBar.OnChangeCurrentSkill(skillSlotNumber)

	def SkillClearCoolTime(self, slotIndex):
		self.wndCharacter.SkillClearCoolTime(slotIndex)
		self.wndTaskBar.SkillClearCoolTime(slotIndex)

	def SelectMouseButtonEvent(self, dir, event):
		self.wndTaskBar.SelectMouseButtonEvent(dir, event)

	## Refresh
	def RefreshAlignment(self):
		self.wndCharacter.RefreshAlignment()

	def RefreshStatus(self):
		self.__CheckDropYang()
		self.wndTaskBar.RefreshStatus()
		if self.wndEnergyBar:
			self.wndEnergyBar.RefreshStatus()
		if self.wndDragonSoul:
			self.wndDragonSoul.RefreshStatus()
		self.wndCharacter.RefreshStatus()
		self.wndExpandedMoney.RefreshStatus()
		if self.wndExpandedMoneyTaskBar:
			self.wndExpandedMoneyTaskBar.RefreshStatus()
		self.wndInventory.RefreshStatus()

		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.wndPetInfoWindow.RefreshStatus()

	def RefreshStamina(self):
		self.wndTaskBar.RefreshStamina()

	def RefreshSkill(self):
		self.wndCharacter.RefreshSkill()
		self.wndTaskBar.RefreshSkill()

	def RefreshSkillCoolTime(self):
		if self.wndTaskBar:
			self.wndTaskBar.RefreshSkillCoolTime()
		if self.wndCharacter:
			self.wndCharacter.RefreshSkillCoolTime()

	def __CheckDropYang(self):
		return
		gold = player.GetElk()
		last = self._dropInfoGold
		self._dropInfoGold = gold
		if last is None or gold <= last or self.dlgDropInfo is None:
			return
		try:
			import exchange
			if shop.IsOpen() or exchange.isTrading():
				return
		except Exception:
			pass
		import advanced_options_runtime
		if advanced_options_runtime.Get("view_drop_ui", True):
			self.dlgDropInfo.AppendYang(gold - last)

	def __CheckNewDropItems(self):
		return
		if self.dlgDropInfo is None:
			return
		import advanced_options_runtime
		if not advanced_options_runtime.Get("view_drop_ui", False):
			return
		slotCount = player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT
		snapshot = {}
		for slot in xrange(slotCount):
			vnum = player.GetItemIndex(slot)
			if vnum:
				snapshot[slot] = (vnum, player.GetItemCount(slot))
		previous = self._dropInfoSnapshot
		self._dropInfoSnapshot = snapshot
		if previous is None:
			return
		for slot, (vnum, count) in snapshot.items():
			oldEntry = previous.get(slot)
			if oldEntry is None:
				self.dlgDropInfo.AppendDropInfo(vnum, count)
			elif oldEntry[0] == vnum and count > oldEntry[1]:
				self.dlgDropInfo.AppendDropInfo(vnum, count - oldEntry[1])
			elif oldEntry[0] != vnum:
				self.dlgDropInfo.AppendDropInfo(vnum, count)

	def RefreshInventory(self):
		self.__CheckNewDropItems()
		if self.wndTaskBar:
			self.wndTaskBar.RefreshQuickSlot()
		if self.wndInventory:
			self.wndInventory.RefreshItemSlot()
		if self.wndDragonSoul:
			self.wndDragonSoul.RefreshItemSlot()

		if app.ENABLE_BIOLOG_RENEWAL:
			if self.wndBiologist:
				self.wndBiologist.RefreshItemCount()

		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory.RefreshItemSlot()

		if app.ENABLE_AURA_COSTUME_SYSTEM:
			if player.IsAuraRefineWindowOpen():
				if self.wndAura and self.wndAura.IsShow():
					self.wndAura.RefreshAuraWindow()

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if player.GetChangeLookWindowOpen() == 1:
				self.wndChangeLook.RefreshChangeLookWindow()

	def RefreshCharacter(self):
		self.wndCharacter.RefreshCharacter()
		self.wndTaskBar.RefreshQuickSlot()

	def RefreshQuest(self):
		self.wndCharacter.RefreshQuest()

	def RefreshSafebox(self):
		self.wndSafebox.RefreshSafebox()

	if app.ENABLE_GUILD_RANK_SYSTEM:
		def OpenGuildRanking(self):
			self.wndGuildRanking.Open()

	# ITEM_MALL
	def RefreshMall(self):
		self.wndMall.RefreshMall()

	def OpenItemMall(self):
		if not self.mallPageDlg:
			self.mallPageDlg = uiShop.MallPageDialog()

		self.mallPageDlg.Open()
	# END_OF_ITEM_MALL

	def RefreshMessenger(self):
		self.wndMessenger.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.wndGuild.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.wndGuild.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.wndGuild.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.wndGuild.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.wndGuild.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.wndGuild.RefreshGuildGradePage()


	def DeleteGuild(self):
		self.wndMessenger.ClearGuildMember()
		self.wndGuild.DeleteGuild()

	def OnBlockMode(self, mode):
		self.dlgSystem.OnBlockMode(mode)

	## Calling Functions
	# PointReset
	def OpenPointResetDialog(self):
		self.dlgPointReset.Show()
		self.dlgPointReset.SetTop()

	def ClosePointResetDialog(self):
		self.dlgPointReset.Close()

	# Shop
	def OpenShopDialog(self, vid):
		self.wndInventory.Show()
		self.wndExpandedMoney.Show()
		self.wndInventory.SetTop()
		self.dlgShop.Open(vid)
		self.dlgShop.SetTop()

	def CloseShopDialog(self):
		self.dlgShop.Close()

	def RefreshShopDialog(self):
		self.dlgShop.Refresh()

	if app.ENABLE_VIEW_CHEST_DROP:
		def AddChestDropInfo(self, chestVnum, pageIndex, slotIndex, itemVnum, itemCount):
			self.dlgChestDrop.AddChestDropItem(int(chestVnum), int(pageIndex), int(slotIndex), int(itemVnum), int(itemCount))

		def RefreshChestDropInfo(self, chestVnum):
			self.dlgChestDrop.RefreshItems(chestVnum)

	## Quest
	def OpenCharacterWindowQuestPage(self):
		self.wndCharacter.Show()
		self.wndCharacter.SetState("QUEST")

	def OpenQuestWindow(self, skin, idx):

		wnds = ()

		q = uiQuest.QuestDialog(skin, idx)
		q.SetWindowName("QuestWindow" + str(idx))
		q.Show()
		if skin:
			q.Lock()
			wnds = self.__HideWindows()

			# UNKNOWN_UPDATE
			q.AddOnDoneEvent(lambda tmp_self, args=wnds: self.__ShowWindows(args))
			# END_OF_UNKNOWN_UPDATE

		if skin:
			q.AddOnCloseEvent(q.Unlock)
		q.AddOnCloseEvent(lambda key = self.wndQuestWindowNewKey:ui.__mem_func__(self.RemoveQuestDialog)(key))
		self.wndQuestWindow[self.wndQuestWindowNewKey] = q

		self.wndQuestWindowNewKey = self.wndQuestWindowNewKey + 1

		# END_OF_UNKNOWN_UPDATE
		
	def RemoveQuestDialog(self, key):
		del self.wndQuestWindow[key]

	## Exchange
	def StartExchange(self):
		self.dlgExchange.OpenDialog()
		self.dlgExchange.Refresh()

	def EndExchange(self):
		self.dlgExchange.CloseDialog()

	def RefreshExchange(self):
		self.dlgExchange.Refresh()

	if app.ENABLE_SLOT_MARKING_SYSTEM:
		def AddExchangeItemSlotIndex(self, idx):
			self.dlgExchange.AddExchangeItemSlotIndex(idx)

	## Party
	def AddPartyMember(self, pid, name):
		self.wndParty.AddPartyMember(pid, name)

		self.__ArrangeQuestButton()

	def UpdatePartyMemberInfo(self, pid):
		self.wndParty.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.wndParty.RemovePartyMember(pid)
		self.__ArrangeQuestButton()

	def LinkPartyMember(self, pid, vid):
		self.wndParty.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.wndParty.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.wndParty.UnlinkAllPartyMember()

	def ExitParty(self):
		self.wndParty.ExitParty()
		self.__ArrangeQuestButton()

	def PartyHealReady(self):
		self.wndParty.PartyHealReady()

	def ChangePartyParameter(self, distributionMode):
		self.wndParty.ChangePartyParameter(distributionMode)

	## Safebox
	def AskSafeboxPassword(self):
		if self.wndSafebox.IsShow():
			return

		# SAFEBOX_PASSWORD
		self.dlgPassword.SetTitle(localeInfo.PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/safebox_password ")
		# END_OF_SAFEBOX_PASSWORD

		self.dlgPassword.ShowDialog()

	def OpenSafeboxWindow(self, size):
		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory.ShowSafeboxWindow(size)

		self.dlgPassword.CloseDialog()
		self.wndSafebox.ShowWindow(size)

	def RefreshSafeboxMoney(self):
		self.wndSafebox.RefreshSafeboxMoney()


	def CommandCloseSafebox(self):
		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory.CommandCloseSafebox()

		self.wndSafebox.CommandCloseSafebox()

	# ITEM_MALL
	def AskMallPassword(self):
		if self.wndMall.IsShow():
			return
		self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/mall_password ")
		self.dlgPassword.ShowDialog()

	def OpenMallWindow(self, size):
		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory.ShowMallWindow(size)

		self.dlgPassword.CloseDialog()
		self.wndMall.ShowWindow(size)

	def CommandCloseMall(self):
		if app.ENABLE_SPECIAL_INVENTORY:
			self.wndSpecialInventory.CommandCloseMall()

		self.wndMall.CommandCloseMall()
	# END_OF_ITEM_MALL

	if app.ENABLE_UN_SEAL_SCROLL_PLUS:
		def OpenUnSealScrollPlusPasswordCheckWindow(self, type):
			if not self.dlgPassword:
				return
			self.dlgPassword.SetSendType(type)
			self.dlgPassword.BindInterfaceClass(self)
			self.dlgPassword.ShowDialog()

		def CheckOpenShopWhenUseUnSealScroll(self):
			if self.privateShopBuilder and self.privateShopBuilder.IsShow():
				return False
			if self.wndShop and self.wndShop.IsShow():
				return False
			return True

		def UnSealScrollPlusPasswordSuccess(self, type):
			if net.UN_SEAL_SCROLL_PLUS_PASSWORD_SUCCESS_INVENTORY == type:
				if self.wndInventory:
					self.wndInventory.UnSealScrollPlusPasswordSuccess()
			elif net.UN_SEAL_SCROLL_PLUS_PASSWORD_SUCCESS_DS_INVENTORY == type:
				if self.wndDragonSoul and self.wndDragonSoul:
					self.wndDragonSoul.UnSealScrollPlusPasswordSuccess()

	## Guild
	def OnStartGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnStartGuildWar(guildSelf, guildOpp)

		guildWarScoreBoard = uiGuild.GuildWarScoreBoard()
		guildWarScoreBoard.Open(guildSelf, guildOpp)
		guildWarScoreBoard.Show()
		self.guildScoreBoardDict[uiGuild.GetGVGKey(guildSelf, guildOpp)] = guildWarScoreBoard

	def OnEndGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnEndGuildWar(guildSelf, guildOpp)

		key = uiGuild.GetGVGKey(guildSelf, guildOpp)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].Destroy()
		del self.guildScoreBoardDict[key]

	# GUILDWAR_MEMBER_COUNT
	def UpdateMemberCount(self, gulidID1, memberCount1, guildID2, memberCount2):
		key = uiGuild.GetGVGKey(gulidID1, guildID2)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].UpdateMemberCount(gulidID1, memberCount1, guildID2, memberCount2)
	# END_OF_GUILDWAR_MEMBER_COUNT

	def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point):
		key = uiGuild.GetGVGKey(gainGuildID, opponentGuildID)
		if not self.guildScoreBoardDict.has_key(key):
			return

		guildBoard = self.guildScoreBoardDict[key]
		guildBoard.SetScore(gainGuildID, opponentGuildID, point)

	## PK Mode
	def OnChangePKMode(self):
		self.wndCharacter.RefreshAlignment()
		self.dlgSystem.OnChangePKMode()

	## Refine
	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type):
		self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.dlgRefineNew.AppendMaterial(vnum, count)

	def ToggleEnergyCrystalWindow(self):
		if self.wndEnergyCrystal:
			self.wndEnergyCrystal.Toggle()

	def OpenEnergyCrystalWindow(self):
		if self.wndEnergyCrystal:
			self.wndEnergyCrystal.Open()

	## Show & Hide
	def ShowDefaultWindows(self):
		self.wndTaskBar.Show()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		self.wndMiniMap.Show()
		self.wndMiniMap.ShowMiniMap()

	def ShowAllWindows(self):
		self.wndTaskBar.Show()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		self.wndCharacter.Show()
		self.wndInventory.Show()
		self.wndExpandedMoney.Show()
		self.wndChat.Show()

		self.wndMiniMap.Show()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Show()
			self.wndExpandedTaskBar.SetTop()

		if app.ENABLE_ZODIAC_MISSION:
			if self.wnd12ziTimer:
				self.wnd12ziTimer.Show()
			if self.wnd12ziReward:
				self.wnd12ziReward.Show()

		if app.ENABLE_RANKING and not app.ENABLE_GLOBAL_RANKING:
			if self.wndRanking:
				self.wndRanking.Open()

	def HideAllWindows(self):
		if self.wndTaskBar:
			self.wndTaskBar.Hide()
		if self.wndDragonSoul:
			self.wndDragonSoul.Hide()
		if self.wndDragonSoulRefine:
			self.wndDragonSoulRefine.Hide()
		if self.wndEnergyBar:
			self.wndEnergyBar.Hide()


		if app.ENABLE_DETAILS_UI:
			if self.wndCharacter:
				self.wndCharacter.Close()
		else:
			if self.wndCharacter:
				self.wndCharacter.Hide()

		if self.wndInventory:
			self.wndInventory.Hide()

		if self.wndChat:
			self.wndChat.Hide()

		if app.ENABLE_GAYA_TICKET_SYSTEM:
			if (self.wndImproveGemTicket):
				self.wndImproveGemTicket.Hide()

		if self.wndExpandedMoney:
			self.wndExpandedMoney.Hide()

		if app.ENABLE_ZODIAC_MISSION:
			if self.wnd12ziTimer:
				self.wnd12ziTimer.Hide()
			if self.wnd12ziReward:
				self.wnd12ziReward.Hide()

		if self.wndMiniMap:
			self.wndMiniMap.Hide()

		if self.wndMessenger:
			self.wndMessenger.Hide()

		if self.wndGuild:
			self.wndGuild.Hide()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Hide()

		if app.ENABLE_BIOLOG_RENEWAL:
			if self.wndBiologist:
				self.wndBiologist.Hide()

		if app.ENABLE_BATTLEPASS_RENEWAL:
			if self.wndBattlePass:
				self.wndBattlePass.Hide()

		if self.wndExpandedMoneyTaskBar:
			self.wndExpandedMoneyTaskBar.Hide()

		if app.ENABLE_SUNG_MAHI_TOWER:
			if self.wndSungMahiWindow:
				self.wndSungMahiWindow.Hide()


		if app.ENABLE_RENEWAL_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Hide()

		if app.ENABLE_SPECIAL_INVENTORY:
			if self.wndSpecialInventory:
				self.wndSpecialInventory.Hide()

		if app.ENABLE_AURA_COSTUME_SYSTEM:
			if self.wndAura:
				self.wndAura.Hide()

		if app.ENABLE_YIN_AND_YANG_ATTR:
			if self.wndYinAndYangInventory and self.wndYinAndYangInventory.IsShow():
				self.wndYinAndYangInventory.Close()

			if self.wndYinAndYangHarmony and self.wndYinAndYangHarmony.IsShow():
				self.wndYinAndYangHarmony.Close()

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.Hide()
				if self.wndPetInfoWindow.wndPetMiniInfo:
					self.wndPetInfoWindow.wndPetMiniInfo.Hide()

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			if self.wndWarpWindow:
				self.wndWarpWindow.Hide()

		if app.ENABLE_RENEWAL_SPECIAL_CHAT:
			if self.wndSpecialChat:
				self.wndSpecialChat.Hide()

		if app.ENABLE_HUNTING_SYSTEM:
			if self.wndHunting:
				self.wndHunting.Hide()

			if self.wndHuntingSelect:
				self.wndHuntingSelect.Hide()

			if self.wndHuntingReward:
				self.wndHuntingReward.Hide()


		if app.ENABLE_RANKING:
			if self.wndRanking:
				self.wndRanking.Close()

	def ShowMouseImage(self):
		self.wndTaskBar.ShowMouseImage()

	def HideMouseImage(self):
		self.wndTaskBar.HideMouseImage()
		
	def ToggleExpandedMoneyButton(self):
		if self.wndExpandedMoney.IsShow():
			self.wndExpandedMoney.Close()
		else:
			self.wndExpandedMoney.Open()

	def ToggleChat(self):
		if TRUE == self.wndChat.IsEditMode():
			self.wndChat.CloseChat()
		else:
			if self.wndWeb and self.wndWeb.IsShow():
				pass
			else:
				self.wndChat.OpenChat()

	def IsOpenChat(self):
		return self.wndChat.IsEditMode()

	def SetChatFocus(self):
		self.wndChat.SetChatFocus()

	if app.ENABLE_RENEWAL_DEAD_PACKET:
		def OpenRestartDialog(self, d_time):
			self.dlgRestart.OpenDialog(d_time)
			self.dlgRestart.SetTop()
	else:
		def OpenRestartDialog(self):
			self.dlgRestart.OpenDialog()
			self.dlgRestart.SetTop()

	def CloseRestartDialog(self):
		self.dlgRestart.Close()

	if app.ENABLE_SUNG_MAHI_TOWER:
		def SetSungMahiRestartDialog(self):
			self.dlgRestart.SetSungMahiRestartDialog()

	if app.ENABLE_GAYA_SYSTEM:
		def BINARY_OpenSelectItemWindowEx(self):
			self.wndItemSelectEx.Open()

		def BINARY_RefreshSelectItemWindowEx(self):
			self.wndItemSelectEx.RefreshSlot()

		def OpenGuiGem(self):
			self.wndGemG.Open()

		def GemCheck(self):
			self.wndGemG.SucceedGem()

		def OpenGuiGemMarket(self):
			self.wndGemM.Open()

		def GemMarketItems(self, vnums, gem, count):
			self.wndGemM.Information(vnums, gem, count)
			self.wndGemM.LoadInformation()

		def GemMarketSlotsDesblock(self, slot0, slot1, slot2, slot3, slot4, slot5):
			self.wndGemM.SlotsDesblock(slot0, slot1, slot2, slot3, slot4, slot5)

		def GemMarketClear(self):
			self.wndGemM.Clear()

		def GemTime(self,time):
			self.wndGemM.Time(time)

	def ToggleSystemDialog(self):
		if FALSE == self.dlgSystem.IsShow():
			self.dlgSystem.OpenDialog()
			self.dlgSystem.SetTop()
		else:
			self.dlgSystem.Close()

	def OpenSystemDialog(self):
		self.dlgSystem.OpenDialog()
		self.dlgSystem.SetTop()

	def ToggleMessenger(self):
		if self.wndMessenger.IsShow():
			self.wndMessenger.Hide()
		else:
			self.wndMessenger.SetTop()
			self.wndMessenger.Show()

	def ToggleMiniMap(self):
		if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
			if FALSE == self.wndMiniMap.isShowMiniMap():
				self.wndMiniMap.ShowMiniMap()
				self.wndMiniMap.SetTop()
			else:
				self.wndMiniMap.HideMiniMap()

		else:
			self.wndMiniMap.ToggleAtlasWindow()

	def PressMKey(self):
		if app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
			self.ToggleMessenger()

		else:
			self.ToggleMiniMap()

	def SetMapName(self, mapName):
		self.wndMiniMap.SetMapName(mapName)

	def MiniMapScaleUp(self):
		self.wndMiniMap.ScaleUp()

	def MiniMapScaleDown(self):
		self.wndMiniMap.ScaleDown()

	def ToggleCharacterWindow(self, state):
		if FALSE == player.IsObserverMode():
			if FALSE == self.wndCharacter.IsShow():
				self.OpenCharacterWindowWithState(state)
			else:
				if state == self.wndCharacter.GetState():
					self.wndCharacter.OverOutItem()
					if app.ENABLE_DETAILS_UI:
						self.wndCharacter.Close()
					else:
						self.wndCharacter.Hide()
				else:
					self.wndCharacter.SetState(state)

	def OpenCharacterWindowWithState(self, state):
		if FALSE == player.IsObserverMode():
			self.wndCharacter.SetState(state)
			self.wndCharacter.Show()
			self.wndCharacter.SetTop()

	if app.ENABLE_TITLE_SYSTEM:
		def TitleSystemSyncReset(self):
			if not self.wndCharacter:
				return
			try:
				self.wndCharacter.titleSystemUnlockedIDs = set()
			except:
				pass
			if self.wndCharacter.wndTitleSystem:
				self.wndCharacter.wndTitleSystem.SetUnlockedTitleIDs(set())
	
		def TitleSystemSyncAdd(self, titleID):
			if not self.wndCharacter:
				return
			try:
				titleID = int(titleID)
			except:
				return
			try:
				self.wndCharacter.titleSystemUnlockedIDs.add(titleID)
			except:
				return
			if self.wndCharacter.wndTitleSystem:
				self.wndCharacter.wndTitleSystem.SetUnlockedTitleIDs(self.wndCharacter.titleSystemUnlockedIDs)
	
		def TitleSystemSyncActive(self, titleID):
			if not self.wndCharacter:
				return
			try:
				titleID = int(titleID)
			except:
				titleID = 0
			try:
				self.wndCharacter.titleSystemActiveID = titleID
			except:
				pass
			if self.wndCharacter.wndTitleSystem:
				self.wndCharacter.wndTitleSystem.SetActiveTitleID(titleID)

	def ToggleCharacterWindowStatusPage(self):
		self.ToggleCharacterWindow("STATUS")

	def SetUseItemMode(self, bUse):
		self.wndInventory.SetUseItemMode(bUse)
		if self.wndDragonSoul:
			self.wndDragonSoul.SetUseItemMode(bUse)

	def DragonSoulActivate(self, deck):
		if self.wndDragonSoul:
			self.wndDragonSoul.ActivateDragonSoulByExtern(deck)

	def DragonSoulKeySelect(self, deck):
		if self.wndDragonSoul:
			self.wndDragonSoul.DragonSoulKeySelect(deck)

	def DragonSoulDeactivate(self):
		if self.wndDragonSoul:
			self.wndDragonSoul.DeactivateDragonSoul()

	def DragonSoulGiveQuilification(self):
		self.DRAGON_SOUL_IS_QUALIFIED = TRUE

	def ToggleDragonSoulWindow(self):
		if FALSE == player.IsObserverMode() and self.wndDragonSoul:
			if FALSE == self.wndDragonSoul.IsShow():
				if self.DRAGON_SOUL_IS_QUALIFIED:
					self.wndDragonSoul.Show()
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DRAGON_SOUL_UNQUALIFIED)
			else:
				self.wndDragonSoul.Close()

	def ToggleDragonSoulWindowWithNoInfo(self):
		if FALSE == player.IsObserverMode() and self.wndDragonSoul:
			if FALSE == self.wndDragonSoul.IsShow():
				if self.DRAGON_SOUL_IS_QUALIFIED:
					self.wndDragonSoul.Show()
			else:
				self.wndDragonSoul.Close()

	def FailDragonSoulRefine(self, reason, inven_type, inven_pos):
		if FALSE == player.IsObserverMode() and self.wndDragonSoulRefine and self.wndDragonSoulRefine.IsShow():
			self.wndDragonSoulRefine.RefineFail(reason, inven_type, inven_pos)

	def SucceedDragonSoulRefine(self, inven_type, inven_pos):
		if FALSE == player.IsObserverMode() and self.wndDragonSoulRefine and self.wndDragonSoulRefine.IsShow():
			self.wndDragonSoulRefine.RefineSucceed(inven_type, inven_pos)

	def OpenDragonSoulRefineWindow(self):
		if FALSE == player.IsObserverMode() and self.wndDragonSoulRefine:
			if FALSE == self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.Show()
				if self.wndDragonSoul and FALSE == self.wndDragonSoul.IsShow():
					self.wndDragonSoul.Show()

	def CloseDragonSoulRefineWindow(self):
		if FALSE == player.IsObserverMode() and self.wndDragonSoulRefine and self.wndDragonSoulRefine.IsShow():
			self.wndDragonSoulRefine.Close()

	def ToggleInventoryWindow(self):
		if FALSE == player.IsObserverMode():
			if FALSE == self.wndInventory.IsShow():
				self.wndInventory.Show()
				self.wndInventory.SetTop()
				self.wndExpandedMoney.Show()
			else:
				self.wndInventory.OverOutItem()
				self.wndInventory.Close()
				self.wndExpandedMoney.Hide()

	if app.ENABLE_AUTO_CHAT:
		def ToggleAutoChatWindow(self):
			if self.wndAutoChat:
				self.wndAutoChat.Toggle()

	def ToggleExpandedButton(self):
		if False == player.IsObserverMode():
			if False == self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Show()
				self.wndExpandedTaskBar.SetTop()
			else:
				self.wndExpandedTaskBar.Close()

	def ToggleExpandedMoneyButton(self):
		if not self.wndExpandedMoneyTaskBar:
			return
		if not self.wndExpandedMoneyTaskBar.IsShow():
			self.wndExpandedMoneyTaskBar.Show()
			self.wndExpandedMoneyTaskBar.SetTop()
		else:
			self.wndExpandedMoneyTaskBar.Close()

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetInformationActivate(self):
			if uiTaskBar.TaskBar.IS_EXPANDED:
				self.wndExpandedTaskBar.SetToolTipText(uiTaskBar.ExpandedTaskBar.BUTTON_PET_INFO, uiScriptLocale.TASKBAR_PET_INFO)

		def TogglePetInformationWindow(self):
			if app.ENABLE_GROWTH_PET_RENEWAL and self.wndCompanion:
				if False == player.IsObserverMode():
					if self.wndCompanion.IsShow() and self.wndCompanion.tab == uiCompanion.TAB_PET:
						self.wndCompanion.Close()
					else:
						self.wndCompanion.Open(uiCompanion.TAB_PET)
				return
			if False == player.IsObserverMode():
				if not self.wndPetInfoWindow.IsShow():
					self.wndPetInfoWindow.Show()
				else:
					self.wndPetInfoWindow.Close()

	def OpenSkillUpgrade(self, upgradeType = None, skillIndex = 0):
		if self.wndSkillUpgrade and False == player.IsObserverMode():
			self.wndSkillUpgrade.Open(upgradeType, skillIndex)

	def ToggleSkillUpgrade(self):
		if self.wndSkillUpgrade and False == player.IsObserverMode():
			self.wndSkillUpgrade.Toggle()

	def GetSkillUpgradeWnd(self):
		return self.wndSkillUpgrade

	def ToggleBraveCapeWindow(self):
		if self.wndBraveCape and False == player.IsObserverMode():
			self.wndBraveCape.Toggle()

	def SetBraveCapeStatus(self, status):
		if self.wndBraveCape:
			self.wndBraveCape.SetStatus(status)

	def OnBraveCapeMapLoaded(self):
		if self.wndBraveCape:
			self.wndBraveCape.OnMapLoaded()

	def SetSkillUpgradeInfo(self, *args):
		if self.wndSkillUpgrade:
			self.wndSkillUpgrade.SetUpgradeInfo(*args)

	def SendSkillUpgradeResult(self, result):
		if self.wndSkillUpgrade:
			self.wndSkillUpgrade.ShowResult(result)

	def SkillUpgradeNegativeGradeConfirm(self):
		if self.wndSkillUpgrade:
			self.wndSkillUpgrade.ShowNegativeGradeConfirmDialog()

	def SkillUpgradeRefresh(self):
		if self.wndSkillUpgrade:
			self.wndSkillUpgrade.Refresh()

	def ToggleCompanionBuffiWnd(self):
		if self.wndCompanion and False == player.IsObserverMode():
			if self.wndCompanion.IsShow() and self.wndCompanion.tab == uiCompanion.TAB_BUFFI:
				self.wndCompanion.Close()
			else:
				self.wndCompanion.Open(uiCompanion.TAB_BUFFI)

	def SetBuffiInformation(self, *args):
		if self.wndCompanion:
			self.wndCompanion.SetBuffiInformation(*args)

	def SetBuffiSkills(self, *args):
		if self.wndCompanion:
			self.wndCompanion.SetBuffiSkills(*args)

	def SetBuffiSkillsBook(self, *args):
		if self.wndCompanion:
			self.wndCompanion.SetBuffiSkillsBook(*args)

	def SetBuffiSkillsCooldown(self, *args):
		if self.wndCompanion:
			self.wndCompanion.SetBuffiSkillsCooldown(*args)

	def SetBuffiName(self, name):
		if self.wndCompanion:
			self.wndCompanion.SetBuffiName(name)

	def Buffi_SetUnsummon(self):
		if self.wndCompanion:
			self.wndCompanion.UnsummonBuffi()

	def GetBuffiSkillPts(self):
		return self.wndCompanion.GetBuffiSkillPts() if self.wndCompanion else 0

	def GetBuffiSkillsPower(self):
		return self.wndCompanion.GetBuffiSkillsPower() if self.wndCompanion else []

	def GetBuffiSkillsBook(self):
		return self.wndCompanion.GetBuffiSkillsBook() if self.wndCompanion else []

	def GetBuffiSkillsCooldown(self):
		return self.wndCompanion.GetBuffiSkillsCooldown() if self.wndCompanion else []

	def ToggleGuildWindow(self):

		if not self.wndGuild.IsShow():
			if self.wndGuild.CanOpen():
				self.wndGuild.Open()
			elif app.ENABLE_GUILD_APPLICATION and self.wndGuildApplication:
				self.ToggleGuildApplication()
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GUILD_YOU_DO_NOT_JOIN)
		else:
			self.wndGuild.OverOutItem()
			self.wndGuild.Hide()

	if app.ENABLE_GUILD_APPLICATION:
		def GetGuildApplicationWnd(self):
			return self.wndGuildApplication

		def GetGuildJoinNotificationWnd(self):
			return self.wndGuildJoinNotification

		def ToggleGuildApplication(self, mode = 0):
			wnd = self.GetGuildApplicationWnd()
			if not wnd:
				return
			if wnd.IsShow():
				wnd.Close()
			else:
				wnd.Open(mode)

		def OpenGuildJoinNotification(self, guildID, guildName, description):
			import advanced_options_runtime
			wnd = self.GetGuildJoinNotificationWnd()
			if not wnd or guild.IsGuildEnable():
				return
			if not advanced_options_runtime.Get("show_guild_join_notification", True):
				return
			wnd.Open(guildID, guildName, description)

	def ToggleChatLogWindow(self):
		if self.wndChatLog.IsShow():
			self.wndChatLog.Hide()
		else:
			self.wndChatLog.Show()


	if app.ENABLE_RENEWAL_SWITCHBOT:
		def ToggleSwitchbotWindow(self):
			if self.wndSwitchbot.IsShow():
				self.wndSwitchbot.Close()
			else:
				self.wndSwitchbot.Open()

		def RefreshSwitchbotWindow(self):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotWindow()

		def RefreshSwitchbotItem(self, slot):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotItem(slot)

	if app.ENABLE_SPECIAL_INVENTORY:
		def ToggleSpecialInventoryWindow(self):
			if FALSE == player.IsObserverMode():
				if FALSE == self.wndSpecialInventory.IsShow():
					self.wndSpecialInventory.Show()
					self.wndSpecialInventory.SetTop()
				else:
					self.wndSpecialInventory.OverOutItem()
					self.wndSpecialInventory.Close()

		def OpenSpecialInventoryWindow(self, category = 0):
			if FALSE == player.IsObserverMode():
				if FALSE == self.wndSpecialInventory.IsShow():
					self.wndSpecialInventory.Show()
					self.wndSpecialInventory.SetTop()
					self.wndSpecialInventory.SetInventoryType(category)

	if app.ENABLE_RENEWAL_SPECIAL_CHAT:
		def OnPickItem(self, item, socket0 = 0):
			item_vnum = int(item)
			self.SpecialChatOnPick(0, item_vnum, int(socket0))

		def SpecialChatOnPick(self, money = 0, item_vnum = 0, socket0 = 0):
			if self.dlgDropInfo:
				if money > 0:
					self.dlgDropInfo.AppendYang(money)
				if item_vnum > 0:
					self.dlgDropInfo.AppendDropInfo(item_vnum, 1, socket0)
				return
			if money > 0:
				money_str = localeInfo.NumberToMoneyString(money)
				self.wndSpecialChat.AddSpecialChatLine(localeInfo.SPECIAL_CHAT_PICK % (money_str))

			if item_vnum > 0:
				import item
				item.SelectItem(item_vnum)
				self.wndSpecialChat.AddSpecialChatLine(localeInfo.SPECIAL_CHAT_PICK % (item.GetItemName()))

	def Highligt_Item(self, inven_type, inven_pos):
		if player.DRAGON_SOUL_INVENTORY == inven_type:
			if self.wndDragonSoul:
				self.wndDragonSoul.HighlightSlot(inven_pos)
			return
		if app.ENABLE_PICKUP_ITEM_EFFECT and player.INVENTORY == inven_type:
			self.wndInventory.HighlightSlot(inven_pos)
			if app.ENABLE_SPECIAL_INVENTORY:
				self.wndSpecialInventory.HighlightSlot(inven_pos)

	def CheckGameButton(self):
		if self.wndGameButton:
			self.wndGameButton.CheckGameButton()

	if app.ENABLE_SUNG_MAHI_TOWER:
		def ToggleSungMahiWindow(self):
			if self.wndSungMahiWindow.IsShow():
				self.wndSungMahiWindow.Close()
			else:
				self.wndSungMahiWindow.Open()
				
		def UpdateSungMahiNotice(self, noticeType, noticeText):
			if self.wndMiniMap.sungMahiCover.IsShow():
				if noticeType == 1:
					self.wndMiniMap.sungMahiCover.SetLevelDescriptionText(noticeText)
				else:
					self.wndMiniMap.sungMahiCover.SetLevelCurseText(noticeText, noticeType)
			
		def SungMahiClearNotice(self, noticeType):
			if self.wndMiniMap.sungMahiCover.IsShow():
				self.wndMiniMap.sungMahiCover.SungMahiClearNotice(noticeType)
			
		def UpdateRoomLevel(self, roomLevel):
			if self.wndMiniMap.sungMahiCover.IsShow():
				self.wndMiniMap.sungMahiCover.SetRoomLevel(roomLevel)
			
		def UpdateTowerLevel(self, towerLevel):
			if self.wndMiniMap.sungMahiCover.IsShow():
				self.wndMiniMap.sungMahiCover.SetLevelInfo(towerLevel)
			
		def UpdateRoomTime(self, roomTime):
			if self.wndMiniMap.sungMahiCover.IsShow():
				self.wndMiniMap.sungMahiCover.UpdateRoomTime(roomTime)

	def __OnClickStatusPlusButton(self):
		self.ToggleCharacterWindow("STATUS")

	def __OnClickSkillPlusButton(self):
		self.ToggleCharacterWindow("SKILL")

	def __OnClickQuestButton(self):
		self.ToggleCharacterWindow("QUEST")

	def __OnClickBuildButton(self):
		self.BUILD_OpenWindow()

	def OpenWebWindow(self, url):
		pass
		#self.wndWeb.Open(url)

	if app.ENABLE_DUNGEON_INFO:
		def DUNGEON_INFO_CHECK_SHOW(self):
			if self.wndTableDungeonInfo:
				if self.wndTableDungeonInfo.IsShow():
					self.wndTableDungeonInfo.Close()
				else:
					import dungeon_info
					dungeon_info.Open()
		def BINARY_TABLE_DUNGEON_INFO_OPEN(self):
			if self.wndTableDungeonInfo:
				self.wndTableDungeonInfo.LoadDateInfo()
				self.wndTableDungeonInfo.Show()

		def BINARY_TABLE_DUNGEON_RANKING_LOAD(self):
			if self.wndTableDungeonInfo:
				self.wndTableDungeonInfo.LoadRanking()

		def BINARY_TABLE_DUNGEON_MISION_LOAD(self):
			if self.wndTableDungeonInfo:
				self.wndTableDungeonInfo.LoadMision()

	# show GIFT
	def ShowGift(self):
		self.wndTaskBar.ShowGift()

	def CloseWbWindow(self):
		self.wndWeb.Close()


	if app.ENABLE_RENEWAL_CUBE:
		def BINARY_CUBE_RENEWAL_OPEN(self):
			self.wndCubeRenewal.Show()


	def OpenCubeWindow(self):
		self.wndCube.Open()

		if FALSE == self.wndInventory.IsShow():
			self.wndInventory.Show()
			self.wndExpandedMoney.Show()

	def ShowItemFinder(self):
		self.wndItemFinder.Show()

	def AppendInfoFinder(self, index, name_monster, prob, activi, vnum, count, name_item):
		self.wndItemFinder.AppendInfo(index, name_monster, prob, activi, vnum, count, name_item)


	def UpdateCubeInfo(self, gold, itemVnum, count):
		self.wndCube.UpdateInfo(gold, itemVnum, count)

	def CloseCubeWindow(self):
		self.wndCube.Close()

	def FailedCubeWork(self):
		self.wndCube.Refresh()

	def SucceedCubeWork(self, itemVnum, count):
		self.wndCube.Clear()

		if 0:
			self.wndCubeResult.SetPosition(*self.wndCube.GetGlobalPosition())
			self.wndCubeResult.SetCubeResultItem(itemVnum, count)
			self.wndCubeResult.Open()
			self.wndCubeResult.SetTop()

	if constInfo.ENABLE_EXPANDED_TASKBAR:
		def PressExpandedTaskbar(self):
			if self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Hide()
			else:
				self.wndExpandedTaskBar.Show()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def ActAcce(self, iAct, bWindow):
			board = (self.wndAcceAbsorption,self.wndAcceCombine)[int(bWindow)]
			if iAct == 1:
				self.ActAcceOpen(board)
			elif iAct == 2:
				self.ActAcceClose(board)
			elif iAct == 3 or iAct == 4:
				self.ActAcceRefresh(board, iAct)

		def ActAcceOpen(self,board):
			if not board.IsOpened():
				board.Open()
			if not self.wndInventory.IsShow():
				self.wndInventory.Show()
			self.wndInventory.RefreshBagSlotWindow()

		def ActAcceClose(self,board):
			if board.IsOpened():
				board.Close()
			self.wndInventory.RefreshBagSlotWindow()

		def ActAcceRefresh(self,board,iAct):
			if board.IsOpened():
				board.Refresh(iAct)
			self.wndInventory.RefreshBagSlotWindow()




	def __HideWindows(self):
		hideWindows = self.wndTaskBar,\
						self.wndCharacter,\
						self.wndInventory,\
						self.wndExpandedMoney,\
						self.wndMiniMap,\
						self.wndGuild,\
						self.wndMessenger,\
						self.wndChat,\
						self.wndParty,\
						self.wndGameButton,

		if self.wndExpandedTaskBar:
			hideWindows += self.wndExpandedTaskBar,

		if self.wndEnergyBar:
			hideWindows += self.wndEnergyBar,
		if self.wndDragonSoul:
			hideWindows += self.wndDragonSoul, self.wndDragonSoulRefine,

		if app.ENABLE_GAYA_TICKET_SYSTEM:
			if (self.wndImproveGemTicket):
				hideWindows += self.wndImproveGemTicket,

		if app.ENABLE_ZODIAC_MISSION:
			if self.wnd12ziTimer:
				hideWindows += self.wnd12ziTimer,
			if self.wnd12ziReward:
				hideWindows += self.wnd12ziReward,



		if app.ENABLE_RENEWAL_SWITCHBOT:
			if self.wndSwitchbot:
				hideWindows += self.wndSwitchbot,

		if app.ENABLE_SPECIAL_INVENTORY:
			if self.wndSpecialInventory:
				hideWindows += self.wndSpecialInventory,

		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				hideWindows += self.wndPetInfoWindow,

		if self.wndCompanion:
			hideWindows += self.wndCompanion,

		if self.wndBraveCape:
			hideWindows += self.wndBraveCape,

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			if self.wndWarpWindow:
				hideWindows += self.wndWarpWindow,

		if app.ENABLE_RENEWAL_SPECIAL_CHAT:
			if self.wndSpecialChat:
				hideWindows += self.wndSpecialChat,

		if app.ENABLE_HUNTING_SYSTEM:
			if self.wndHunting:
				hideWindows += self.wndHunting,

			if self.wndHuntingSelect:
				hideWindows += self.wndHuntingSelect,

			if self.wndHuntingReward:
				hideWindows += self.wndHuntingReward,

		if app.ENABLE_BIOLOG_RENEWAL:
			if self.wndBiologist:
				hideWindows += self.wndBiologist,

		if app.ENABLE_BATTLEPASS_RENEWAL:
			if self.wndBattlePass:
				hideWindows += self.wndBattlePass,

		if app.ENABLE_RANKING:
			if self.wndRanking:
				hideWindows += self.wndRanking,

		if app.ENABLE_IKASHOP_RENEWAL:
			hideWindows += self.wndIkashopBusiness, self.wndIkashopSearchShop
			if app.EXTEND_IKASHOP_ULTIMATE:
				hideWindows += self.wndIkashopShopSkin,

		hideWindows = filter(lambda x:x.IsShow(), hideWindows)
		map(lambda x:x.Hide(), hideWindows)
		import sys

		self.HideAllQuestButton()
		self.HideAllWhisperButton()

		if self.wndChat.IsEditMode():
			self.wndChat.CloseChat()

		return hideWindows

	def __ShowWindows(self, wnds):
		import sys
		map(lambda x:x.Show(), wnds)
		global IsQBHide
		if not IsQBHide:
			self.ShowAllQuestButton()
		else:
			self.HideAllQuestButton()

		self.ShowAllWhisperButton()

	def BINARY_OpenAtlasWindow(self):
		if self.wndMiniMap:
			self.wndMiniMap.ShowAtlas()


	def BINARY_SetObserverMode(self, flag):
		self.wndGameButton.SetObserverMode(flag)

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def BINARY_OpenSelectItemWindow(self):
		self.wndItemSelect.Open()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

	def OpenPrivateShopInputNameDialog(self):
		if app.ENABLE_AURA_COSTUME_SYSTEM:
			if self.wndAura and self.wndAura.IsShow():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
				return

		if app.ENABLE_GROWTH_PET_SYSTEM:
			pet_id = player.GetActivePetItemId()
			if pet_id:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
				return

		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
		inputDialog.SetMaxLength(32)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OpenPrivateShopBuilder))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.ClosePrivateShopInputNameDialog))
		inputDialog.Open()
		self.inputDialog = inputDialog

	def ClosePrivateShopInputNameDialog(self):
		self.inputDialog = None
		return TRUE

	def OpenPrivateShopBuilder(self):
		if app.ENABLE_AURA_COSTUME_SYSTEM:
			if self.wndAura and self.wndAura.IsShow():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_OPEN_OTHER_WINDOW)
				return

		if app.ENABLE_GROWTH_PET_SYSTEM:
			pet_id = player.GetActivePetItemId()
			if pet_id:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
				return

		if not self.inputDialog:
			return TRUE

		if not len(self.inputDialog.GetText()):
			return TRUE

		self.privateShopBuilder.Open(self.inputDialog.GetText())
		self.ClosePrivateShopInputNameDialog()
		return TRUE

	def AppearPrivateShop(self, vid, text):

		board = uiPrivateShopBuilder.PrivateShopAdvertisementBoard()
		board.Open(vid, text)

		self.privateShopAdvertisementBoardDict[vid] = board

	def DisappearPrivateShop(self, vid):
		if not self.privateShopAdvertisementBoardDict.has_key(vid):
			return

		del self.privateShopAdvertisementBoardDict[vid]
		uiPrivateShopBuilder.DeleteADBoard(vid)

	### Equipment ###

	def OpenEquipmentDialog(self, vid):
		dlg = uiEquipmentDialog.EquipmentDialog()
		dlg.SetItemToolTip(self.tooltipItem)
		dlg.SetCloseEvent(ui.__mem_func__(self.CloseEquipmentDialog))
		dlg.Open(vid)

		self.equipmentDialogDict[vid] = dlg

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count, dwChangeLookVnum):
			if not vid in self.equipmentDialogDict:
				return
			self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count, dwChangeLookVnum)
	else:
		def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
			if not vid in self.equipmentDialogDict:
				return
			self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogSocket(slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogAttr(slotIndex, attrIndex, type, value)

	if app.ENABLE_SUNGMA_SCORE:
		def SetEquipmentDialogSungmaScore(self, vid, slotIndex, value):
			if not vid in self.equipmentDialogDict:
				return
			self.equipmentDialogDict[vid].SetEquipmentDialogSungmaScore(slotIndex, value)

	def CloseEquipmentDialog(self, vid):
		if not vid in self.equipmentDialogDict:
			return
		del self.equipmentDialogDict[vid]

	def BINARY_ClearQuest(self, index):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

	def RecvQuest(self, index, name):
		self.BINARY_RecvQuest(index, name, "file", localeInfo.GetLetterImageName())

	def BINARY_RecvQuest(self, index, name, iconType, iconName):

		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

		btn = uiWhisper.WhisperButton()

		import item
		if "item"==iconType:
			item.SelectItem(int(iconName))
			buttonImageFileName=item.GetIconImageFileName()
		else:
			buttonImageFileName=iconName
			btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
			btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
			btn.SetDownVisual(localeInfo.GetLetterOpenImageName())

		if not app.ENABLE_RENEWAL_QUEST:
			btn.SetToolTipText(name, -20, 35)
			btn.ToolTipText.SetHorizontalAlignLeft()

			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
			btn.Show()
		else:
			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)

		btn.index = index
		btn.name = name

		self.questButtonList.insert(0, btn)
		self.__ArrangeQuestButton()

	def __ArrangeQuestButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		if self.wndParty.IsShow():
			xPos = 100 + 30
		else:
			xPos = 20

		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for btn in self.questButtonList:
			if app.ENABLE_RENEWAL_QUEST:
				btn.SetToolTipText(str(len(self.questButtonList)))
				btn.ToolTipText.SetHorizontalAlignCenter()

			btn.SetPosition(xPos + (int(count/yCount) * 100), yPos + (count%yCount * 63))
			count += 1

			global IsQBHide
			if IsQBHide:
				btn.Hide()
			else:
				if app.ENABLE_RENEWAL_QUEST and count > 0:
					btn.Hide()
				else:
					btn.Show()

	def __StartQuest(self, btn):
		if app.ENABLE_RENEWAL_QUEST:
			self.__OnClickQuestButton()
			self.HideAllQuestButton()
		else:
			event.QuestButtonClick(btn.index)
			self.__DestroyQuestButton(btn)

	def __FindQuestButton(self, index):
		for btn in self.questButtonList:
			if btn.index == index:
				return btn

		return 0

	def __DestroyQuestButton(self, btn):
		btn.SetEvent(0)
		self.questButtonList.remove(btn)
		self.__ArrangeQuestButton()

	def HideAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Hide()

	def ShowAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Show()
			if app.ENABLE_RENEWAL_QUEST:
				break
	### Whisper ###

	def __InitWhisper(self):
		chat.InitWhisper(self)

	if app.ENABLE_WHISPER_MESSENGER:
		def __GetWhisperMessenger(self):
			return self.wndWhisperMessenger

		def PrepareGuildWhisper(self, name, line):
			if uiWhisperMessenger.GUILD_WHISPER_MARK not in line:
				return line
			messenger = self.__GetWhisperMessenger()
			if messenger:
				messenger.SetGuildSender(name)
			return line.replace(uiWhisperMessenger.GUILD_WHISPER_MARK, " : ", 1)

		def RecvWhisperMessenger(self, name, line, isSystem = FALSE):
			messenger = self.__GetWhisperMessenger()
			if not messenger:
				return
			if messenger.IsExcluded(name):
				return
			isOpen = messenger.RecvWhisperLine(name, line, isSystem)
			if self.IsGameMasterName(name):
				messenger.SetGameMaster(name)
			self.RefreshMessengerButton()
			if isOpen or isSystem or name == "[Guild]" or messenger.IsMuted(name):
				return
			self.__ReopenMessengerButton()
			if name.startswith("[") or messenger.IsGuildSender(name):
				btn = self.__FindWhisperButton(name)
				if 0 == btn:
					btn = self.__MakeSystemWhisperButton(name)
				btn.Flash()
			else:
				chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))
			if app.ENABLE_BLINK_ALERT:
				app.FlashApplication()

		def HandleWhisperNotLogon(self, name):
			messenger = self.__GetWhisperMessenger()
			return messenger and messenger.OnWhisperNotLogon(name)

		def RecvOfflineWhisper(self, sender, sentAt, text):
			messenger = self.__GetWhisperMessenger()
			if not messenger:
				return
			isOpen = messenger.RecvOfflineMessage(sender, sentAt, text)
			self.RefreshMessengerButton()
			if not isOpen:
				self.__ReopenMessengerButton()
				chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (sender))

		def RecvOfflineWhisperResult(self, result, name):
			messenger = self.__GetWhisperMessenger()
			if messenger:
				messenger.OnOfflineMessageResult(result, name)

		def RefreshMessengerButton(self):
			button = self.wndMessengerButton
			messenger = self.__GetWhisperMessenger()
			if button and messenger:
				button.badge.SetUnread(messenger.GetTotalUnreadCount())

		def ShowMessengerQuickCloseTip(self):
			tip = self.messengerQuickCloseTip
			if tip:
				tip.FitIconTextLine()
				tip.ShowToolTip()
				tip.SetTop()

		def HideMessengerQuickCloseTip(self):
			tip = self.messengerQuickCloseTip
			if tip:
				tip.HideToolTip()

		def __IsCtrlPressed(self):
			return app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL)

		def __OnClickMessengerButton(self):
			self.HideMessengerQuickCloseTip()
			messenger = self.__GetWhisperMessenger()
			if messenger and self.__IsCtrlPressed():
				messenger.MarkAllRead()
				for btn in list(self.whisperButtonList):
					btn.Hide()
					self.__DestroyWhisperButton(btn)
				if messenger.IsShow():
					messenger.Close()
				self.RefreshMessengerButton()
				constInfo.MESSENGER_BUTTON_CLOSED = True
				self.wndMessengerButton.Hide()
				return
			self.ToggleWhisperMessenger()

		def __ReopenMessengerButton(self):
			button = self.wndMessengerButton
			if button and constInfo.MESSENGER_BUTTON_CLOSED:
				constInfo.MESSENGER_BUTTON_CLOSED = False
				button.Show()

		def __MakeSystemWhisperButton(self, name):
			button = uiWhisperMessenger.SystemWhisperButton(name)
			button.SetEvent(ui.__mem_func__(self.ShowWhisperDialog), button)
			button.SetHoverEvent(ui.__mem_func__(self.ShowMessengerQuickCloseTip), ui.__mem_func__(self.HideMessengerQuickCloseTip))
			button.Show()
			self.whisperButtonList.insert(0, button)
			self.__ArrangeWhisperButton()
			return button

		def RecvGlobalChat(self, payload):
			messenger = self.__GetWhisperMessenger()
			if messenger:
				messenger.RecvGlobalChat(payload)

		def RecvWhisperPlayerInfo(self, name, found, empire, race, online, guildName):
			messenger = self.__GetWhisperMessenger()
			if messenger:
				messenger.SetConversationInfo(name, found, empire, race, online, guildName)

		def RecvGlobalChatCooldown(self, seconds):
			messenger = self.__GetWhisperMessenger()
			if messenger:
				messenger.RecvGlobalCooldown(seconds)

		def OnWhisperConversationRead(self, name):
			btn = self.__FindWhisperButton(name)
			if 0 != btn:
				btn.Hide()
				self.__DestroyWhisperButton(btn)
				self.HideMessengerQuickCloseTip()
			self.RefreshMessengerButton()

		def ToggleWhisperMessenger(self):
			messenger = self.__GetWhisperMessenger()
			if messenger:
				messenger.Toggle()

	def OpenWhisperDialogWithoutTarget(self):
		if app.ENABLE_WHISPER_MESSENGER and self.__GetWhisperMessenger():
			self.wndWhisperMessenger.Open()
			self.wndWhisperMessenger.OpenNewConversation()
			return

		if not self.dlgWhisperWithoutTarget:
			dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
			dlgWhisper.BindInterface(self)
			dlgWhisper.LoadDialog()
			dlgWhisper.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)
			dlgWhisper.SetPosition(self.windowOpenPosition * 30,self.windowOpenPosition * 30)
			dlgWhisper.Show()
			self.dlgWhisperWithoutTarget = dlgWhisper

			self.windowOpenPosition = (self.windowOpenPosition + 1) % 5

		else:
			self.dlgWhisperWithoutTarget.SetTop()
			self.dlgWhisperWithoutTarget.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)

	def RegisterTemporaryWhisperDialog(self, name):
		if not self.dlgWhisperWithoutTarget:
			return

		btn = self.__FindWhisperButton(name)
		if 0 != btn:
			self.__DestroyWhisperButton(btn)

		elif self.whisperDialogDict.has_key(name):
			oldDialog = self.whisperDialogDict[name]
			oldDialog.Destroy()
			del self.whisperDialogDict[name]

		self.whisperDialogDict[name] = self.dlgWhisperWithoutTarget
		self.dlgWhisperWithoutTarget.OpenWithTarget(name)
		self.dlgWhisperWithoutTarget = None
		self.__CheckGameMaster(name)

	if app.ENABLE_EXTENDED_WHISPER_DETAILS and app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def RecieveWhisperDetails(self, name, country, countryFlag = ""):
			if app.ENABLE_COUNTRY_FLAG and self.wndWhisperMessenger:
				self.wndWhisperMessenger.SetCountryFlag(name, countryFlag)

			if self.whisperDialogDict.has_key(name):
				self.whisperDialogDict[name].SetCountryFlag(country)
			else:
				btn = self.__FindWhisperButton(name)
				if btn != 0:
					btn.countryID = country

	def OpenWhisperWithText(self, name, text):
		self.OpenWhisperDialog(name)
		line = None
		if app.ENABLE_WHISPER_MESSENGER and self.wndWhisperMessenger:
			line = self.wndWhisperMessenger.chatLine
		elif self.whisperDialogDict.has_key(name):
			line = self.whisperDialogDict[name].chatLine
		if line:
			line.SetText("")
			line.SetFocus()
			ime.PasteString(text)

	def OpenWhisperDialog(self, name):
		if app.ENABLE_WHISPER_MESSENGER and self.__GetWhisperMessenger():
			self.wndWhisperMessenger.Open(name)
			return

		if not self.whisperDialogDict.has_key(name):
			dlg = self.__MakeWhisperDialog(name)
			dlg.OpenWithTarget(name)
			dlg.chatLine.SetFocus()
			dlg.Show()

			self.__CheckGameMaster(name)
			btn = self.__FindWhisperButton(name)
			if 0 != btn:
				self.__DestroyWhisperButton(btn)

	def RecvWhisper(self, name):
		if not self.whisperDialogDict.has_key(name):
			btn = self.__FindWhisperButton(name)
			if 0 == btn:
				btn = self.__MakeWhisperButton(name)
				btn.Flash()

				if app.ENABLE_BLINK_ALERT:
					app.FlashApplication()

				chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))

			else:
				btn.Flash()

				if app.ENABLE_BLINK_ALERT:
					app.FlashApplication()

		elif self.IsGameMasterName(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def MakeWhisperButton(self, name):
		self.__MakeWhisperButton(name)

	def ShowWhisperDialog(self, btn):
		if app.ENABLE_WIKI_SYSTEM and btn.name == "[W?K?]":
			self.__DestroyWhisperButton(btn)
			self.OpenWikiWindow()
			return

		if app.ENABLE_WHISPER_MESSENGER and self.__GetWhisperMessenger():
			name = btn.name
			btn.Hide()
			self.__DestroyWhisperButton(btn)
			self.HideMessengerQuickCloseTip()
			if self.__IsCtrlPressed():
				self.wndWhisperMessenger.MarkRead(name)
				return
			self.wndWhisperMessenger.Open(name)
			return

		try:
			self.__MakeWhisperDialog(btn.name)
			dlgWhisper = self.whisperDialogDict[btn.name]
			dlgWhisper.OpenWithTarget(btn.name)
			dlgWhisper.Show()
			self.__CheckGameMaster(btn.name)
		except:
			import dbg
			dbg.TraceError("interface.ShowWhisperDialog - Failed to find key")

		self.__DestroyWhisperButton(btn)

	def MinimizeWhisperDialog(self, name):

		if 0 != name:
			self.__MakeWhisperButton(name)

		self.CloseWhisperDialog(name)

	def CloseWhisperDialog(self, name):

		if 0 == name:

			if self.dlgWhisperWithoutTarget:
				self.dlgWhisperWithoutTarget.Destroy()
				self.dlgWhisperWithoutTarget = None

			return

		try:
			dlgWhisper = self.whisperDialogDict[name]
			dlgWhisper.Destroy()
			del self.whisperDialogDict[name]
		except:
			import dbg
			dbg.TraceError("interface.CloseWhisperDialog - Failed to find key")

	def __ArrangeWhisperButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		xPos = screenWidth - 70
		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		yShift = 0
		if app.ENABLE_WHISPER_MESSENGER and self.wndMessengerButton:
			yShift = -30
			self.wndMessengerButton.SetPosition(xPos, yPos + 63 + yShift)
			count = 2
		for button in self.whisperButtonList:

			button.SetPosition(xPos + (int(count/yCount) * -50), yPos + (count%yCount * 63) + yShift)
			count += 1

	def __FindWhisperButton(self, name):
		for button in self.whisperButtonList:
			if button.name == name:
				return button

		return 0

	def __MakeWhisperDialog(self, name):
		dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
		dlgWhisper.BindInterface(self)
		dlgWhisper.LoadDialog()
		dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
		self.whisperDialogDict[name] = dlgWhisper

		self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		return dlgWhisper

	def ShowWhisperToolTip(self):
		if app.ENABLE_WHISPER_CLOSE_SHORTCUT and self.whisper_tooltip:
			self.whisper_tooltip.FitIconTextLine()
			self.whisper_tooltip.SetTop()
			self.whisper_tooltip.Show()

	def HideWhisperTooltip(self):
		if app.ENABLE_WHISPER_CLOSE_SHORTCUT and self.whisper_tooltip:
			self.whisper_tooltip.Hide()

	def __MakeWhisperButton(self, name):
		whisperButton = uiWhisper.WhisperButton()
		if app.ENABLE_WIKI_SYSTEM and name == "[W?K?]":
			whisperButton.SetUpVisual("d:/ymir work/ui/game/whisper/wikipedia.tga")
			whisperButton.SetOverVisual("d:/ymir work/ui/game/whisper/wikipedia_over.tga")
			whisperButton.SetDownVisual("d:/ymir work/ui/game/whisper/wikipedia.tga")
			whisperButton.SetToolTipTextWithColor(name, 0xffe7a83b)
		else:
			whisperButton.SetUpVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetOverVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetDownVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			if self.IsGameMasterName(name):
				whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
			else:
				whisperButton.SetToolTipText(name)
		whisperButton.ToolTipText.SetHorizontalAlignCenter()
		whisperButton.SetEvent(ui.__mem_func__(self.ShowWhisperDialog), whisperButton)
		if app.ENABLE_WHISPER_CLOSE_SHORTCUT:
			whisperButton.SetOverInEvent(ui.__mem_func__(self.ShowWhisperToolTip))
			whisperButton.SetOverOutEvent(ui.__mem_func__(self.HideWhisperTooltip))
		import advanced_options_runtime
		if advanced_options_runtime.Get("whisper_sender_letter", True): whisperButton.Show()
		whisperButton.name = name

		self.whisperButtonList.insert(0, whisperButton)
		self.__ArrangeWhisperButton()

		return whisperButton

	def __DestroyWhisperButton(self, button):
		button.SetEvent(0)
		self.whisperButtonList.remove(button)
		self.__ArrangeWhisperButton()
		if app.ENABLE_WHISPER_CLOSE_SHORTCUT:
			self.HideWhisperTooltip()

	def HideAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Hide()
		if app.ENABLE_WHISPER_MESSENGER and self.wndMessengerButton:
			self.wndMessengerButton.Hide()

	def ShowAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Show()
		if app.ENABLE_WHISPER_MESSENGER and self.wndMessengerButton and not constInfo.MESSENGER_BUTTON_CLOSED:
			self.wndMessengerButton.Show()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def RefreshVisibleCostume(self):
			self.wndInventory.RefreshVisibleCostume()

	if app.ENABLE_SPECIAL_INVENTORY:
		def CloseLoadSafeboxEvent(self):
			if not self.wndSpecialInventory:
				return

			self.wndSpecialInventory.CloseLoadSafeboxEvent()

		def CloseLoadMallEvent(self):
			if not self.wndSpecialInventory:
				return

			self.wndSpecialInventory.CloseLoadMallEvent()

	def __CheckGameMaster(self, name):
		if not self.listGMName.has_key(name):
			return
		if self.whisperDialogDict.has_key(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def RegisterGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return
		self.listGMName[name] = "GM"

	def IsGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return TRUE
		else:
			return FALSE

	### Guild Building ###

	def BUILD_OpenWindow(self):
		self.wndGuildBuilding = uiGuild.BuildGuildBuildingWindow()
		self.wndGuildBuilding.Open()
		self.wndGuildBuilding.wnds = self.__HideWindows()
		self.wndGuildBuilding.SetCloseEvent(ui.__mem_func__(self.BUILD_CloseWindow))

	def BUILD_CloseWindow(self):
		self.__ShowWindows(self.wndGuildBuilding.wnds)
		self.wndGuildBuilding = None

	def BUILD_OnUpdate(self):
		if not self.wndGuildBuilding:
			return

		if self.wndGuildBuilding.IsPositioningMode():
			import background
			x, y, z = background.GetPickingPoint()
			self.wndGuildBuilding.SetBuildingPosition(x, y, z)

	def BUILD_OnMouseLeftButtonDown(self):
		if not self.wndGuildBuilding:
			return

		# GUILD_BUILDING
		if self.wndGuildBuilding.IsPositioningMode():
			self.wndGuildBuilding.SettleCurrentPosition()
			return TRUE
		elif self.wndGuildBuilding.IsPreviewMode():
			pass
		else:
			return TRUE
		# END_OF_GUILD_BUILDING
		return FALSE

	def BUILD_OnMouseLeftButtonUp(self):
		if not self.wndGuildBuilding:
			return

		if not self.wndGuildBuilding.IsPreviewMode():
			return TRUE

		return FALSE

	def BULID_EnterGuildArea(self, areaID):
		# GUILD_BUILDING
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()

		if mainCharacterName != masterName:
			return

		if areaID != player.GetGuildID():
			return
		# END_OF_GUILD_BUILDING

		self.wndGameButton.ShowBuildButton()

	def BULID_ExitGuildArea(self, areaID):
		self.wndGameButton.HideBuildButton()






	def IsEditLineFocus(self):
		if self.ChatWindow.chatLine.IsFocus():
			return 1

		if self.ChatWindow.chatToLine.IsFocus():
			return 1

		return 0

	def AttachItemFromSafebox(self, slotIndex, itemIndex):
		if self.wndInventory and self.wndInventory.IsShow():
			self.wndInventory.AttachItemFromSafebox(slotIndex, itemIndex)

		return TRUE

	def AttachInvenItemToOtherWindowSlot(self, slotWindow, slotIndex):
		if self.wndSafebox and self.wndSafebox.IsShow():
			return self.wndSafebox.AttachItemFromInventory(slotWindow, slotIndex)

		return FALSE

	def EmptyFunction(self):
		pass

	if app.ENABLE_RANKING:
		def OpenRanking(self):
			if self.wndRanking:
				self.wndRanking.Open()

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

	if app.ENABLE_GLOBAL_RANKING:
		def LoadRankData(self, page, timeIdx, category, secondsToReset, ownValue, rankCmd):
			if self.wndRanking:
				self.wndRanking.LoadRankData(page, timeIdx, category, secondsToReset, ownValue, rankCmd)

		def RankingClearData(self):
			if self.wndRanking:
				self.wndRanking.ClearData()

		def RankingAddRank(self, position, level, points, name, realPosition):
			if self.wndRanking:
				self.wndRanking.AddRank(position, name, points, level, realPosition)

		def RankingRefresh(self):
			if self.wndRanking:
				self.wndRanking.RefreshList()
				self.wndRanking.OnScroll()

	def IsShowDlgQuestionWindow(self):
		if self.wndInventory.IsDlgQuestionShow():
			return TRUE
		elif self.wndDragonSoul and self.wndDragonSoul.IsDlgQuestionShow():
			return TRUE
		else:
			return FALSE

	def CloseDlgQuestionWindow(self):
		if self.wndInventory.IsDlgQuestionShow():
			self.wndInventory.CancelDlgQuestion()
		if self.wndDragonSoul and self.wndDragonSoul.IsDlgQuestionShow():
			self.wndDragonSoul.CancelDlgQuestion()

	def DeactivateSlot(self, slotindex, type):
		self.wndInventory.DeactivateSlot(slotindex, type)

	def ActivateSlot(self, slotindex, type):
		self.wndInventory.ActivateSlot(slotindex, type)

	if app.ENABLE_RENDER_TARGET:
		def MakeRenderTargetWindow(self):
			if self.wndRenderTarget == None:
				self.wndRenderTarget = uiRenderTarget.RenderTargetWindow()

		def OpenRenderTargetWindow(self, renderType = 0, renderVnum = 11299):
			self.MakeRenderTargetWindow()
			self.wndRenderTarget.Open(renderType, renderVnum)

	if app.ENABLE_IKASHOP_RENEWAL:
		def ToggleIkashopBusinessBoard(self):
			self.wndIkashopBusiness.Toggle()

		def ToggleIkashopSearchShopBoard(self):
			self.wndIkashopSearchShop.Toggle()

		def SearchShopForItem(self, itemVnum):
			board = self.wndIkashopSearchShop
			if not itemVnum or not board:
				return
			import item
			item.SelectItem(itemVnum)
			itemName = item.GetItemName()
			if not itemName:
				board.Open()
				return
			board._OnClickResetFilters()
			board.inputNameEdit.SetText(itemName)
			board._OnClickSearchButton()

	if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
		def OnChangePickUPMode(self):
			self.dlgSystem.OnChangePickUPMode()

	if app.ENABLE_RENEWAL_SKILL_SELECT:
		def OpenSkillSelectWindow(self, job):
			self.wndSkillSelect.Open(job)

	if app.ENABLE_NEW_DUNGEON_LIB:
		def MakeDungeonTimerWindow(self):
			self.wndDungeonTimer = uiDungeonTimer.Cooldown()
			self.wndDungeonTimer.Hide()

	if app.ENABLE_DUNGEON_INFO:
		def MakeDungeonInfo(self):
			if self.wndDungeonInfo == None:
				self.wndDungeonInfo = uiDungeonInfo.DungeonInfo()

		def OpenDungeonInfo(self):
			self.MakeDungeonInfo()
			if self.wndDungeonInfo.IsShow():
				self.wndDungeonInfo.Close()
			else:
				self.wndDungeonInfo.Open()

	if app.ENABLE_ITEMSHOP:
		def MakeItemShopWindow(self):
			if not self.wndItemShop:
				self.wndItemShop = uiItemShopNew.ItemShopWindow()

		def OpenItemShopWindow(self):
			if not self.wndItemShop:
				self.wndItemShop = uiItemShopNew.ItemShopWindow()

			if self.wndItemShop.IsShow():
				self.wndItemShop.Close()
			else:
				self.wndItemShop.Open()

		def OpenItemShopMainWindow(self):
			self.MakeItemShopWindow()
			self.wndItemShop.Open()
			self.wndItemShop.LoadFirstOpening()

		def ItemShopHideLoading(self):
			self.MakeItemShopWindow()
			self.wndItemShop.Open()
			self.wndItemShop.CloseLoading()

		def ItemShopPurchasesWindow(self):
			self.MakeItemShopWindow()
			self.wndItemShop.Open()
			self.wndItemShop.OpenPurchasesWindow()

		def ItemShopUpdateItem(self, itemID, itemMaxSellingCount):
			self.MakeItemShopWindow()
			self.wndItemShop.UpdateItem(itemID, itemMaxSellingCount)

		def ItemShopSetDragonCoin(self, lldCoins, lldJCoins = 0):
			if not self.wndItemShop:
				self.wndItemShop = uiItemShopNew.ItemShopWindow()

			self.wndItemShop.SetDragonCoin(lldCoins)

			if app.USE_ITEMSHOP_RENEWED:
				self.wndItemShop.SetDragonJeton(lldJCoins)

		def SetWheelItemData(self, cmd):
			self.MakeItemShopWindow()
			self.wndItemShop.SetWheelItemData(str(cmd))

		def OnSetWhell(self, giftIndex):
			self.MakeItemShopWindow()
			self.wndItemShop.OnSetWhell(int(giftIndex))

		def GetWheelGiftData(self, itemVnum, itemCount):
			self.MakeItemShopWindow()
			self.wndItemShop.GetWheelGiftData(int(itemVnum), int(itemCount))

	if app.ENABLE_WIKI_SYSTEM:
		def SearchWikiForItem(self, itemVnum):
			if not itemVnum:
				return
			if self.wndWiki == None:
				self.__MakeWiki()
			if self.wndWiki:
				if not self.wndWiki.IsShow():
					self.wndWiki.Open()
				self.wndWiki.SearchItem(itemVnum)

		def SearchWikiForMob(self, mobVnum):
			if not mobVnum:
				return
			if self.wndWiki == None:
				self.__MakeWiki()
			if self.wndWiki:
				if not self.wndWiki.IsShow():
					self.wndWiki.Open()
				self.wndWiki.ShowItemInfo(mobVnum, 1)

		def OpenWikiWindow(self):
			if self.wndWiki == None:
				self.__MakeWiki()
			if self.wndWiki and self.wndWiki.IsShow():
				self.wndWiki.Close()
			elif self.wndWiki:
				self.wndWiki.Open()

		def __MakeWiki(self):
			if self.wndWiki == None:
				self.wndWiki = uiWiki.EncyclopediaofGame()
				self.wndInventory.BindWikiWindow(self.wndWiki)
				if self.wndInventoryNew:
					self.wndInventoryNew.BindWikiWindow(self.wndWiki)

		def RecvReadWiki(self):
			if app.ENABLE_WHISPER_MESSENGER:
				return
			name = "[W?K?]"
			if not self.whisperDialogDict.has_key(name):
				btn = self.__FindWhisperButton(name)
				if 0 == btn:
					btn = self.__MakeWhisperButton(name)
					btn.Flash()
					if app.ENABLE_BLINK_ALERT:
						app.FlashApplication()
					chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))
				else:
					btn.Flash()
					if app.ENABLE_BLINK_ALERT:
						app.FlashApplication()


	if app.ENABLE_SLOT_MARKING_SYSTEM:
		def MarkUnusableInvenSlotOnTopWnd(self, onTopWnd, InvenSlot):
			if app.ENABLE_SLOT_MARKING_SYSTEM:
				if onTopWnd == player.ON_TOP_WND_SHOP and self.dlgShop and self.dlgShop.CantSellInvenItem(InvenSlot):
					return TRUE
				elif onTopWnd == player.ON_TOP_WND_SAFEBOX and self.wndSafebox and self.wndSafebox.CantCheckInItem(InvenSlot):
					return TRUE
				elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP and self.privateShopBuilder:
					if app.ENABLE_LOCK_SLOT_WHEN_SHOP_BUILDING:
						if self.privateShopBuilder.CantTradableItem(InvenSlot, player.INVENTORY):
							return TRUE
					else:
						if self.privateShopBuilder.CantTradableItem(InvenSlot):
							return TRUE
				elif onTopWnd == player.ON_TOP_WND_EXCHANGE and self.dlgExchange and self.dlgExchange.CantTradableItem(InvenSlot):
					return TRUE

			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				if onTopWnd == player.ON_TOP_WND_ACCE_COMBINE and self.wndAcceCombine and self.wndAcceCombine.CantTradableItem(InvenSlot):
					return TRUE
				elif onTopWnd == player.ON_TOP_WND_ACCE_ABSORB and self.wndAcceAbsorption and self.wndAcceAbsorption.CantTradableItem(InvenSlot):
					return TRUE

			return FALSE

		def SetOnTopWindow(self, onTopWnd):
			self.OnTopWindow = onTopWnd

		def GetOnTopWindow(self):
			return self.OnTopWindow

		def MarkUnusableDSInvenSlotOnTopWnd(self, onTopWnd, slotIndex):
			if onTopWnd == player.ON_TOP_WND_SHOP and self.dlgShop and self.dlgShop.CantSellDSItem(slotIndex):
				return TRUE
			elif onTopWnd == player.ON_TOP_WND_SAFEBOX and self.wndSafebox and self.wndSafebox.CantCheckInDSItem(slotIndex):
				return TRUE
			elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP and self.privateShopBuilder:
				if app.ENABLE_LOCK_SLOT_WHEN_SHOP_BUILDING:
					if self.privateShopBuilder.CantTradableItem(slotIndex, player.DRAGON_SOUL_INVENTORY):
						return TRUE
			elif onTopWnd == player.ON_TOP_WND_EXCHANGE and self.dlgExchange:
				if self.dlgExchange.CantTradableItem(slotIndex, player.DRAGON_SOUL_INVENTORY):
					return TRUE
			return FALSE

		def RefreshMarkInventoryBag(self):
			if self.wndInventory and self.wndInventory.IsShow():
				self.wndInventory.RefreshBagSlotWindow()

			if app.ENABLE_SPECIAL_INVENTORY:
				if self.wndSpecialInventory and self.wndSpecialInventory.IsShow():
					self.wndSpecialInventory.RefreshBagSlotWindow()

	if app.ENABLE_AURA_COSTUME_SYSTEM:
		def AuraWindowOpen(self, type):
			if self.wndAura.IsShow():
				return

			if self.inputDialog or self.privateShopBuilder.IsShow():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ACCE_NOT_OPEN_PRIVATE_SHOP)
				return

			if self.dlgRefineNew and self.dlgRefineNew.IsShow():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ACCE_NOT_OPEN_REFINE)
				return

			self.wndAura.Open(type)

			if not self.wndInventory.IsShow():
				self.wndInventory.Show()

		def AuraWindowClose(self):
			if not self.wndAura.IsShow():
				return

			self.wndAura.CloseWindow()

	if app.ENABLE_ZODIAC_MISSION:
		def __Make12ziRewardWindow(self):
			self.wnd12ziReward = ui12zi.Reward12ziWindow()
			self.wnd12ziReward.SetItemToolTip(self.tooltipItem)
			self.wnd12ziReward.Hide()
		def __Make12ziTimerWindow(self):
			self.wnd12ziTimer = ui12zi.FloorLimitTimeWindow()
			self.wnd12ziTimer.Hide()

	if app.ENABLE_TRACK_WINDOW:
		def TrackWindowCheckPacket(self):
			self.wndTrackWindow.CheckPacket()
		def MakeTrackWindow(self):
			if self.wndTrackWindow == None:
				self.wndTrackWindow = uiTrack.TrackWindow()
		def OpenTrackWindow(self):
			self.MakeTrackWindow()
			if self.wndTrackWindow.IsShow():
				self.wndTrackWindow.Close()
			else:
				self.wndTrackWindow.Open()
		def TrackDungeonInfo(self, cmdData):
			self.MakeTrackWindow()
			self.wndTrackWindow.TrackDungeonInfo(cmdData)
		def TrackBossInfo(self, bossID, bossLeftTime, bossChannel):
			self.MakeTrackWindow()
			self.wndTrackWindow.TrackBossInfo(int(bossID), int(bossLeftTime), int(bossChannel))


	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetHatchingWindowCommand(self, command):
			if self.wndPetInfoWindow:
				if self.wndPetInfoWindow.wndPetHatching:
					self.wndPetInfoWindow.wndPetHatching.PetHatchingWindowCommand(command)

		def PetNameChangeWindowCommand(self, command):
			if self.wndPetInfoWindow:
				if self.wndPetInfoWindow.wndPetNameChange:
					self.wndPetInfoWindow.wndPetNameChange.PetNameChangeWindowCommand(command)

		def PetSkillUpgradeDlgOpen(self, slot, index, gold):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.OpenPetSkillUpGradeQuestionDialog(slot, index, gold)

		def PetFlashEvent(self, index):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetFlashEvent(index)

		def PetInfoBindAffectShower(self, affect_shower):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetInfoBindAffectShower(affect_shower)

		def PetAffectShowerRefresh(self):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetAffectShowerRefresh()

		def PetFeedReuslt(self, result):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetFeedReuslt(result)

		def PetAttrDetermineResult(self, byType):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetAttrDetermineResult(byType)

		def PetAttrChangeResult(self, slotIndex, byType):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetAttrChangeResult(slotIndex, byType)

		def PetReviveResult(self, result):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetReviveResult(result)

		def PetWindowTypeResult(self, result):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetWindowTypeResult(result)

		def TogglePetInformationWindow(self):
			if app.ENABLE_GROWTH_PET_RENEWAL and self.wndCompanion:
				if FALSE == player.IsObserverMode():
					if self.wndCompanion.IsShow() and self.wndCompanion.tab == uiCompanion.TAB_PET:
						self.wndCompanion.Close()
					else:
						self.wndCompanion.Open(uiCompanion.TAB_PET)
				return
			if FALSE == player.IsObserverMode():
				if not self.wndPetInfoWindow.IsShow():
					self.wndPetInfoWindow.Show()
				else:
					self.wndPetInfoWindow.Close()

	if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
		def OpenWarpWindow(self):
			if app.ENABLE_TELEPORT_MAP_WINDOW and app.ENABLE_DUNGEON_INFO_WINDOW:
				if self.wndDungeonTrack == None:
					self.wndDungeonTrack = uiDungeonWindow.DungeonWindow()
				if self.wndDungeonTrack.IsShow() and self.wndDungeonTrack.GetPage() == "MAP":
					self.wndDungeonTrack.Close()
				else:
					self.wndDungeonTrack.Open("MAP")
				return
			if self.wndWarpWindow.IsShow():
				self.wndWarpWindow.Close()
			else:
				self.wndWarpWindow.Open()

	if app.ENABLE_TRACK_WINDOW:
		def TrackWindowCheckPacket(self):
			self.wndTrackWindow.CheckPacket()

		def MakeTrackWindow(self):
			if self.wndTrackWindow == None:
				self.wndTrackWindow = uiTrack.TrackWindow()

		def OpenTrackWindow(self):
			self.MakeTrackWindow()
			if self.wndTrackWindow.IsShow():
				self.wndTrackWindow.Close()
			else:
				self.wndTrackWindow.Open()

		def TrackDungeonInfo(self, cmdData):
			self.MakeTrackWindow()
			self.wndTrackWindow.TrackDungeonInfo(cmdData)

		def TrackBossInfo(self, bossID, bossLeftTime, bossChannel):
			self.MakeTrackWindow()
			self.wndTrackWindow.TrackBossInfo(int(bossID), int(bossLeftTime), int(bossChannel))

		def TrackRecvInfo(self, content):
			content = content.replace("$", " ")
			self.RegisterGameMasterName(localeInfo.SYSTEM_WHISPER)
			chat.AppendWhisper(chat.WHISPER_TYPE_CHAT, localeInfo.SYSTEM_WHISPER, content)
			self.RecvWhisper(localeInfo.SYSTEM_WHISPER)


	if app.ENABLE_MOVE_COSTUME_ACCE_ATTR:
		def ItemCombinationDialogOpen(self):
			if self.wndItemCombination:
				self.wndItemCombination.Open()

		def ItemCombinationDialogClose(self):
			if self.wndItemCombination and self.wndItemCombination.IsShow():
				self.wndItemCombination.Close()
	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def ChangeWindowOpen(self, type):
			if self.wndChangeLook:
				self.wndChangeLook.Open(type)

		def IsShowDlgQuestionWindow(self):
			if self.wndInventory.IsDlgQuestionShow():
				return TRUE
			elif self.wndDragonSoul and self.wndDragonSoul.IsDlgQuestionShow():
				return TRUE
			else:
				return FALSE

		def CloseDlgQuestionWindow(self):
			if self.wndInventory.IsDlgQuestionShow():
				self.wndInventory.CancelDlgQuestion()
			if self.wndDragonSoul and self.wndDragonSoul.IsDlgQuestionShow():
				self.wndDragonSoul.CancelDlgQuestion()

	def SetAffectShower(self, shower):
		import _weakref
		self.uiAffectshower = _weakref.proxy(shower)
		if app.ENABLE_AFFECTSHOWER_TOOLTIP_RENEWAL:
			if self.wndMiniMap:
				self.uiAffectshower.SetMiniMapWidth(self.wndMiniMap.GetWidth())
			if self.wndParty:
				self.uiAffectshower.SetPartyWindow(self.wndParty)
		if app.ENABLE_STATUS_EFFECT_SHOWER:
			try:
				if self.uitargetBoard:
					self.uitargetBoard.BindAffectShower(shower)
			except (AttributeError, TypeError):
				pass

	def GetAffectData(self, affect_type):
		if self.uiAffectshower == None:
			return None
		return self.uiAffectshower.GetAffectData(affect_type)


	if app.ENABLE_HUNTING_SYSTEM:
		def ToggleHuntingWindow(self):
			if self.wndHunting.IsShow():
				self.wndHunting.Close()
			elif self.wndHuntingSelect.IsShow():
				self.wndHuntingSelect.Close()
			else:
				net.SendHuntingAction(1, 0)

		def OpenHuntingWindowMain(self, level, monster, cur_count, dest_count, money_min, money_max, exp_min, exp_max, race_item, race_item_count):
			if self.wndHunting:
				self.wndHunting.OpenMain(level, monster, cur_count, dest_count, money_min, money_max, exp_min, exp_max, race_item, race_item_count)
				self.wndHunting.SetTop()
				constInfo.HUNTING_BUTTON_FLASH = 0

		def OpenHuntingWindowSelect(self, level, type ,monster, count, money_min, money_max, exp_min, exp_max, race_item, race_item_count):
			if self.wndHunting and self.wndHunting.IsShow():
				self.wndHunting.CloseWithMini()
			self.wndHuntingSelect.OpenSelect(level, type ,monster, count, money_min, money_max, exp_min, exp_max, race_item, race_item_count)
			constInfo.HUNTING_BUTTON_FLASH = 0

		def OpenHuntingWindowReward(self, level, reward, reward_count, random_reward, random_reward_count, money, exp):
			if False == self.wndHuntingReward.IsShow():
				self.wndHuntingReward.OpenReward(level, reward, reward_count, random_reward, random_reward_count, money, exp)
				self.wndHuntingReward.SetTop()

		def UpdateHuntingMission(self, count):
			if self.wndHunting:
				self.wndHunting.UpdateMission(count)

		def HuntingSetRandomItemsMain(self, item_vnum, item_count):
			if self.wndHunting:
				self.wndHunting.SetRandomItemTable(item_vnum, item_count)

		def HuntingSetRandomItemsSelect(self, item_vnum, item_count):
			if self.wndHuntingSelect:
				self.wndHuntingSelect.SetRandomItemTable(item_vnum, item_count)


	if app.__DUNGEON_INFO__:
		def DungeonInfoQuestIdx(self, questIdx):
			constInfo.dungeonInfoQuestIdx = int(questIdx)

		def DungeonInfoQuestCMD(self):
			net.SendQuestInputStringPacket(constInfo.dungeonInfoCMD)
			constInfo.dungeonInfoCMD = ""

		def OpenDungeonInfo(self):
			try:
				if app.ENABLE_DUNGEON_INFO_WINDOW:
					if self.wndDungeonTrack == None:
						self.wndDungeonTrack = uiDungeonWindow.DungeonWindow()
					if self.wndDungeonTrack.IsShow():
						self.wndDungeonTrack.Close()
					else:
						self.wndDungeonTrack.Open()
					return
				if self.wndDungeonTrack == None:
					self.wndDungeonTrack = uiDungeonTrack.DungeonTrack()
				if self.wndDungeonTrack.IsShow():
					self.wndDungeonTrack.Close()
				else:
					self.wndDungeonTrack.Open()
			except Exception, e:
				import dbg
				dbg.TraceError("OpenDungeonInfo Error: %s" % str(e))

		def DungeonInfoCooldown(self, clean, data):
			dungeonData = uiDungeonTrack.dungeonData
			if int(clean):
				for mobIdx, dungeonInfo in dungeonData.items():
					dungeonInfo["server_cooldown"] = 0
					dungeonInfo["server_completed"] = 0
					dungeonInfo["server_fastest"] = 0
					dungeonInfo["server_damage"] = 0
					dungeonInfo["whisper_info"] = False
			if data != "" and data != "-":
				dungeonList = data[:len(data)-1].split("#")
				for dungeonInfo in dungeonList:
					dungeonSplitData = dungeonInfo.split("|")
					if len(dungeonSplitData) >= 5:
						bossIdx = int(dungeonSplitData[0])
						if dungeonData.has_key(bossIdx):
							if dungeonData[bossIdx]["server_cooldown"] != app.GetGlobalTimeStamp() + int(dungeonSplitData[1]):
								dungeonData[bossIdx]["whisper_info"] = False
							dungeonData[bossIdx]["server_cooldown"] = 0 if int(dungeonSplitData[1]) <= 0 else app.GetGlobalTimeStamp() + int(dungeonSplitData[1])
							dungeonData[bossIdx]["server_completed"] = int(dungeonSplitData[2])
							dungeonData[bossIdx]["server_fastest"] = int(dungeonSplitData[3])
							dungeonData[bossIdx]["server_damage"] = int(dungeonSplitData[4])
							if len(dungeonSplitData) >= 11:
								dungeonData[bossIdx]["server_dps"] = int(dungeonSplitData[5])
								dungeonData[bossIdx]["current_daily_limit"] = int(dungeonSplitData[6])
								dungeonData[bossIdx]["daily_limit"] = int(dungeonSplitData[7])
								dungeonData[bossIdx]["server_average_fastest"] = int(dungeonSplitData[8])
								dungeonData[bossIdx]["server_best_fastest"] = int(dungeonSplitData[9])
								dungeonData[bossIdx]["server_daily_reset"] = app.GetGlobalTimeStamp() + int(dungeonSplitData[10])
							# ENABLE_DUNGEON_LIMIT_RENEWAL: pc used today|weekly stack
							if len(dungeonSplitData) >= 13:
								dungeonData[bossIdx]["current_daily_limit_pc"] = int(dungeonSplitData[11])
								dungeonData[bossIdx]["daily_stack"] = int(dungeonSplitData[12])
			if self.wndDungeonManager == None:
				self.wndDungeonManager = uiDungeonTrack.DungeonManager()
			if self.wndDungeonTrack == None:
				if app.ENABLE_DUNGEON_INFO_WINDOW:
					self.wndDungeonTrack = uiDungeonWindow.DungeonWindow()
				else:
					self.wndDungeonTrack = uiDungeonTrack.DungeonTrack()
			self.wndDungeonTrack.Refresh()

		def LoadServerData(self, mobIdx, rankIdx, cmd):
			if self.wndDungeonTrack != None:
				self.wndDungeonTrack.LoadServerData(int(mobIdx), int(rankIdx), cmd)

	if app.__AUTO_HUNT__:
		def AutoHuntStatus(self, status):
			if self.wndAutoHunt:
				self.wndAutoHunt.SetStatus(True if int(status) else False)
		def CheckAutoLogin(self):
			if self.wndAutoHunt == None:
				self.wndAutoHunt = uiAutoHunt.Window()
			self.wndAutoHunt.CheckAutoLogin()
		def OpenAutoHunt(self):
			if self.wndAutoHunt == None:
				self.wndAutoHunt = uiAutoHunt.Window()
			if self.wndAutoHunt.IsShow():
				self.wndAutoHunt.Close()
			else:
				self.wndAutoHunt.Open()
		def ToggleAutoHuntWindow(self):
			if self.wndAutoHunt == None:
				self.wndAutoHunt = uiAutoHunt.Window()
			if self.wndAutoHunt.IsShow():
				self.wndAutoHunt.Close()
			else:
				self.wndAutoHunt.Open()

	if app.ENABLE_BATTLEPASS_RENEWAL:
		def ToggleBattlePassWindow(self):
			if self.wndBattlePass:
				self.wndBattlePass.Toggle()

		def BattlePassInfo(self, data):
			if self.wndBattlePass:
				self.wndBattlePass.SetInfo(data)

		def BattlePassMissions(self, data):
			if self.wndBattlePass:
				self.wndBattlePass.SetMissions(data)

		def BattlePassMission(self, data):
			if self.wndBattlePass:
				self.wndBattlePass.SetMission(data)

		def BattlePassResult(self, data):
			if self.wndBattlePass:
				self.wndBattlePass.OnResult(data)

	if app.ENABLE_BIOLOG_RENEWAL:
		def ToggleBiologistWindow(self):
			if self.wndBiologist:
				self.wndBiologist.Toggle()

		def OpenBiologistWindow(self):
			if self.wndBiologist:
				self.wndBiologist.Open()

		def BiologistInfo(self, data):
			if self.wndBiologist:
				self.wndBiologist.SetInfo(data)

		def BiologistResult(self, code, value):
			if self.wndBiologist:
				self.wndBiologist.OnResult(code, value)


	if app.ENABLE_GAYA_TICKET_SYSTEM:
		def OpenGemTicket(self, itemPos):
			self.wndImproveGemTicket.Open(itemPos)

	if app.ENABLE_YIN_AND_YANG_ATTR:
		def OpenYinAndYangInventory(self):
			if self.wndYinAndYangInventory:
				self.wndYinAndYangInventory.Open()

		def CloseYinAndYangInventory(self):
			if self.wndYinAndYangInventory:
				self.wndYinAndYangInventory.Close()

		def ToggleYinAndYangInventory(self):
			if self.wndYinAndYangInventory:
				if self.wndYinAndYangInventory.IsShow():
					self.wndYinAndYangInventory.Close()
				else:
					self.wndYinAndYangInventory.Open()

		def OpenYinAndYangHarmony(self):
			if self.wndYinAndYangHarmony:
				self.wndYinAndYangHarmony.Open()

		def CloseYinAndYangHarmony(self):
			if self.wndYinAndYangHarmony:
				self.wndYinAndYangHarmony.Close()

		def ToggleYinAndYangHarmony(self):
			if self.wndYinAndYangHarmony:
				if self.wndYinAndYangHarmony.IsShow():
					self.wndYinAndYangHarmony.Close()
				else:
					self.wndYinAndYangHarmony.Open()

if __name__ == "__main__":

	import app
	import wndMgr
	import systemSetting
	import mouseModule
	import grp
	import ui
	import localeInfo

	app.SetMouseHandler(mouseModule.mouseController)
	app.SetHairColorEnable(TRUE)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	app.Create(localeInfo.APP_TITLE, systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	mouseModule.mouseController.Create()

	class TestGame(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)

			localeInfo.LoadLocaleData()
			player.SetItemData(0, 27001, 10)
			player.SetItemData(1, 27004, 10)

			self.interface = Interface()
			self.interface.MakeInterface()
			self.interface.ShowDefaultWindows()
			self.interface.RefreshInventory()

		def __del__(self):
			ui.Window.__del__(self)

		def OnUpdate(self):
			app.UpdateGame()

		def OnRender(self):
			app.RenderGame()
			grp.PopState()
			grp.SetInterfaceRenderState()

	game = TestGame()
	game.SetSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	game.Show()

	app.Loop()
