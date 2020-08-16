# import re

# file = open('nd2ReadSDK.h', 'r', encoding='utf-8')
# file_write = open('nd2.py', 'w')

# res = {'void':'None', 'LIMUINT':'ctypes.c_uint', 'LIMINT':'ctypes.c_int', 'LIMRESULT':'ctypes.c_int', 'LIMSIZE':'ctypes.c_size_t', 'LIMFILEHANDLE':'ctypes.c_int'}
# arg = {'void*':'ctypes.c_void_p', 'LIMWCHAR':'ctypes.c_wchar', 'LIMWSTR':'ctypes.c_wchar_p', 'LIMCWSTR':'ctypes.c_wchar_p', 'LIMUINT':'ctypes.c_uint', 'LIMUINT*':'ctypes.POINTER(ctypes.c_uint)', 'LIMSIZE':'ctypes.c_size_t', 'LIMINT':'ctypes.c_int', 'LIMBOOL':'ctypes.c_int', 'LIMRESULT':'ctypes.c_int', 'double':'ctypes.c_double', 'double*':'ctypes.POINTER(ctypes.c_double)', 'LIMFILEHANDLE':'ctypes.c_int', 'LIMATTRIBUTES*':'ctypes.POINTER(LIMATTRIBUTES)', 'LIMMETADATA_DESC*':'ctypes.POINTER(LIMMETADATA_DESC)', 'LIMTEXTINFO*':'ctypes.POINTER(LIMTEXTINFO)', 'LIMEXPERIMENT*':'ctypes.POINTER(LIMEXPERIMENT)', 'LIMPICTURE*':'ctypes.POINTER(LIMPICTURE)', 'LIMLOCALMETADATA*':'ctypes.POINTER(LIMLOCALMETADATA)', 'LIMBINARIES*':'ctypes.POINTER(LIMBINARIES)', 'LIMFILEUSEREVENT*':'ctypes.POINTER(LIMFILEUSEREVENT)'}

# for line in file:
	# linearray = re.split("[\t\n, ();]+", line)
	# if len(linearray) < 3:
		# continue
	# elif linearray[0] == 'LIMFILEAPI':
		# for _ in range(linearray.count('const')):
			# linearray.remove('const')
		# for i in range(3, len(linearray) -1 , 2):
			# if linearray[i] not in ('void*', 'LIMWCHAR', 'LIMWSTR', 'LIMCWSTR', 'LIMUINT', 'LIMUINT*', 'LIMSIZE', 'LIMINT', 'LIMBOOL', 'LIMRESULT', 'double', 'double*', 'LIMFILEHANDLE', 'LIMATTRIBUTES*', 'LIMMETADATA_DESC*', 'LIMTEXTINFO*', 'LIMEXPERIMENT*', 'LIMPICTURE*', 'LIMLOCALMETADATA*', 'LIMBINARIES*', 'LIMFILEUSEREVENT*'):
				# print(f'arg: {linearray[i]}')
		# if linearray[1] not in ('void', 'LIMUINT', 'LIMINT', 'LIMRESULT', 'LIMFILEHANDLE', 'LIMSIZE'):
			# print(f'res: {linearray[1]}')
		# text = f'\t#{line}'
		# file_write.write(text)
		# text = f'\t{linearray[2]} = nd2.{linearray[2]}\n'
		# file_write.write(text)
		# text = f'\t{linearray[2]}.argtypes = ['
		# for i in range(3, len(linearray) -3 , 2):
			# text = f'{text}{arg[linearray[i]]}, '
		# text = f'{text}{arg[linearray[len(linearray) - 3]]}]\n'
		# file_write.write(text)
		# text = f'\t{linearray[2]}.restype = {res[linearray[1]]}\n'
		# file_write.write(text)

# file.close()
# file_write.close()

import ctypes
import os
import sys

os.environ["PATH"] += ';Libraries\\ND2SDK'
nd2 = ctypes.windll.LoadLibrary('v6_w32_nd2ReadSDK.dll')

LIMMAXBINARIES = 128
LIMMAXPICTUREPLANES = 256
LIMMAXEXPERIMENTLEVEL = 8
LIMSTRETCH_QUICK = 1
LIMSTRETCH_SPLINES = 2
LIMSTRETCH_LINEAR = 3

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
		  -19: 'LIM_ERR_VERSION'}

