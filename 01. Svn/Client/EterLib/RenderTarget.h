// Ara:
		void SetScale(float fScale);
		bool IsShow() { return m_visible; }
		void SetZoom(bool bZoom);

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
		bool SetTransparent();
#endif


// Ara:
	private:

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
		DWORD m_dwTextureWidth = 0;
		DWORD m_dwTextureHeight = 0;
		int m_iCenterOnBoundBox = 0;
#endif

