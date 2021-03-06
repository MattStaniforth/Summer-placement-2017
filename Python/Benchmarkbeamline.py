import os
import math
import numpy as np
import time

##################################################################################################################

#This version of the script will generate a geometry consisting of a beamline and a source,
#with a layer of shielding around both. This is divided up into a number of sections specified by user input. This 
#code does define volumes, physical surfaces, and physical volumes.

lb = float(input('Input (in centimetres) the length of the beamline: '))
wb = float(input('Input (in centimetres) the width of the beamline: '))
hb = float(input('Input (in centimetres) the height of the beamline: '))

ws = float(input('Input (in centimetres) the total width of the outer shielding: '))
hs = float(input('Input (in centimetres) the total height of the outer shielding: '))

rtot = input('Input how many regions you wish you segment the beamline into in order to calculate the average flux: ')

srcl = float(input('Input the length of the source volume: (It is important that this is NOT equal to the length of your beamline divided by the number of regions youre segmenting the beamline into) '))

floc = input('Input the full path location of where you would like the output saved (include "" around path): ')



Points = [] #This array will contain the points we wish to define. 
Lines = [] #This array will contain every pair of points which is connected by a line (ie all the lines we wish to
           #define.

##################################################################################################################

#First we define all the points in the geometry.

#First we define the outer points for the outer shielding

for i in range(0,rtot+1): #Need rtot+1 else we don't include the last set of points.
                           
    Points.append([0,0,i*(lb/rtot)])
    Points.append([0,hs,i*(lb/rtot)])
    Points.append([ws,hs,i*(lb/rtot)])
    Points.append([ws,0,i*(lb/rtot)])


#Second we define the points for the beamline (simultaeneously the inner points for the outer shielding)

for i in range(0,rtot+1): 
    
    Points.append([(ws/2) - (wb/2), (hs/2) - (hb/2), i*(lb/rtot)])
    Points.append([(ws/2) - (wb/2), (hs/2) + (hb/2), i*(lb/rtot)])
    Points.append([(ws/2) + (wb/2), (hs/2) + (hb/2), i*(lb/rtot)])
    Points.append([(ws/2) + (wb/2), (hs/2) - (hb/2), i*(lb/rtot)])
    

#Finally we define the remaining 4 points needed to define the source cube

Points.append([(ws/2) - (wb/2), (hs/2) - (hb/2), srcl])
Points.append([(ws/2) - (wb/2), (hs/2) + (hb/2), srcl])
Points.append([(ws/2) + (wb/2), (hs/2) + (hb/2), srcl])
Points.append([(ws/2) + (wb/2), (hs/2) - (hb/2), srcl])

#We have now defined all the points.

##################################################################################################################

#We now need to define all the lines.
    
for i in range(0,len(Points)):
     
    #For every point, if there is another point in the geometry where only one 
    #co-ordinate is different, and that point is the closest such point, we 
    #want a line joining those two points. 
     
    samexy=[] #This is the array where the xy co-ords are the same
    sameyz=[] #This is the array where the yz co-ords are the same
    samexz=[] #This is the array where the xz co-ords are the same
    
    diffsz=[] #This is the array with the differences in the z co-ordinate between points i and j
    diffsx=[] #This is the array with the differences in the x co-ordinate between points i and j
    diffsy=[] #This is the array with the differences in the y co-ordinate between points i and j
    
    
    for j in range(0,len(Points)): #This loop finds, for Point[i], every point which lines on either the same x, y or z axis.
                                    #It then calculates the distance along that axis between Point[i] and those points,
                                    #and stores these values in a list. We then find the closest point, and join Point[i] with that
                                    #point with a line. 
                                    
         
        if Points[j][0] == Points[i][0] and Points[j][1] == Points[i][1] and Points[j][2] > Points[i][2]:
            diffsz.append([Points[j][2]-Points[i][2],j]) #Append to diffsz the difference in z co-ordinate
            
        elif Points[j][1] == Points[i][1] and Points[j][2] == Points[i][2] and Points[j][0] > Points[i][0]:
            diffsx.append([Points[j][0]-Points[i][0],j]) #Append to diffsx the difference in x co-ordinate
            
        elif Points[j][0] == Points[i][0] and Points[j][2] == Points[i][2] and Points[j][1] > Points[i][1]:
            diffsy.append([Points[j][1]-Points[i][1],j]) #Append to diffsy the difference in y co-ordinate      
                            
    if len(diffsz)>0: #If there is another point with the same x and y co-ordinates, len(diffsz) > 0.
        diffsz0 = []
        
        for k in range(0,len(diffsz)):
            diffsz0.append(diffsz[k][0])
        
        index=np.argmin(diffsz0)
            
        Lines.append([i,diffsz[index][1]]) #Find the point closest and we will have a line between this Point[i] and that point.
        
    if len(diffsx)>0: #If there is another point with the same y and z co-ordinates, len(diffsx) > 0.
        diffsx0 = []
        
        for k in range(0,len(diffsx)):
            diffsx0.append(diffsx[k][0])
            
        index = np.argmin(diffsx0)
        Lines.append([i,diffsx[index][1]]) #Find the point closest and we will have a line between this Point[i] and that point.
        
    if len(diffsy)>0: #If there is another point with the same x and z co-ordinates, len(diffsy) > 0.
        
        diffsy0=[]
        
        for k in range(0,len(diffsy)):
            diffsy0.append(diffsy[k][0])
        
        index=np.argmin(diffsy0)
        Lines.append([i,diffsy[index][1]]) #Find the point closest and we will have a line between this Point[i] and that point.
        
        
