# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 17:19:12 2018

@author: tanner
"""
import getpass


class FWAS_PATHS():
    def __init__(self):
        self.userSpace=getpass.getuser()        
        if(getpass.getuser() =="tanner"):
            self.userSpace="tanner"
            self.userID=1
            self.generalDataPath = self.generalDataPaths[1]
            self.alertDataPath = self.alertDataPaths[1]
            self.radarColorPath = self.radarColorPaths[1]
        if(getpass.getuser() =="ubuntu"):
            self.userSpace="ubuntu"
            self.userID=0
            self.generalDataPath = self.generalDataPaths[0]
            self.alertDataPath = self.alertDataPaths[0]
            self.radarColorPath = self.radarColorPaths[0]
        else:
            self.userSpace="ubuntu"
            self.userID=0
            self.generalDataPath = self.generalDataPaths[0]
            self.alertDataPath = self.alertDataPaths[0]
            self.radarColorPath = self.radarColorPaths[0]
        
        self.forecastDataPath = self.generalDataPath+"HRRR/grib/"
        self.conusRadarPath = self.generalDataPath+"CONUS_RADAR/"
        self.ncrDataPath = self.generalDataPath+"NCR/"
        self.nexradDataPath = self.generalDataPath+"NEXRAD/"
        self.nifcDataPath = self.generalDataPath+"NIFC/"    
        self.thresholdArchivePath =self. generalDataPath+"threshold_archive/"
        self.wwaDataPath = self.generalDataPath+"WWA/" 
       
       
    userSpace = "ubuntu"
    userID=0
    generalDataPaths = ["/home/ubuntu/fwas_data/",
                   "/home/tanner/src/gitFWAS/FWAS/data/"] 
                   
    alertDataPaths = ["/srv/shiny-server/fwas/data/",
                    "/home/tanner/src/gitFWAS/alert_data/"]
                    
    radarColorPaths = ["/home/ubuntu/src/FWAS/data/colors.csv",
                      "/home/tanner/src/gitFWAS/FWAS/data/colors.csv"]
                      
    generalDataPath = ""
    alertDataPath = ""
    radarColorPath = ""
    forecastDataPath = generalDataPath+"HRRR/grib/"
    conusRadarPath = generalDataPath+"CONUS_RADAR/"
    ncrDataPath = generalDataPath+"NCR/"
    nexradDataPath = generalDataPath+"NEXRAD/"
    nifcDataPath = generalDataPath+"NIFC/"    
    thresholdArchivePath = generalDataPath+"threshold_archive/"
    wwaDataPath = generalDataPath+"WWA/"

            
#    #Paths
#                      
#    #Used in
#    #AlertManager
#    #AlertRemoval
#    #CheckforDupe
#    #RADAR_One      
#    #threshold_archive
#    #WWA_One
#
#    #Used in  
#    #calcTime
#    #HRRR_Fetch
#    #HRRR_Parse                
#    forecastDataPath = generalDataPath+"HRRR/grib/"
#    
#    #Used in:
#    #CONUS_RADAR_Fetch
#    #CONUS_RADAR_Parse
#    #CONUS_RADAR_Run
#    conusRadarPath = generalDataPath+"CONUS_RADAR/"
#  
#    #Used in:
#    #NCR_Fetch
#    ncrDataPath = generalDataPath+"NCR/"
#    
#    #Used in:
#    #NCR_Parse
#
#    
#    #Used in:
#    #NEXRAD_Fetch
#    #NEXRAD_Parse
#    nexradDataPath = generalDataPath+"NEXRAD/"
#    
#    #Used in:
#    #NIFC
#    nifcDataPath = generalDataPath+"NIFC/"    
#    
#    #Used in:
#    #threshold_archive
#    thresholdArchivePath = generalDataPath+"threshold_archive/"
#    
#    #used in:
#    #WWA_*
    wwaDataPath = generalDataPath+"WWA/"
    
    def set_user(self,user):
        self.userSpace=str(user)
        if(user=="ubuntu"):
            self.userID=0
        if(user=="tanner"):
            self.userID=1
    def get_user(self):
        return self.userSpace
        
    def get_alertDataPath(self):
        return self.alertDataPath
    
    def get_forecastDataPath(self):
        return self.forecastDataPath
    
    def get_conusRadarPath(self):
        return self.conusRadarPath
    
    def get_ncrDataPath(self):
        return self.ncrDataPath

    def get_radarColorPath(self):
        return self.radarColorPath

    def get_nexradDataPath(self):
        return self.nexradDataPath
    
    def get_nifcDataPath(self):
        return self.nifcDataPath

    def get_thresholdArchivePath(self):
        return self.thresholdArchivePath
    
    def get_wwaDataPath(self):
        return self.wwaDataPath
