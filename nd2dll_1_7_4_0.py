import ctypes
import os
import sys

os.environ["PATH"] += ';Libraries\\ND2SDK_1.7.4.0'
nd2 = ctypes.windll.LoadLibrary('Libraries\\ND2SDK_1.7.4.0\\nd2readsdk-shared.dll')

LIM_ERR = {0:  'LIM_OK',
		  -1:  'LIM_ERR_UNEXPECTED',
		  -2:  'LIM_ERR_NOTIMPL',
		  -3:  'LIM_ERR_OUTOFMEMORY',
		  -4:  'LIM_ERR_INVALIDARG',
		  -5:  'LIM_ERR_NOINTERFACE',
		  -6:  'LIM_ERR_ctypes.POINTER',
		  -7:  'LIM_ERR_HANDLE',
		  -8:  'LIM_ERR_ABORT',
		  -9:  'LIM_ERR_FAIL',
		  -10: 'LIM_ERR_ACCESSDENIED',
		  -11: 'LIM_ERR_OS_FAIL',
		  -12: 'LIM_ERR_NOTINITIALIZED',
		  -13: 'LIM_ERR_NOTFOUND',
		  -14: 'LIM_ERR_IMPL_FAILED',
		  -15: 'LIM_ERR_DLG_CANCELED',
		  -16: 'LIM_ERR_DB_PROC_FAILED',
		  -17: 'LIM_ERR_OUTOFRANGE',
		  -18: 'LIM_ERR_PRIVILEGES',
		  -19: 'LIM_ERR_VERSION',}

class LIMPICTURE(ctypes.Structure):
	_fields_ = [('uiWidth', ctypes.c_uint),
				('uiHeight', ctypes.c_uint),
				('uiBitsPerComp', ctypes.c_uint),
				('uiComponents', ctypes.c_uint),
				('uiWidthBytes', ctypes.c_uint),
				('uiSize', ctypes.c_size_t),
				('pImageData', ctypes.c_void_p)]