#To reiterate, what the above does is loop through all the points in the geometry, and for each of them finds any
#other point which is only different in one co-ordinate. It then finds the closest such point in each of the three
#directions (x, y, z), and defines a line between the current point and that point. It avoids duplicating lines by
#only searching for closest points in the positive direction along each of the axes.
        
##################################################################################################################
                      
#Available but commented out here is the chance to test the geometry with just points and lines defined. 

##################################################################################################################

#os.chdir(floc)
#geometry = open('Testgeometry.geo','w')

#for i in range(0,len(Points)):
    #geometry.write("Point(" + str(i+1) + ") = {" + str(Points[i][0]) + ", " + str(Points[i][1]) + ", " + str(Points[i][2]) + ", " + "10};" +"\n")
            
#for j in range(0,len(Lines)):
    #geometry.write("Line(" + str(j+1) + ") = {" + str(Lines[j][0]+1) + ", " + str(Lines[j][1]+1) + "};" +"\n")

#time.sleep(1)

#geometry.close()

##################################################################################################################

#Now we define the surfaces

Surfaces=[]

#The way I've chosen to get the surfaces defined is rather convoluted. For every vertical line (line in yLines), 
#there will be surfaces connected to it along either the z or x axis, but not necessarily both. We find, for each
#vertical line, the closest vertical line further along the z axis, and the closest vertical line further along 
#the x axis. These two lines will be two of the lines in the Line Loop which makes up a surface. We then find the 
#other two lines connecting these lines, and make a surface loop out of the four of them.

yLines=[] #This will be the list containing all the vertical lines.

for line in Lines:
    if Points[line[0]][0]==Points[line[1]][0] and Points[line[0]][2]==Points[line[1]][2]:
        yLines.append(line) #If the x and z co-ordinates of the two points at either end of the line are the same, append the line to yLines.

#yLines now contains all the vertical lines.
        
for line in yLines:
    
    newsurfacex=[] #This will be the surface along the x axis associated with this line, if it exists.
    newsurfacez=[] #This will be the surface along the z axis associated with this line, if it exists.
    xplanelines=[] #All the lines lying in the same plane as this line in the direction of the x axis.
    zplanelines=[] #All the lines lying in the same plane as this line in the direction of the y axis. 
    
    for anotherline in yLines:
        
        if Points[anotherline[0]][0] == Points[line[0]][0] and Points[anotherline[0]][1] == Points[line[0]][1] and Points[anotherline[1]][0] == Points[line[1]][0] and Points[anotherline[1]][1] == Points[line[1]][1] and Points[anotherline[0]][2] > Points[line[0]][2] and Points[anotherline[1]][2] > Points[line[1]][2]:
            zplanelines.append(anotherline) #If there is another line in yLines with points having the same x and y co-ordinates
                                            #as this one, append it to zplanelines.
            
        elif Points[anotherline[0]][2] == Points[line[0]][2] and Points[anotherline[0]][1] == Points[line[0]][1] and Points[anotherline[1]][2] == Points[line[1]][2] and Points[anotherline[1]][1] == Points[line[1]][1] and Points[anotherline[0]][0] > Points[line[0]][0] and Points[anotherline[1]][0] > Points[line[1]][0]:
            xplanelines.append(anotherline) #If there is another line in yLines with points havingthe same y and z co-ordinates
                                            #as this one, append it to xplanelines.
            
        elif Points[anotherline[0]][2] == Points[line[0]][2] and Points[anotherline[1]][2] == Points[line[1]][2] and Points[anotherline[0]][0] > Points[line[0]][0] and Points[anotherline[1]][0] > Points[line[1]][0]:
            
            if Points[anotherline[0]][1] > Points[line[0]][1] and Points[anotherline[1]][1] < Points[line[1]][1]:
                   xplanelines.append(anotherline) #If there is another line in yLines which lines in the same plane as this one
                                                   #but doesn't have the same y co-ordinates, that means we're looking at
                                                   #one of the lines making up the beamline. That will eventually be part of a
                                                   #subloop of the lineloop for this surface, and so we must take it into account. 
        

    
