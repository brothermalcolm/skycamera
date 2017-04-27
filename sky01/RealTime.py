#%% Import libraries
import numpy as np
import glob
import os
import datetime as dt
import pvlib
import math
import cv2
import connection

#%% --- Read directory content --- #
Bin_List = glob.glob('RealTime/*.bin')
JPEG_List = glob.glob('RealTime/*.jpeg')

#%% --- Select binary images who haven't been converted as a JPEG image --- #
Bin_List = set([os.path.splitext(x)[0] for x in Bin_List])
JPEG_List = set([os.path.splitext(x)[0] for x in JPEG_List])
Bin_List = sorted(list(Bin_List.difference(JPEG_List)))

#%% --- Read image properties --- #
Longitude,Latitude,Elevation,MeanT,MeanP,I0ref,Period,Factor,Width,Height = \
    [x.split('\t')[0] for x in open('CamSpec.txt').readlines()]
mean_pressure = 1e2 * np.float(MeanP)   # Pressure in Pascals
mean_temperature = np.float(MeanT)      # Temperature in degC

#%% --- Loop over the selected images --- #
for x in Bin_List:
    #%% -- Get Image ID, time info and Day ID -- #
    ImageID = os.path.basename(x)
    posix_time = np.int(ImageID)
    utc_date = dt.datetime.utcfromtimestamp(posix_time)
    local_date = dt.datetime.fromtimestamp(posix_time)
    DayID = (local_date - dt.datetime(1970, 1, 1)).days     # Number of days since epoch time

    #%% MALCOLM: EDIT THIS
    # -- Read data associated to the current image -- #
    connection = connection.getConnection()     # Connect to DB
    cursor = connection.cursor()
    cursor.callproc("sp_join_skyghi", (ImageID))
    InfoLine = cursor.fetchall()
    connection.close()
    print(InfoLine)
    InfoLine[0] = ''

    #%% -- If information are found, process the data -- #
    if InfoLine[0] != '':
        # Get sun position
        solar_position = pvlib.solarposition.get_solarposition(
            utc_date,np.float(Latitude),np.float(Longitude),pressure=mean_pressure, altitude=np.float(Elevation),
            temperature=mean_temperature,delta_t=36.0, raw_spa_output=True)

        # Get extraterrestrial irradiance [W/m2]
        earthsun_distance = pvlib.solarposition.nrel_earthsun_distance(utc_date, delta_t=36.0)  # [Astronomical Units]
        extra_irradiance = np.double(I0ref)/math.pow(earthsun_distance,2)                   # Extraterestrial irradiance

        # Get airmass
        air_mass = pvlib.atmosphere.relativeairmass(solar_position.apparent_zenith, model='kastenyoung1989')

        # Concatenate the results
        solar_data = [solar_position.apparent_zenith[0], solar_position.azimuth[0], extra_irradiance, air_mass[0]]
        solar_data = ['%.4f' % xx for xx in solar_data]                 # reduce the precision of solar_data
        Header = ['Timestamp'] + Header[5:] + ['Solar Zenith Angle [deg]', 'Solar Azimuth Angle [deg]',
                                               'Extra Irradiance [W/m2]', 'Airmass']
        InfoLine = [local_date.strftime('%a, %d %b %Y %H:%M:%S')] + InfoLine[5:-1] + solar_data

        # Save data associated to the current image as text file
        TextData = zip(Header, InfoLine)                                # Combine Header and InfoLine
        TxtFilePath = 'RealTime/' + ImageID + '.txt'
        TxtFileID = open(TxtFilePath, 'w')
        for y in TextData:
            TxtFileID.write('\t'.join(str(s) for s in y) + '\n')
        TxtFileID.close()

        #%% Read the binary image
        Raw = np.fromfile(x + '.bin', dtype='uint16').reshape(np.int(Width), np.int(Height))

        # Convert to RGB image (demosaicing) and get the mean value for each channel
        HRGB = np.double(cv2.cvtColor(Raw, cv2.COLOR_BayerBG2BGR))
        MeanRGB = np.mean(HRGB, axis=(0,1))

        # Convert to gray and get the mean value
        Gray = cv2.cvtColor(Raw,cv2.COLOR_BayerBG2GRAY)
        MeanGray = cv2.mean(Gray)

        # White balance
        WB = MeanGray[0]/MeanRGB
        B = HRGB[:, :, 0] * WB[0]
        G = HRGB[:, :, 1] * WB[1]
        R = HRGB[:, :, 2] * WB[2]
        HRGBwb = cv2.merge((B,G,R))

        # Generate the tonemap image
        #ToneMap = cv2.createTonemapReinhard(gamma=0.8, intensity=+3, light_adapt=0.7)
        ToneMap = cv2.createTonemapReinhard(gamma=0.7, intensity=+3, light_adapt=0.6)
        ToneHRGBwb = ToneMap.process(np.float32(HRGBwb))
        RGB = np.clip(ToneHRGBwb*255, 0, 255).astype('uint8')

        # Apply a Contrast Limited Adaptive Histogram Equalization (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        Bc = clahe.apply(RGB[:, :, 0])
        Gc = clahe.apply(RGB[:, :, 1])
        Rc = clahe.apply(RGB[:, :, 2])
        RGBc = cv2.merge((Bc, Gc, Rc))

        # Save image as JPEG
        cv2.imwrite(x + '.jpeg',RGBc)

        # Display image
        #cv2.imshow(x,RGBc)

#cv2.waitKey(0)
#cv2.destroyAllWindows()

#t = time.time()
#print time.time() - t