#LIMFILEAPI LIMFILEHANDLE   Lim_FileOpenForRead(LIMCWSTR wszFileName);
Lim_FileOpenForRead = nd2.Lim_FileOpenForRead
Lim_FileOpenForRead.argtypes = [ctypes.c_wchar_p]
Lim_FileOpenForRead.restype = ctypes.c_void_p
#LIMFILEAPI LIMFILEHANDLE   Lim_FileOpenForReadUtf8(LIMCSTR szFileNameUtf8);
Lim_FileOpenForReadUtf8 = nd2.Lim_FileOpenForReadUtf8
Lim_FileOpenForReadUtf8.argtypes = [ctypes.c_wchar_p]
Lim_FileOpenForReadUtf8.restype = ctypes.c_void_p
#LIMFILEAPI void            Lim_FileClose(LIMFILEHANDLE hFile);
Lim_FileClose = nd2.Lim_FileClose
Lim_FileClose.argtypes = [ctypes.c_void_p]
Lim_FileClose.restype = None
#LIMFILEAPI LIMSIZE         Lim_FileGetCoordSize(LIMFILEHANDLE hFile);
Lim_FileGetCoordSize = nd2.Lim_FileGetCoordSize
Lim_FileGetCoordSize.argtypes = [ctypes.c_void_p]
Lim_FileGetCoordSize.restype = ctypes.c_int
#LIMFILEAPI LIMUINT         Lim_FileGetCoordInfo(LIMFILEHANDLE hFile, LIMUINT coord, LIMSTR type, LIMSIZE maxTypeSize);
Lim_FileGetCoordInfo = nd2.Lim_FileGetCoordInfo
Lim_FileGetCoordInfo.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_int]
Lim_FileGetCoordInfo.restype = ctypes.c_uint
#LIMFILEAPI LIMUINT         Lim_FileGetSeqCount(LIMFILEHANDLE hFile);
Lim_FileGetSeqCount = nd2.Lim_FileGetSeqCount
Lim_FileGetSeqCount.argtypes = [ctypes.c_void_p]
Lim_FileGetSeqCount.restype = ctypes.c_uint
#LIMFILEAPI LIMBOOL         Lim_FileGetSeqIndexFromCoords(LIMFILEHANDLE hFile, const LIMUINT * coords, LIMSIZE coordCount, LIMUINT* seqIdx);
Lim_FileGetSeqIndexFromCoords = nd2.Lim_FileGetSeqIndexFromCoords
Lim_FileGetSeqIndexFromCoords.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.c_int, ctypes.POINTER(ctypes.c_uint)]
Lim_FileGetSeqIndexFromCoords.restype = ctypes.c_int
#LIMFILEAPI LIMSIZE         Lim_FileGetCoordsFromSeqIndex(LIMFILEHANDLE hFile, LIMUINT seqIdx, LIMUINT* coords, LIMSIZE maxCoordCount);
Lim_FileGetCoordsFromSeqIndex = nd2.Lim_FileGetCoordsFromSeqIndex
Lim_FileGetCoordsFromSeqIndex.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.c_int]
Lim_FileGetCoordsFromSeqIndex.restype = ctypes.c_int
#LIMFILEAPI LIMSTR          Lim_FileGetAttributes(LIMFILEHANDLE hFile);
Lim_FileGetAttributes = nd2.Lim_FileGetAttributes
Lim_FileGetAttributes.argtypes = [ctypes.c_void_p]
Lim_FileGetAttributes.restype = ctypes.c_char_p
#LIMFILEAPI LIMSTR          Lim_FileGetMetadata(LIMFILEHANDLE hFile);
Lim_FileGetMetadata = nd2.Lim_FileGetMetadata
Lim_FileGetMetadata.argtypes = [ctypes.c_void_p]
Lim_FileGetMetadata.restype = ctypes.c_char_p
#LIMFILEAPI LIMSTR          Lim_FileGetFrameMetadata(LIMFILEHANDLE hFile, LIMUINT uiSeqIndex);
Lim_FileGetFrameMetadata = nd2.Lim_FileGetFrameMetadata
Lim_FileGetFrameMetadata.argtypes = [ctypes.c_void_p, ctypes.c_uint]
Lim_FileGetFrameMetadata.restype = ctypes.c_char_p
#LIMFILEAPI LIMSTR          Lim_FileGetTextinfo(LIMFILEHANDLE hFile);
Lim_FileGetTextinfo = nd2.Lim_FileGetTextinfo
Lim_FileGetTextinfo.argtypes = [ctypes.c_void_p]
Lim_FileGetTextinfo.restype = ctypes.c_char_p
#LIMFILEAPI LIMSTR          Lim_FileGetExperiment(LIMFILEHANDLE hFile);
Lim_FileGetExperiment = nd2.Lim_FileGetExperiment
Lim_FileGetExperiment.argtypes = [ctypes.c_void_p]
Lim_FileGetExperiment.restype = ctypes.c_char_p
#LIMFILEAPI LIMRESULT       Lim_FileGetImageData(LIMFILEHANDLE hFile, LIMUINT uiSeqIndex, LIMPICTURE* pPicture);
Lim_FileGetImageData = nd2.Lim_FileGetImageData
Lim_FileGetImageData.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(LIMPICTURE)]
Lim_FileGetImageData.restype = ctypes.c_int
#LIMFILEAPI void            Lim_FileFreeString(LIMSTR str);
Lim_FileFreeString = nd2.Lim_FileFreeString
Lim_FileFreeString.argtypes = [ctypes.c_char_p]
Lim_FileFreeString.restype = None
#LIMFILEAPI LIMSIZE         Lim_InitPicture(LIMPICTURE* pPicture, LIMUINT width, LIMUINT height, LIMUINT bpc, LIMUINT components);
Lim_InitPicture = nd2.Lim_InitPicture
Lim_InitPicture.argtypes = [ctypes.POINTER(LIMPICTURE), ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
Lim_InitPicture.restype = ctypes.c_int
#LIMFILEAPI void            Lim_DestroyPicture(LIMPICTURE* pPicture);
Lim_DestroyPicture = nd2.Lim_DestroyPicture
Lim_DestroyPicture.argtypes = [ctypes.POINTER(LIMPICTURE)]
Lim_DestroyPicture.restype = None