#Now for every line in yLines we have lists xplanelines and zplanelines of lines lying in the same plane moving positively along either the z or x axis. 
    
    if len(xplanelines)==1:
        
        newsurfacex.append(line)
        newsurfacex.append(xplanelines[0]) #If there is only one other vertical line lying in the same plane in 
                                           #the x direction, then this line and that line will form a surface.
        
        for i in range(0,len(Lines)): #This loop searches the rest of the lines for the two lines linking the two
                                       #lines above so that we can make a surface out of them.
            if Lines[i][0] == xplanelines[0][0]:
                if Lines[i][1] == line[0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][0] == xplanelines[0][1]:
                if Lines[i][1] == line[0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][0] == line[1]:
                if Lines[i][1] == xplanelines[0][0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][0] == line[1]:
                if Lines[i][1] == xplanelines[0][1]:
                    newsurfacex.append(Lines[i])
            if Lines[i][1] == xplanelines[0][0]:
                if Lines[i][0] == line[0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][1] == xplanelines[0][1]:
                if Lines[i][0] == line[0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][1] == line[1]:
                if Lines[i][0] == xplanelines[0][0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][1] == line[1]:
                if Lines[i][0] == xplanelines[0][1]:
                    newsurfacex.append(Lines[i])
                    
    if len(xplanelines) == 3: #If there are three other lines in the same plane as this one in the x direction,
                              #then we're looking at a surface which will need to contain a subloop. (A surface
                              #within a surface)
        
        newsurfacex.append(line)
        newsurfacex.append(xplanelines[0]) #First, find the four lines connecting the lines which make up the outer
                                           #surface.
        
        for i in range(0,len(Lines)):
            if Lines[i][0] == xplanelines[0][0]:
                if Lines[i][1] == line[0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][0] == xplanelines[0][1]:
                if Lines[i][1] == line[0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][0] == line[1]:
                if Lines[i][1] == xplanelines[0][0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][0] == line[1]:
                if Lines[i][1] == xplanelines[0][1]:
                    newsurfacex.append(Lines[i])
            if Lines[i][1] == xplanelines[0][0]:
                if Lines[i][0] == line[0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][1] == xplanelines[0][1]:
                if Lines[i][0] == line[0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][1] == line[1]:
                if Lines[i][0] == xplanelines[0][0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][1] == line[1]:
                if Lines[i][0] == xplanelines[0][1]:
                    newsurfacex.append(Lines[i])
        
        newsurfacex.append(xplanelines[1])
        newsurfacex.append(xplanelines[2]) #We then find the four lines making up the inner surface.
                    
        for i in range(0,len(Lines)):
            if Lines[i][0] == xplanelines[1][0]:
                if Lines[i][1] == xplanelines[2][0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][0] == xplanelines[1][1]:
                if Lines[i][1] == xplanelines[2][0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][0] == xplanelines[2][1]:
                if Lines[i][1] == xplanelines[1][0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][0] == xplanelines[2][1]:
                if Lines[i][1] == xplanelines[1][1]:
                    newsurfacex.append(Lines[i])
            if Lines[i][1] == xplanelines[1][0]:
                if Lines[i][0] == xplanelines[2][0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][1] == xplanelines[1][1]:
                if Lines[i][0] == xplanelines[2][0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][1] == xplanelines[2][1]:
                if Lines[i][0] == xplanelines[1][0]:
                    newsurfacex.append(Lines[i])
            if Lines[i][1] == xplanelines[2][1]:
                if Lines[i][0] == xplanelines[1][1]:
                    newsurfacex.append(Lines[i]) 
    
    if len(zplanelines)>0:
        newsurfacez.append(line)
        
        diffsz=[]
        
        for i in range(0,len(zplanelines)):
            
            diffsz.append(Points[zplanelines[i][0]][2] - Points[line[0]][2])
           
        indx=np.argmin(diffsz) 
        
        #if indx == 10:
            #for i in range(0,len(zplanelines)):
                #print [Points[zplanelines[i][0]][0],Points[zplanelines[i][0]][1],Points[zplanelines[i][0]][2]]
                #print [Points[zplanelines[i][1]][0],Points[zplanelines[i][1]][1],Points[zplanelines[i][1]][2]]
        
        newsurfacez.append(zplanelines[indx])
        
        for i in range(0,len(Lines)):
            if Lines[i][0] == line[0]:
                if Lines[i][1] == zplanelines[indx][0]:
                    newsurfacez.append(Lines[i])
            if Lines[i][0] == line[1]:
                if Lines[i][1] == zplanelines[indx][0]:
                    newsurfacez.append(Lines[i])
            if Lines[i][0] == zplanelines[indx][1]:
                if Lines[i][1] == line[0]:
                    newsurfacez.append(Lines[i])
            if Lines[i][0] == zplanelines[indx][1]:
                if Lines[i][1] == line[1]:
                    newsurfacez.append(Lines[i])
            if Lines[i][1] == line[0]:
                if Lines[i][0] == zplanelines[indx][0]:
                    newsurfacez.append(Lines[i])
            if Lines[i][1] == line[1]:
                if Lines[i][0] == zplanelines[indx][0]:
                    newsurfacez.append(Lines[i])
            if Lines[i][1] == zplanelines[indx][1]:
                if Lines[i][0] == line[0]:
                    newsurfacez.append(Lines[i])
            if Lines[i][1] == zplanelines[indx][1]:
                if Lines[i][0] == line[1]:
                    newsurfacez.append(Lines[i])
    
    if len(newsurfacex)>0:                
        Surfaces.append(newsurfacex)
    if len(newsurfacez)>0:
        Surfaces.append(newsurfacez)
    
            
