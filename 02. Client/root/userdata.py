import os

ROOT = "Data" + os.sep + "UserData"


def GetPath(fileName, subDir = "", oldName = None):
	folder = ROOT
	if subDir:
		folder = folder + os.sep + subDir
	try:
		if not os.path.isdir(folder):
			os.makedirs(folder)
	except:
		pass
	path = folder + os.sep + fileName
	if oldName is None:
		oldName = fileName
	try:
		if oldName and os.path.isfile(oldName):
			if os.path.isfile(path):
				os.remove(oldName)
			else:
				os.rename(oldName, path)
	except:
		pass
	return path


def MoveOldFiles(prefix, suffix, subDir, newName):
	"""Moves every old root file prefix<name>suffix to Data/UserData/subDir/newName % name (once per client start)."""
	try:
		names = os.listdir(".")
	except:
		return
	for fileName in names:
		if fileName.startswith(prefix) and fileName.endswith(suffix) and len(fileName) > len(prefix) + len(suffix):
			GetPath(newName % fileName[len(prefix):-len(suffix)], subDir, fileName)
