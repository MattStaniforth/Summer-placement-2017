README

The following is a short guide on how the Python scripts contained in this folder work, and how to use them. It also contains some small suggestions if the scripts are not working. The main suggestion is to only try to input geometries that are physically possible. 

Important: We use the perspective where the y axis is vertical, the x axis is horizontal and parallel to the screen you look at, and the z axis is perpendicular to the screen you look at. When we mention "length" or "thickness" we mean distance in the direction of the z axis. Height is therefore referring to distance on the y axis, and width is referring to the x axis. When referring to the beamline we mean specifically the vacuum region in the centre of the geometry, not the outer shielding part. 

When mentioning input, we mean the input prompted for when you run the script. It will prompt for user input, and no other input is required other than what is prompted for.

--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------

1. Beamlineorwall.py

This script can create two types of geometry. It is possible to create what we're calling a "wall" geometry, or a usual beamline geometry.

i. Beamline geometry

a. Straight beamline

The straight beamline geometry consists of a beamline (a rectangular prism), some outer shielding around it, and a source volume. The source volume is placed at the start of the beamline, and has the same height and width as the beamline itself. For this reason, the only user input required in the "length" of the source volume. We will already know it's height and width because we'll've already defined the height and width of the beamline.

You need to input three things. Firstly, the dimensions of the outer shielding (height, width, length). Secondly, the height and width of the beamline. We already know it's length because we put the length of the outer shielding in, and we presume that the beamline goes all the way through the outer shielding. Lastly, the length of the source volume, as explained above.

The code then creates the geometry, calls it Beamlinegeometry.txt, and puts it in whatever directory you specified when it prompted you for one.

--------------------------------------------------------------------------------------------

b. Kinked beamline

Very similar to the above. The only extra input information is length of the beamline after the kink, and angle of the kink.

--------------------------------------------------------------------------------------------

ii. Wall geometry

The wall geometry consists of a Source volume, a "wall" and a detector. The detector is a surface, as opposed to a volume, and so the output quantity would be a surface current. The wall has a hole in it. This isn't particularly useful as any sort of practical example, but it's interesting and probably quite useful in terms of trying out different settings in .feml files to see what changing various options can do to the output solutions. The user needs to input:

-The dimensions of the wall (height, weight, thickness).
-The dimensions of the hole (height and width).
-The "location" of the hole. The hole does not have to be in the centre of the wall, it can be anywhere else in the wall. If viewing the geometry with the y axis pointing upwards, the x axis pointing right, and the z axis coming out of the screen towards you, the input should be the distance in x and y of the bottom left corner of the hole from the bottom left corner of the wall.
For example, if your wall has corner points at coordinates (0,0,3), (0,2,3), (2,2,3), (2,0,3), (0,0,3.1), (0,2,3.1), (2,2,3.1), (2,0,3.1), and you set the (x,y) for hole location to be (1,1), with your hole having height and width (0.1,0.1), you would end up with a hole in the wall with points at coordinates (1,1,3),( 1,1.1,3), (1.1,1.1,3), (1.1,1,3), (1,1,3.1), (1,1.1,3.1), (1.1,1.1,3.1,), (1.1,1,3.1).
-Source dimensions(height, width, length).
-Source to wall distance. This is the distance between the closest two surfaces of the source and wall to eachother. The nearest face of the source to the wall will be parallel with the wall. 
-Source location. This is defined in a similar manner to the location of the hole, defined by an x and y distance of the bottom left corner of the source from the bottom left corner of the source (where the perspective and the term bottom left are defined as in the section on the location of the hole).
-Detector dimensions (height and width). The "detector" is a rectangular surface on the other side of the wall from the hole. 
-Detector location. This is defined similarly to hole location and source location.
-Detector to wall. This is the distance between the detector and the nearest face of the wall.

Once these are input, you should be ready to go. The script calculates the location of each point it needs to define based on what the above inputs were. It then defines the lines, surfaces, volumes, physical surfaces and physical volumes.

The script then creates the geometry and calls it Wallgeometry.txt, and saves it in whatever directory you specified when prompted for one.

--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------

2.Benchmarkbeamline.py

This script creates a beamline geometry which is divided up into sections. 

The point of this is that when running a goal based adapt on a beamline, if you're adapting to a "detector region" at the end of the beamline, you may not have enough angles for the angle order in use to get neutrons to the end of the beamline. This is typical for beamline type problems (particularly longer, thinner beamlines), and this may cause the solver to fail (or give a ridiculous answer). 

The point of dividing the beamline into sections is that now, you can do a goal based adapt on regions progressively further along the beamline, to see how far you can get with a certain angle order. Instead of adapting to a "detector region" at the end of the beamline, you could instead adapt to a region less far down the beamline, and see if the adapt works with that goal. This enables you to better estimate the required number of angles for specific beamline type problems.

Although the geometry created by this script is simple (simply a beamline with some outer shielding), this will give a good approximation for the number of angles required for fetch to solve on beamlines of different widths and lengths.

IMPORTANT:

1.) You must still define Volumes, Physical Surfaces and Physical Volumes yourself. The script will not do this for you. 

2.) Input a geometry that makes sense. If you try to put in a beamline which is wider than it's outer shielding, the code will simply break. If you try to put in a beamline whose length is shorter than the length of the source cube, the code will break.

3.) The script seems to work for me when I try any geometrically and Physically possible geometry - but I have not properly tested it. If something's not working, and you're sure that your geometry makes good sense, there may well be something wrong with the code. 