zLines=[]

for line in Lines:
    if Points[line[0]][0]==Points[line[1]][0] and Points[line[0]][1]==Points[line[1]][1]:
        zLines.append(line) #If the x and y co-ordinates of the two points at either end of the line are the same, append the line to yLines.
        
#zLines now contains all the lines perpendicular to the z axis.
        
for line in zLines:
    newsurfacey=[]
    yplanelines=[]

    for anotherline in zLines:
        if Points[anotherline[0]][1] == Points[line[0]][1] and Points[anotherline[0]][2] == Points[line[0]][2] and Points[anotherline[1]][1] == Points[line[1]][1] and Points[anotherline[1]][2] == Points[line[1]][2] and Points[anotherline[0]][0] > Points[line[0]][0] and Points[anotherline[1]][0] > Points[line[1]][0]:
            yplanelines.append(anotherline)       
    
    if len(yplanelines)>0:
        newsurfacey.append(line)
        newsurfacey.append(yplanelines[0])
        diffsy=[]
        
        for i in range(0,len(yplanelines)):
            
            diffsy.append(Points[yplanelines[i][0]][2] - Points[line[0]][2])
           
        index=np.argmin(diffsy)
        
        for i in range(0,len(Lines)):
            if Lines[i][0] == line[0]:
                if Lines[i][1] == yplanelines[index][0]:
                    newsurfacey.append(Lines[i])
            if Lines[i][0] == line[1]:
                if Lines[i][1] == yplanelines[index][0]:
                    newsurfacey.append(Lines[i])
            if Lines[i][0] == yplanelines[index][1]:
                if Lines[i][1] == line[0]:
                    newsurfacey.append(Lines[i])
            if Lines[i][0] == yplanelines[index][1]:
                if Lines[i][1] == line[1]:
                    newsurfacey.append(Lines[i])
            if Lines[i][1] == line[0]:
                if Lines[i][0] == yplanelines[index][0]:
                    newsurfacey.append(Lines[i])
            if Lines[i][1] == line[1]:
                if Lines[i][0] == yplanelines[index][0]:
                    newsurfacey.append(Lines[i])
            if Lines[i][1] == yplanelines[index][1]:
                if Lines[i][0] == line[0]:
                    newsurfacey.append(Lines[i])
            if Lines[i][1] == yplanelines[index][1]:
                if Lines[i][0] == line[1]:
                    newsurfacey.append(Lines[i])
                    
    if len(newsurfacey)>0:                
        Surfaces.append(newsurfacey)

