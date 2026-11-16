// PyObject *renderTargetSetMount(PyObject *poSelf, PyObject *poArgs) icinde:
// Ara:
		if (target->IsReady())
		{
			target->GetModel()->MountHorse(iItemVnum);

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
			target->GetModel()->AttachHorseSaddle();
			target->GetModel()->Refresh(CRaceMotionData::NAME_WAIT, true);
#endif


// Ara:
	CRenderTargetManager::Instance().GetRenderTarget(index)->SetZoom(bZoom);
	return Py_BuildNone();
}

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
#include "PythonSkill.h"
PyObject *renderTargetUseSkill(PyObject *poSelf, PyObject *poArgs)
{
	int iIndex, iSkill, iGrade;
	if (!PyTuple_GetInteger(poArgs, 0, &iIndex) || !PyTuple_GetInteger(poArgs, 1, &iSkill) || !PyTuple_GetInteger(poArgs, 2, &iGrade))
		return Py_BadArgument();

	const std::shared_ptr<CRenderTarget> target = CRenderTargetManager::Instance().GetRenderTarget(iIndex);
	if (!target || !target->IsReady())
		return Py_BuildNone();

	CPythonSkill::SSkillData *pSkillData;
	if (!CPythonSkill::Instance().GetSkillData(iSkill, &pSkillData) || pSkillData->IsNoMotion())
		return Py_BuildNone();

	target->GetModel()->NEW_UseSkill(iSkill, pSkillData->GetSkillMotionIndex(iGrade), 1, false);
	return Py_BuildNone();
}

PyObject *renderTargetSetShining(PyObject *poSelf, PyObject *poArgs)
{
	int iIndex, iSlot, iVnum;
	if (!PyTuple_GetInteger(poArgs, 0, &iIndex) || !PyTuple_GetInteger(poArgs, 1, &iSlot) || !PyTuple_GetInteger(poArgs, 2, &iVnum))
		return Py_BadArgument();

	const std::shared_ptr<CRenderTarget> target = CRenderTargetManager::Instance().GetRenderTarget(iIndex);
	if (target && target->IsReady())
		target->GetModel()->SetShining(static_cast<BYTE>(iSlot), static_cast<DWORD>(iVnum));
	return Py_BuildNone();
}

// renderTarget.SetTransparent(index): see-through preview (no background, alpha texture)
PyObject *renderTargetSetTransparent(PyObject *poSelf, PyObject *poArgs)
{
	int iIndex;
	if (!PyTuple_GetInteger(poArgs, 0, &iIndex))
		return Py_BadArgument();

	const std::shared_ptr<CRenderTarget> target = CRenderTargetManager::Instance().GetRenderTarget(iIndex);
	if (target)
		target->SetTransparent();
	return Py_BuildNone();
}

PyObject *renderTargetCopyMainAffects(PyObject *poSelf, PyObject *poArgs)
{
	int iIndex;
	if (!PyTuple_GetInteger(poArgs, 0, &iIndex))
		return Py_BadArgument();

	const std::shared_ptr<CRenderTarget> target = CRenderTargetManager::Instance().GetRenderTarget(iIndex);
	CInstanceBase* pMain = CPythonCharacterManager::Instance().GetMainInstancePtr();
	if (!target || !target->IsReady() || !pMain)
		return Py_BuildNone();

	CAffectFlagContainer kFlags;
	for (UINT eAffect = 0; eAffect < CInstanceBase::AFFECT_NUM; ++eAffect)
	{
		if (eAffect != CInstanceBase::AFFECT_INVISIBILITY && pMain->IsAffect(eAffect))
			kFlags.Set(eAffect, true);
	}
	target->GetModel()->SetAffectFlagContainer(kFlags);
	return Py_BuildNone();
}
#endif


// void initRenderTarget() icinde:
// Ara:
		{"Zoom", renderZoomCamera, METH_VARARGS },
		{"SetZoom", renderSetZoom, METH_VARARGS },
		{"SetScale", renderSetScale, METH_VARARGS },

// Altina ekle:
#ifdef ENABLE_COSTUME_SHOP
		{"UseSkill", renderTargetUseSkill, METH_VARARGS },
		{"SetShining", renderTargetSetShining, METH_VARARGS },
		{"CopyMainAffects", renderTargetCopyMainAffects, METH_VARARGS },
		{"SetTransparent", renderTargetSetTransparent, METH_VARARGS },
#endif

