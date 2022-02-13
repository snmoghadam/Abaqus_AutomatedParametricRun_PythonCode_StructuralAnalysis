#-----------------------------------------------------------------------------
#Parametric ABAQUS Model of Anchored Pile with Through Pile Connection
#-----------------------------------------------------------------------------

#---Imports-------------------------------------------------------------------
from ModelParams import *
import ModelParams

#----------1. Clear Display---------------------------------------------------
#Clear ABAQUS viewport display
session.viewports['Viewport: 1'].setValues(displayedObject=None)

#-------------2. Model Creation-----------------------------------------------

#changeKey() method is used to change the name of model
#mdb is used to access the model database
#the default model name is 'Model-1' which will be changed to TPileCnctnModel

mdb.models.changeKey(fromName='Model-1', toName='TPileCnctnModel')
TPileCnctnModel=mdb.models['TPileCnctnModel']

#-------------3. Part Creation------------------------------------------------

#ConstrainedSketch() method is used to access to Line() and Rectangle() methods, and etc.
#giving a value to 'sheetSize' sets the sheet size

#---Parts to be defined:
#1. Soldier Pile (SldrPilePart)
#2. Pipe (PipePart)
#3. Cover Plate (CvrPltPart)
#4. Wedge Plate (WdgPltPart)
#5. Bearing Plate (BrngPltPart)

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
SldrPilePart.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.5*PipeOD)                                      #Datum18
SldrPilePart.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=-0.5*PipeOD)                                     #Datum19
SldrPilePart.DatumPlaneByPointNormal(point=(0,0.5*ISecD,AnchorPZ+0.5*PipeOD/math.cos(AnchorIA)), normal=SldrPileDatums[11]) #Datum20
#SldrPilePart.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=AnchorPZ+0.5*PipeOD/math.cos(AnchorIA))          #Datum20
SldrPilePart.DatumPlaneByPointNormal(point=(0,0.5*ISecD,AnchorPZ-0.5*PipeOD/math.cos(AnchorIA)), normal=SldrPileDatums[11]) #Datum21
#SldrPilePart.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=AnchorPZ-0.5*PipeOD/math.cos(AnchorIA))          #Datum21
SldrPilePart.DatumPlaneByPointNormal(point=(0,0.5*ISecD,AnchorPZ+0.5*LWPlt), normal=SldrPileDatums[11]) #Datum22
#SldrPilePart.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=AnchorPZ+0.5*LWPlt)                              #Datum22
SldrPilePart.DatumPlaneByPointNormal(point=(0,0.5*ISecD,AnchorPZ-0.5*LWPlt), normal=SldrPileDatums[11]) #Datum23
#SldrPilePart.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=AnchorPZ-0.5*LWPlt)                              #Datum23
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

#partitioning pile on wedge plate footprint

RefPnt=(0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[18], faces=SldrPileFace)

RefPnt=(-0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[19], faces=SldrPileFace)

RefPnt=(0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[18], faces=SldrPileFace)

RefPnt=(-0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[19], faces=SldrPileFace)

RefPnt=(0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[18], faces=SldrPileFace)

RefPnt=(-0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[19], faces=SldrPileFace)

RefPnt=(0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[18], faces=SldrPileFace)

RefPnt=(-0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[19], faces=SldrPileFace)



#partitioning pile perpendicular to wedge plate footprint

RefPnt=(0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[23], faces=SldrPileFace)

RefPnt=(-0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[23], faces=SldrPileFace)

RefPnt=(0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[22], faces=SldrPileFace)

RefPnt=(-0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[22], faces=SldrPileFace)

RefPnt=(0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[23], faces=SldrPileFace)

RefPnt=(-0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[23], faces=SldrPileFace)

RefPnt=(0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[22], faces=SldrPileFace)

RefPnt=(-0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[22], faces=SldrPileFace)

RefPnt=(0,0,0.5*PileLngt-0.5*(PipeMD/math.cos(AnchorIA)))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[23], faces=SldrPileFace)

RefPnt=(0,0,0.5*PileLngt+0.5*(PipeMD/math.cos(AnchorIA)))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[22], faces=SldrPileFace)

#partitioning pile perpendicular to wedge plate footprint

RefPnt=(0,0,0.5*PileLngt-0.5*(PipeMD/math.cos(AnchorIA)))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[21], faces=SldrPileFace)

RefPnt=(0,0,0.5*PileLngt+0.5*(PipeMD/math.cos(AnchorIA)))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[20], faces=SldrPileFace)

RefPnt=(0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[21], faces=SldrPileFace)

RefPnt=(-0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[21], faces=SldrPileFace)

RefPnt=(0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[20], faces=SldrPileFace)

RefPnt=(-0.5*PipeMD*math.sin(Tetha45),0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[20], faces=SldrPileFace)

