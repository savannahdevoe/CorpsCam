# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 16:26:36 2026

@author: sdevo

Pulling ARGUS images from days where cusps have been IDd on beach using
spectral threshold methodology from O'Dea & Brodie (2022)

"""
import pickle
import datetime

from my_CorpsCam_Funcs import CorpsCam_SaveOneImage_from_EachDay

#%% First load datetime array of days when we have cusps identified on the beach

# # (File Origin - cuspProcessing.py)    
cuspTimePickle = ('F:\\ORISEPostDoc\\Equilibrium_Models\\cuspData\\mytry_1mContour\\4-100mfilter\\unique_cuspTimes2015-2026_1m_contour_4-100mFilt.pickle')

with open(cuspTimePickle,"rb") as f:
    dailyCuspTimes = pickle.load(f)        
    
# # Save directory for ARGUS images:
saveDir = r'F:\ORISEPostDoc\Equilibrium_Models\cuspData\mytry_1mContour\4-100mfilter\ArgusCheck'

#%% Download north-facing camera timex image on days we have cusps

station='FrfTower'; # Station Name (in readMe.txt).
camera='c1';#'cxgeo'; # Camera Number
itype = 'timex'
for dt in dailyCuspTimes:
    dt = datetime.datetime(dt.year,dt.month,dt.day,17,00,00) # UTC... pull photo at noon (or 1 pm depending on EDT/EST)
    CorpsCam_SaveOneImage_from_EachDay(dt,station,camera,itype,saveDir,hrdefault=17,writeempty=1)


