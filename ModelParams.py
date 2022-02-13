#-----------Model Parametrs---------------------------------------------------

#---1. Soldier pile parameters
#ISecD           >>Depth of I Section 
#ISecB           >>Width of I Section 
#ISecTw          >>Web Thickness of I Section 
#ISecTf          >>Flange Thickness of I Section 
#PileLngt        >>Length of I Section 

#---2. Pipe parameters
#PipeOD          >>Pipe Outer Diameter 
#PipeT           >>Pipe Thickness
#PipeMD          >>Pipe Mid-Diameter
#PipeLngt        >>Pipe Length 

#---3. Cover plate parameters
#CPltH           >>Height of Cover Plate
#CPltB           >>Width of Cover Plate
#CPltT           >>Thickness of Cover Plate

#---4. Wedge plate prameters
#WPltH           >>Height of Wedge plate
#WPltB1          >>Larger Width of Wedge Plate
#WPltB2          >>Smaller Width of Wedge Plate
#WPltT           >>Thickness of Wedge Plate

#---5. Bearing plate parameters
#BPltH           >>Height of Bearing Plate
#BPltB           >>Width of Bearing Plate 
#BPltT           >>Thickness of Bearing Plate

#---6. Anchor parameters
#AnchorD         >>Anchor Diameter
#AnchorL         >>Anchor Length 
#AnchorIA        >>Anchor Inclination Angle
#AnchorPX        >>Anchor Reference Point X Coordinate
#AnchorPY        >>Anchor Reference Point y Coordinate
#AnchorPZ        >>Anchor Reference Point z Coordinate

#-----Abaqus Imports---------------------------------------------------------------------
import sketch                   #Importing all objects of sketch
import part                     #Importing all objects of part
import regionToolset            #Importing Obects of Region() method
import material                 #Imprting material objects
import section                  #Importing section object
import assembly                 #Importing assembly objects
import step                     #Importing step objects
import mesh                     #Importing mesh object
import job                      #Importing job objects
import visualization            #Importing visualization object
from abaqus import *            #Importing ABAQUS Python Modules
from abaqusConstants import *   #Importing ABAQUS Python Constants

#-----Python Imports---------------------------------------------------------------------
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import *
from numpy import *

#-----Geometrrical properties of I section Soldier Pile----------------------------------
#---Soldier pile is assumed to be HP14X73 (metric: HP346x370) 

Tetha45=45*(math.pi)/180 

ISecD=0.346      #Depth of I Section 
ISecB=0.370      #Width of I Section 
ISecTw=0.0128    #Web Thickness of I Section 
ISecTf=0.0128    #Flange Thickness of I Section 
PileLngt=5       #Length of I Section 
PlLftMsh=0.5*PileLngt+0.5
PlRgtMsh=0.5*PileLngt-0.5

#-----Anchor Properties------------------------------------------------------------------

AnchorD=0.61         #Anchor Diameter
AnchorL=10           #Anchor Length 
AnchorIA=30          #Anchor Inclination Angle
AnchorIA=AnchorIA*(math.pi)/180
AnchorCSArea=(math.pi)*(math.pow(AnchorD, 2))/4
AnchorMPX=AnchorL*math.cos(AnchorIA)    #X of Anchor Mid-Point in Part Local Coordinate
AnchorMPY=AnchorL*math.sin(AnchorIA)    #Y of Anchor Mid-Point in Part Local Coordinate
AnchorMPZ=0                             #Z of Anchor Mid-Point in Part Local Coordinate

#In part local coordinate: Z is along the pile length
#Y is along the pile depth and X is along the pile width
AnchorPX=0             #X of Anchor Reference Point in Part Local Coordinate
AnchorPY=0.5*ISecD     #Y of Anchor Reference Point in Part Local Coordinate

#Z of Anchor Reference Point in Part Local Coordinate
AnchorPZ=0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)  

#-----Geometrrical properties of Pipe in the connection----------------------------------

PipeOD=0.219                       #Pipe Outer Diameter 
PipeT=0.0127                       #Pipe Thickness
PipeMD=PipeOD-PipeT                #Pipe Mid-Diameter
PipeLngt=ISecD/math.cos(AnchorIA)  #Pipe Length 

#-----Geometrrical properties of Cover Plate---------------------------------------------

CPltH=0.762      #Height of Cover Plate
CPltB=0.356      #Width of Cover Plate
CPltT=0.019      #Thickness of Cover Plate

#-----Geometrrical properties of Wedge Plate---------------------------------------------

WPltH=0.305    #Height of Wedge plate
WPltB1=0.227   #Larger Width of Wedge Plate
WPltB2=0.051   #Smaller Width of Wedge Plate
WPltT=0.019    #Thickness of Wedge Plate
LWPlt=pow(WPltH**2+(WPltB1-WPltB2)**2,0.5) #Length of Wedge plate

#-----Geometrrical properties of Bearing Plate-------------------------------------------

BPltH=0.305      #Height of Bearing Plate
BPltB=0.219      #Width of Bearing Plate 
BPltT=0.044      #Thickness of Bearing Plate

#-----Anchor Max Resultant Displacement--------------------------------------------------

MaxDisp=0.1

#-----Steel Material Properties

ESteel=200E9              #Elastic modulus of steel in Pa
NuSteel=0.3               #Poison's ration of steel
RhoSteel=7800             #Mass density of steel in Kg/m^3

FyPile=345027465          #Yield stress of Pile in Pa
EyPile=0                  #Yield Plastic strain of Pile
FrPile=891360000          #Rupture stress of Pile in Pa
ErPile=0.177864756793955  #Rupture Plastic strain of Pile

FyPipe=289875120          #Yield stress of Pipe in Pa
EyPipe=0                  #Yield Plastic strain of Pipe
FrPipe=825240000          #Rupture stress of Pipe in Pa
ErPipe=0.178195356793955  #Rupture Plastic strain of Plate

FyPlate=248435790         #Yield stress of Plate in Pa
EyPlate=0                 #Yield Plastic strain of Plate
FrPlate=775560000         #Rupture stress of Plate in Pa
ErPlate=0.178443756793955 #Rupture Plastic strain of Plate











