# ND2_Reader for windows only

# New version *nd2reader_1_7_4_0*

## Import library
``` python
from ND2_Reader import nd2reader_1_7_4_0 as nd2reader
```
## Import ND2 file
``` python
filename = 'path\\name'
nd2_file = nd2reader.ND2_Reader(f'{filename}.nd2')
print(f'dimension = {nd2_file.frame_shape} * {nd2_file.experiment_count}')
print(f'recording_time = {nd2_file.experiment_time.tm_hour}:{nd2_file.experiment_time.tm_min}:{nd2_file.experiment_time.tm_sec}, {nd2_file.experiment_time.tm_year}/{nd2_file.experiment_time.tm_mon}/{nd2_file.experiment_time.tm_mday}')
```

## File info
``` python
nd2_file.print_description()
```

## Get an image
``` python
frame = nd2_file.get_frame(time = 0, multipoint = 0, z = 0, other = 0, channel = 0)
image = frame.image
```

## Frame metadata
``` python
nd2_file.print_frame_metadata(time = 0, multipoint = 0, z = 0, other = 0)
```

## Close ND2 file 
``` python
nd2_file.close()
```

# Old version *nd2reader*

## Import library
``` python
from ND2_Reader import nd2reader
```
## Import ND2 file
``` python
filename = 'path\\name.nd2'
nd2_file = nd2reader.ND2_Reader(f'{filename}')
print(f'dimension = {nd2_file.frame_shape} * {nd2_file.experiment_count}')
print(f'recording_time = {nd2_file.experiment_time.tm_hour}:{nd2_file.experiment_time.tm_min}:{nd2_file.experiment_time.tm_sec}, {nd2_file.experiment_time.tm_year}/{nd2_file.experiment_time.tm_mon}/{nd2_file.experiment_time.tm_mday}')
```

## Get images
``` python
t = 0
frame = nd2_file.get_frame(time = t, multipoint = 0, z = 0, other = 0)
image = frame.image
```

## File info
``` python
print(f'{nd2_file.attributes}') # attributes
print(f'{nd2_file.metadata}') # metadata
print(f'{nd2_file.experiment}') # experiment
print(f'{nd2_file.textinfo}') # textinfo
print(f'{nd2_file.binaryinfo}') # binaryinfo
print(f'{nd2_file.puiXFields}') # puiXFields
print(f'{nd2_file.puiYFields}') # puiYFields
print(f'{nd2_file.pdOverlap}') # pdOverlap
print(f'{nd2_file.zStackHome}') # zStackHome
print(f'{nd2_file.frame_shape}') # frame_shape
print(f'{nd2_file.frame_count}') # frame_count
print(f'{nd2_file.experiment_count}') # experiment_count
print(f'{nd2_file.pixel_type}') # pixel_type
print(f'{nd2_file.experiment_time}') # experiment_time
```

## Close ND2 file 
``` python
nd2_file.close()
```