LIMLOOP = {0: 'LIMLOOP_TIME',
		   1: 'LIMLOOP_MULTIPOINT',
		   2: 'LIMLOOP_Z',
		   3: 'LIMLOOP_OTHER'}

class LIMPICTURE(ctypes.Structure):
	_fields_ = [('uiWidth', ctypes.c_uint),
				('uiHeight', ctypes.c_uint),
				('uiBitsPerComp', ctypes.c_uint),
				('uiComponents', ctypes.c_uint),
				('uiWidthBytes', ctypes.c_uint),
				('uiSize', ctypes.c_size_t),
				('pImageData', ctypes.c_void_p)]

class LIMBINARYDESCRIPTOR(ctypes.Structure):
	_fields_ = [('wszName', ctypes.c_wchar * 256),
				('wszCompName', ctypes.c_wchar * 256),
				('uiColorRGB', ctypes.c_uint)]

class LIMBINARIES(ctypes.Structure):
	_fields_ = [('uiCount', ctypes.c_uint),
				('pDescriptors', LIMBINARYDESCRIPTOR * LIMMAXBINARIES)]

class LIMPICTUREPLANE_DESC(ctypes.Structure):
	_fields_ = [('uiCompCount', ctypes.c_uint), # Number of physical components
				('uiColorRGB', ctypes.c_uint), # RGB color for display
				('wszName', ctypes.c_wchar * 256), # Name for display
				('wszOCName', ctypes.c_wchar * 256), # Name of the Optical Configuration
				('dEmissionWL', ctypes.c_double)]

class LIMMETADATA_DESC(ctypes.Structure):
	_fields_ = [('dTimeStart', ctypes.c_double), # Absolute Time in JDN
				('dAngle', ctypes.c_double), # Camera Angle
				('dCalibration', ctypes.c_double), #um/px (0.0 = uncalibrated)
				('dAspect', ctypes.c_double), # pixel aspect (always 1.0)
				('wszObjectiveName', ctypes.c_wchar * 256),
				('dObjectiveMag', ctypes.c_double), # Optional additional information
				('dObjectiveNA', ctypes.c_double), # dCalibration takes into accont all these
				('dRefractIndex1', ctypes.c_double),
				('dRefractIndex2', ctypes.c_double),
				('dPinholeRadius', ctypes.c_double),
				('dZoom', ctypes.c_double),
				('dProjectiveMag', ctypes.c_double),
				('uiImageType', ctypes.c_uint), # 0 (normal), 1 (spectral)
				('uiPlaneCount', ctypes.c_uint), # Number of logical planes (uiPlaneCount <= uiComponentCount)
				('uiComponentCount', ctypes.c_uint), # Number of physical components (same as uiComp in LIMFILEATTRIBUTES)
				('pPlanes', LIMPICTUREPLANE_DESC * LIMMAXPICTUREPLANES)]

class LIMTEXTINFO(ctypes.Structure):
	_fields_ = [('wszImageID', ctypes.c_wchar * 256),
				('wszType', ctypes.c_wchar * 256),
				('wszGroup', ctypes.c_wchar * 256),
				('wszSampleID', ctypes.c_wchar * 256),
				('wszAuthor', ctypes.c_wchar * 256),
				('wszDescription', ctypes.c_wchar * 4096),
				('wszCapturing', ctypes.c_wchar * 4096),
				('wszSampling', ctypes.c_wchar * 256),
				('wszLocation', ctypes.c_wchar * 256),
				('wszDate', ctypes.c_wchar * 256),
				('wszConclusion', ctypes.c_wchar * 256),
				('wszInfo1', ctypes.c_wchar * 256),
				('wszInfo2', ctypes.c_wchar * 256),
				('wszOptics', ctypes.c_wchar * 256),
				('wszAppVersion', ctypes.c_wchar * 256)]

class LIMEXPERIMENTLEVEL(ctypes.Structure):
	_fields_ = [('uiExpType', ctypes.c_uint),  # see LIMLOOP_TIME etc.
				('uiLoopSize', ctypes.c_uint),  # Number of images in the loop
				('dInterval', ctypes.c_double)]  # ms (for Time), um (for ZStack), -1.0 (for Multipoint)

