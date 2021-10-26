# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 10:26:48 2021

@author: 22007604
"""
import os
import glob

if __name__ == "__main__":
    
    os.chdir(r"E:\Kelp")

    from tools import SAFE2band, raster2array, array2raster, get_origin
    from index import ndvi
    
    wd = r"E:\Kelp\Data"
    year_study = ["2018", "2021"]
    
    os.chdir(wd)
    year_list = glob.glob("*") 
    
    for year in year_list:
        if year in year_study:
            year_fd = os.path.join(wd,year) #fd : folder
            os.chdir(year_fd)
            
            #open image Sentinel-2
            S2_list = glob.glob("*.SAFE")
            print("There are %s Sentinel-2 tiles in %s."%(len(S2_list),year))
            
            for S2_safe in S2_list:
                
                #define .SAFE path name
                SAFE_path = os.path.join(year_fd,S2_safe)
                granule_path = os.path.join(SAFE_path, "GRANULE")
                os.chdir(granule_path)
                geopos = get_origin(SAFE_path)


#%%
                
                #define band path name and open raster
                B4_20m_fn = SAFE2band(SAFE_path, "B04", "20m")
                B4_20m = raster2array(B4_20m_fn)
                
                B7_20m_fn = SAFE2band(SAFE_path, "B07", "20m")
                B7_20m = raster2array(B7_20m_fn)
                
                #apply mask
                
                #compute index and save as TIF raster in result dir
                ndvi_20m = ndvi(B7_20m, B4_20m)
                
                result_path = os.path.join(year_fd, "results")
                
                #define georeference parameters of the tile
                raster_origin = (600000,4600000)
                pixel_width = 10
                pixel_height = 10
                
                if not os.exist(result_path):
                    os.mkdir(result_path)
                os.chdir(result_path)
                array2raster("S2_NDVI.tif", raster_origin, pixel_width,
                             pixel_height, ndvi_20m) 
