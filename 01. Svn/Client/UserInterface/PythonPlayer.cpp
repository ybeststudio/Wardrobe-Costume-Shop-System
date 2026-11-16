// const TItemData * CPythonPlayer::GetItemData(TItemPos Cell) const icinde:
// Ara:
	case SWITCHBOT:
		return &m_playerStatus.aSwitchbotItem[Cell.cell];

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	case WARDROBE:
		return &m_playerStatus.aWardrobeItem[Cell.cell];
#endif


// void CPythonPlayer::SetItemData(TItemPos Cell, const TItemData & c_rkItemInst) icinde:
// Ara:
			return;
		}
	}

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	++m_dwItemRevision;
#endif


// void CPythonPlayer::SetItemData(TItemPos Cell, const TItemData & c_rkItemInst) icinde:
// Ara:
	case SWITCHBOT:
		m_playerStatus.aSwitchbotItem[Cell.cell] = c_rkItemInst;
		break;

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	case WARDROBE:
		m_playerStatus.aWardrobeItem[Cell.cell] = c_rkItemInst;
		break;
#endif

