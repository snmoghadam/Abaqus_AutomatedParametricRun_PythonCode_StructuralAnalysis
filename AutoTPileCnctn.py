#-----------------------------------------------------------------------------
#Parametric ABAQUS Model of Anchored Pile with Through Pile Connection
#-----------------------------------------------------------------------------
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

#---6. Anchor parameters
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

#-----Section Properties-----------------------------------------------------------------
HPSecNM=np.array(
[["HP18X204"],
["HP18X181"],
["HP18X157"],
["HP18X135"],
["HP16X183"],
["HP16X162"],
["HP16X141"],
["HP16X121"],
["HP16X101"],
["HP16X88"],
["HP14X117"],
["HP14X102"],
["HP14X89"],
["HP14X73"],
["HP12X89"],
["HP12X84"],
["HP12X74"],
["HP12X63"],
["HP12X53"],
["HP10X57"],
["HP10X42"],
["HP8X36"]])

HPSecDF=np.array(
[[0.46482,0.45974,0.028702,0.028702],
[0.4572,0.4572,0.0254,0.0254],
[0.44958,0.45466,0.022098,0.022098],
[0.4445,0.45212,0.01905,0.01905],
[0.4191,0.41402,0.028702,0.028702],
[0.41402,0.40894,0.0254,0.0254],
[0.4064,0.4064,0.022225,0.022225],
[0.40132,0.40386,0.01905,0.01905],
[0.3937,0.40132,0.015875,0.015875],
[0.38862,0.39878,0.013716,0.013716],
[0.36068,0.37846,0.020447,0.020447],
[0.3556,0.37592,0.017907,0.017907],
[0.35052,0.37338,0.015621,0.015621],
[0.34544,0.37084,0.012827,0.012827],
[0.31496,0.31242,0.018288,0.018288],
[0.31242,0.31242,0.017399,0.017399],
[0.30734,0.30988,0.015367,0.015494],
[0.30226,0.30734,0.013081,0.013081],
[0.29972,0.3048,0.011049,0.011049],
[0.253746,0.25908,0.014351,0.014351],
[0.24638,0.25654,0.010541,0.010668],
[0.203708,0.207264,0.011303,0.011303]])

PipeSecNM=np.array(
[["Pipe8Std"],
["Pipe10Std"],
["Pipe12Std"],
["Pipe8XStrong"],
["Pipe10XStrong"],
["Pipe12XStrong"],
["Pipe8XXStrong"]])

PipeSecDF=np.array(
[[0.219202,0.00762],
[0.27432,0.008636],
[0.32512,0.0088646],
[0.219202,0.011811],
[0.27432,0.011811],
[0.32512,0.011811],
[0.219202,0.0207264]])

#-------------Loop over the sections-----------------------------------------------------