class LIMEXPERIMENT(ctypes.Structure):
	_fields_ = [('uiLevelCount', ctypes.c_uint),
				('pAllocatedLevels', LIMEXPERIMENTLEVEL * LIMMAXEXPERIMENTLEVEL)]

class LIMLOCALMETADATA(ctypes.Structure):
	_fields_ = [('dTimeMSec', ctypes.c_double),
				('dXPos', ctypes.c_double),
				('dYPos', ctypes.c_double),
				('dZPos', ctypes.c_double)]

class LIMATTRIBUTES(ctypes.Structure):
	_fields_ = [('uiWidth', ctypes.c_uint),  # Width of images
				('uiWidthBytes', ctypes.c_uint),  # Line length 4-byte aligned
				('uiHeight', ctypes.c_uint),  # Height if images
				('uiComp', ctypes.c_uint),  # Number of components
				('uiBpcInMemory', ctypes.c_uint),  # Bits per component 8, 16 or 32 (for float image)
				('uiBpcSignificant', ctypes.c_uint),  # Bits per component used 8 .. 16 or 32 (for float image)
				('uiSequenceCount', ctypes.c_uint),  # Number of images in the sequence
				('uiTileWidth', ctypes.c_uint),  # If an image is tiled size of the tile/strip 
				('uiTileHeight', ctypes.c_uint),  # otherwise both zero 
				('uiCompression', ctypes.c_uint),  # 0 (lossless), 1 (lossy), 2 (None)
				('uiQuality', ctypes.c_uint)]  # 0 (worst) - 100 (best)

class LIMFILEUSEREVENT(ctypes.Structure):
	_fields_ = [('uiID', ctypes.c_uint),
				('dTime', ctypes.c_double),
				('wsType', ctypes.c_wchar * 128),
				('wsDescription', ctypes.c_wchar * 256)]