for i in range(0,len(Surfaces)):
    if len(Surfaces[i])==4:
        x=Surfaces[i][1]
        y=Surfaces[i][2]
        if Surfaces[i][0][0] != Surfaces[i][1][0] and Surfaces[i][0][0] != Surfaces[i][1][1] and Surfaces[i][0][1] != Surfaces[i][1][0] and Surfaces[i][0][1] != Surfaces[i][1][1]:
            Surfaces[i][1]=y
            Surfaces[i][2]=x
    elif len(Surfaces[i])==8:
        x=Surfaces[i][1]
        y=Surfaces[i][2]
        w=Surfaces[i][5]
        z=Surfaces[i][6]
        if Surfaces[i][0][0] != Surfaces[i][1][0] and Surfaces[i][0][0] != Surfaces[i][1][1] and Surfaces[i][0][1] != Surfaces[i][1][0] and Surfaces[i][0][1] != Surfaces[i][1][1]:
            Surfaces[i][1]=y
            Surfaces[i][2]=x
        if Surfaces[i][4][0] != Surfaces[i][5][0] and Surfaces[i][4][0] != Surfaces[i][5][1] and Surfaces[i][4][1] != Surfaces[i][5][0] and Surfaces[i][4][1] != Surfaces[i][5][1]:
            Surfaces[i][5]=z
            Surfaces[i][6]=w  
            
Surfacesindexes=[]       
 
for i in range(0,len(Surfaces)):
    Surfacesindexes.append([])
    for j in range(0,len(Surfaces[i])):
        for k in range(0,len(Lines)):
            if Surfaces[i][j][0] == Lines[k][0] and Surfaces[i][j][1] == Lines[k][1]:
                Surfacesindexes[i].append(k)      
                
for i in range(0,len(Surfaces)):
    if len(Surfaces[i]) == 4:
        if Surfaces[i][0][1] != Surfaces[i][1][0]:
            if Surfaces[i][0][1] != Surfaces[i][1][1]:
                if Surfacesindexes[i][0] != 0:
                    Surfacesindexes[i][0]=-Surfacesindexes[i][0]
                else:
                    Surfacesindexes[i][0]="-0.0"
                if Surfaces[i][0][0] != Surfaces[i][1][0]:
                    if Surfacesindexes[i][1] != 0:
                        Surfacesindexes[i][1] = -Surfacesindexes[i][1]
                    else:
                        Surfacesindexes[i][1] = "-0.0"
            else:
                if Surfacesindexes[i][1] != 0:
                    Surfacesindexes[i][1] = -Surfacesindexes[i][1]
                else:
                    Surfacesindexes[i][1] = "-0.0"
                
        if Surfaces[i][2][1] != Surfaces[i][3][0]:
            if Surfaces[i][2][1] != Surfaces[i][3][1]:
                if Surfacesindexes[i][2] != 0:
                    Surfacesindexes[i][2]=-Surfacesindexes[i][2]
                else:
                    Surfacesindexes[i][2] = "-0.0"
                    
                if Surfaces[i][2][0] != Surfaces[i][3][0]:
                    if Surfacesindexes[i][3] !=0:
                        Surfacesindexes[i][3] = -Surfacesindexes[i][3]
                    else:
                        Surfacesindexes[i][3] = "-0.0"
                        
            else:
                if Surfacesindexes[i][3] !=0:
                    Surfacesindexes[i][3] = -Surfacesindexes[i][3]
                else:
                    Surfacesindexes[i][3] = "-0.0"
                        
    else:
        if Surfaces[i][0][1] != Surfaces[i][1][0]:
            if Surfaces[i][0][1] != Surfaces[i][1][1]:
                if Surfacesindexes[i][0] != 0:
                    Surfacesindexes[i][0]=-Surfacesindexes[i][0]
                else:
                    Surfacesindexes[i][0]="-0.0"
                if Surfaces[i][0][0] != Surfaces[i][1][0]:
                    if Surfacesindexes[i][1] != 0:
                        Surfacesindexes[i][1] = -Surfacesindexes[i][1]
                    else:
                        Surfacesindexes[i][1] = "-0.0"
            else:
                if Surfacesindexes[i][1] != 0:
                    Surfacesindexes[i][1] = -Surfacesindexes[i][1]
                else:
                    Surfacesindexes[i][1] = "-0.0"
                
        if Surfaces[i][2][1] != Surfaces[i][3][0]:
            if Surfaces[i][2][1] != Surfaces[i][3][1]:
                if Surfacesindexes[i][2] != 0:
                    Surfacesindexes[i][2]=-Surfacesindexes[i][2]
                else:
                    Surfacesindexes[i][2] = "-0.0"
                    
                if Surfaces[i][2][0] != Surfaces[i][3][0]:
                    if Surfacesindexes[i][3] !=0:
                        Surfacesindexes[i][3] = -Surfacesindexes[i][3]
                    else:
                        Surfacesindexes[i][3] = "-0.0"
            else:
                if Surfacesindexes[i][3] != 0:
                    Surfacesindexes[i][3] = -Surfacesindexes[i][3]
                else:
                    Surfacesindexes[i][3] = "-0.0"
        
        if Surfaces[i][4][1] != Surfaces[i][5][0]:
            if Surfaces[i][4][1] != Surfaces[i][5][1]:
                if Surfacesindexes[i][4] != 0:
                    Surfacesindexes[i][4]=-Surfacesindexes[i][4]
                else:
                    Surfacesindexes[i][4]="-0.0"
                if Surfaces[i][4][0] != Surfaces[i][5][0]:
                    if Surfacesindexes[i][5] != 0:
                        Surfacesindexes[i][5] = -Surfacesindexes[i][5]
                    else:
                        Surfacesindexes[i][5] = "-0.0"
            else:
                if Surfacesindexes[i][5] != 0:
                    Surfacesindexes[i][5] = -Surfacesindexes[i][5]
                else:
                    Surfacesindexes[i][5] = "-0.0"
                
        if Surfaces[i][6][1] != Surfaces[i][7][0]:
            if Surfaces[i][6][1] != Surfaces[i][7][1]:
                if Surfacesindexes[i][6] != 0:
                    Surfacesindexes[i][6]=-Surfacesindexes[i][6]
                else:
                    Surfacesindexes[i][6] = "-0.0"
                    
                if Surfaces[i][6][0] != Surfaces[i][7][0]:
                    if Surfacesindexes[i][7] !=0:
                        Surfacesindexes[i][7] = -Surfacesindexes[i][7]
                    else:
                        Surfacesindexes[i][7] = "-0.0" 
            else:
                if Surfacesindexes[i][7] != 0:
                    Surfacesindexes[i][7] = -Surfacesindexes[i][7]
                else:
                    Surfacesindexes[i][7] = "-0.0"      
     