for iHSec in range(0,22,1):
 for iPSec in range(0,7,1):
 
  #-----Geometrrical properties of I section Soldier Pile----------------------------------
  #---Soldier pile is assumed to be HP14X73 (metric: HP346x370) 

  Tetha45=45*(math.pi)/180 

  ISecD=HPSecDF[iHSec][0]     #Depth of I Section 
  ISecB=HPSecDF[iHSec][1]     #Width of I Section 
  ISecTw=HPSecDF[iHSec][2]    #Web Thickness of I Section 
  ISecTf=HPSecDF[iHSec][3]    #Flange Thickness of I Section 
  PileLngt=5              #Length of I Section 
  PlLftMsh=0.5*PileLngt+0.5
  PlRgtMsh=0.5*PileLngt-0.5

  #-----Anchor Properties------------------------------------------------------------------

  AnchorIA=30          #Anchor Inclination Angle
  AnchorIA=AnchorIA*(math.pi)/180

  #In part local coordinate: Z is along the pile length
  #Y is along the pile depth and X is along the pile width
  AnchorPX=0             #X of Anchor Reference Point in Part Local Coordinate
  AnchorPY=0.5*ISecD     #Y of Anchor Reference Point in Part Local Coordinate

  #Z of Anchor Reference Point in Part Local Coordinate
  AnchorPZ=0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)  

  #-----Geometrrical properties of Pipe in the connection----------------------------------

  PipeOD=PipeSecDF[iPSec][0]             #Pipe Outer Diameter 
  PipeT=PipeSecDF[iPSec][1]              #Pipe Thickness
  PipeMD=PipeOD-PipeT                #Pipe Mid-Diameter
  PipeLngt=ISecD/math.cos(AnchorIA)  #Pipe Length 
  
  #-------------Geometrical Condition for Pipe---------------------------------------------
  
  if (0.5*(ISecB-PipeOD))>(ISecB/8):

   #-----Anchor Max Resultant Displacement--------------------------------------------------

   MaxDisp=0.1

   #-----Steel Material Properties

   ESteel=200E9              #Elastic modulus of steel in Pa
   NuSteel=0.3               #Poison's ration of steel
   RhoSteel=7800             #Mass density of steel in Kg/m^3

   FyPile=345027465          #Yield stress of Pile in Pa
   EyPile=0                  #Yield Plastic strain of Pile

   FyPipe=289875120          #Yield stress of Pipe in Pa
   EyPipe=0                  #Yield Plastic strain of Pipe

   #-----Mesh Size---------------------------------------------------------------
   OvrMeshSiz=0.01
   HoleSegSize=0.008
   HoleTBSgmntNo=math.trunc((PipeMD*math.pi)/(4*HoleSegSize))
   HoleWSgmntNo=math.trunc(ISecD/(OvrMeshSiz*math.cos(AnchorIA)))

   #----------1. Clear Display---------------------------------------------------
   #Clear ABAQUS viewport display
   session.viewports['Viewport: 1'].setValues(displayedObject=None)

   #-------------2. Model Creation-----------------------------------------------

   #changeKey() method is used to change the name of model
   #mdb is used to access the model database
   #the default model name is 'Model-1' which will be changed to TPileCnctnModel
   ModelName=HPSecNM[iHSec][0]+PipeSecNM[iPSec][0]

   #mdb.models.changeKey(fromName='Model-1', toName=ModelName)
   mdb.Model(name=ModelName, modelType=STANDARD_EXPLICIT)
   TPileCnctnModel=mdb.models[ModelName]

   #-------------3. Part Creation------------------------------------------------

   #ConstrainedSketch() method is used to access to Line() and Rectangle() methods, and etc.
   #giving a value to 'sheetSize' sets the sheet size

   #---Parts to be defined:
   #1. Soldier Pile (SldrPilePart)
   #2. Pipe (PipePart)

   #---1. Soldier Pile part

   #Sketch of Sodier Pile I section
   SldrPileSecSketch=TPileCnctnModel.ConstrainedSketch(name='SldrPileSecSketch',sheetSize=10)

   SldrPileSecPnts=((0,-0.5*ISecD), (0,0.5*ISecD),
   (-0.5*ISecB,-0.5*ISecD), (0.5*ISecB,-0.5*ISecD),
   (-0.5*ISecB,0.5*ISecD), (0.5*ISecB,0.5*ISecD))

   for i in range(0,len(SldrPileSecPnts)-1,2):
    SldrPileSecSketch.Line(point1=SldrPileSecPnts[i] , point2=SldrPileSecPnts[i+1])

   #part() method is used to create part
   #THREE_D is a symbolic constant
   #BaseSolidExtrude() method is used to create feature object based on our sketch
   #The depth value is the extrusion length (by defalt along z axis)

   #Soldier Pile Part Creation
   SldrPilePart=TPileCnctnModel.Part(name='SldrPilePart',
   dimensionality=THREE_D, type=DEFORMABLE_BODY)
   SldrPilePart.BaseShellExtrude(sketch=SldrPileSecSketch, depth=PileLngt)

   #Through Pile Connection Hole

   SldrPileDatumPnts=((AnchorPX,AnchorPY,AnchorPZ), 
   (AnchorPX,AnchorPY+1/math.tan(AnchorIA),AnchorPZ+1),
   (AnchorPX,AnchorPY+1/math.tan(AnchorIA)+0.5*PipeMD*math.sin(AnchorIA),AnchorPZ+1-0.5*PipeMD*math.cos(AnchorIA)),
   (AnchorPX,AnchorPY+math.tan(AnchorIA),AnchorPZ-1),
   (0,0,PlLftMsh),
   (0,0,PlRgtMsh),
   (0.5*ISecB,0.5*ISecD,PlLftMsh+0.5*ISecD*math.tan(AnchorIA)),
   (-0.5*ISecB,0.5*ISecD,PlLftMsh+0.5*ISecD*math.tan(AnchorIA)),
   (0.5*ISecB,-0.5*ISecD,PlLftMsh-0.5*ISecD*math.tan(AnchorIA)),
   (-0.5*ISecB,-0.5*ISecD,PlLftMsh-0.5*ISecD*math.tan(AnchorIA)),
   (0.5*ISecB,0.5*ISecD,PlRgtMsh+0.5*ISecD*math.tan(AnchorIA)),
   (-0.5*ISecB,0.5*ISecD,PlRgtMsh+0.5*ISecD*math.tan(AnchorIA)),
   (0.5*ISecB,-0.5*ISecD,PlRgtMsh-0.5*ISecD*math.tan(AnchorIA)),
   (-0.5*ISecB,-0.5*ISecD,PlRgtMsh-0.5*ISecD*math.tan(AnchorIA)),
   (0.5*ISecB,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)),
   (-0.5*ISecB,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)),
   (0.5*ISecB,-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)),
   (-0.5*ISecB,-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)),)

   SldrPilePart.DatumPointByCoordinate(coords=SldrPileDatumPnts[0]) #Datum2
   SldrPilePart.DatumPointByCoordinate(coords=SldrPileDatumPnts[1]) #Datum3
   SldrPilePart.DatumPointByCoordinate(coords=SldrPileDatumPnts[2]) #Datum4
   SldrPileDatums= SldrPilePart.datums
   SldrPilePart.DatumAxisByTwoPoint(point1=SldrPileDatums[2], point2=SldrPileDatums[3])    #Datum5
   SldrPilePart.DatumAxisByTwoPoint(point1=SldrPileDatums[3], point2=SldrPileDatums[4])    #Datum6
   SldrPileDatums= SldrPilePart.datums
   SldrPilePart.DatumPlaneByPointNormal(point=SldrPileDatums[3], normal=SldrPileDatums[5]) #Datum7
   SldrPileDatums= SldrPilePart.datums
   SldrPilePart.DatumPointByCoordinate(coords=SldrPileDatumPnts[3])                        #Datum8
   SldrPilePart.DatumPointByCoordinate(coords=SldrPileDatumPnts[4])                        #Datum9
   SldrPilePart.DatumPointByCoordinate(coords=SldrPileDatumPnts[5])                        #Datum10
   SldrPileDatums= SldrPilePart.datums
   SldrPilePart.DatumAxisByTwoPoint(point1=SldrPileDatums[2], point2=SldrPileDatums[8])    #Datum11
   SldrPileDatums= SldrPilePart.datums
   SldrPilePart.DatumPlaneByPointNormal(point=SldrPileDatums[9], normal=SldrPileDatums[11]) #Datum12
   SldrPilePart.DatumPlaneByPointNormal(point=SldrPileDatums[10], normal=SldrPileDatums[11]) #Datum13
   SldrPilePart.DatumPlaneByPointNormal(point=SldrPileDatums[2], normal=SldrPileDatums[11]) #Datum14
   SldrPilePart.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.0)               #Datum15 
   SldrPilePart.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.5+PlLftMsh+0.5*ISecD*math.tan(AnchorIA))       #Datum16
   SldrPilePart.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=-0.5+PlRgtMsh-0.5*ISecD*math.tan(AnchorIA))      #Datum17
   SldrPileDatums= SldrPilePart.datums

   TPileHoleSecTrns = SldrPilePart.MakeSketchTransform(sketchPlane=SldrPileDatums[7], sketchUpEdge=SldrPileDatums[6], 
       sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=SldrPileDatumPnts[1])
   TPileHoleSecSketch = TPileCnctnModel.ConstrainedSketch(name='TPileHoleSecSketch',
           sheetSize=10, transform=TPileHoleSecTrns)
   TPileHoleSecSketch.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, 0.5*PipeMD))
   SldrPilePart.CutExtrude(sketchPlane=SldrPileDatums[7], sketchUpEdge=SldrPileDatums[6], sketchPlaneSide=SIDE1, 
       sketchOrientation=RIGHT, sketch=TPileHoleSecSketch, flipExtrudeDirection=OFF)

   #Partitioning Pile for meshing

   #Transition

   SldrPileFaces = SldrPilePart.faces
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[4],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[16], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[5],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[17], faces=SldrPileFace)

   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[6],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[16], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[7],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[16], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[8],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[16], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[9],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[16], faces=SldrPileFace)

   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[10],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[17], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[11],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[17], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[12],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[17], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[13],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[17], faces=SldrPileFace)

   #partitioning pile on left and right of pipe

   SldrPileFaces = SldrPilePart.faces
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[4],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[12], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[5],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[13], faces=SldrPileFace)

   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[6],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[12], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[7],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[12], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[8],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[12], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[9],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[12], faces=SldrPileFace)

   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[10],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[13], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[11],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[13], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[12],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[13], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[13],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[13], faces=SldrPileFace)

   #partitioning pile on pipe axis

   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[14],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[14], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[15],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[14], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[16],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[14], faces=SldrPileFace)
   SldrPileFace=SldrPileFaces.findAt((SldrPileDatumPnts[17],))
   SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[14], faces=SldrPileFace)

   #Overal Mesh Size

   SldrPilePart.seedPart(size=OvrMeshSiz, deviationFactor=0.1, minSizeFactor=0.1)

   #---Upper Hole

   SgmntNo=HoleTBSgmntNo

   RefPnt=(0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPileEdge=SldrPileEdges.findAt((RefPnt,))
   SldrPilePart.seedEdgeByNumber(edges=SldrPileEdge, number=SgmntNo, constraint=FIXED)

   RefPnt=(-0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPileEdge=SldrPileEdges.findAt((RefPnt,))
   SldrPilePart.seedEdgeByNumber(edges=SldrPileEdge, number=SgmntNo, constraint=FIXED)

   RefPnt=(0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPileEdge=SldrPileEdges.findAt((RefPnt,))
   SldrPilePart.seedEdgeByNumber(edges=SldrPileEdge, number=SgmntNo, constraint=FIXED)

   RefPnt=(-0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPileEdge=SldrPileEdges.findAt((RefPnt,))
   SldrPilePart.seedEdgeByNumber(edges=SldrPileEdge, number=SgmntNo, constraint=FIXED)

   #---Lower Hole

   SgmntNo=HoleTBSgmntNo

   RefPnt=(0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPileEdge=SldrPileEdges.findAt((RefPnt,))
   SldrPilePart.seedEdgeByNumber(edges=SldrPileEdge, number=SgmntNo, constraint=FIXED)

   RefPnt=(-0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPileEdge=SldrPileEdges.findAt((RefPnt,))
   SldrPilePart.seedEdgeByNumber(edges=SldrPileEdge, number=SgmntNo, constraint=FIXED)

   RefPnt=(0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPileEdge=SldrPileEdges.findAt((RefPnt,))
   SldrPilePart.seedEdgeByNumber(edges=SldrPileEdge, number=SgmntNo, constraint=FIXED)

   RefPnt=(-0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPileEdge=SldrPileEdges.findAt((RefPnt,))
   SldrPilePart.seedEdgeByNumber(edges=SldrPileEdge, number=SgmntNo, constraint=FIXED)

  #---At pipe contact

   SgmntNo=HoleWSgmntNo

   RefPnt=(0,0,0.5*PileLngt+0.5*(PipeMD/math.cos(AnchorIA)))
   SldrPileEdges=SldrPilePart.edges
   SldrPileEdge=SldrPileEdges.findAt((RefPnt,))
   SldrPilePart.seedEdgeByNumber(edges=SldrPileEdge, number=SgmntNo, constraint=FIXED)

   RefPnt=(0,0,0.5*PileLngt-0.5*(PipeMD/math.cos(AnchorIA)))
   SldrPileEdges=SldrPilePart.edges
   SldrPileEdge=SldrPileEdges.findAt((RefPnt,))
   SldrPilePart.seedEdgeByNumber(edges=SldrPileEdge, number=SgmntNo, constraint=FIXED)

   #Mesh part

   SldrPileElmntType = mesh.ElemType(elemCode=S4R, elemLibrary=STANDARD, 
   secondOrderAccuracy=ON, hourglassControl=DEFAULT)

   #SldrPileElmntType = mesh.ElemType(elemCode=S8R, elemLibrary=STANDARD)

   SldrPileFace=SldrPilePart.faces[:]
   SldrPileMeshRgn=(SldrPileFace, )
   SldrPilePart.setElementType(regions=SldrPileMeshRgn, elemTypes=(SldrPileElmntType,))

   SldrPileFace=SldrPilePart.faces[:]
   SldrPilePart.setMeshControls(regions=SldrPileFace, elemShape=QUAD, algorithm=MEDIAL_AXIS)
   #SldrPilePart.setMeshControls(regions=SldrPileFace, technique=STRUCTURED)

   RefPnt=(0,0,0.5*PileLngt+0.5*(PipeMD/math.cos(AnchorIA)))
   SldrPileFaces=SldrPilePart.faces
   SldrPileFace1=SldrPileFaces.findAt((RefPnt,))
   RefPnt=(0,0,0.5*PileLngt-0.5*(PipeMD/math.cos(AnchorIA)))
   SldrPileFaces=SldrPilePart.faces
   SldrPileFace2=SldrPileFaces.findAt((RefPnt,))
   SldrPileFace=SldrPileFace1+SldrPileFace2
   SldrPilePart.setMeshControls(regions=SldrPileFace, algorithm=ADVANCING_FRONT)

   SldrPilePart.generateMesh()

   # Nodes Sets for Contacts

   #Soldier Pile - Pipe Top

   RefPnt=(0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPilePipeTopEdge=SldrPileEdges.findAt((RefPnt,))
   RefPnt=(-0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPilePipeTopEdge=SldrPilePipeTopEdge+SldrPileEdges.findAt((RefPnt,))
   RefPnt=(0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPilePipeTopEdge=SldrPilePipeTopEdge+SldrPileEdges.findAt((RefPnt,))
   RefPnt=(-0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPilePipeTopEdge=SldrPilePipeTopEdge+SldrPileEdges.findAt((RefPnt,))

   SldrPilePart.Set('SldrPilePipeTopEdge',edges=SldrPilePipeTopEdge)
   SldrPilePipeTopEdgeNodes=SldrPilePart.sets['SldrPilePipeTopEdge'].nodes
   SldrPilePart.Set(nodes=SldrPilePipeTopEdgeNodes, name='SldrPilePipeTopEdgeNodes')

   #Soldier Pile - Pipe Bottom

   RefPnt=(0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPilePipeBottomEdge=SldrPileEdges.findAt((RefPnt,))
   RefPnt=(-0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPilePipeBottomEdge=SldrPilePipeBottomEdge+SldrPileEdges.findAt((RefPnt,))
   RefPnt=(0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPilePipeBottomEdge=SldrPilePipeBottomEdge+SldrPileEdges.findAt((RefPnt,))
   RefPnt=(-0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
   SldrPileEdges=SldrPilePart.edges
   SldrPilePipeBottomEdge=SldrPilePipeBottomEdge+SldrPileEdges.findAt((RefPnt,))

   SldrPilePart.Set('SldrPilePipeBottomEdge',edges=SldrPilePipeBottomEdge)
   SldrPilePipeBottomEdgeNodes=SldrPilePart.sets['SldrPilePipeBottomEdge'].nodes
   SldrPilePart.Set(nodes=SldrPilePipeBottomEdgeNodes, name='SldrPilePipeBottomEdgeNodes')

   #Soldier Pile - Pipe Side 1

   RefPnt=(0,0,0.5*PileLngt+0.5*(PipeMD/math.cos(AnchorIA)))
   SldrPileEdges=SldrPilePart.edges
   SldrPileSideEdge1=SldrPileEdges.findAt((RefPnt,))

   SldrPilePart.Set('SldrPileSideEdge1',edges=SldrPileSideEdge1)
   SldrPileSideEdgeNodes1=SldrPilePart.sets['SldrPileSideEdge1'].nodes
   SldrPilePart.Set(nodes=SldrPileSideEdgeNodes1, name='SldrPileSideEdgeNodes1')

   #Soldier Pile - Pipe Side 2

   RefPnt=(0,0,0.5*PileLngt-0.5*(PipeMD/math.cos(AnchorIA)))
   SldrPileEdges=SldrPilePart.edges
   SldrPileSideEdge2=SldrPileEdges.findAt((RefPnt,))

   SldrPilePart.Set('SldrPileSideEdge2',edges=SldrPileSideEdge2)
   SldrPileSideEdgeNodes2=SldrPilePart.sets['SldrPileSideEdge2'].nodes
   SldrPilePart.Set(nodes=SldrPileSideEdgeNodes2, name='SldrPileSideEdgeNodes2')

   #---2. Pipe part

   #Sketch of Pipe section
   PipeSecSketch=TPileCnctnModel.ConstrainedSketch(name='SldrPileSecSketch',sheetSize=10)
   PipeSecSketch.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, 0.5*PipeMD))

   PipePart=TPileCnctnModel.Part(name='PipePart',dimensionality=THREE_D, type=DEFORMABLE_BODY)
   PipePart.BaseShellExtrude(sketch=PipeSecSketch, depth=PipeLngt+PipeMD/math.tan(AnchorIA))

   PipeDatumPnts=((0,0,0.5*PipeMD/math.tan(AnchorIA)), 
   (0,0,PipeLngt+0.5*PipeMD/math.tan(AnchorIA)),
   (0,0.5*PipeMD,0), 
   (0,0.5*PipeMD,PipeLngt),
   (0,0.5*PipeMD,PipeLngt+PipeMD/math.tan(AnchorIA)))

   CordZ0=0.5*PipeMD/math.tan(AnchorIA)

   PipePart.DatumPointByCoordinate(coords=PipeDatumPnts[0]) #Datum2
   PipePart.DatumPointByCoordinate(coords=PipeDatumPnts[1]) #Datum3
   PipePart.DatumPointByCoordinate(coords=PipeDatumPnts[2]) #Datum4
   PipePart.DatumPointByCoordinate(coords=PipeDatumPnts[3]) #Datum5
   PipeDatums= PipePart.datums

   PipePart.DatumAxisByTwoPoint(point1=PipeDatums[2], point2=PipeDatums[4])    #Datum6
   PipePart.DatumAxisByTwoPoint(point1=PipeDatums[3], point2=PipeDatums[5])    #Datum7
   PipeDatums= PipePart.datums

   PipePart.DatumPlaneByPointNormal(point=PipeDatums[2], normal=PipeDatums[6]) #Datum8
   PipePart.DatumPlaneByPointNormal(point=PipeDatums[3], normal=PipeDatums[7]) #Datum9
   PipePart.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0)  #Datum10  
   PipePart.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0)  #Datum11
   PipeDatums= PipePart.datums

   PipeFaces = PipePart.faces
   PipeFace=PipeFaces.findAt((PipeDatumPnts[2],))
   PipePart.PartitionFaceByDatumPlane(datumPlane=PipeDatums[8], faces=PipeFace)
   PipeFaces = PipePart.faces
   PipeFace=PipeFaces.findAt((PipeDatumPnts[3],))
   PipePart.PartitionFaceByDatumPlane(datumPlane=PipeDatums[9], faces=PipeFace)

   PipeFaces = PipePart.faces
   PipeFace=PipeFaces.findAt((PipeDatumPnts[2],))
   PipePart.RemoveFaces(faceList = PipeFace, deleteCells=True)
   PipeFaces = PipePart.faces
   PipeFace=PipeFaces.findAt((PipeDatumPnts[4],))
   PipePart.RemoveFaces(faceList = PipeFace, deleteCells=True)

   #Partitioning Pipe for mesh size setting

   RefPnt=(0,0.5*PipeMD,CordZ0+0.5*PipeLngt)
   PipeFaces = PipePart.faces
   PipeFace=PipeFaces.findAt((RefPnt,))
   PipePart.PartitionFaceByDatumPlane(datumPlane=PipeDatums[10], faces=PipeFace)

   RefPnt=(0.5*PipeMD,0,CordZ0+0.5*PipeLngt)
   PipeFaces = PipePart.faces
   PipeFace=PipeFaces.findAt((RefPnt,))
   PipePart.PartitionFaceByDatumPlane(datumPlane=PipeDatums[11], faces=PipeFace)

   RefPnt=(-0.5*PipeMD,0,CordZ0+0.5*PipeLngt)
   PipeFaces = PipePart.faces
   PipeFace=PipeFaces.findAt((RefPnt,))
   PipePart.PartitionFaceByDatumPlane(datumPlane=PipeDatums[11], faces=PipeFace)

   #Mesh size

   #---Right ellipse

   SgmntNo=HoleTBSgmntNo

   CordX=0.5*PipeMD*math.cos(Tetha45)
   CordY=((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeEdge=PipeEdges.findAt((RefPnt,))
   PipePart.seedEdgeByNumber(edges=PipeEdge, number=SgmntNo, constraint=FIXED)

   CordX=-0.5*PipeMD*math.cos(Tetha45)
   CordY=((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeEdge=PipeEdges.findAt((RefPnt,))
   PipePart.seedEdgeByNumber(edges=PipeEdge, number=SgmntNo, constraint=FIXED)

   CordX=0.5*PipeMD*math.cos(Tetha45)
   CordY=-((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeEdge=PipeEdges.findAt((RefPnt,))
   PipePart.seedEdgeByNumber(edges=PipeEdge, number=SgmntNo, constraint=FIXED)

   CordX=-0.5*PipeMD*math.cos(Tetha45)
   CordY=-((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeEdge=PipeEdges.findAt((RefPnt,))
   PipePart.seedEdgeByNumber(edges=PipeEdge, number=SgmntNo, constraint=FIXED)

   #---Left ellipse

   SgmntNo=HoleTBSgmntNo

   CordX=0.5*PipeMD*math.cos(Tetha45)
   CordY=((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+PipeLngt+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeEdge=PipeEdges.findAt((RefPnt,))
   PipePart.seedEdgeByNumber(edges=PipeEdge, number=SgmntNo, constraint=FIXED)

   CordX=-0.5*PipeMD*math.cos(Tetha45)
   CordY=((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+PipeLngt+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeEdge=PipeEdges.findAt((RefPnt,))
   PipePart.seedEdgeByNumber(edges=PipeEdge, number=SgmntNo, constraint=FIXED)

   CordX=0.5*PipeMD*math.cos(Tetha45)
   CordY=-((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+PipeLngt+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeEdge=PipeEdges.findAt((RefPnt,))
   PipePart.seedEdgeByNumber(edges=PipeEdge, number=SgmntNo, constraint=FIXED)

   CordX=-0.5*PipeMD*math.cos(Tetha45)
   CordY=-((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+PipeLngt+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeEdge=PipeEdges.findAt((RefPnt,))
   PipePart.seedEdgeByNumber(edges=PipeEdge, number=SgmntNo, constraint=FIXED)

   #---Along pipe Axis

   SgmntNo=HoleWSgmntNo

   RefPnt=(0,0.5*PipeMD,CordZ0+0.5*PipeLngt)
   PipeEdges=PipePart.edges
   PipeEdge=PipeEdges.findAt((RefPnt,))
   PipePart.seedEdgeByNumber(edges=PipeEdge, number=SgmntNo, constraint=FIXED)

   RefPnt=(0,-0.5*PipeMD,CordZ0+0.5*PipeLngt)
   PipeEdges=PipePart.edges
   PipeEdge=PipeEdges.findAt((RefPnt,))
   PipePart.seedEdgeByNumber(edges=PipeEdge, number=SgmntNo, constraint=FIXED)

   RefPnt=(0.5*PipeMD,0,CordZ0+0.5*PipeLngt)
   PipeEdges=PipePart.edges
   PipeEdge=PipeEdges.findAt((RefPnt,))
   PipePart.seedEdgeByNumber(edges=PipeEdge, number=SgmntNo, constraint=FIXED)

   RefPnt=(-0.5*PipeMD,0,CordZ0+0.5*PipeLngt)
   PipeEdges=PipePart.edges
   PipeEdge=PipeEdges.findAt((RefPnt,))
   PipePart.seedEdgeByNumber(edges=PipeEdge, number=SgmntNo, constraint=FIXED)

   #Mesh part

   PipeElmntType = mesh.ElemType(elemCode=S4R, elemLibrary=STANDARD, 
   secondOrderAccuracy=ON, hourglassControl=DEFAULT)

   #PipeElmntType = mesh.ElemType(elemCode=S8R, elemLibrary=STANDARD)

   PipeFace=PipePart.faces[:]
   PipeMeshRgn=(PipeFace, )
   PipePart.setElementType(regions=PipeMeshRgn, elemTypes=(PipeElmntType,))

   PipeFace=PipePart.faces[:]
   PipePart.setMeshControls(regions=PipeFace, elemShape=QUAD, algorithm=MEDIAL_AXIS)
   #PipePart.setMeshControls(regions=PipeFace, algorithm=ADVANCING_FRONT)

   PipePart.generateMesh()

   # Nodes Sets for Contacts

   #Soldier Pile - Pipe Bottom

   CordX=0.5*PipeMD*math.cos(Tetha45)
   CordY=((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeBottomEdge=PipeEdges.findAt((RefPnt,))
   CordX=-0.5*PipeMD*math.cos(Tetha45)
   CordY=((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeBottomEdge=PipeBottomEdge+PipeEdges.findAt((RefPnt,))
   CordX=0.5*PipeMD*math.cos(Tetha45)
   CordY=-((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeBottomEdge=PipeBottomEdge+PipeEdges.findAt((RefPnt,))
   CordX=-0.5*PipeMD*math.cos(Tetha45)
   CordY=-((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeBottomEdge=PipeBottomEdge+PipeEdges.findAt((RefPnt,))

   PipePart.Set('PipeBottomEdge',edges=PipeBottomEdge)
   PipeBottomEdgeNodes=PipePart.sets['PipeBottomEdge'].nodes
   PipePart.Set(nodes=PipeBottomEdgeNodes, name='PipeBottomEdgeNodes')

   #Soldier Pile - Pipe Top

   CordX=0.5*PipeMD*math.cos(Tetha45)
   CordY=((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+PipeLngt+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeTopEdge=PipeEdges.findAt((RefPnt,))
   CordX=-0.5*PipeMD*math.cos(Tetha45)
   CordY=((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+PipeLngt+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeTopEdge=PipeTopEdge+PipeEdges.findAt((RefPnt,))
   CordX=0.5*PipeMD*math.cos(Tetha45)
   CordY=-((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+PipeLngt+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeTopEdge=PipeTopEdge+PipeEdges.findAt((RefPnt,))
   CordX=-0.5*PipeMD*math.cos(Tetha45)
   CordY=-((0.5*PipeMD/math.cos(AnchorIA))*math.sin(Tetha45))*math.cos(AnchorIA)
   CordZ=CordZ0+PipeLngt+CordY*math.tan(AnchorIA)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipePart.edges
   PipeTopEdge=PipeTopEdge+PipeEdges.findAt((RefPnt,))

   PipePart.Set('PipeTopEdge',edges=PipeTopEdge)
   PipeTopEdgeNodes=PipePart.sets['PipeTopEdge'].nodes
   PipePart.Set(nodes=PipeTopEdgeNodes, name='PipeTopEdgeNodes')

   #Soldier Pile - Pipe Side 1

   RefPnt=(0,0.5*PipeMD,CordZ0+0.5*PipeLngt)
   PipeEdges=PipePart.edges
   PipeEdgeSide1=PipeEdges.findAt((RefPnt,))

   PipePart.Set('PipeEdgeSide1',edges=PipeEdgeSide1)
   PipeEdgeNodesSide1=PipePart.sets['PipeEdgeSide1'].nodes
   PipePart.Set(nodes=PipeEdgeNodesSide1, name='PipeEdgeNodesSide1')

   #Soldier Pile - Pipe Side 2

   RefPnt=(0,-0.5*PipeMD,CordZ0+0.5*PipeLngt)
   PipeEdges=PipePart.edges
   PipeEdgeSide2=PipeEdges.findAt((RefPnt,))

   PipePart.Set('PipeEdgeSide2',edges=PipeEdgeSide2)
   PipeEdgeNodesSide2=PipePart.sets['PipeEdgeSide2'].nodes
   PipePart.Set(nodes=PipeEdgeNodesSide2, name='PipeEdgeNodesSide2')

   #-------------4. Material Creation--------------------------------------------

   #using Density() and Elastic() objects to set density and elastic 
   #material properties at different tempratures

   PileSteelMaterial=TPileCnctnModel.Material(name='PileSteelMat')
   PileSteelMaterial.Density(table=((RhoSteel, ), ))
   PileSteelMaterial.Elastic(table=((ESteel, NuSteel),))
   PileSteelMaterial.Plastic(table=((FyPile, EyPile),))

   PipeSteelMaterial=TPileCnctnModel.Material(name='PipeSteelMat')
   PipeSteelMaterial.Density(table=((RhoSteel, ), ))
   PipeSteelMaterial.Elastic(table=((ESteel, NuSteel),))
   PipeSteelMaterial.Plastic(table=((FyPipe, EyPipe),))

   #-------------5. Section Creation and Assignment------------------------------

   #---Sections to be defined:
   #1. Soldier Pile (SldrPileSec)
   #2. Pipe (PipeSec)
   #3. Cover Plate (CvrPltSec)
   #4. Wedge Plate (WdgPltSec)
   #5. Bearing Plate (BrngPltSec)
   #6. Anchor (AnchorSec)

   #HomogeneousShellSection() method is used to create shell sections
   #Assigning the created section to Soldier Pile Part
   #A region object is created based on sequence of cells
   #The seqence of cells would be vertex, edge, node or face obects
   #SectionAssignment() method is used for section assignment

   #TrussSection() method is used to create truss sections
   #Assigning the created section to truss members
   #findAt() method finds edges defined by the coordinates of their mid-point
   #or vertices of the edges

   #---1. Soldier Pile Section

   SldrPileSec=TPileCnctnModel.HomogeneousShellSection(
   name='SldrPileSec', material='PileSteelMat', thicknessType=UNIFORM, thickness=ISecTw)

   SldrPileFace=SldrPilePart.faces[:]
   SldrPileRegion = SldrPilePart.Set(faces=SldrPileFace, name='SPSet-Sec')

   SldrPilePart.SectionAssignment(region=SldrPileRegion, sectionName='SldrPileSec', offset=0.0, 
   offsetType=MIDDLE_SURFACE, offsetField='', 
   thicknessAssignment=FROM_SECTION)

   #---2. Pipe Section

   PipeSec=TPileCnctnModel.HomogeneousShellSection(
   name='PipeSec', material='PipeSteelMat', thicknessType=UNIFORM, thickness=PipeT)

   PipeFace=PipePart.faces[:]
   PipeRegion = PipePart.Set(faces=PipeFace, name='PFSet-Sec')

   PipePart.SectionAssignment(region=PipeRegion, sectionName='PipeSec', offset=0.0, 
   offsetType=MIDDLE_SURFACE, offsetField='', 
   thicknessAssignment=FROM_SECTION)

   #-------------6. Assembly and Instance Creation-------------------------------

   #---Model Assembly
   TPileCnctnAssembly=TPileCnctnModel.rootAssembly
   TPileCnctnAssembly.DatumCsysByDefault(CARTESIAN)

   #---SldrPileInstance

   SldrPileInstance=TPileCnctnAssembly.Instance(
   name='SldrPileInstance', part=SldrPilePart, dependent=ON)

   #---PipeInstance

   PipeInstance=TPileCnctnAssembly.Instance(
   name='PipeInstance', part=PipePart, dependent=ON)

   #---Fixing Assembly

   RefCrd=((0,0,0), (1,0,0), (0,1,0), (0,0,1))
   RAngl=90

   TPileCnctnAssembly.translate(instanceList=('PipeInstance', ), 
   vector=(AnchorPX, AnchorPY, AnchorPZ-PipeLngt-0.5*PipeMD/math.tan(AnchorIA)))
   TPileCnctnAssembly.rotate(instanceList=('PipeInstance', ), axisPoint=(AnchorPX,AnchorPY,AnchorPZ), 
   axisDirection=RefCrd[3], angle=2*RAngl)
   TPileCnctnAssembly.rotate(instanceList=('PipeInstance', ), axisPoint=(AnchorPX,AnchorPY,AnchorPZ), 
   axisDirection=RefCrd[1], angle=-2*AnchorIA*180/math.pi)

   #-------------7. Step Creation------------------------------------------------

   #static step is created by StaticStep() method which is used for loading
   #this is the step next to initial step defined by default

   TPileCnctnModel.StaticStep(
   name='LoadStep1', previous='Initial', description='Loading Step')

   mdb.models[ModelName].steps['LoadStep1'].setValues(
   stabilizationMagnitude=0.0002, stabilizationMethod=DAMPING_FACTOR, 
   continueDampingFactors=False, adaptiveDampingRatio=None, 
   initialInc=0.01, minInc=1e-15, maxInc=0.1, nlgeom=ON)

   mdb.models[ModelName].steps['LoadStep1'].control.setValues(
   allowPropagation=OFF, resetDefaultValues=OFF, timeIncrementation=(4.0, 
   8.0, 9.0, 16.0, 10.0, 4.0, 12.0, 15.0, 6.0, 3.0, 50.0))


   #-------------8. Field Output Requests Definition-----------------------------

   #Default field output defined by ABAQUS is 'F-Output-1'
   #The default name is changed and new parameters of interest are defined

   TPileCnctnModel.fieldOutputRequests.changeKey(
   fromName='F-Output-1', toName='FieldOutputs')

   TPileCnctnModel.fieldOutputRequests['FieldOutputs'].setValues(
   variables=('S', 'E', 'PEMAG', 'U', 'RF', 'CF'))

   #-------------9. Apply Loads--------------------------------------------------

   #Load is displacement type and will be applied in bondary condition

   #-------------10. Apply Boundary Condition------------------------------------

   #Contacts
   #TPileCnctnModel.ContactProperty('GeneralContact')
   #TPileCnctnModel.interactionProperties['GeneralContact'].TangentialBehavior(
   #formulation=ROUGH)
   #TPileCnctnModel.interactionProperties['GeneralContact'].NormalBehavior(
   #pressureOverclosure=HARD, allowSeparation=OFF, constraintEnforcementMethod=DEFAULT)

   #TPileCnctnModel.ContactStd(name='OverallContact', createStepName='Initial')
   #TPileCnctnModel.interactions['OverallContact'].includedPairs.setValuesInStep(
   #stepName='Initial', useAllstar=ON)
   #TPileCnctnModel.interactions['OverallContact'].contactPropertyAssignments.appendInStep(
   #stepName='Initial', assignments=((GLOBAL, SELF, 'GeneralContact'), ))

   #Pipe Sodier Pile Contact
   region1=TPileCnctnAssembly.instances['SldrPileInstance'].sets['SldrPileSideEdgeNodes1']
   region2=TPileCnctnAssembly.instances['PipeInstance'].sets['PipeEdgeNodesSide1']
   TPileCnctnModel.Tie(name='SldrPilePipeSideEdge1', master=region1, 
   slave=region2, positionToleranceMethod=SPECIFIED, 
   positionTolerance=0.01, adjust=ON, tieRotations=ON, thickness=ON)

   region1=TPileCnctnAssembly.instances['SldrPileInstance'].sets['SldrPileSideEdgeNodes2']
   region2=TPileCnctnAssembly.instances['PipeInstance'].sets['PipeEdgeNodesSide2']
   TPileCnctnModel.Tie(name='SldrPilePipeSideEdge2', master=region1, 
   slave=region2, positionToleranceMethod=SPECIFIED, 
   positionTolerance=0.01, adjust=ON, tieRotations=ON, thickness=ON)

   region1=TPileCnctnAssembly.instances['SldrPileInstance'].sets['SldrPilePipeTopEdgeNodes']
   region2=TPileCnctnAssembly.instances['PipeInstance'].sets['PipeTopEdgeNodes']
   TPileCnctnModel.Tie(name='SldrPilePipeTop', master=region2, 
   slave=region1, positionToleranceMethod=SPECIFIED, 
   positionTolerance=0.01, adjust=ON, tieRotations=ON, thickness=ON)

   region1=TPileCnctnAssembly.instances['SldrPileInstance'].sets['SldrPilePipeBottomEdgeNodes']
   region2=TPileCnctnAssembly.instances['PipeInstance'].sets['PipeBottomEdgeNodes']
   TPileCnctnModel.Tie(name='SldrPilePipeBottom', master=region2, 
   slave=region1, positionToleranceMethod=SPECIFIED, 
   positionTolerance=0.01, adjust=ON, tieRotations=ON, thickness=ON)

   #Boundary Constraints

   SldrPileEdges = SldrPileInstance.edges

   #Left Boundary Condition

   RefPnt=(0.5*ISecB-ISecTf,0.5*ISecD,PileLngt)
   SldrPileLeftFlngEdge1 = SldrPileEdges.findAt((RefPnt,))
   RefPnt=(-0.5*ISecB+ISecTf,0.5*ISecD,PileLngt)
   SldrPileLeftFlngEdge2 = SldrPileEdges.findAt((RefPnt,))
   RefPnt=(0.5*ISecB-ISecTf,-0.5*ISecD,PileLngt)
   SldrPileLeftFlngEdge3 = SldrPileEdges.findAt((RefPnt,))
   RefPnt=(-0.5*ISecB+ISecTf,-0.5*ISecD,PileLngt)
   SldrPileLeftFlngEdge4 = SldrPileEdges.findAt((RefPnt,))
   RefPnt=(0,0,PileLngt)
   SldrPileLeftWebEdge = SldrPileEdges.findAt((RefPnt,))

   SldrPileLeftEdge=SldrPileLeftFlngEdge1+SldrPileLeftFlngEdge2+SldrPileLeftFlngEdge3
   SldrPileLeftEdge=SldrPileLeftEdge+SldrPileLeftFlngEdge4+SldrPileLeftWebEdge

   SldrPileLeftBoundary = TPileCnctnAssembly.Set(edges=SldrPileLeftEdge, name='SldrPileLeftBoundary')

   TPileCnctnModel.DisplacementBC(name='LeftBndrCndtn', 
   createStepName='Initial', region=SldrPileLeftBoundary, u1=SET, u2=SET, u3=SET, 
   ur1=SET, ur2=SET, ur3=SET, amplitude=UNSET, distributionType=UNIFORM, 
   fieldName='', localCsys=None)

   #Right Boundary Condition

   RefPnt=(0.5*ISecB-ISecTf,0.5*ISecD,0)
   SldrPileRightFlngEdge1 = SldrPileEdges.findAt((RefPnt,))
   RefPnt=(-0.5*ISecB+ISecTf,0.5*ISecD,0)
   SldrPileRightFlngEdge2 = SldrPileEdges.findAt((RefPnt,))
   RefPnt=(0.5*ISecB-ISecTf,-0.5*ISecD,0)
   SldrPileRightFlngEdge3 = SldrPileEdges.findAt((RefPnt,))
   RefPnt=(-0.5*ISecB+ISecTf,-0.5*ISecD,0)
   SldrPileRightFlngEdge4 = SldrPileEdges.findAt((RefPnt,))
   RefPnt=(0,0,0)
   SldrPileRightWebEdge = SldrPileEdges.findAt((RefPnt,))

   SldrPileRightEdge=SldrPileRightFlngEdge1+SldrPileRightFlngEdge2+SldrPileRightFlngEdge3
   SldrPileRightEdge=SldrPileRightEdge+SldrPileRightFlngEdge4+SldrPileRightWebEdge

   SldrPileRightBoundary = TPileCnctnAssembly.Set(edges=SldrPileRightEdge, name='SldrPileRightBoundary')

   TPileCnctnModel.DisplacementBC(name='RightBndrCndtn', 
   createStepName='Initial', region=SldrPileRightBoundary, u1=SET, u2=SET, u3=SET, 
   ur1=SET, ur2=SET, ur3=SET, amplitude=UNSET, distributionType=UNIFORM, 
   fieldName='', localCsys=None)

   #Anchor Displacement Load

   CordX=0.5*PipeMD*math.sin(Tetha45)
   CordY=AnchorPY
   CordZ=AnchorPZ+(0.5*PipeMD/math.cos(AnchorIA))*math.cos(Tetha45)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipeInstance.edges
   PipeTopEdge1 = PipeEdges.findAt((RefPnt,))

   CordX=-0.5*PipeMD*math.sin(Tetha45)
   CordY=AnchorPY
   CordZ=AnchorPZ+(0.5*PipeMD/math.cos(AnchorIA))*math.cos(Tetha45)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipeInstance.edges
   PipeTopEdge2 = PipeEdges.findAt((RefPnt,))

   CordX=0.5*PipeMD*math.sin(Tetha45)
   CordY=AnchorPY
   CordZ=AnchorPZ-(0.5*PipeMD/math.cos(AnchorIA))*math.cos(Tetha45)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipeInstance.edges
   PipeTopEdge3 = PipeEdges.findAt((RefPnt,))

   CordX=-0.5*PipeMD*math.sin(Tetha45)
   CordY=AnchorPY
   CordZ=AnchorPZ-(0.5*PipeMD/math.cos(AnchorIA))*math.cos(Tetha45)
   RefPnt=(CordX,CordY,CordZ)
   PipeEdges = PipeInstance.edges
   PipeTopEdge4 = PipeEdges.findAt((RefPnt,))

   PipeTopEdge=PipeTopEdge1+PipeTopEdge2+PipeTopEdge3+PipeTopEdge4

   AnchorDispBoundary = TPileCnctnAssembly.Set(edges=PipeTopEdge, name='AnchorDispBoundary')
   TPileCnctnModel.DisplacementBC(name='AnchorDisplacement', 
   createStepName='LoadStep1', region=AnchorDispBoundary, u1=UNSET, 
   u2=-MaxDisp*(math.cos(AnchorIA)), u3=-MaxDisp*(math.sin(AnchorIA)), 
   ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
   distributionType=UNIFORM, fieldName='', localCsys=None)

   #---History output request for Anchor point displacement and reaction force

   mdb.models[ModelName].HistoryOutputRequest(name='AnchorDispHis', 
   createStepName='LoadStep1', variables=('U1', 'U2', 'U3', 'UR1', 'UR2', 
   'UR3', 'UT'), region=AnchorDispBoundary, sectionPoints=DEFAULT, rebar=EXCLUDE)

   mdb.models[ModelName].HistoryOutputRequest(name='AnchorRctnHis', 
   createStepName='LoadStep1', variables=('RT', ), region=AnchorDispBoundary, 
   sectionPoints=DEFAULT, rebar=EXCLUDE)
   
   #-------------11. Mesh Generation---------------------------------------------

   #Mesh generation has been done part-by-part

   #-------------12. Job Creation------------------------------------------------

   #A job is created by Job() method
   
   AnalysisName=ModelName+"Analysis"

   mdb.Job(name=AnalysisName, model=ModelName, type=ANALYSIS,
   explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, 
   description='TPileCnctnStressAnls', parallelizationMethodExplicit=DOMAIN,
   multiprocessingMode=DEFAULT, numDomains=1, userSubroutine='', numCpus=1,
   memory=50, memoryUnits=PERCENTAGE, scratch='', echoPrint=OFF, 
   modelPrint=OFF, contactPrint=OFF, historyPrint=OFF)

   #Job is submitted by submit() method
   #waitForCompletion() makes ABAQUS to wait for job completion

   mdb.jobs[AnalysisName].submit(consistencyChecking=OFF)
   mdb.jobs[AnalysisName].waitForCompletion()

   #-------------13. Post Processing---------------------------------------------

   #No Need to be set at this stage
    