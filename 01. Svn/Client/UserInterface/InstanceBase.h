// Ara:
		float GetBaseHeight();
		// ETC
		CActorInstance& GetGraphicThingInstanceRef();

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
		void AttachHorseSaddle() { __AttachHorseSaddle(); }
#endif