RefPnt=(0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[21], faces=SldrPileFace)

RefPnt=(-0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)-0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[21], faces=SldrPileFace)

RefPnt=(0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[20], faces=SldrPileFace)

RefPnt=(-0.5*PipeMD*math.sin(Tetha45),-0.5*ISecD,0.5*PileLngt-0.5*ISecD*math.tan(AnchorIA)+0.5*(PipeMD/math.cos(AnchorIA))*math.cos(Tetha45))
SldrPileFace=SldrPileFaces.findAt((RefPnt,))
SldrPilePart.PartitionFaceByDatumPlane(datumPlane=SldrPileDatums[20], faces=SldrPileFace)


#Mesh size

#Overal Mesh Size

OvrMeshSiz=0.01
SldrPilePart.seedPart(size=OvrMeshSiz, deviationFactor=0.1, minSizeFactor=0.1)

#constraining the mesh numbers on wedge plate footprint

SgmntNo=13
RefPnt=(0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.125*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileEdge1=SldrPileEdges.findAt((RefPnt,))
RefPnt=(0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.125*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileEdge2=SldrPileEdges.findAt((RefPnt,))
RefPnt=(-0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.125*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileEdge3=SldrPileEdges.findAt((RefPnt,))
RefPnt=(-0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.125*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileEdge4=SldrPileEdges.findAt((RefPnt,))
SldrPileEdge=SldrPileEdge1+SldrPileEdge2+SldrPileEdge3+SldrPileEdge4
SldrPilePart.seedEdgeByNumber(edges=SldrPileEdge, number=SgmntNo, constraint=FIXED)

SgmntNo=5
RefPnt=(0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.375*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileEdge1=SldrPileEdges.findAt((RefPnt,))
RefPnt=(0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.375*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileEdge2=SldrPileEdges.findAt((RefPnt,))
RefPnt=(-0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.375*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileEdge3=SldrPileEdges.findAt((RefPnt,))
RefPnt=(-0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.375*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileEdge4=SldrPileEdges.findAt((RefPnt,))
SldrPileEdge=SldrPileEdge1+SldrPileEdge2+SldrPileEdge3+SldrPileEdge4
SldrPilePart.seedEdgeByNumber(edges=SldrPileEdge, number=SgmntNo, constraint=FIXED)

#---Upper Hole

SgmntNo=20

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

SgmntNo=20

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

SgmntNo=40

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

#Soldier Pile - Wedge Plate Contact
RefPnt=(0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.125*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileWdgEdge1=SldrPileEdges.findAt((RefPnt,))
RefPnt=(0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.125*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileWdgEdge1=SldrPileWdgEdge1+SldrPileEdges.findAt((RefPnt,))
RefPnt=(0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.375*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileWdgEdge1=SldrPileWdgEdge1+SldrPileEdges.findAt((RefPnt,))
RefPnt=(0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.375*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileWdgEdge1=SldrPileWdgEdge1+SldrPileEdges.findAt((RefPnt,))

SldrPilePart.Set('SldrPileWdgEdge1',edges=SldrPileWdgEdge1)
SldrPileWdgNodesEdge1=SldrPilePart.sets['SldrPileWdgEdge1'].nodes
SldrPilePart.Set(nodes=SldrPileWdgNodesEdge1, name='SldrPileWdgNodesEdge1')

RefPnt=(-0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.125*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileWdgEdge2=SldrPileEdges.findAt((RefPnt,))
RefPnt=(-0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.125*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileWdgEdge2=SldrPileWdgEdge2+SldrPileEdges.findAt((RefPnt,))
RefPnt=(-0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)+0.375*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileWdgEdge2=SldrPileWdgEdge2+SldrPileEdges.findAt((RefPnt,))
RefPnt=(-0.5*PipeOD,0.5*ISecD,0.5*PileLngt+0.5*ISecD*math.tan(AnchorIA)-0.375*LWPlt)
SldrPileEdges=SldrPilePart.edges
SldrPileWdgEdge2=SldrPileWdgEdge2+SldrPileEdges.findAt((RefPnt,))

SldrPilePart.Set('SldrPileWdgEdge2',edges=SldrPileWdgEdge2)
SldrPileWdgNodesEdge2=SldrPilePart.sets['SldrPileWdgEdge2'].nodes
SldrPilePart.Set(nodes=SldrPileWdgNodesEdge2, name='SldrPileWdgNodesEdge2')

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

SgmntNo=20

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

SgmntNo=20

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

SgmntNo=40

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

#---4. Wedge Plate Part

#Sketch of Wedge Plate section
WdgPltSecSketch=TPileCnctnModel.ConstrainedSketch(name='WdgPltSecSketch',sheetSize=10)

WdgPltSecPnts=((0,0), (WPltB1,0),
 (WPltB2,WPltH), (0,WPltH), (0,0))

for i in range(0,len(WdgPltSecPnts)-1,1):
 WdgPltSecSketch.Line(point1=WdgPltSecPnts[i] , point2=WdgPltSecPnts[i+1])

#Wedge Plate Part Creation
WdgPltPart=TPileCnctnModel.Part(name='WdgPltPart',
dimensionality=THREE_D, type=DEFORMABLE_BODY)
WdgPltPart.BaseShell(sketch=WdgPltSecSketch)

WPltTheta=math.atan((WPltB1-WPltB2)/WPltH)

WdgPltPart.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=(0.5*LWPlt-0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta))        #Datum2
WdgPltPart.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=(0.5*LWPlt+0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta))        #Datum3
WdgPltPart.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.5*LWPlt*math.cos(WPltTheta))                                        #Datum4
WdgPltDatums= WdgPltPart.datums


RefPnt=(0,0.5*(0.5*LWPlt-0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltFaces = WdgPltPart.faces
WdgPltFace=WdgPltFaces.findAt((RefPnt,))
WdgPltPart.PartitionFaceByDatumPlane(datumPlane=WdgPltDatums[2], faces=WdgPltFace)

RefPnt=(0,0.5*LWPlt*math.cos(WPltTheta),0)
WdgPltFaces = WdgPltPart.faces
WdgPltFace=WdgPltFaces.findAt((RefPnt,))
WdgPltPart.PartitionFaceByDatumPlane(datumPlane=WdgPltDatums[4], faces=WdgPltFace)

RefPnt=(0,(0.5*LWPlt+0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltFaces = WdgPltPart.faces
WdgPltFace=WdgPltFaces.findAt((RefPnt,))
WdgPltPart.PartitionFaceByDatumPlane(datumPlane=WdgPltDatums[3], faces=WdgPltFace)



#Mesh size

SgmntNo=5
RefPnt=(WPltB1-(0.25*LWPlt-0.25*PipeOD/math.cos(AnchorIA))*math.sin(WPltTheta),0.5*(0.5*LWPlt-0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltPart.seedEdgeByNumber(edges=WdgPltEdge, number=SgmntNo, constraint=FIXED)

SgmntNo=13
RefPnt=(WPltB1-(0.5*LWPlt-0.25*PipeOD/math.cos(AnchorIA))*math.sin(WPltTheta),(0.5*LWPlt-0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltPart.seedEdgeByNumber(edges=WdgPltEdge, number=SgmntNo, constraint=FIXED)

SgmntNo=13
RefPnt=(WPltB1-(0.5*LWPlt+0.25*PipeOD/math.cos(AnchorIA))*math.sin(WPltTheta),(0.5*LWPlt+0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltPart.seedEdgeByNumber(edges=WdgPltEdge, number=SgmntNo, constraint=FIXED)

SgmntNo=5
RefPnt=(WPltB1-(0.75*LWPlt+0.25*PipeOD/math.cos(AnchorIA))*math.sin(WPltTheta),(0.75*LWPlt+0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltPart.seedEdgeByNumber(edges=WdgPltEdge, number=SgmntNo, constraint=FIXED)



SgmntNo=5
RefPnt=(0,(0.25*LWPlt-0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltPart.seedEdgeByNumber(edges=WdgPltEdge, number=SgmntNo, constraint=FIXED)

SgmntNo=13
RefPnt=(0,(0.5*LWPlt-0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltPart.seedEdgeByNumber(edges=WdgPltEdge, number=SgmntNo, constraint=FIXED)

SgmntNo=13
RefPnt=(0,(0.5*LWPlt+0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltPart.seedEdgeByNumber(edges=WdgPltEdge, number=SgmntNo, constraint=FIXED)

SgmntNo=5
RefPnt=(0,(0.75*LWPlt+0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltPart.seedEdgeByNumber(edges=WdgPltEdge, number=SgmntNo, constraint=FIXED)


#Mesh part

WdgPltElmntType = mesh.ElemType(elemCode=S4R, elemLibrary=STANDARD, 
secondOrderAccuracy=ON, hourglassControl=DEFAULT)

#WdgPltElmntType = mesh.ElemType(elemCode=S8R, elemLibrary=STANDARD)


WdgPltFace=WdgPltPart.faces[:]
WdgPltMeshRgn=(WdgPltFace, )
WdgPltPart.setElementType(regions=WdgPltMeshRgn, elemTypes=(WdgPltElmntType,))

WdgPltFace=WdgPltPart.faces[:]
WdgPltPart.setMeshControls(regions=WdgPltFace, elemShape=QUAD, algorithm=MEDIAL_AXIS)
#WdgPltPart.setMeshControls(regions=WdgPltFace, algorithm=ADVANCING_FRONT)

WdgPltPart.generateMesh()

# Nodes Sets for Contacts

#Wedge Plate Edge 1
RefPnt=(0,0.5*(0.5*LWPlt-0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltEdge1=WdgPltEdge

RefPnt=(0,(0.5*LWPlt-0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltEdge1=WdgPltEdge1+WdgPltEdge

RefPnt=(0,(0.5*LWPlt+0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltEdge1=WdgPltEdge1+WdgPltEdge

RefPnt=(0,WPltH-0.5*(0.5*LWPlt-0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltEdge1=WdgPltEdge1+WdgPltEdge

WdgPltPart.Set('WdgPltEdge1',edges=WdgPltEdge1)
WdgPltNodesEdg1=WdgPltPart.sets['WdgPltEdge1'].nodes
WdgPltPart.Set(nodes=WdgPltNodesEdg1, name='WdgPltNodesEdg1')

#Wedge Plate Edge 2
RefPnt=(WPltB1-0.5*(0.5*LWPlt-0.5*PipeOD/math.cos(AnchorIA))*math.sin(WPltTheta),
0.5*(0.5*LWPlt-0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltEdge2=WdgPltEdge

RefPnt=(WPltB1-(0.5*LWPlt-0.25*PipeOD/math.cos(AnchorIA))*math.sin(WPltTheta),
(0.5*LWPlt-0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltEdge2=WdgPltEdge2+WdgPltEdge

RefPnt=(WPltB1-(0.5*LWPlt+0.25*PipeOD/math.cos(AnchorIA))*math.sin(WPltTheta),
(0.5*LWPlt+0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltEdge2=WdgPltEdge2+WdgPltEdge

RefPnt=(WPltB1-(WPltH-0.5*(0.5*LWPlt-0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta))*math.tan(WPltTheta),
WPltH-0.5*(0.5*LWPlt-0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
WdgPltEdges=WdgPltPart.edges
WdgPltEdge=WdgPltEdges.findAt((RefPnt,))
WdgPltEdge2=WdgPltEdge2+WdgPltEdge

WdgPltPart.Set('WdgPltEdge2',edges=WdgPltEdge2)
WdgPltNodesEdg2=WdgPltPart.sets['WdgPltEdge2'].nodes
WdgPltPart.Set(nodes=WdgPltNodesEdg2, name='WdgPltNodesEdg2')


#---5. Bearing Plate Part

#Sketch of Bearing Plate section
BrngPltSecSketch=TPileCnctnModel.ConstrainedSketch(name='BrngPltSketch',sheetSize=10)
BrngPltSecSketch.rectangle(point1=(0,0),point2=(BPltB, BPltH))

#Bearing Plate Part Creation
BrngPltPart=TPileCnctnModel.Part(name='BrngPltPart',
dimensionality=THREE_D, type=DEFORMABLE_BODY)
BrngPltPart.BaseShell(sketch=BrngPltSecSketch)

BrngPltPart.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=(0.5*LWPlt-0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta))        #Datum2
BrngPltPart.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=(0.5*LWPlt+0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta))        #Datum3
BrngPltPart.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.5*LWPlt*math.cos(WPltTheta))                                        #Datum4
BrngPltPart.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.5*BPltB)                                                            #Datum5
BrngPltDatums= BrngPltPart.datums


RefPnt=(0,0.5*(0.5*LWPlt-0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
BrngPltFaces = BrngPltPart.faces
BrngPltFace=BrngPltFaces.findAt((RefPnt,))
BrngPltPart.PartitionFaceByDatumPlane(datumPlane=BrngPltDatums[2], faces=BrngPltFace)

RefPnt=(0,0.5*LWPlt*math.cos(WPltTheta),0)
BrngPltFaces = BrngPltPart.faces
BrngPltFace=BrngPltFaces.findAt((RefPnt,))
BrngPltPart.PartitionFaceByDatumPlane(datumPlane=BrngPltDatums[4], faces=BrngPltFace)

RefPnt=(0,(0.5*LWPlt+0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
BrngPltFaces = BrngPltPart.faces
BrngPltFace=BrngPltFaces.findAt((RefPnt,))
BrngPltPart.PartitionFaceByDatumPlane(datumPlane=BrngPltDatums[3], faces=BrngPltFace)

#Mesh size

SgmntNo=5
RefPnt=(0,(0.25*LWPlt-0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
BrngPltEdges=BrngPltPart.edges
BrngPltEdge=BrngPltEdges.findAt((RefPnt,))
BrngPltPart.seedEdgeByNumber(edges=BrngPltEdge, number=SgmntNo, constraint=FIXED)

SgmntNo=13
RefPnt=(0,(0.5*LWPlt-0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
BrngPltEdges=BrngPltPart.edges
BrngPltEdge=BrngPltEdges.findAt((RefPnt,))
BrngPltPart.seedEdgeByNumber(edges=BrngPltEdge, number=SgmntNo, constraint=FIXED)

SgmntNo=13
RefPnt=(0,(0.5*LWPlt+0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
BrngPltEdges=BrngPltPart.edges
BrngPltEdge=BrngPltEdges.findAt((RefPnt,))
BrngPltPart.seedEdgeByNumber(edges=BrngPltEdge, number=SgmntNo, constraint=FIXED)

SgmntNo=5
RefPnt=(0,(0.75*LWPlt+0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
BrngPltEdges=BrngPltPart.edges
BrngPltEdge=BrngPltEdges.findAt((RefPnt,))
BrngPltPart.seedEdgeByNumber(edges=BrngPltEdge, number=SgmntNo, constraint=FIXED)

#Partition for displacement application at anchor point

RefPnt=(0.5*BPltB,0.25*LWPlt*math.cos(WPltTheta),0)
BrngPltFaces = BrngPltPart.faces
BrngPltFace=BrngPltFaces.findAt((RefPnt,))
BrngPltPart.PartitionFaceByDatumPlane(datumPlane=BrngPltDatums[5], faces=BrngPltFace)

RefPnt=(0.5*BPltB,0.75*LWPlt*math.cos(WPltTheta),0)
BrngPltFaces = BrngPltPart.faces
BrngPltFace=BrngPltFaces.findAt((RefPnt,))
BrngPltPart.PartitionFaceByDatumPlane(datumPlane=BrngPltDatums[5], faces=BrngPltFace)

RefPnt=(0.5*BPltB,BPltH,0)
BrngPltFaces = BrngPltPart.faces
BrngPltFace=BrngPltFaces.findAt((RefPnt,))
BrngPltPart.PartitionFaceByDatumPlane(datumPlane=BrngPltDatums[5], faces=BrngPltFace)

RefPnt=(0.5*BPltB,0,0)
BrngPltFaces = BrngPltPart.faces
BrngPltFace=BrngPltFaces.findAt((RefPnt,))
BrngPltPart.PartitionFaceByDatumPlane(datumPlane=BrngPltDatums[5], faces=BrngPltFace)

#Mesh part

BrngPltElmntType = mesh.ElemType(elemCode=S4R, elemLibrary=STANDARD, 
secondOrderAccuracy=ON, hourglassControl=DEFAULT)

#BrngPltElmntType = mesh.ElemType(elemCode=S8R, elemLibrary=STANDARD)

BrngPltFace=BrngPltPart.faces[:]
BrngPltMeshRgn=(BrngPltFace, )
BrngPltPart.setElementType(regions=BrngPltMeshRgn, elemTypes=(BrngPltElmntType,))

BrngPltFace=WdgPltPart.faces[:]
BrngPltPart.setMeshControls(regions=WdgPltFace, elemShape=QUAD, algorithm=MEDIAL_AXIS)
#BrngPltPart.setMeshControls(regions=BrngPltFace, algorithm=ADVANCING_FRONT)

BrngPltPart.generateMesh()


# Nodes Sets for Contacts

#Bearing Plate Edge 1
RefPnt=(0,0.5*(0.5*LWPlt-0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
BrngPltEdges=BrngPltPart.edges
BrngPltEdge=BrngPltEdges.findAt((RefPnt,))
BrngPltEdge1=BrngPltEdge

RefPnt=(0,(0.5*LWPlt-0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
BrngPltEdges=BrngPltPart.edges
BrngPltEdge=BrngPltEdges.findAt((RefPnt,))
BrngPltEdge1=BrngPltEdge1+BrngPltEdge

RefPnt=(0,(0.5*LWPlt+0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
BrngPltEdges=BrngPltPart.edges
BrngPltEdge=BrngPltEdges.findAt((RefPnt,))
BrngPltEdge1=BrngPltEdge1+BrngPltEdge

RefPnt=(0,BPltH-0.5*(0.5*LWPlt-0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
BrngPltEdges=BrngPltPart.edges
BrngPltEdge=BrngPltEdges.findAt((RefPnt,))
BrngPltEdge1=BrngPltEdge1+BrngPltEdge

BrngPltPart.Set('BrngPltEdge1',edges=BrngPltEdge1)
BrngPltNodesEdg1=BrngPltPart.sets['BrngPltEdge1'].nodes
BrngPltPart.Set(nodes=BrngPltNodesEdg1, name='BrngPltNodesEdg1')

#Bearing Plate Edge 2

RefPnt=(BPltB,0.5*(0.5*LWPlt-0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
BrngPltEdges=BrngPltPart.edges
BrngPltEdge=BrngPltEdges.findAt((RefPnt,))
BrngPltEdge2=BrngPltEdge

RefPnt=(BPltB,(0.5*LWPlt-0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
BrngPltEdges=BrngPltPart.edges
BrngPltEdge=BrngPltEdges.findAt((RefPnt,))
BrngPltEdge2=BrngPltEdge2+BrngPltEdge

RefPnt=(BPltB,(0.5*LWPlt+0.25*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
BrngPltEdges=BrngPltPart.edges
BrngPltEdge=BrngPltEdges.findAt((RefPnt,))
BrngPltEdge2=BrngPltEdge2+BrngPltEdge

RefPnt=(BPltB,BPltH-0.5*(0.5*LWPlt-0.5*PipeOD/math.cos(AnchorIA))*math.cos(WPltTheta),0)
BrngPltEdges=BrngPltPart.edges
BrngPltEdge=BrngPltEdges.findAt((RefPnt,))
BrngPltEdge2=BrngPltEdge2+BrngPltEdge

BrngPltPart.Set('BrngPltEdge2',edges=BrngPltEdge2)
BrngPltNodesEdg2=BrngPltPart.sets['BrngPltEdge2'].nodes
BrngPltPart.Set(nodes=BrngPltNodesEdg2, name='BrngPltNodesEdg2')


#-------------4. Material Creation--------------------------------------------

#using Density() and Elastic() objects to set density and elastic 
#material properties at different tempratures

PileSteelMaterial=TPileCnctnModel.Material(name='PileSteelMat')
PileSteelMaterial.Density(table=((RhoSteel, ), ))
PileSteelMaterial.Elastic(table=((ESteel, NuSteel),))
PileSteelMaterial.Plastic(table=((FyPile, EyPile),))
#PileSteelMaterial.Plastic(table=((FyPile, EyPile),(FrPile, ErPile)))
#PileSteelMaterial.Plastic(table=(
#(2.00E+08,0.0000),(2.46E+08,0.0235),(2.94E+08,0.0473),
#(3.74E+08,0.0934),(4.37E+08,0.1376),(4.80E+08,0.1799)))

PipeSteelMaterial=TPileCnctnModel.Material(name='PipeSteelMat')
PipeSteelMaterial.Density(table=((RhoSteel, ), ))
PipeSteelMaterial.Elastic(table=((ESteel, NuSteel),))
PipeSteelMaterial.Plastic(table=((FyPipe, EyPipe),))
#PipeSteelMaterial.Plastic(table=((FyPipe, EyPipe),(FrPipe, ErPipe)))
#PipeSteelMaterial.Plastic(table=(
#(2.00E+08,0.0000),(2.46E+08,0.0235),(2.94E+08,0.0473),
#(3.74E+08,0.0934),(4.37E+08,0.1376),(4.80E+08,0.1799)))

WdgPlateSteelMaterial=TPileCnctnModel.Material(name='WdgPlateSteelMat')
WdgPlateSteelMaterial.Density(table=((RhoSteel, ), ))
WdgPlateSteelMaterial.Elastic(table=((ESteel, NuSteel),))
WdgPlateSteelMaterial.Plastic(table=((FyPlate, EyPlate),))
#WdgPlateSteelMaterial.Plastic(table=((FyPlate, EyPlate),(FrPlate, ErPlate)))
#WdgPlateSteelMaterial.Plastic(table=(
#(2.00E+08,0.0000),(2.46E+08,0.0235),(2.94E+08,0.0473),
#(3.74E+08,0.0934),(4.37E+08,0.1376),(4.80E+08,0.1799)))

BrngPlateSteelMaterial=TPileCnctnModel.Material(name='BrngPlateSteelMat')
BrngPlateSteelMaterial.Density(table=((RhoSteel, ), ))
BrngPlateSteelMaterial.Elastic(table=((ESteel, NuSteel),))

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

#---4. Wedge Plate Section

WdgPltSec=TPileCnctnModel.HomogeneousShellSection(
name='WdgPltSec', material='WdgPlateSteelMat', thicknessType=UNIFORM, thickness=WPltT)

WdgPltFace=WdgPltPart.faces[:]
WdgPltRegion = WdgPltPart.Set(faces=WdgPltFace, name='WPltFSet-Sec')

WdgPltPart.SectionAssignment(region=WdgPltRegion, sectionName='WdgPltSec', offset=0.0, 
offsetType=MIDDLE_SURFACE, offsetField='', 
thicknessAssignment=FROM_SECTION)

#---5. Bearing Plate Section

BrngPltSec=TPileCnctnModel.HomogeneousShellSection(
name='BrngPltSec', material='BrngPlateSteelMat', thicknessType=UNIFORM, thickness=BPltT)

BrngPltFace=BrngPltPart.faces[:]
BrngPltRegion = BrngPltPart.Set(faces=BrngPltFace, name='BPltFSet-Sec')

BrngPltPart.SectionAssignment(region=BrngPltRegion, sectionName='BrngPltSec', offset=0.0, 
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

#---WdgPltInstance

WdgPltInstance1=TPileCnctnAssembly.Instance(
name='WdgPltInstance1', part=WdgPltPart, dependent=ON)

WdgPltInstance2=TPileCnctnAssembly.Instance(
name='WdgPltInstance2', part=WdgPltPart, dependent=ON)

#---BrngPltInstance

BrngPltInstance=TPileCnctnAssembly.Instance(
name='BrngPltInstance', part=BrngPltPart, dependent=ON)

#---Fixing Assembly

RefCrd=((0,0,0), (1,0,0), (0,1,0), (0,0,1))
RAngl=90

TPileCnctnAssembly.translate(instanceList=('PipeInstance', ), 
vector=(AnchorPX, AnchorPY, AnchorPZ-PipeLngt-0.5*PipeMD/math.tan(AnchorIA)))
TPileCnctnAssembly.rotate(instanceList=('PipeInstance', ), axisPoint=(AnchorPX,AnchorPY,AnchorPZ), 
axisDirection=RefCrd[3], angle=2*RAngl)
TPileCnctnAssembly.rotate(instanceList=('PipeInstance', ), axisPoint=(AnchorPX,AnchorPY,AnchorPZ), 
axisDirection=RefCrd[1], angle=-2*AnchorIA*180/math.pi)

TPileCnctnAssembly.translate(instanceList=('WdgPltInstance1', ), 
vector=(AnchorPX+0.5*PipeOD-WPltB2, AnchorPY-WPltH, AnchorPZ+0.5*LWPlt))

WPltRA=math.atan((WPltB1-WPltB2)/WPltH)
TPileCnctnAssembly.rotate(instanceList=('WdgPltInstance1', ), axisPoint=(AnchorPX+0.5*PipeOD,AnchorPY,AnchorPZ+0.5*LWPlt), 
axisDirection=RefCrd[2], angle=-RAngl)
TPileCnctnAssembly.rotate(instanceList=('WdgPltInstance1', ), axisPoint=(AnchorPX+0.5*PipeOD,AnchorPY,AnchorPZ+0.5*LWPlt), 
axisDirection=RefCrd[1], angle=RAngl+WPltRA*180/math.pi)

TPileCnctnAssembly.translate(instanceList=('WdgPltInstance2', ), 
vector=(AnchorPX-0.5*PipeOD-WPltB2, AnchorPY-WPltH, AnchorPZ+0.5*LWPlt))

TPileCnctnAssembly.rotate(instanceList=('WdgPltInstance2', ), axisPoint=(AnchorPX-0.5*PipeOD,AnchorPY,AnchorPZ+0.5*LWPlt), 
axisDirection=RefCrd[2], angle=-RAngl)
TPileCnctnAssembly.rotate(instanceList=('WdgPltInstance2', ), axisPoint=(AnchorPX-0.5*PipeOD,AnchorPY,AnchorPZ+0.5*LWPlt), 
axisDirection=RefCrd[1], angle=RAngl+WPltRA*180/math.pi)



WPltTV=(AnchorPX-0.5*BPltB,AnchorPY+(0.5*WPltB1+0.5*WPltB2)*math.cos(WPltRA)-0.5*BPltH,AnchorPZ+(0.5*WPltB1+0.5*WPltB2)*math.sin(WPltRA))
WPltRP=(AnchorPX,AnchorPY+(0.5*WPltB1+0.5*WPltB2)*math.cos(WPltRA),AnchorPZ+(0.5*WPltB1+0.5*WPltB2)*math.sin(WPltRA))
TPileCnctnAssembly.translate(instanceList=('BrngPltInstance', ), vector=WPltTV)
TPileCnctnAssembly.rotate(instanceList=('BrngPltInstance', ), axisPoint=WPltRP, 
axisDirection=RefCrd[1], angle=-(90-WPltRA*180/math.pi))

#-------------7. Step Creation------------------------------------------------

#static step is created by StaticStep() method which is used for loading
#this is the step next to initial step defined by default

TPileCnctnModel.StaticStep(
name='LoadStep1', previous='Initial', description='Loading Step')

mdb.models['TPileCnctnModel'].steps['LoadStep1'].setValues(
stabilizationMagnitude=0.0002, stabilizationMethod=DAMPING_FACTOR, 
continueDampingFactors=False, adaptiveDampingRatio=None, 
initialInc=0.01, minInc=1e-15, maxInc=0.1, nlgeom=ON)

mdb.models['TPileCnctnModel'].steps['LoadStep1'].control.setValues(
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

#Wedge Plate Bearing Plate Contact
region1=TPileCnctnAssembly.instances['BrngPltInstance'].sets['BrngPltEdge1']
region2=TPileCnctnAssembly.instances['WdgPltInstance2'].sets['WdgPltNodesEdg1']
TPileCnctnModel.Tie(name='WdgBrng1', master=region1, 
slave=region2, positionToleranceMethod=SPECIFIED, 
positionTolerance=0.01, adjust=ON, tieRotations=ON, thickness=ON)

region1=TPileCnctnAssembly.instances['BrngPltInstance'].sets['BrngPltEdge2']
region2=TPileCnctnAssembly.instances['WdgPltInstance1'].sets['WdgPltNodesEdg1']
TPileCnctnModel.Tie(name='WdgBrng2', master=region1, 
slave=region2, positionToleranceMethod=SPECIFIED, 
positionTolerance=0.01, adjust=ON, tieRotations=ON, thickness=ON)

#Wedge Plate Sodier Pile Contact
region1=TPileCnctnAssembly.instances['SldrPileInstance'].sets['SldrPileWdgNodesEdge1']
region2=TPileCnctnAssembly.instances['WdgPltInstance1'].sets['WdgPltNodesEdg2']
TPileCnctnModel.Tie(name='PileWdg1', master=region2, 
slave=region1, positionToleranceMethod=SPECIFIED, 
positionTolerance=0.01, adjust=ON, tieRotations=ON, thickness=ON)

region1=TPileCnctnAssembly.instances['SldrPileInstance'].sets['SldrPileWdgNodesEdge2']
region2=TPileCnctnAssembly.instances['WdgPltInstance2'].sets['WdgPltNodesEdg2']
TPileCnctnModel.Tie(name='PileWdg2', master=region2, 
slave=region1, positionToleranceMethod=SPECIFIED, 
positionTolerance=0.01, adjust=ON, tieRotations=ON, thickness=ON)

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

TPileCnctnModel.TabularAmplitude(name='AnchorDispAmp', 
timeSpan=STEP, smooth=SOLVER_DEFAULT, data=((0.0, 1.0), (1.0, 1.0)))

BrngPltVertices = BrngPltInstance.vertices

RefPnt=(AnchorPX,AnchorPY+0.5*(WPltB1+WPltB2)*(math.cos(WPltTheta)),AnchorPZ+0.5*(WPltB1+WPltB2)*(math.sin(WPltTheta)))
AnchorVertex = BrngPltVertices.findAt((RefPnt,))

AnchorDispBoundary = TPileCnctnAssembly.Set(vertices=AnchorVertex, name='AnchorVertex')

TPileCnctnModel.DisplacementBC(name='AnchorDisplacement', 
createStepName='LoadStep1', region=AnchorDispBoundary, u1=UNSET, 
u2=-MaxDisp*(math.cos(WPltTheta)), u3=-MaxDisp*(math.sin(WPltTheta)), 
ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude='AnchorDispAmp', fixed=OFF, 
distributionType=UNIFORM, fieldName='', localCsys=None)

mdb.models['TPileCnctnModel'].boundaryConditions['AnchorDisplacement'].setValues(amplitude=UNSET)

#---History output request for Anchor point displacement and reaction force

mdb.models['TPileCnctnModel'].HistoryOutputRequest(name='AnchorDispHis', 
createStepName='LoadStep1', variables=('U1', 'U2', 'U3', 'UR1', 'UR2', 
'UR3', 'UT'), region=AnchorDispBoundary, sectionPoints=DEFAULT, rebar=EXCLUDE)

mdb.models['TPileCnctnModel'].HistoryOutputRequest(name='AnchorRctnHis', 
createStepName='LoadStep1', variables=('RT', ), region=AnchorDispBoundary, 
sectionPoints=DEFAULT, rebar=EXCLUDE)

#-------------11. Mesh Generation---------------------------------------------

#Mesh generation has been done part-by-part

#-------------12. Job Creation------------------------------------------------

#A job is created by Job() method

mdb.Job(name='TPileCnctnAnls', model='TPileCnctnModel', type=ANALYSIS,
explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, 
description='TPileCnctnStressAnls', parallelizationMethodExplicit=DOMAIN,
multiprocessingMode=DEFAULT, numDomains=1, userSubroutine='', numCpus=1,
memory=50, memoryUnits=PERCENTAGE, scratch='', echoPrint=OFF, 
modelPrint=OFF, contactPrint=OFF, historyPrint=OFF)

#Job is submitted by submit() method
#waitForCompletion() makes ABAQUS to wait for job completion

mdb.jobs['TPileCnctnAnls'].submit(consistencyChecking=OFF)
mdb.jobs['TPileCnctnAnls'].waitForCompletion()

#-------------13. Post Processing---------------------------------------------

#No Need to be set at this stage
    