##################################################################################################################
                      
#Available but commented out here is the chance to test the geometry with just 
#points and lines and surfaces defined. It should look here as it looks at the very end, but
#we've yet to define surfaces and volumes.                      

##################################################################################################################



os.chdir(floc)
geometry = open('Testgeometry.geo','w')

for i in range(0,len(Points)):
    geometry.write("Point(" + str(i+1) + ") = {" + str(Points[i][0]) + ", " + str(Points[i][1]) + ", " + str(Points[i][2]) + ", " + "10};" +"\n")
            
for j in range(0,len(Lines)):
    geometry.write("Line(" + str(j+1) + ") = {" + str(Lines[j][0]+1) + ", " + str(Lines[j][1]+1) + "};" +"\n")

for k in range(0,len(Surfacesindexes)):
    string = "Line Loop(%d) = {" % (k+1)
    for l in range(0,len(Surfacesindexes[k])):
        if l < (len(Surfacesindexes[k])-1):
            if float(Surfacesindexes[k][l])>0:
                string = string + str(Surfacesindexes[k][l]+1)+", "
            elif float(Surfacesindexes[k][l])<0:
                string = string + str(Surfacesindexes[k][l]-1)+", "
            elif Surfacesindexes[k][l] == "-0.0":
                string = string + str(float(Surfacesindexes[k][l]) -1)+", "
            else:
                string = string + str(Surfacesindexes[k][l]+1)+", "
            
        else:
            if float(Surfacesindexes[k][l])>0:
                string = string + str(Surfacesindexes[k][l]+1)+"};"
            elif float(Surfacesindexes[k][l])<0:
                string = string + str(Surfacesindexes[k][l]-1)+"};"
            elif Surfacesindexes[k][l] == "-0.0":
                string = string + str(float(Surfacesindexes[k][l]) -1)+"};"
            else:
                string = string + str(Surfacesindexes[k][l]+1)+"};"
                                
    geometry.write(string +"\n")
    geometry.write("Plane Surface(%d) = {%d};\n" % (k+1,k+1))
    
geometry.close()
        
##################################################################################################################
