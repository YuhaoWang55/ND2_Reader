from Libraries import nd2dll_1_7_4_0 as nd2dll

import ctypes
import os
import sys
import time
import numpy
import re
import ast
import pprint

class ND2_frame:
	image = None
	x = 0.0 # um
	y = 0.0 # um
	z = 0.0 # um
	t = 0.0 # ms
	channel = None # channel name
	
	def __init__(self, image, x, y, z, t, channel):
		self.image = image
		self.x = x
		self.y = y
		self.z = z
		self.t = t
		self.channel = channel
	

class ND2_Reader:
	
	handle = None
	attributes = None
	metadata = None # Global metadata, here contains the pixel size, the objective magnification and NA, components color, etc. However those information might be incorrect, there for those feature should be assigned manually.
	experiment = None
	textinfo = None # The exposure time and other important features are contained in 'wszCapturing' and 'wszDescription', however maybe it is more convenient to just record them down. See function print_description.
	puiXFields = ctypes.c_uint(0) # Large Image Dimensions
	puiYFields = ctypes.c_uint(0) # Large Image Dimensions
	pdOverlap = ctypes.c_double(0) # Large Image Dimensions
	zStackHome = ctypes.c_uint(0)
	
	frame_shape = None
	frame_count = 0
	experiment_count = [0, 0, 0, 0] #[time, multipoint, z, other]
	pixel_type = numpy.uint16
	# experiment_time = time.gmtime()
	experiment_time = None
	
	def __init__(self, filename):
		# open handle
		self.handle = nd2dll.Lim_FileOpenForRead(filename)
		
		# obtain attributes, metadata, experiment, text, and binary information
		attributes = nd2dll.Lim_FileGetAttributes(self.handle).decode()
		self.attributes = ast.literal_eval(attributes)
		metadata = nd2dll.Lim_FileGetMetadata(self.handle).decode()
		metadata = metadata.replace('true', 'True')
		metadata = metadata.replace('false', 'False')
		self.metadata = ast.literal_eval(metadata)
		experiment = nd2dll.Lim_FileGetExperiment(self.handle).decode()
		experiment = experiment.replace('true', 'True')
		experiment = experiment.replace('false', 'False')
		self.experiment = ast.literal_eval(experiment)
		textinfo = nd2dll.Lim_FileGetTextinfo(self.handle).decode()
		self.textinfo = ast.literal_eval(textinfo)
		
		# capture main features
		if self.attributes['componentCount'] > 1:
			self.frame_shape = (self.attributes['heightPx'], self.attributes['widthPx'], self.attributes['componentCount'])
		else:
			self.frame_shape = (self.attributes['heightPx'], self.attributes['widthPx'])
		self.frame_count = self.attributes['sequenceCount']
		for i in range(len(self.experiment)):
			self.experiment_count[self.experiment[i]['nestingLevel']] = self.experiment[i]['count']
		## I should write a check point to calculate if frame_count = Pi(experiment_count[i] != 0)
		self.pixel_type = {8: numpy.uint8, 16: numpy.uint16, 32: numpy.float32}[self.attributes['bitsPerComponentInMemory']]
		try:
			self.experiment_time = time.strptime(self.textinfo['date'], '%Y/%m/%d  %H:%M:%S')
		except:
			try:
				self.experiment_time = time.strptime(self.textinfo['date'], '%m/%d/%Y  %I:%M:%S %p')
			except:
				self.experiment_time = time.strptime( re.split(' ', self.textinfo['date'])[2], '%H:%M:%S')
	
	def print_description(self):
		print(self.textinfo['capturing'])
		print()
		print(self.textinfo['description'])
	
	def get_frame(self, time, multipoint, z, channel, other):
		buf_picture = nd2dll.LIMPICTURE()
		buf_picture_size = nd2dll.Lim_InitPicture(buf_picture, self.attributes['widthPx'], self.attributes['heightPx'], self.attributes['bitsPerComponentInMemory'], self.attributes['componentCount'])
		array_shape = self.attributes['widthPx'] * self.attributes['heightPx'] * self.attributes['componentCount']
		array_size = {8: ctypes.c_uint8, 16: ctypes.c_uint16, 32: ctypes.c_float}[self.attributes['bitsPerComponentInMemory']] * array_shape
		
		seq_index = ctypes.c_uint(0)
		nd2dll.Lim_FileGetSeqIndexFromCoords(self.handle, (ctypes.c_uint * 4)(time, multipoint, z, other), len(self.experiment), seq_index)
		nd2dll.Lim_FileGetImageData(self.handle, seq_index, buf_picture)
		image = numpy.ndarray(self.frame_shape, self.pixel_type, array_size.from_address(buf_picture.pImageData)).copy()
		
		frameMetadata = nd2dll.Lim_FileGetFrameMetadata(self.handle, seq_index).decode()
		frameMetadata = frameMetadata.replace('true', 'True')
		frameMetadata = frameMetadata.replace('false', 'False')
		frameMetadata = ast.literal_eval(frameMetadata)
		metadata = frameMetadata['channels'][channel]
		
		if self.attributes['componentCount'] > 1:
			frame = ND2_frame(image[:,:,channel], metadata['position']['stagePositionUm'][0], metadata['position']['stagePositionUm'][1], metadata['position']['stagePositionUm'][2], metadata['time']['relativeTimeMs'], metadata['channel']['name'])
		else:
			frame = ND2_frame(image, metadata['position']['stagePositionUm'][0], metadata['position']['stagePositionUm'][1], metadata['position']['stagePositionUm'][2], metadata['time']['relativeTimeMs'], metadata['channel']['name'])
		
		# release memory
		nd2dll.Lim_DestroyPicture(buf_picture)
		del image, buf_picture
		
		return(frame)
	
	def print_frame_metadata(self, time, multipoint, z, other):
		seq_index = ctypes.c_uint(0)
		nd2dll.Lim_FileGetSeqIndexFromCoords(self.handle, (ctypes.c_uint * 4)(time, multipoint, z, other), len(self.experiment), seq_index)
		frameMetadata = nd2dll.Lim_FileGetFrameMetadata(self.handle, seq_index).decode()
		frameMetadata = frameMetadata.replace('true', 'True')
		frameMetadata = frameMetadata.replace('false', 'False')
		frameMetadata = ast.literal_eval(frameMetadata)
		for i in range(self.attributes['componentCount']):
			print(f'======CHANNEL - {i}======')
			pprint.pprint(frameMetadata['channels'][i])
	
	def close(self):
		if self.handle:
			# self.nd2.Lim_DestroyPicture(self.buf_p)
			nd2dll.Lim_FileClose(self.handle)
			self.handle = None
