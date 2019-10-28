# python3 /path/to/file.py /sourcepath /targetpath
import sys
import rasterio
import numpy as np
import os
import matplotlib.pyplot as plt

def phi_func(sourcepath, targetpath, device):

    try:

        # create targetpath if not exist
        os.makedirs(targetpath, exist_ok = True)

        # do calculate phi for dji images
        if device == 'dji':
            with rasterio.open(sourcepath+'/odm_orthophoto.tif') as src:
                band1 = src.read(1)
            with rasterio.open(sourcepath+'/odm_orthophoto.tif') as src:
                band2 = src.read(2)
            # calc ndvi
            np.seterr(divide='ignore', invalid='ignore')
            ndvi = (band1 + band2) / (band2 - band1)

        elif device == "sentera":
            # read original tif
            with rasterio.open(sourcepath+'/odm_orthophoto.tif') as src:
                band1 = src.read(1)
            with rasterio.open(sourcepath+'/odm_orthophoto.tif') as src:
                band2 = src.read(3)
            # calc ndvi
            np.seterr(divide='ignore', invalid='ignore')
            band1   = np.multiply(band1, 0.188)
            band2 = np.multiply(band2, 1.236)
            ndvi = (band2 - band1) / (band2 + band1)
        
        elif device == "agrocam":
            # read original tif
            with rasterio.open(sourcepath+'/odm_orthophoto.tif') as src:
                band1 = src.read(1)
            with rasterio.open(sourcepath+'/odm_orthophoto.tif') as src:
                band2 = src.read(2)
            # calc ndvi
            np.seterr(divide='ignore', invalid='ignore')
            ndvi = (band1 + band2) / (band2 - band1)

        else:
            # log critical - unsupported device
            raise ValueError('unsupported device')
        
        ndvi2 = np.transpose(np.nonzero(np.nan_to_num(ndvi)))
        
        def scale(X, x_min, x_max):
            nom = (X-X.min(axis=0))*(x_max-x_min)
            denom = X.max(axis=0) - X.min(axis=0)
            denom[denom==0] = 1
            return x_min + nom/denom 

        ndvi2 = scale(ndvi2, 0, 1)
        maxi = round(ndvi2.mean()*1.3,1)
        mini = round(ndvi2.mean()*0.3,1)
        #print(maxi,mini) 
        # save ndvi png
        plt.imshow(ndvi, cmap='RdYlGn')
        plt.clim(mini,maxi)
        plt.axis('off')
        plt.savefig(targetpath+'/ndvi.png', bbox_inches="tight")

        # save ndvi npy
        np.save(targetpath+'/ndvi.npy', ndvi)


    except ValueError as e:
        # log critical in phi_func
        # log exception
        return 7 # unsupported device

    except OSError as e:
        # log critical in phi_func
        # log exception
        return 2 # permissions, invalid file names, etc ...

    except Exception as e:
        # log critical in phi_func
        # log exception
        return 254 # unknown exception occured



# arguments
if __name__ == "__main__":
    ret_code = 100
    if (len(sys.argv) == 4):
        try:
            module = sys.argv[0]
            sourcepath = sys.argv[1]
            targetpath = sys.argv[2]
            device = sys.argv[3]

            ret_code = phi_func(sourcepath, targetpath, device)

        except Exception as e:
            # log critical in phi_func
            # log exception
            ret_code = 254 # unknown exception occured
        finally:
            sys.exit(ret_code)
            
    else:
        sys.exit(1) # 1 ~ invalid number of arguments. expected: sourcepath, targetpath, device 

