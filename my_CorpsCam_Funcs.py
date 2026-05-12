# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 10:15:37 2026

@author: sdevo
"""
import datetime
import numpy as np
import requests
import os
import glob

# Based on Brittany Bruder's Matlab & Python CorpsCam Codes for downloading files
# Written by Savannah DeVoe for Python

# # Example usagae:
# station='FrfTower'; # Station Name (in readMe.txt).
# camera='c1';#'cxgeo'; # Camera Number
# itype = 'snap'
# saveDir = 'F:\ORISEPostDoc\Equilibrium_Models\cuspData\mytry_1mContour\ArgusCheck'

# dtime = datetime.datetime(2015,10,8,17,00,00) # NOTE: Time in UTC

# # Generate url and filename
# CorpsCam_url, fname = CorpsCam_urlGenerator(station,camera,itype,dtime)

# # Pull image and save to specific directory
# outfilename = websave_py(f'{saveDir}\{fname}',CorpsCam_url);

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def CorpsCam_urlGenerator(station,camera,itype,t_in):
    base='https://coastalimaging.erdc.dren.mil/'
    
    # Adjust Parameters Based on File itype
    posstype = ['snap','var','timex','bright','dark','rundark']
    
    # If an oblique, the file is a jpg
    if (np.isin(itype,posstype)) and (not camera=='cx'):
        ftype='jpg'
           
    # If a rectified product, it is a tif file
    if camera=='cxgeo': 
        ftype='tif'
    
    tstr1 = f'{t_in.year:04d}_{t_in.month:02d}_{t_in.day:02d}'
    tstr2 = f'{t_in.year:04d}{t_in.month:02d}{t_in.day:02d}T{t_in.hour:02d}{t_in.minute:02d}{t_in.second:02d}Z'
    
    # Build File Name
    fname=f'{tstr2}.{station}.{camera}.{itype}.{ftype}'
    
    ## Build Directory Structure
    # Obliques
    if (ftype=='jpg') and (not camera=='cx'):
        ds=f'{station}/Raw/Obliques/{camera}/{tstr1}/' 
    else:
        ds=f'{station}/Processed/Orthophotos/{camera}/{tstr1}/'

    
    ## Build url
    CHLci_url = f'{base}{ds}{fname}'
    
    return CHLci_url, fname

def websave_py(filename, url, writeemtpy=1):
    """
    Saves content from a web service specified by url to a file.
    Equivalent to MATLAB's websave(filename, url).
    """
    
    writefile = writeemtpy

    try:
        

        # Perform the HTTP GET request to the URL
        response = requests.get(url, stream=True)
        # Raise an exception for bad status codes (e.g., 404 Not Found)
        response.raise_for_status()

        # Open the file in write-binary mode and save the content
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Content successfully saved to {os.path.abspath(filename)}")
        return os.path.abspath(filename)
    except requests.exceptions.RequestException as e:
        if writefile==1:
            print(f"Error downloading the file: {e}. Writing empty image.")
            with open(filename, 'wb') as f:
                pass
        return None
 
def CorpsCam_SaveOneImage_from_EachDay(dt,station,camera,itype,saveDir,hrdefault=17,writeempty=1):
    """
    Download ONE image from the day. Defaults to 170000 UTC unless specified otherwise.
    If that time isn't available, check every hour (150000-220000) on the hour,
    then check every half hour if still no image found.
    If no images at all, will default write an empty file anyways.
    Parameters
    ----------
    dt : datetime for the day you want to pull the image. can have an hr, min, sec.
         this code will remove the HMS and set to hrdefault0000
    station : camera location (e.g., 'FrfTower')
    camera : camera number (e.g., 'c1')
    itype : image type (e.g., 'snap')
    saveDir : string to file output location (e.g., 'O:\\usr\\OutputDir')
    Returns
    -------
    None.
    """
    
    dtime_orig = datetime.datetime(dt.year,dt.month,dt.day,hrdefault,00,00) # UTC... pull photo at noon (or 1 pm)
    # Generate url and filename
    CorpsCam_url_orig, fname_orig = CorpsCam_urlGenerator(station,camera,itype,dtime_orig)
    # Pull image and save to specific directory
    outfilename_orig = websave_py(f'{saveDir}\{fname_orig}',CorpsCam_url_orig,writeempty)
    # if outfilename_orig is None:
    #     break
    outfilename = outfilename_orig
    i=0
    hourloop = [15, 16, 18, 19, 20, 21, 22]
    while (outfilename is None):# and (i<7): # also check other hours of that day
        dtime = datetime.datetime(dt.year,dt.month,dt.day,hourloop[i],00,00)
        # Generate url and filename
        CorpsCam_url, fname = CorpsCam_urlGenerator(station,camera,itype,dtime)
        # Pull image and save to specific directory
        outfilename = websave_py(f'{saveDir}\{fname}',CorpsCam_url,writeempty)
        i+=1
        if i>=7:
            break
    i=0
    hourloop = [15, 16, 17, 18, 19, 20, 21, 22]
    while (outfilename is None):# and (i<8): # if still nothing, check at half hour:
        dtime = datetime.datetime(dt.year,dt.month,dt.day,hourloop[i],30,00)
        # Generate url and filename
        CorpsCam_url, fname = CorpsCam_urlGenerator(station,camera,itype,dtime)
        # Pull image and save to specific directory
        outfilename = websave_py(f'{saveDir}\{fname}',CorpsCam_url,writeempty)
        i+=1
        if i>=8:
            break
        
    # if you wanted timex but it's not available, see if snap is instead:
    if itype=='timex' and outfilename is None:
         i=0
         hourloop = [15, 16, 18, 19, 20, 21, 22]
         while (outfilename is None):# and (i<7): # also check other hours of that day
             dtime = datetime.datetime(dt.year,dt.month,dt.day,hourloop[i],00,00)
             # Generate url and filename
             CorpsCam_url, fname = CorpsCam_urlGenerator(station,camera,'snap',dtime)
             # Pull image and save to specific directory
             outfilename = websave_py(f'{saveDir}\{fname}',CorpsCam_url,writeempty)
             i+=1
             if i>=7:
                 break
             
         i=0
         hourloop = [15, 16, 17, 18, 19, 20, 21, 22]
         while (outfilename is None):# and (i<8): # if still nothing, check at half hour:
             dtime = datetime.datetime(dt.year,dt.month,dt.day,hourloop[i],30,00)
             # Generate url and filename
             CorpsCam_url, fname = CorpsCam_urlGenerator(station,camera,'snap',dtime)
             # Pull image and save to specific directory
             outfilename = websave_py(f'{saveDir}\{fname}',CorpsCam_url,writeempty)
             i+=1
             if i>=8:
                 break
            
    # delete the other empty files except:
    if (outfilename_orig is None):
        if (outfilename is None): # the original 170000 timestamp one if we couldn't find any images that day
            filekeep = f'{saveDir}\{fname_orig}'
        else: # OR keep the last file (the good file) we found:
            filekeep = outfilename
    else:
        filekeep = outfilename_orig
        
    prefix = f"{saveDir}"
    # Pattern to match all files starting with "test_file_" in the current directory
    pattern = f"{prefix}\{dt.year:04d}{dt.month:02d}{dt.day:02d}*" 
    # Get a list of all files matching the pattern
    files_to_delete = glob.glob(pattern)
    
    # Iterate over the list of files and delete each one
    for file_path in files_to_delete:
        if not file_path==filekeep:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e.strerror}")