#LIMFILEAPI LIMFILEHANDLE   Lim_FileOpenForRead(LIMCWSTR wszFileName);
Lim_FileOpenForRead = nd2.Lim_FileOpenForRead
Lim_FileOpenForRead.argtypes = [ctypes.c_wchar_p]
Lim_FileOpenForRead.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_FileGetAttributes(LIMFILEHANDLE hFile, LIMATTRIBUTES* pFileAttributes);
Lim_FileGetAttributes = nd2.Lim_FileGetAttributes
Lim_FileGetAttributes.argtypes = [ctypes.c_int, ctypes.POINTER(LIMATTRIBUTES)]
Lim_FileGetAttributes.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_FileGetMetadata(LIMFILEHANDLE hFile, LIMMETADATA_DESC* pFileMetadata);
Lim_FileGetMetadata = nd2.Lim_FileGetMetadata
Lim_FileGetMetadata.argtypes = [ctypes.c_int, ctypes.POINTER(LIMMETADATA_DESC)]
Lim_FileGetMetadata.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_FileGetTextinfo(LIMFILEHANDLE hFile, LIMTEXTINFO* pFileTextinfo);
Lim_FileGetTextinfo = nd2.Lim_FileGetTextinfo
Lim_FileGetTextinfo.argtypes = [ctypes.c_int, ctypes.POINTER(LIMTEXTINFO)]
Lim_FileGetTextinfo.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_FileGetExperiment(LIMFILEHANDLE hFile, LIMEXPERIMENT* pFileExperiment);
Lim_FileGetExperiment = nd2.Lim_FileGetExperiment
Lim_FileGetExperiment.argtypes = [ctypes.c_int, ctypes.POINTER(LIMEXPERIMENT)]
Lim_FileGetExperiment.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_FileGetImageData(LIMFILEHANDLE hFile, LIMUINT uiSeqIndex, LIMPICTURE* pPicture, LIMLOCALMETADATA* pImgInfo);
Lim_FileGetImageData = nd2.Lim_FileGetImageData
Lim_FileGetImageData.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.POINTER(LIMPICTURE), ctypes.POINTER(LIMLOCALMETADATA)]
Lim_FileGetImageData.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_FileGetImageRectData(LIMFILEHANDLE hFile, LIMUINT uiSeqIndex, LIMUINT uiDstTotalW, LIMUINT uiDstTotalH, LIMUINT uiDstX, LIMUINT uiDstY, LIMUINT uiDstW, LIMUINT uiDstH, void* pBuffer, LIMUINT uiDstLineSize, LIMINT iStretchMode, LIMLOCALMETADATA* pImgInfo);
Lim_FileGetImageRectData = nd2.Lim_FileGetImageRectData
Lim_FileGetImageRectData.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint, ctypes.c_int, ctypes.POINTER(LIMLOCALMETADATA)]
Lim_FileGetImageRectData.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_FileGetBinaryDescriptors(LIMFILEHANDLE hFile, LIMBINARIES* pBinaries);
Lim_FileGetBinaryDescriptors = nd2.Lim_FileGetBinaryDescriptors
Lim_FileGetBinaryDescriptors.argtypes = [ctypes.c_int, ctypes.POINTER(LIMBINARIES)]
Lim_FileGetBinaryDescriptors.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_FileGetBinary(LIMFILEHANDLE hFile, LIMUINT uiSequenceIndex, LIMUINT uiBinaryIndex, LIMPICTURE* pPicture);
Lim_FileGetBinary = nd2.Lim_FileGetBinary
Lim_FileGetBinary.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(LIMPICTURE)]
Lim_FileGetBinary.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_FileClose(LIMFILEHANDLE hFile);
Lim_FileClose = nd2.Lim_FileClose
Lim_FileClose.argtypes = [ctypes.c_int]
Lim_FileClose.restype = ctypes.c_int
#LIMFILEAPI LIMSIZE		 Lim_InitPicture(LIMPICTURE* pPicture, LIMUINT width, LIMUINT height, LIMUINT bpc, LIMUINT components);
Lim_InitPicture = nd2.Lim_InitPicture
Lim_InitPicture.argtypes = [ctypes.POINTER(LIMPICTURE), ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
Lim_InitPicture.restype = ctypes.c_size_t
#LIMFILEAPI void			Lim_DestroyPicture(LIMPICTURE* pPicture);
Lim_DestroyPicture = nd2.Lim_DestroyPicture
Lim_DestroyPicture.argtypes = [ctypes.POINTER(LIMPICTURE)]
Lim_DestroyPicture.restype = None
#LIMFILEAPI LIMUINT		 Lim_GetSeqIndexFromCoords(LIMEXPERIMENT* pExperiment, LIMUINT* pExpCoords);
Lim_GetSeqIndexFromCoords = nd2.Lim_GetSeqIndexFromCoords
Lim_GetSeqIndexFromCoords.argtypes = [ctypes.POINTER(LIMEXPERIMENT), ctypes.POINTER(ctypes.c_uint)]
Lim_GetSeqIndexFromCoords.restype = ctypes.c_uint
#LIMFILEAPI void			Lim_GetCoordsFromSeqIndex(LIMEXPERIMENT* pExperiment, LIMUINT uiSeqIdx, LIMUINT* pExpCoords);
Lim_GetCoordsFromSeqIndex = nd2.Lim_GetCoordsFromSeqIndex
Lim_GetCoordsFromSeqIndex.argtypes = [ctypes.POINTER(LIMEXPERIMENT), ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)]
Lim_GetCoordsFromSeqIndex.restype = None
#LIMFILEAPI LIMRESULT	   Lim_GetMultipointName(LIMFILEHANDLE hFile, LIMUINT uiPointIdx, LIMWSTR wstrPointName);
Lim_GetMultipointName = nd2.Lim_GetMultipointName
Lim_GetMultipointName.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.c_wchar_p]
Lim_GetMultipointName.restype = ctypes.c_int
#LIMFILEAPI LIMINT		  Lim_GetZStackHome(LIMFILEHANDLE hFile);
Lim_GetZStackHome = nd2.Lim_GetZStackHome
Lim_GetZStackHome.argtypes = [ctypes.c_int]
Lim_GetZStackHome.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_GetLargeImageDimensions(LIMFILEHANDLE hFile, LIMUINT* puiXFields, LIMUINT* puiYFields, double* pdOverlap);
Lim_GetLargeImageDimensions = nd2.Lim_GetLargeImageDimensions
Lim_GetLargeImageDimensions.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_double)]
Lim_GetLargeImageDimensions.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_GetRecordedDataInt(LIMFILEHANDLE hFile, LIMCWSTR wszName, LIMINT uiSeqIndex, LIMINT *piData);
Lim_GetRecordedDataInt = nd2.Lim_GetRecordedDataInt
Lim_GetRecordedDataInt.argtypes = [ctypes.c_int, ctypes.c_wchar_p, ctypes.c_int, ctypes.c_int]
Lim_GetRecordedDataInt.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_GetRecordedDataDouble(LIMFILEHANDLE hFile, LIMCWSTR wszName, LIMINT uiSeqIndex, double* pdData);
Lim_GetRecordedDataDouble = nd2.Lim_GetRecordedDataDouble
Lim_GetRecordedDataDouble.argtypes = [ctypes.c_int, ctypes.c_wchar_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
Lim_GetRecordedDataDouble.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_GetRecordedDataString(LIMFILEHANDLE hFile, LIMCWSTR wszName, LIMINT uiSeqIndex, LIMWSTR wszData);
Lim_GetRecordedDataString = nd2.Lim_GetRecordedDataString
Lim_GetRecordedDataString.argtypes = [ctypes.c_int, ctypes.c_wchar_p, ctypes.c_int, ctypes.c_wchar_p]
Lim_GetRecordedDataString.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_GetNextUserEvent(LIMFILEHANDLE hFile, LIMUINT *puiNextID, LIMFILEUSEREVENT* pEventInfo);
Lim_GetNextUserEvent = nd2.Lim_GetNextUserEvent
Lim_GetNextUserEvent.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.POINTER(LIMFILEUSEREVENT)]
Lim_GetNextUserEvent.restype = ctypes.c_int
#LIMFILEAPI LIMINT		  Lim_GetCustomDataCount(LIMFILEHANDLE hFile);
Lim_GetCustomDataCount = nd2.Lim_GetCustomDataCount
Lim_GetCustomDataCount.argtypes = [ctypes.c_int]
Lim_GetCustomDataCount.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_GetCustomDataInfo(LIMFILEHANDLE hFile, LIMINT uiCustomDataIndex, LIMWSTR wszName, LIMWSTR wszDescription, LIMINT *piType, LIMINT *piFlags);
Lim_GetCustomDataInfo = nd2.Lim_GetCustomDataInfo
Lim_GetCustomDataInfo.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_int, ctypes.c_int]
Lim_GetCustomDataInfo.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_GetCustomDataDouble(LIMFILEHANDLE hFile, LIMINT uiCustomDataIndex, double* pdData);
Lim_GetCustomDataDouble = nd2.Lim_GetCustomDataDouble
Lim_GetCustomDataDouble.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
Lim_GetCustomDataDouble.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_GetCustomDataString(LIMFILEHANDLE hFile, LIMINT uiCustomDataIndex, LIMWSTR wszData, LIMINT *piLength);
Lim_GetCustomDataString = nd2.Lim_GetCustomDataString
Lim_GetCustomDataString.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_wchar_p, ctypes.c_int]
Lim_GetCustomDataString.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_GetStageCoordinates(LIMFILEHANDLE hFile, LIMUINT uiPosCount, LIMUINT* puiSeqIdx, LIMUINT* puiXPos, LIMUINT* puiYPos, double* pdXPos, double *pdYPos, double *pdZPos, LIMINT iUseAlignment);
Lim_GetStageCoordinates = nd2.Lim_GetStageCoordinates
Lim_GetStageCoordinates.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]
Lim_GetStageCoordinates.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_SetStageAlignment(LIMFILEHANDLE hFile, LIMUINT uiPosCount, double* pdXSrc, double* pdYSrc, double* pdXDst, double *pdYDst);
Lim_SetStageAlignment = nd2.Lim_SetStageAlignment
Lim_SetStageAlignment.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
Lim_SetStageAlignment.restype = ctypes.c_int
#LIMFILEAPI LIMRESULT	   Lim_GetAlignmentPoints(LIMFILEHANDLE hFile, LIMUINT* puiPosCount, LIMUINT* puiSeqIdx, LIMUINT* puiXPos, LIMUINT* puiYPos, double *pdXPos, double *pdYPos);
# In this function, the value pdXPos and pdYPos should be arrays, which means the call would return in error
Lim_GetAlignmentPoints = nd2.Lim_GetAlignmentPoints
Lim_GetAlignmentPoints.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
Lim_GetAlignmentPoints.restype = ctypes.c_int




