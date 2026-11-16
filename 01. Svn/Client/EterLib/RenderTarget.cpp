// CRenderTarget::CRenderTarget(const DWORD width, const DWORD height) : icinde:
// Ara:
	}
	f_zoom = 0.0f;
	m_renderTargetTexture = std::move(pTex);

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
	m_dwTextureWidth = width;
	m_dwTextureHeight = height;
#endif


// Ara:
}

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
bool CRenderTarget::SetTransparent()
{
	auto pTex = std::make_unique<CGraphicRenderTargetTexture>();
	if (!pTex->Create(m_dwTextureWidth, m_dwTextureHeight, D3DFMT_A8R8G8B8, D3DFMT_D16))
	{
		TraceError("CRenderTarget::SetTransparent: Could not create an alpha texture %ux%u", m_dwTextureWidth, m_dwTextureHeight);
		return false;
	}
	RECT rect = *m_renderTargetTexture->GetRenderingRect();
	pTex->SetRenderingRect(&rect);
	m_renderTargetTexture = std::move(pTex);
	m_background.reset();
	return true;
}
#endif


// void CRenderTarget::SelectModel(const int index, bool isFromScale) icinde:
// Ara:
			m_v3Eye.y = -(fRaceHeight * 8.9f);
			m_v3Eye.z = 0.0f;
			m_v3Target.z = fRaceHeight / 2.0f;

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
			// GetHeight is only the extent; a model floating above the ground (flying pets) is centred once it is posed
			m_iCenterOnBoundBox = 3;
#endif


// void CRenderTarget::RenderModel() icinde:
// Ara:
	if (m_bShowModel)
	{
		m_pModel->Update();

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
		if (m_iCenterOnBoundBox > 0 && --m_iCenterOnBoundBox == 0)
		{
			D3DXVECTOR3 v3Min, v3Max;
			m_pModel->GetGraphicThingInstanceRef().GetBoundBox(&v3Min, &v3Max);
			if (v3Max.z > v3Min.z && v3Max.z < 100000.0f)
			{
				const float fCenter = (v3Min.z + v3Max.z) / 2.0f;	// world pose, already scaled
				m_v3Eye.z += fCenter - m_v3Target.z;
				m_v3Target.z = fCenter;
			}
		}
#endif


// void CRenderTarget::RenderModel() icinde:
// Ara:
		m_pModel->Render();

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
		m_pModel->GetGraphicThingInstanceRef().RenderAllAttachingEffectWiki();
#endif

