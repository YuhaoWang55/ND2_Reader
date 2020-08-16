from Libraries import nd2dll

import ctypes
import os
import sys
import time
import numpy
import re

class ND2_frame:
	image = None
	x = 0.0 # um
	y = 0.0 # um
	z = 0.0 # um
	t = 0.0 # ms
	
	def __init__(self, image, x, y, z, t):
		self.image = image
		self.x = x
		self.y = y
		self.z = z
		self.t = t
	

class ND2_Reader:
	
	handle = None
	attributes = nd2dll.LIMATTRIBUTES()
	metadata = nd2dll.LIMMETADATA_DESC() # Global metadata, here contains the pixel size, the objective magnification and NA, components color, etc. However those information might be incorrect, there for those feature should be assigned manually.
	experiment = nd2dll.LIMEXPERIMENT()
	textinfo = nd2dll.LIMTEXTINFO() # The exposure time and other important features are contained in 'wszCapturing' and 'wszDescription', however maybe it is more convenient to just record them down. See function print_description.
	binaryinfo = nd2dll.LIMBINARIES()
	puiXFields = ctypes.c_uint(0) # Large Image Dimensions
	puiYFields = ctypes.c_uint(0) # Large Image Dimensions
	pdOverlap = ctypes.c_double(0) # Large Image Dimensions
	zStackHome = ctypes.c_uint(0)
	
	frame_shape = None
	frame_count = 0
	experiment_count = [0, 0, 0, 0]
	pixel_type = numpy.uint16
	# experiment_time = time.gmtime()
	experiment_time = None
	
	def __init__(self, filename):
		# open handle
		self.handle = nd2dll.Lim_FileOpenForRead(filename)
		
		# obtain attributes, metadata, experiment, text, and binary information
		nd2dll.Lim_FileGetAttributes(self.handle, self.attributes)
		nd2dll.Lim_FileGetMetadata(self.handle, self.metadata)
		nd2dll.Lim_FileGetExperiment(self.handle, self.experiment)
		nd2dll.Lim_FileGetTextinfo(self.handle, self.textinfo)
		nd2dll.Lim_FileGetBinaryDescriptors(self.handle, self.binaryinfo)
		nd2dll.Lim_GetLargeImageDimensions(self.handle, self.puiXFields, self.puiYFields, self.pdOverlap)
		# I still don't know what exactly the function Lim_GetAlignmentPoints does, whereas the possible bug has been described in 'nd2dll.py'
		self.zStackHome = ctypes.c_uint(nd2dll.Lim_GetZStackHome(self.handle))
		
		# capture main features
		if self.attributes.uiComp > 1:
			self.frame_shape = (self.attributes.uiHeight, self.attributes.uiWidth, self.attributes.uiComp)
		else:
			self.frame_shape = (self.attributes.uiHeight, self.attributes.uiWidth)
		self.frame_count = self.attributes.uiSequenceCount
		for i in range(self.experiment.uiLevelCount):
			self.experiment_count[self.experiment.pAllocatedLevels[i].uiExpType] = self.experiment.pAllocatedLevels[i].uiLoopSize
		## I should write a check point to calculate if frame_count = Pi(experiment_count[i] != 0)
		self.pixel_type = {8: numpy.uint8, 16: numpy.uint16, 32: numpy.float32}[self.attributes.uiBpcInMemory]
		try:
			self.experiment_time = time.strptime(self.textinfo.wszDate, '%Y/%m/%d  %H:%M:%S')
		except:
			try:
				self.experiment_time = time.strptime(self.textinfo.wszDate, '%m/%d/%Y  %I:%M:%S %p')
			except:
				self.experiment_time = time.strptime( re.split(' ', self.textinfo.wszDate)[2], '%H:%M:%S')
	
	def print_description(self):
		print(self.textinfo.wszCapturing)
		print()
		print(self.textinfo.wszDescription)
	
	def get_frame(self, time, multipoint, z, other):
		# initialize read buffers and metadata
		buf_picture = nd2dll.LIMPICTURE()
		buf_picture_size = nd2dll.Lim_InitPicture(buf_picture, self.attributes.uiWidth, self.attributes.uiHeight, self.attributes.uiBpcInMemory, self.attributes.uiComp)
		buf_metadata = nd2dll.LIMLOCALMETADATA()
		
		array_shape = self.attributes.uiWidth * self.attributes.uiHeight * self.attributes.uiComp
		array_size = {8: ctypes.c_uint8, 16: ctypes.c_uint16, 32: ctypes.c_float}[self.attributes.uiBpcInMemory] * array_shape
		
		seq_index = nd2dll.Lim_GetSeqIndexFromCoords(self.experiment, (ctypes.c_uint * 4)(time, multipoint, z, other))
		# or Lim_GetCoordsFromSeqIndex()
		nd2dll.Lim_FileGetImageData(self.handle, seq_index, buf_picture, buf_metadata)
		
		image = numpy.ndarray(self.frame_shape, self.pixel_type, array_size.from_address(buf_picture.pImageData)).copy()
		frame = ND2_frame(image, buf_metadata.dXPos, buf_metadata.dYPos, buf_metadata.dZPos, buf_metadata.dTimeMSec)
		
		# release memory
		nd2dll.Lim_DestroyPicture(buf_picture)
		del image, buf_picture
		
		return(frame)
	
	def close(self):
		if self.handle:
			# self.nd2.Lim_DestroyPicture(self.buf_p)
			nd2dll.Lim_FileClose(self.handle)
			self.handle = None
