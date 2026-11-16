// Ara:
			TItemData			aSwitchbotItem[SWITCHBOT_SLOT_COUNT];

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
			TItemData			aWardrobeItem[c_Wardrobe_Count];
#endif


// Ara:
		bool m_isDirMov;
		float m_fCmrRotSpd;
		TPlayerStatus m_playerStatus;

// Altina ekle:
#ifdef ENABLE_WARDROBE_SYSTEM
	public:
		DWORD GetItemRevision() const { return m_dwItemRevision; }
	protected:
		DWORD m_dwItemRevision = 1;	// changes whenever an item slot changes (wardrobe owned / storage views)
#endif

