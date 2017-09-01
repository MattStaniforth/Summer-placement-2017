import os
import math

directory = input('Input the full directory of the output file in which you want the output saved as a string (ie "C:\Users\me\Desktop") ')

################################################################################
################################################################################
################################################################################

#This code can produce either a "wall" geometry (explained in documentation) or
#a beamline geometry to user specifications. It contains the ability to create
#a kinked beamline.

#UPDATE 24/08/17: This code can now produce the relevant .feml files for any of 
#the above choices. This is possible because volume and surface labels are fixed
#for these geometries. Many options in the .feml files that get set up may not 
#be what the user wants - but these are easy to change. It can be helpful when 
#building a .feml file to have a base to work from. 

#This relies on the user, when generating the mesh from the geometry, naming the
#mesh file with exactly the same name as the geometry.

#In both the wall and the beamline we assume for simplicity that the wall or
#beamline respectively is to be made out of pure Fe56. This can be changed in
#the .feml file afterwards if necessary by the user very easily. We also assume
#for simplicity that the void area in the wall example and the beamline region
#in the beamline example are to be vacuous regions. This can similarly be
#changed retrospectively by the user if necessary.

#Future updates possible: Include ability to write more complicated materials 
#into the .feml at the user's specification (IE allow user to input "steel", 
#'copper', etc.). Include possibility to have user input centimetres, as opposed 
#to metres. Currently we think it's better results if you put units in metres as 
#opposed to centimetres or anything else, and then convert.

################################################################################
################################################################################
################################################################################

which = input('Wall or Beamline? (0 for Wall or 1 for beamline) ')

################################################################################

if which == 1: #The user has chosen to define a beamline geometry.
    
    kink = input('Input 1 for a straight beamline or 0 for a kinked beamline ')

    if kink == 1: #Here the user has specified a straight beamline geometry. The
                  #information we need for this is the dimensions of the outer
                  #shielding, the width and height of the actual beamline, and
                  #the length of the source volume sitting in the end of the 
                  #beamline.

        shield = input('Enter the dimensions of the outer shield ((x,y,z) format) - all dimensions input should be in units of metres: ')
        beamline = input('Enter the width and height of the beamline ((s,t) format): ')
        source = input('Enter the length of the source volume: ')
        se = input('Enter the number of energy groups you\'re using. You must include all groups below the one you want. If you want group 45 for example, you must include 46 and 47, and you should in-put a value of 3 here. If using only the bottom energy group, put 1: ')
        ss = input('Enter the strength of the source in neutrons per unit volume for each energy group (Example: If using two energy groups, input "1e7 1e6" where you have 1e7 neutrons per unit volume for one group and 1e6 for the other group. If using just one energy group, put one value): ')
        aop = input('Enter the polar angle order for the angular expansion(where we are using the HAAR_WAVELETS option): ')
        aoa = input('Enter the azimuthal angle order for the angular expansion: ')

        x=float(shield[0])
        y=float(shield[1])
        z=float(shield[2])

        s=float(beamline[0])
        t=float(beamline[1])

        d=float(source)

        Points=[]
        Lines=[]
        Lineloops=[] #IE surfaces
        Volumes=[]

#First we define the points.

        #Points for the outer shield
        Point1=(0,0,0)
        Points.append((0,0,0))
        Point2=(x,0,0)
        Points.append((x,0,0))
        Point3=(x,y,0)
        Points.append((x,y,0))
        Point4=(0,y,0)
        Points.append((0,y,0))
        Point5=(0,0,z)
        Points.append((0,0,z))
        Point6=(x,0,z)
        Points.append((x,0,z))
        Point7=(x,y,z)
        Points.append((x,y,z))
        Point8=(0,y,z)
        Points.append((0,y,z))

        #Points for the front of the source cube
        Point9=(x/2 - s/2,y/2 - t/2,0)
        Points.append((x/2 - s/2,y/2 - t/2,0))
        Point10=(x/2 + s/2,y/2 - t/2,0)
        Points.append((x/2 + s/2,y/2 - t/2,0))
        Point11=(x/2 + s/2,y/2 + t/2,0)
        Points.append((x/2 + s/2,y/2 + t/2,0))
        Point12=(x/2 - s/2,y/2 + t/2,0)
        Points.append((x/2 - s/2,y/2 + t/2,0))

        #Points for the back of the source cube/front of the beamline
        Point13=(x/2 - s/2,y/2 - t/2,d)
        Points.append((x/2 - s/2,y/2 - t/2,d))
        Point14=(x/2 + s/2,y/2 - t/2,d)
        Points.append((x/2 + s/2,y/2 - t/2,d))
        Point15=(x/2 + s/2,y/2 + t/2,d)
        Points.append((x/2 + s/2,y/2 + t/2,d))
        Point16=(x/2 - s/2,y/2 + t/2,d)
        Points.append((x/2 - s/2,y/2 + t/2,d))
    
        #Points for the end of the beamline/target area
        Point17=(x/2 - s/2,y/2 - t/2,z)
        Points.append((x/2 - s/2,y/2 - t/2,z))
        Point18=(x/2 + s/2,y/2 - t/2,z)
        Points.append((x/2 + s/2,y/2 - t/2,z))
        Point19=(x/2 + s/2,y/2 + t/2,z)
        Points.append((x/2 + s/2,y/2 + t/2,z))
        Point20=(x/2 - s/2,y/2 + t/2,z)
        Points.append((x/2 - s/2,y/2 + t/2,z))
    
#Now we define the lines. Unlike in the code which generates the "benchmark
#beamline", here we have simply hard-coded what the lines should be.

        #Lines making up the Outer shield
        #Front face
        Line1=(1,2)
        Lines.append((1,2))
        Line2=(2,3)
        Lines.append((2,3))
        Line3=(3,4)
        Lines.append((3,4))
        Line4=(4,1)
        Lines.append((4,1))
        #Back face
        Line5=(5,6)
        Lines.append((5,6))
        Line6=(6,7)
        Lines.append((6,7))
        Line7=(7,8)
        Lines.append((7,8))
        Line8=(8,5)
        Lines.append((8,5))
        #Along the shield
        Line9=(1,5)
        Lines.append((1,5))
        Line10=(2,6)
        Lines.append((2,6))
        Line11=(3,7)
        Lines.append((3,7))
        Line12=(4,8)
        Lines.append((4,8))
    
        #Lines making up the source and beamline
        #Front of source
        Line13=(9,10)
        Lines.append((9,10))
        Line14=(10,11)
        Lines.append((10,11))
        Line15=(11,12)
        Lines.append((11,12))
        Line16=(12,9)
        Lines.append((12,9))
        #Back of source/front of beamline
        Line17=(13,14)
        Lines.append((13,14))
        Line18=(14,15)
        Lines.append((14,15))
        Line19=(15,16)
        Lines.append((15,16))
        Line20=(16,13)
        Lines.append((16,13))
        #End of beamline/target
        Line21=(17,18)
        Lines.append((17,18))
        Line22=(18,19)
        Lines.append((18,19))
        Line23=(19,20)
        Lines.append((19,20))
        Line24=(20,17)
        Lines.append((20,17))
        #Lines along source cube
        Line25=(9,13)
        Lines.append((9,13))
        Line26=(10,14)
        Lines.append((10,14))
        Line27=(11,15)
        Lines.append((11,15))
        Line28=(12,16)
        Lines.append((12,16))
        #Lines along beamline
        Line29=(13,17)
        Lines.append((13,17))
        Line30=(14,18)
        Lines.append((14,18))
        Line31=(15,19)
        Lines.append((15,19))
        Line32=(16,20)
        Lines.append((16,20))
        
#Now we define the surfaces

        #Line loops for surfaces
        #Outer shield
        Lineloop1=(-4,12,8,-9)
        Lineloops.append(Lineloop1)
        Lineloop2=(-9,1,10,-5)
        Lineloops.append(Lineloop2)
        Lineloop3=(2,11,-6,-10)
        Lineloops.append(Lineloop3)
        Lineloop4=(-12,-3,11,7)
        Lineloops.append(Lineloop4)
        Lineloop5=(1,2,3,4,13,14,15,16)
        Lineloops.append(Lineloop5)
        Lineloop6=(5,6,7,8,21,22,23,24)
        Lineloops.append(Lineloop6)
        #Source cube
        Lineloop7=(13,14,15,16)
        Lineloops.append(Lineloop7)
        Lineloop8=(17,18,19,20) #Back of source cube also front of beamline
        Lineloops.append(Lineloop8)
        Lineloop9=(-26,14,27,-18)
        Lineloops.append(Lineloop9)
        Lineloop10=(-15,27,19,-28)
        Lineloops.append(Lineloop10)
        Lineloop11=(-16,28,20,-25)
        Lineloops.append(Lineloop11)
        Lineloop12=(13,26,-17,-25)
        Lineloops.append(Lineloop12)
        #Beamline
        Lineloop13=(17,30,-21,-29)
        Lineloops.append(Lineloop13)
        Lineloop14=(18,31,-22,-30)
        Lineloops.append(Lineloop14)
        Lineloop15=(-19,31,23,-32)
        Lineloops.append(Lineloop15)
        Lineloop16=(-29,-20,32,24)
        Lineloops.append(Lineloop16)
        Lineloop17=(21,22,23,24)
        Lineloops.append(Lineloop17)
        
#Finally the volumes
        #Volumes
        Volume1=(7,8,9,10,11,12)
        Volumes.append(Volume1)
        Volume2=(13,14,15,16,17,8)
        Volumes.append(Volume2)
        Volume3=(1,2,3,4,5,6,9,10,11,12,13,14,15,16) #Everything without the faces of the source cube and beamline.
        Volumes.append(Volume3)
        
        os.chdir(directory)
        
        geometry=open('Beamlinegeometry.txt','w')
        
################################################################################
#The following section is just writing what we've got to a text file in the 
#appropriate syntax for Gmesh to read it.
################################################################################  
   
        for i in range(0,len(Points)):
            geometry.write("Point(" + str(i+1) + ") = {" + str(Points[i][0]) + ", " + str(Points[i][1]) + ", " + str(Points[i][2]) + ", " + "10};" +"\n")
            
        for j in range(0,len(Lines)):
            geometry.write("Line(" + str(j+1) + ") = {" + str(Lines[j][0]) + ", " + str(Lines[j][1]) + "};" +"\n")
        
        for k in range(0,len(Lineloops)):
            string = "Line Loop(%d) = {" % (k+1)
            for l in range(0,len(Lineloops[k])):
                if l < (len(Lineloops[k])-1):
                    string = string + str(Lineloops[k][l])+", "
                else:
                    string = string + str(Lineloops[k][l])+"};"
            geometry.write(string +"\n")
            geometry.write("Plane Surface(%d) = {%d};\n" % (k+1,k+1))
        
        for m in range(0,len(Volumes)):
            string2 = "Surface Loop(" + str(m+1) + ") = {"
            for n in range(0,len(Volumes[m])):
                if n < (len(Volumes[m])-1):
                    string2 = string2 + str(Volumes[m][n])+", "
                else:
                    string2 = string2 + str(Volumes[m][n])+"};"
            geometry.write(string2 +"\n")
            geometry.write("Volume(%d) = {%d};\n" % (m+1,m+1))
            
        geometry.write("Physical Surface(100) = {5, 7};\n")
        geometry.write("Physical Surface(200) = {6, 17};\n")
        geometry.write("Physical Surface(300) = {1};\n")
        geometry.write("Physical Surface(400) = {2};\n")
        geometry.write("Physical Surface(500) = {3};\n")
        geometry.write("Physical Surface(600) = {4};\n")
        geometry.write("Physical Volume(700) = {1}; //Source volume\n") #Physical Volume(700) is the source cube
        geometry.write("Physical Volume(800) = {2}; //Beamline\n") #Physical Volume(800) is the Beamline
        geometry.write("Physical Volume(900) = {3}; //Outer shielding\n") #Physical Volume 900 is the Outer shielding
        
        geometry.close()
        
        feml = open('rad_Beamlinegeometry.txt','w')
        
        feml.writelines(['<?xml version=\'1.0\' encoding=\'utf-8\'?>\n',
        '<FETCH_only_radiation_options>\n',
        '<geometry>\n',
        '<dimension>\n',
        '<integer_value rank="0">3</integer_value>\n',
        '</dimension>\n',
        '<mesh name="CoordinateMesh">\n',
        '<from_file file_name="Beamlinegeometry">\n',
        '<format name="gmsh"/>\n',
        '<stat>\n',
        '<include_in_stat/>\n',
        '</stat>\n',
        '</from_file>\n',
        '</mesh>\n',
        '<mesh name="RadParticleMesh">\n',
        '<from_mesh>\n',
        '<mesh name="CoordinateMesh"/>\n',
        '<stat>\n',
        '<exclude_from_stat/>\n',
        '</stat>\n',
        '</from_mesh>\n',
        '</mesh>\n',
        '<mesh name="RadParticleMaterialMesh">\n',
        '<from_mesh>\n',
        '<mesh name="CoordinateMesh"/>\n',
        '<mesh_continuity>\n',
        '<string_value>discontinuous</string_value>\n',
        '</mesh_continuity>\n',
        '<stat>\n',
        '<exclude_from_stat/>\n',
        '</stat>\n',
        '</from_mesh>\n',
        '</mesh>\n',
        '<mesh name="RadParticleMeshCG">\n',
        '<from_mesh>\n',
        '<mesh name="CoordinateMesh"/>\n',
        '<mesh_continuity>\n',
        '<string_value>continuous</string_value>\n',
        '</mesh_continuity>\n',
        '<stat>\n',
        '<exclude_from_stat/>\n',
        '</stat>\n',
        '</from_mesh>\n',
        '</mesh>\n',
        '<mesh name="RadParticleMeshSGS">\n',
        '<from_mesh>\n',
        '<mesh name="CoordinateMesh"/>\n',
        '<mesh_continuity>\n',
        '<string_value>discontinuous</string_value>\n',
        '</mesh_continuity>\n',
        '<stat>\n',
        '<exclude_from_stat/>\n',
        '</stat>\n',
        '</from_mesh>\n',
        '</mesh>\n',
        '<mesh name="OutputMesh">\n',
        '<from_mesh>\n',
        '<mesh name="CoordinateMesh"/>\n',
        '<stat>\n',
        '<exclude_from_stat/>\n',
        '</stat>\n',
        '</from_mesh>\n',
        '</mesh>\n',
        '<quadrature>\n',
        '<degree>\n',
        '<integer_value rank="0">4</integer_value>\n',
        '</degree>\n',
        '</quadrature>\n',
        '</geometry>\n',
        '<io>\n',
        '<dump_format>\n',
        '<string_value>vtk</string_value>\n',
        '</dump_format>\n',
        '<dump_period_in_timesteps>\n',
        '<constant>\n',
        '<integer_value rank="0">1</integer_value>\n',
        '</constant>\n',
        '</dump_period_in_timesteps>\n',
        '<output_mesh name="OutputMesh"/>\n',
        '<stat/>\n',
        '</io>\n',
        '<timestepping>\n',
        '<current_time>\n',
        '<real_value rank="0">0.0</real_value>\n',
        '</current_time>\n',
        '<timestep>\n',
        '<real_value rank="0">1.0</real_value>\n',
        '</timestep>\n',
        '<finish_time>\n',
        '<real_value rank="0">1.0</real_value>\n',
        '</finish_time>\n',
        '</timestepping>\n',
        '<particle charge="Neutral" name="Neutron">\n',
        '<method name="Deterministic">\n',
        '<equation name="TimeIndependent">\n',
        '<group_iteration/>\n',
        '</equation>\n',
        '<group_set name="All">\n',
        '<number_of_groups>\n',
        '<integer_value rank="0">'+str(se)+'</integer_value>\n',
        '</number_of_groups>\n',
        '<angular_discretisation name="RADIANT">\n',
        '<radiant_angular_discretisation name="HAAR_WAVELETS">\n',
        '<angle_order_polar>\n',
        '<integer_value rank="0">'+str(aop)+'</integer_value>\n',
        '</angle_order_polar>\n',
        '<angle_order_azimuthal>\n',
        '<integer_value rank="0">'+str(aoa)+'</integer_value>\n',
        '</angle_order_azimuthal>\n',
        '</radiant_angular_discretisation>\n',
        '<scatter_order>\n',
        '<integer_value rank="0">0</integer_value>\n',
        '</scatter_order>\n',
        '<store_inverse_of_D_matrix>\n',
        '<disable_internal_storage/>\n',
        '</store_inverse_of_D_matrix>\n',
        '<solver name="Internal">\n',
        '<iterative_method name="FGMRES"/>\n',
        '<preconditioner name="MULTIGRID"/>\n',
        '</solver>\n',
        '<angular_flux_field>\n',
        '<cg_mesh name="RadParticleMeshCG"/>\n',
        '<sgs_mesh name="RadParticleMeshSGS"/>\n',
        '<spatial_discretisation>\n',
        '<subgrid_scale/>\n',
        '</spatial_discretisation>\n',
        '<initial_condition name="WholeMesh">\n',
        '<constant>\n',
        '<real_value rank="0">0</real_value>\n',
        '</constant>\n',
        '</initial_condition>\n',
        '<fixed_source name="src_cube">\n',
        '<source_strength>\n',
        '<real_value shape="1" rank="1">'+str(ss)+'</real_value>\n',
        '</source_strength>\n',
        '<region_ids>\n',
        '<integer_value shape="1" rank="1">700</integer_value>\n',
        '</region_ids>\n',
        '</fixed_source>\n',
        '<output/>\n',
        '<stat/>\n',
        '<detectors>\n',
        '<include_in_detectors/>\n',
        '</detectors>\n',
        '<steady_state>\n',
        '<include_in_steady_state/>\n',
        '</steady_state>\n',
        '<consistent_interpolation/>\n',
        '</angular_flux_field>\n',
        '<scalar_field name="RadParticleScalarFlux">\n',
        '<diagnostic>\n',
        '<algorithm name="Internal"/>\n',
        '<mesh name="RadParticleMeshFullSGS"/>\n',
        '<output/>\n',
        '<stat/>\n',
        '<galerkin_projection>\n',
        '<discontinuous/>\n',
        '</galerkin_projection>\n',
        '</diagnostic>\n',
        '</scalar_field>\n',
        '<scalar_field name="RadParticleContinuousScalarFlux">\n',
        '<diagnostic>\n',
        '<algorithm name="Internal"/>\n',
        '<mesh name="RadParticleMeshCG"/>\n',
        '<output/>\n',
        '<stat/>\n',
        '<consistent_interpolation/>\n',
        '</diagnostic>\n',
        '</scalar_field>\n',
        '<scalar_field name="RadParticleScalarSGSComponent">\n',
        '<diagnostic>\n',
        '<algorithm name="Internal"/>\n',
        '<mesh name="RadParticleMeshSGS"/>\n',
        '<output/>\n',
        '<stat/>\n',
        '<galerkin_projection>\n',
        '<discontinuous/>\n',
        '</galerkin_projection>\n',
        '</diagnostic>\n',
        '</scalar_field>\n',
        '<vector_field name="RadParticleCurrent">\n',
        '<diagnostic>\n',
        '<algorithm name="Internal"/>\n',
        '<mesh name="RadParticleMeshFullSGS"/>\n',
        '<output/>\n',
        '<stat/>\n',
        '<galerkin_projection>\n',
        '<discontinuous/>\n',
        '</galerkin_projection>\n',
        '</diagnostic>\n',
        '</vector_field>\n',
        '<scalar_field name="RadParticleScalarSource">\n',
        '<diagnostic>\n',
        '<algorithm name="Internal"/>\n',
        '<mesh name="RadParticleMeshFullSGS"/>\n',
        '<output/>\n',
        '<stat/>\n',
        '<galerkin_projection>\n',
        '<discontinuous/>\n',
        '</galerkin_projection>\n',
        '</diagnostic>\n',
        '</scalar_field>\n',
        '</angular_discretisation>\n',
        '</group_set>\n',
        '<output_quantities>\n',
        '<quantity name="av_flux">\n',
        '<quantity_type name="Average_flux">\n',
        '<all_groups/>\n',
        '<all_regions/>\n',
        '</quantity_type>\n',
        '</quantity>\n',
        '</output_quantities>\n',
        '<material_data_set name="mat_dataset">\n',
        '<from_bugle particle_type="Neutron" file_name="bugle96">\n',
        '<start_group>\n',
        '<integer_value rank="0">'+str(int(47+(1-se)))+'</integer_value>\n',
        '</start_group>\n',
        '<physical_material name="shield">\n'   ,      
        '<isotopic_composition name="WeightPercent">\n',
        '<mass_density>\n',
        '<real_value rank="0">7.85</real_value>\n',
        '</mass_density>\n',
        '<isotope mass_number="56" name="Fe56">\n',
        '<real_value rank="0">1</real_value>\n',
        '</isotope>\n',
        '</isotopic_composition>\n',
        '</physical_material>\n',
        '<physical_material name="void">\n',
        '<isotopic_composition name="WeightPercent">\n',
        '<mass_density>\n',
        '<real_value rank="0">0</real_value>\n',
        '</mass_density>\n',
        '<isotope mass_number="56" name="Fe56">\n',
        '<real_value rank="0">1</real_value>\n',
        '</isotope>\n',
        '</isotopic_composition>\n',
        '</physical_material>\n',
        '</from_bugle>\n',
        '<convert name="cm_to_metre"/>\n',
        '</material_data_set>\n',
        '<material_mapping>\n',
        '<material_mesh name="RadParticleMaterialMesh"/>\n',
        '<region>\n',
        '<region_ids name="Outer_shield">\n',
        '<integer_value shape="1" rank="1">900</integer_value>\n',
        '<physical_material name="shield"/>\n',
        '</region_ids>\n',
        '<region_ids name="Src_cube">\n',
        '<integer_value shape="1" rank="1">700</integer_value>\n',
        '<physical_material name="void"/>\n',
        '</region_ids>\n',
        '<region_ids name="Beamline">\n',
        '<integer_value shape="1" rank="1">800</integer_value>\n',
        '<physical_material name="void"/>\n',
        '</region_ids>\n',
        '</region>\n',
        '</material_mapping>\n',
        '</method>\n',
        '</particle>\n',
        '</FETCH_only_radiation_options>\n'])

        feml.close()
        
################################################################################  
        
    else:
        
        #In the case we have a kink in the beamline. Now we need all the
        #information we had before, except we also need the angle of the kink,
        #and the length of the beamline after the kink.
        
        shield1 = input('Enter the dimensions of the outer shield before the kink ((x,y,z) format): ')
        angle = input('Enter the angle of the kink - assumed to be in the horizontal plane swept clockwise from the z axis - in radians: ')
        shield2 = input('Enter the length of the part of the beamline after the kink: ')
        beamline = input('Enter the width and height of the beamline ((s,t) format): ')
        source = input('Enter the length of the source volume: ')
        
        x=shield1[0]
        y=shield1[1]
        z=shield1[2]
        
        s=beamline[0]
        t=beamline[1]
    
        d=source
        
        w = angle
        
        l = shield2    
  
        Points=[]
        Lines=[]
        Lineloops=[]
        Volumes=[]

#First we define the points

        #Points for the outer shield before the kink
        Point1=(0,0,0)
        Points.append((0,0,0))
        Point2=(x,0,0)
        Points.append((x,0,0))
        Point3=(x,y,0)
        Points.append((x,y,0))
        Point4=(0,y,0)
        Points.append((0,y,0))
        Point5=(0,0,z)
        Points.append((0,0,z))
        Point6=(x,0,z)
        Points.append((x,0,z))
        Point7=(x,y,z)
        Points.append((x,y,z))
        Point8=(0,y,z)
        Points.append((0,y,z))    
    
        #Points for the front of the source cube
        Point9=(x/2 - s/2,y/2 - t/2,0)
        Points.append((x/2 - s/2,y/2 - t/2,0))
        Point10=(x/2 + s/2,y/2 - t/2,0)
        Points.append((x/2 + s/2,y/2 - t/2,0))
        Point11=(x/2 + s/2,y/2 + t/2,0)
        Points.append((x/2 + s/2,y/2 + t/2,0))
        Point12=(x/2 - s/2,y/2 + t/2,0)
        Points.append((x/2 - s/2,y/2 + t/2,0))
    
        #Points for the back of the source cube/front of the beamline
        Point13=(x/2 - s/2,y/2 - t/2,d)
        Points.append((x/2 - s/2,y/2 - t/2,d))
        Point14=(x/2 + s/2,y/2 - t/2,d)
        Points.append((x/2 + s/2,y/2 - t/2,d))
        Point15=(x/2 + s/2,y/2 + t/2,d)
        Points.append((x/2 + s/2,y/2 + t/2,d))
        Point16=(x/2 - s/2,y/2 + t/2,d)
        Points.append((x/2 - s/2,y/2 + t/2,d))
        
        #Points for the end of the beamline before the kink
        Point17=(x/2 - s/2,y/2 - t/2,z)
        Points.append((x/2 - s/2,y/2 - t/2,z))
        Point18=(x/2 + s/2,y/2 - t/2,z)
        Points.append((x/2 + s/2,y/2 - t/2,z))
        Point19=(x/2 + s/2,y/2 + t/2,z)
        Points.append((x/2 + s/2,y/2 + t/2,z))
        Point20=(x/2 - s/2,y/2 + t/2,z)
        Points.append((x/2 - s/2,y/2 + t/2,z))
        
        #Points for the end of the outer shield area after the kink
        Point21=(-l*math.sin(w),0,z+z*math.cos(w))
        Points.append(Point21)
        Point22=(x-l*math.sin(w),0,z+z*math.cos(w))
        Points.append(Point22)
        Point23=(x-l*math.sin(w),y,z+z*math.cos(w))
        Points.append(Point23)
        Point24=(-l*math.sin(w),y,z+z*math.cos(w))
        Points.append(Point24)
        
        #Points for the end of the beamline/target area after the kink
        Point25=(x/2 - s/2 - l*math.sin(w),y/2 - t/2,z+z*math.cos(w))
        Points.append(Point25)
        Point26=(x/2 + s/2 - l*math.sin(w),y/2 - t/2,z+z*math.cos(w))
        Points.append(Point26)
        Point27=(x/2 + s/2 - l*math.sin(w),y/2 + t/2,z+z*math.cos(w))
        Points.append(Point27)
        Point28=(x/2 - s/2 - l*math.sin(w),y/2 + t/2,z+z*math.cos(w))
        Points.append(Point28)
            
#Now we define the lines.
           
        #Lines making up the Outer shield
        #Front face
        Line1=(1,2)
        Lines.append((1,2))
        Line2=(2,3)
        Lines.append((2,3))
        Line3=(3,4)
        Lines.append((3,4))
        Line4=(4,1)
        Lines.append((4,1))
        #Back face before kink
        Line5=(5,6)
        Lines.append((5,6))
        Line6=(6,7)
        Lines.append((6,7))
        Line7=(7,8)
        Lines.append((7,8))
        Line8=(8,5)
        Lines.append((8,5))
        #Along the shield before kink
        Line9=(1,5)
        Lines.append((1,5))
        Line10=(2,6)
        Lines.append((2,6))
        Line11=(3,7)
        Lines.append((3,7))
        Line12=(4,8)
        Lines.append((4,8))
        
        #Lines making up the source and beamline before kink
        #Front of source
        Line13=(9,10)
        Lines.append((9,10))
        Line14=(10,11)
        Lines.append((10,11))
        Line15=(11,12)
        Lines.append((11,12))
        Line16=(12,9)
        Lines.append((12,9))
        #Back of source/front of beamline
        Line17=(13,14)
        Lines.append((13,14))
        Line18=(14,15)
        Lines.append((14,15))
        Line19=(15,16)
        Lines.append((15,16))
        Line20=(16,13)
        Lines.append((16,13))
        #End of beamline before kink
        Line21=(17,18)
        Lines.append((17,18))
        Line22=(18,19)
        Lines.append((18,19))
        Line23=(19,20)
        Lines.append((19,20))
        Line24=(20,17)
        Lines.append((20,17))
        #Lines along source cube
        Line25=(9,13)
        Lines.append((9,13))
        Line26=(10,14)
        Lines.append((10,14))
        Line27=(11,15)
        Lines.append((11,15))
        Line28=(12,16)
        Lines.append((12,16))
        #Lines along beamline before kink
        Line29=(13,17)
        Lines.append((13,17))
        Line30=(14,18)
        Lines.append((14,18))
        Line31=(15,19)
        Lines.append((15,19))
        Line32=(16,20)
        Lines.append((16,20))
        
        #Lines making up outer shield after kink
        Line33=(21,22)
        Lines.append(Line33)
        Line34=(22,23)
        Lines.append(Line34)
        Line35=(23,24)
        Lines.append(Line35)
        Line36=(24,21)
        Lines.append(Line36)
        Line37=(5,21)
        Lines.append(Line37)
        Line38=(6,22)
        Lines.append(Line38)
        Line39=(7,23)
        Lines.append(Line39)
        Line40=(8,24)
        Lines.append(Line40)
        
        #Lines making up beamline after kink
        #Lines along beamline
        Line41=(17,25)
        Lines.append(Line41)
        Line42=(18,26)
        Lines.append(Line42)
        Line43=(19,27)
        Lines.append(Line43)
        Line44=(20,28)
        Lines.append(Line44)
        #End of beamline/target
        Line45=(25,26)
        Lines.append(Line45)
        Line46=(26,27)
        Lines.append(Line46)
        Line47=(27,28)
        Lines.append(Line47)
        Line48=(28,25)
        Lines.append(Line48)
        
        #Line loops for surfaces
        #Outer shield
        Lineloop1=(-4,12,8,-9)
        Lineloops.append(Lineloop1)
        Lineloop2=(-9,1,10,-5)
        Lineloops.append(Lineloop2)
        Lineloop3=(2,11,-6,-10)
        Lineloops.append(Lineloop3)
        Lineloop4=(-12,-3,11,7)
        Lineloops.append(Lineloop4)
        Lineloop5=(1,2,3,4,13,14,15,16)
        Lineloops.append(Lineloop5)
        Lineloop6=(5,6,7,8,21,22,23,24)
        Lineloops.append(Lineloop6)
        #Source cube
        Lineloop7=(13,14,15,16)
        Lineloops.append(Lineloop7)
        Lineloop8=(17,18,19,20) #Back of source cube also front of beamline
        Lineloops.append(Lineloop8)
        Lineloop9=(-26,14,27,-18)
        Lineloops.append(Lineloop9)
        Lineloop10=(-15,27,19,-28)
        Lineloops.append(Lineloop10)
        Lineloop11=(-16,28,20,-25)
        Lineloops.append(Lineloop11)
        Lineloop12=(13,26,-17,-25)
        Lineloops.append(Lineloop12)
        #Beamline before kink
        Lineloop13=(17,30,-21,-29)
        Lineloops.append(Lineloop13)
        Lineloop14=(18,31,-22,-30)
        Lineloops.append(Lineloop14)
        Lineloop15=(-19,31,23,-32)
        Lineloops.append(Lineloop15)
        Lineloop16=(-29,-20,32,24)
        Lineloops.append(Lineloop16)
        Lineloop17=(21,22,23,24)
        Lineloops.append(Lineloop17)
        #Beamline after kink
        Lineloop18=(43,47,-44,-23)
        Lineloops.append(Lineloop18)
        Lineloop19=(42,46,-43,-22)
        Lineloops.append(Lineloop19)
        Lineloop20=(41,45,-42,-21)
        Lineloops.append(Lineloop20)
        Lineloop21=(44,48,-41,-24)
        Lineloops.append(Lineloop21)
        Lineloop22=(45,46,47,48)
        Lineloops.append(Lineloop22)
        #Outer shield after kink
        Lineloop23=(39,35,-40,-7)
        Lineloops.append(Lineloop23)
        Lineloop24=(38,34,-39,-6)
        Lineloops.append(Lineloop24)
        Lineloop25=(37,33,-38,-5)
        Lineloops.append(Lineloop25)
        Lineloop26=(40,36,-37,-8)
        Lineloops.append(Lineloop26)
        Lineloop27=(33,34,35,36,45,46,47,48)
        Lineloops.append(Lineloop27)
        
        #Volumes
        Volume1=(7,8,9,10,11,12) #Source cube
        Volumes.append(Volume1)
        Volume2=(8,13,14,15,16,18,19,20,21,22) #Beamline
        Volumes.append(Volume2)
        Volume3=(1,2,3,4,5,23,24,25,26,27,18,19,20,21,13,14,15,16,9,10,11,12) #Everything without the faces of the source cube and beamline.
        Volumes.append(Volume3)

################################################################################      
#We now write this to a text file in the Gmesh syntax.
################################################################################  

        os.chdir(directory)
        
        geometry=open('Beamlinegeometrybent.txt','w')
        
        for i in range(0,len(Points)):
            geometry.write("Point(" + str(i+1) + ") = {" + str(Points[i][0]) + ", " + str(Points[i][1]) + ", " + str(Points[i][2]) + ", " + "10};" +"\n")
            
        for j in range(0,len(Lines)):
            geometry.write("Line(" + str(j+1) + ") = {" + str(Lines[j][0]) + ", " + str(Lines[j][1]) + "};" +"\n")
        
        for k in range(0,len(Lineloops)):
            string = "Line Loop(%d) = {" % (k+1)
            for l in range(0,len(Lineloops[k])):
                if l < (len(Lineloops[k])-1):
                    string = string + str(Lineloops[k][l])+", "
                else:
                    string = string + str(Lineloops[k][l])+"};"
            geometry.write(string +"\n")
            geometry.write("Plane Surface(%d) = {%d};\n" % (k+1,k+1))
        
        for m in range(0,len(Volumes)):
            string2 = "Surface Loop(" + str(m+1) + ") = {"
            for n in range(0,len(Volumes[m])):
                if n < (len(Volumes[m])-1):
                    string2 = string2 + str(Volumes[m][n])+", "
                else:
                    string2 = string2 + str(Volumes[m][n])+"};"
            geometry.write(string2 +"\n")
            geometry.write("Volume(%d) = {%d};\n" % (m+1,m+1))
            
        geometry.close
            
        geometry.write("Physical Surface(100) = {5, 7};\n")
        geometry.write("Physical Surface(200) = {22, 27};\n")
        geometry.write("Physical Surface(300) = {1};\n")
        geometry.write("Physical Surface(400) = {2,25};\n")
        geometry.write("Physical Surface(500) = {3};\n")
        geometry.write("Physical Surface(600) = {4,23};\n")
        geometry.write("Physical Surface(700) = {26};\n")
        geometry.write("Physical Surface(800) = {24};\n")
        geometry.write("Physical Volume(1100) = {1}; //Source volume\n")
        geometry.write("Physical Volume(1200) = {2}; //Beamline\n")
        geometry.write("Physical Volume(1300) = {3}; /Outer shielding\n")
        
        feml = open('rad_Beamlinegeometrybent.txt','w')
        
        feml.writelines(['<?xml version=\'1.0\' encoding=\'utf-8\'?>\n',
        '<FETCH_only_radiation_options>\n',
        '<geometry>\n',
        '<dimension>\n',
        '<integer_value rank="0">3</integer_value>\n',
        '</dimension>\n',
        '<mesh name="CoordinateMesh">\n',
        '<from_file file_name="Beamlinegeometrybent">\n',
        '<format name="gmsh"/>\n',
        '<stat>\n',
        '<include_in_stat/>\n',
        '</stat>\n',
        '</from_file>\n',
        '</mesh>\n',
        '<mesh name="RadParticleMesh">\n',
        '<from_mesh>\n',
        '<mesh name="CoordinateMesh"/>\n',
        '<stat>\n',
        '<exclude_from_stat/>\n',
        '</stat>\n',
        '</from_mesh>\n',
        '</mesh>\n',
        '<mesh name="RadParticleMaterialMesh">\n',
        '<from_mesh>\n',
        '<mesh name="CoordinateMesh"/>\n',
        '<mesh_continuity>\n',
        '<string_value>discontinuous</string_value>\n',
        '</mesh_continuity>\n',
        '<stat>\n',
        '<exclude_from_stat/>\n',
        '</stat>\n',
        '</from_mesh>\n',
        '</mesh>\n',
        '<mesh name="RadParticleMeshCG">\n',
        '<from_mesh>\n',
        '<mesh name="CoordinateMesh"/>\n',
        '<mesh_continuity>\n',
        '<string_value>continuous</string_value>\n',
        '</mesh_continuity>\n',
        '<stat>\n',
        '<exclude_from_stat/>\n',
        '</stat>\n',
        '</from_mesh>\n',
        '</mesh>\n',
        '<mesh name="RadParticleMeshSGS">\n',
        '<from_mesh>\n',
        '<mesh name="CoordinateMesh"/>\n',
        '<mesh_continuity>\n',
        '<string_value>discontinuous</string_value>\n',
        '</mesh_continuity>\n',
        '<stat>\n',
        '<exclude_from_stat/>\n',
        '</stat>\n',
        '</from_mesh>\n',
        '</mesh>\n',
        '<mesh name="OutputMesh">\n',
        '<from_mesh>\n',
        '<mesh name="CoordinateMesh"/>\n',
        '<stat>\n',
        '<exclude_from_stat/>\n',
        '</stat>\n',
        '</from_mesh>\n',
        '</mesh>\n',
        '<quadrature>\n',
        '<degree>\n',
        '<integer_value rank="0">4</integer_value>\n',
        '</degree>\n',
        '</quadrature>\n',
        '</geometry>\n',
        '<io>\n',
        '<dump_format>\n',
        '<string_value>vtk</string_value>\n',
        '</dump_format>\n',
        '<dump_period_in_timesteps>\n',
        '<constant>\n',
        '<integer_value rank="0">1</integer_value>\n',
        '</constant>\n',
        '</dump_period_in_timesteps>\n',
        '<output_mesh name="OutputMesh"/>\n',
        '<stat/>\n',
        '</io>\n',
        '<timestepping>\n',
        '<current_time>\n',
        '<real_value rank="0">0.0</real_value>\n',
        '</current_time>\n',
        '<timestep>\n',
        '<real_value rank="0">1.0</real_value>\n',
        '</timestep>\n',
        '<finish_time>\n',
        '<real_value rank="0">1.0</real_value>\n',
        '</finish_time>\n',
        '</timestepping>\n',
        '<particle charge="Neutral" name="Neutron">\n',
        '<method name="Deterministic">\n',
        '<equation name="TimeIndependent">\n',
        '<group_iteration/>\n',
        '</equation>\n',
        '<group_set name="All">\n',
        '<number_of_groups>\n',
        '<integer_value rank="0">'+str(se)+'</integer_value>\n',
        '</number_of_groups>\n',
        '<angular_discretisation name="RADIANT">\n',
        '<radiant_angular_discretisation name="HAAR_WAVELETS">\n',
        '<angle_order_polar>\n',
        '<integer_value rank="0">'+str(aop)+'</integer_value>\n',
        '</angle_order_polar>\n',
        '<angle_order_azimuthal>\n',
        '<integer_value rank="0">'+str(aoa)+'</integer_value>\n',
        '</angle_order_azimuthal>\n',
        '</radiant_angular_discretisation>\n',
        '<scatter_order>\n',
        '<integer_value rank="0">0</integer_value>\n',
        '</scatter_order>\n',
        '<store_inverse_of_D_matrix>\n',
        '<disable_internal_storage/>\n',
        '</store_inverse_of_D_matrix>\n',
        '<solver name="Internal">\n',
        '<iterative_method name="FGMRES"/>\n',
        '<preconditioner name="MULTIGRID"/>\n',
        '</solver>\n',
        '<angular_flux_field>\n',
        '<cg_mesh name="RadParticleMeshCG"/>\n',
        '<sgs_mesh name="RadParticleMeshSGS"/>\n',
        '<spatial_discretisation>\n',
        '<subgrid_scale/>\n',
        '</spatial_discretisation>\n',
        '<initial_condition name="WholeMesh">\n',
        '<constant>\n',
        '<real_value rank="0">0</real_value>\n',
        '</constant>\n',
        '</initial_condition>\n',
        '<fixed_source name="src_cube">\n',
        '<source_strength>\n',
        '<real_value shape="1" rank="1">'+str(ss)+'</real_value>\n',
        '</source_strength>\n',
        '<region_ids>\n',
        '<integer_value shape="1" rank="1">1100</integer_value>\n',
        '</region_ids>\n',
        '</fixed_source>\n',
        '<output/>\n',
        '<stat/>\n',
        '<detectors>\n',
        '<include_in_detectors/>\n',
        '</detectors>\n',
        '<steady_state>\n',
        '<include_in_steady_state/>\n',
        '</steady_state>\n',
        '<consistent_interpolation/>\n',
        '</angular_flux_field>\n',
        '<scalar_field name="RadParticleScalarFlux">\n',
        '<diagnostic>\n',
        '<algorithm name="Internal"/>\n',
        '<mesh name="RadParticleMeshFullSGS"/>\n',
        '<output/>\n',
        '<stat/>\n',
        '<galerkin_projection>\n',
        '<discontinuous/>\n',
        '</galerkin_projection>\n',
        '</diagnostic>\n',
        '</scalar_field>\n',
        '<scalar_field name="RadParticleContinuousScalarFlux">\n',
        '<diagnostic>\n',
        '<algorithm name="Internal"/>\n',
        '<mesh name="RadParticleMeshCG"/>\n',
        '<output/>\n',
        '<stat/>\n',
        '<consistent_interpolation/>\n',
        '</diagnostic>\n',
        '</scalar_field>\n',
        '<scalar_field name="RadParticleScalarSGSComponent">\n',
        '<diagnostic>\n',
        '<algorithm name="Internal"/>\n',
        '<mesh name="RadParticleMeshSGS"/>\n',
        '<output/>\n',
        '<stat/>\n',
        '<galerkin_projection>\n',
        '<discontinuous/>\n',
        '</galerkin_projection>\n',
        '</diagnostic>\n',
        '</scalar_field>\n',
        '<vector_field name="RadParticleCurrent">\n',
        '<diagnostic>\n',
        '<algorithm name="Internal"/>\n',
        '<mesh name="RadParticleMeshFullSGS"/>\n',
        '<output/>\n',
        '<stat/>\n',
        '<galerkin_projection>\n',
        '<discontinuous/>\n',
        '</galerkin_projection>\n',
        '</diagnostic>\n',
        '</vector_field>\n',
        '<scalar_field name="RadParticleScalarSource">\n',
        '<diagnostic>\n',
        '<algorithm name="Internal"/>\n',
        '<mesh name="RadParticleMeshFullSGS"/>\n',
        '<output/>\n',
        '<stat/>\n',
        '<galerkin_projection>\n',
        '<discontinuous/>\n',
        '</galerkin_projection>\n',
        '</diagnostic>\n',
        '</scalar_field>\n',
        '</angular_discretisation>\n',
        '</group_set>\n',
        '<output_quantities>\n',
        '<quantity name="av_flux">\n',
        '<quantity_type name="Average_flux">\n',
        '<all_groups/>\n',
        '<all_regions/>\n',
        '</quantity_type>\n',
        '</quantity>\n',
        '</output_quantities>\n',
        '<material_data_set name="mat_dataset">\n',
        '<from_bugle particle_type="Neutron" file_name="bugle96">\n',
        '<start_group>\n',
        '<integer_value rank="0">'+str(int(47+(1-se)))+'</integer_value>\n',
        '</start_group>\n',
        '<physical_material name="shield">\n'   ,      
        '<isotopic_composition name="WeightPercent">\n',
        '<mass_density>\n',
        '<real_value rank="0">7.85</real_value>\n',
        '</mass_density>\n',
        '<isotope mass_number="56" name="Fe56">\n',
        '<real_value rank="0">1</real_value>\n',
        '</isotope>\n',
        '</isotopic_composition>\n',
        '</physical_material>\n',
        '<physical_material name="void">\n',
        '<isotopic_composition name="WeightPercent">\n',
        '<mass_density>\n',
        '<real_value rank="0">0</real_value>\n',
        '</mass_density>\n',
        '<isotope mass_number="56" name="Fe56">\n',
        '<real_value rank="0">1</real_value>\n',
        '</isotope>\n',
        '</isotopic_composition>\n',
        '</physical_material>\n',
        '</from_bugle>\n',
        '<convert name="cm_to_metre"/>\n',
        '</material_data_set>\n',
        '<material_mapping>\n',
        '<material_mesh name="RadParticleMaterialMesh"/>\n',
        '<region>\n',
        '<region_ids name="Outer_shield">\n',
        '<integer_value shape="1" rank="1">1300</integer_value>\n',
        '<physical_material name="shield"/>\n',
        '</region_ids>\n',
        '<region_ids name="Src_cube">\n',
        '<integer_value shape="1" rank="1">1100</integer_value>\n',
        '<physical_material name="void"/>\n',
        '</region_ids>\n',
        '<region_ids name="Beamline">\n',
        '<integer_value shape="1" rank="1">1200</integer_value>\n',
        '<physical_material name="void"/>\n',
        '</region_ids>\n',
        '</region>\n',
        '</material_mapping>\n',
        '</method>\n',
        '</particle>\n',
        '</FETCH_only_radiation_options>\n'])

        feml.close()
        
################################################################################   
       
else: 
    #In this case the user has chosen to define a wall geometry. This is 
    #explained in detail in the documentation. We need various information:
    #Wall dimensions (height, width, thickness)
    #Hole dimensions (Height and width)
    #Hole location (where exactly the hole is in the wall - it doesn't have to be
    #in the centre)
    #Source dimensions (Height, width, length)
    #Distance between source and wall (scalar)
    #Location of the source in relation to the wall
    #Similarly for the detector surface.
    
    #If the value to be input is a scalar, it need only be a number. If the 
    #input needed is a tuple (ie an (x,y) co-ordinate, it should be put in in 
    #that format. 

    walldim = input('Wall dimensions: Enter the dimensions of the wall ((x,y,z) format where z is thickness): ')
    holedim = input('Hole dimensions: Enter the height and width of the hole ((h,w) format): ')
    holeloc = input('Hole location: Enter the displacement of the bottom left corner of the hole in the xy-plane from the bottom left corner of the wall ((x,y) format): ')
    srcdim = input('Source dimensions: Enter the dimensions of the source cube ((x,y,z) format): ')
    srctowall = input('Source to wall distance: Enter the distance between the furthest face of the source cube and the wall (in the z direction): ')
    srcloc = input('Source location: Enter the displacement of the source cube in the xy-plane from the bottom left corner of the wall ((x,y) format): ')
    detdim = input('Detector dimensions: Enter the dimensions of the detector ((x,y) format): ')
    detloc = input('Detector location: Enter the displacement of the detector in the xy-plane from the bottom left corner of the wall ((x,y) format): ')
    dettowall = input('Detector to wall: Enter the distance between the detector and the wall: ')

    wdx=float(walldim[0])
    wdy=float(walldim[1])
    wdz=float(walldim[2])

    hdx=float(holedim[0])
    hdy=float(holedim[1])

    hlx=float(holeloc[0])
    hly=float(holeloc[1])
    
    sdx=float(srcdim[0])
    sdy=float(srcdim[1])
    sdz=float(srcdim[2])
    
    s2w=float(srctowall)
    
    slx=float(srcloc[0])
    sly=float(srcloc[1])
    
    ddx=float(detdim[0])
    ddy=float(detdim[1])
    
    dlx=float(detloc[0])
    dly=float(detloc[1])
    
    d2w=float(dettowall)
    
    cubex = wdx
    cubey = wdy
    cubez = s2w + wdz + d2w
    
#First we define the points

    Points = []
    
    #Outer cube front face
    Points.append((0,0,0)) #0
    Points.append((0,cubey,0)) #1
    Points.append((cubex,cubey,0)) #2
    Points.append((cubex,0,0)) #3
    
    #Outer cube back face
    Points.append((0,0,cubez)) #4
    Points.append((0,cubey,cubez)) #5
    Points.append((cubex,cubey,cubez)) #6
    Points.append((cubex,0,cubez)) #7
    
    #Wall front face
    Points.append((0,0,s2w)) #8
    Points.append((0,cubey,s2w)) #11
    Points.append((cubex,cubey,s2w)) #10
    Points.append((cubex,0,s2w)) #9
    
    #Wall back face
    Points.append((0,0,s2w+wdz)) #12
    Points.append((0,cubey,s2w+wdz))
    Points.append((cubex,cubey,s2w+wdz))
    Points.append((cubex,0,s2w+wdz))
    
    #Hole front face
    
    Points.append((hlx,hly,s2w)) #16
    Points.append((hlx+hdx,hly,s2w))
    Points.append((hlx+hdx,hly+hdy,s2w))
    Points.append((hlx,hly+hdy,s2w))
    
    #Hole back face
    
    Points.append((hlx,hly,s2w+wdz)) #20
    Points.append((hlx+hdx,hly,s2w+wdz))
    Points.append((hlx+hdx,hly+hdy,s2w+wdz))
    Points.append((hlx,hly+hdy,s2w+wdz))    
    
    #Source front face
    Points.append((slx,sly,0)) #24
    Points.append((slx+sdx,sly,0))
    Points.append((slx+sdx,sly+sdy,0))
    Points.append((slx,sly+sdy,0))
    
    #Source back face
    Points.append((slx,sly,sdz)) #28
    Points.append((slx+sdx,sly,sdz))
    Points.append((slx+sdx,sly+sdy,sdz))
    Points.append((slx,sly+sdy,sdz))
    
    #Detector
    
    Points.append((dlx,dly,cubez)) #32
    Points.append((dlx+ddx,dly,cubez))
    Points.append((dlx+ddx,dly+ddy,cubez))
    Points.append((dlx,dly+ddy,cubez))
    
    os.chdir(directory)
    
    geometry=open('Wallgeometry.txt','w')
    
    for i in range(0,len(Points)):
        geometry.write("Point(" + str(i+1) + ") = {" + str(Points[i][0]) + ", " + str(Points[i][1]) + ", " + str(Points[i][2]) + ", " + "10};" +"\n")

#We now define and write the lines directly to the text file, because there's
#nothing else we need to do.        
    geometry.writelines([
    'Line(1) = {4, 3};\n',
    'Line(2) = {3, 2};\n',
    'Line(3) = {2, 1};\n',
    'Line(4) = {1, 4};\n',
    'Line(5) = {12, 11};\n',
    'Line(6) = {11, 10};\n',
    'Line(7) = {10, 9};\n',
    'Line(8) = {9, 12};\n',
    'Line(9) = {16, 15};\n',
    'Line(10) = {15, 14};\n',
    'Line(11) = {14, 13};\n',
    'Line(12) = {13, 16};\n',
    'Line(13) = {8, 7};\n',
    'Line(14) = {7, 6};\n',
    'Line(15) = {6, 5};\n',
    'Line(16) = {5, 8};\n',
    'Line(17) = {4, 12};\n',
    'Line(18) = {3, 11};\n',
    'Line(19) = {2, 10};\n',
    'Line(20) = {1, 9};\n',
    'Line(21) = {12, 16};\n',
    'Line(22) = {11, 15};\n',
    'Line(23) = {10, 14};\n',
    'Line(24) = {9, 13};\n',
    'Line(25) = {16, 8};\n',
    'Line(26) = {15, 7};\n',
    'Line(27) = {14, 6};\n',
    'Line(28) = {13, 5};\n',
    'Line(29) = {28, 27};\n',
    'Line(30) = {27, 26};\n',
    'Line(31) = {26, 25};\n',
    'Line(32) = {25, 28};\n',
    'Line(33) = {32, 31};\n',
    'Line(34) = {31, 30};\n',
    'Line(35) = {30, 29};\n',
    'Line(36) = {29, 32};\n',
    'Line(37) = {20, 19};\n',
    'Line(38) = {19, 18};\n',
    'Line(39) = {18, 17};\n',
    'Line(40) = {17, 20};\n',
    'Line(41) = {24, 23};\n',
    'Line(42) = {23, 22};\n',
    'Line(43) = {22, 21};\n',
    'Line(44) = {21, 24};\n',
    'Line(45) = {36, 35};\n',
    'Line(46) = {35, 34};\n',
    'Line(47) = {34, 33};\n',
    'Line(48) = {33, 36};\n',
    'Line(49) = {28, 32};\n',
    'Line(50) = {27, 31};\n',
    'Line(51) = {26, 30};\n',
    'Line(52) = {25, 29};\n',
    'Line(53) = {20, 24};\n',
    'Line(54) = {19, 23};\n',
    'Line(55) = {18, 22};\n',
    'Line(56) = {17, 21};\n',
    'Line Loop(59) = {1, 2, 3, 4, -32, -31, -30, -29};\n',
    'Plane Surface(59) = {59};\n',
    'Line Loop(62) = {5, 6, 7, 8, -40, -39, -38, -37};\n',
    'Plane Surface(62) = {62};\n',
    'Line Loop(66) = {9, 10, 11, 12, -44, -43, -42, -41};\n',
    'Plane Surface(66) = {66};\n',
    'Line Loop(69) = {13, 14, 15, 16, -48, -47, -46, -45};\n',
    'Plane Surface(69) = {69};\n',
    'Line Loop(70) = {29, 30, 31, 32};\n',
    'Plane Surface(70) = {70};\n',
    'Line Loop(72) = {36, 33, 34, 35};\n',
    'Plane Surface(72) = {72};\n',
    'Line Loop(73) = {37, 38, 39, 40};\n',
    'Plane Surface(73) = {73};\n',
    'Line Loop(74) = {41, 42, 43, 44};\n',
    'Plane Surface(74) = {74};\n',
    'Line Loop(75) = {45, 46, 47, 48};\n',
    'Plane Surface(75) = {75};\n',
    'Line Loop(77) = {29, 50, -33, -49};\n',
    'Plane Surface(77) = {77};\n',
    'Line Loop(79) = {30, 51, -34, -50};\n',
    'Plane Surface(79) = {79};\n',
    'Line Loop(81) = {31, 52, -35, -51};\n',
    'Plane Surface(81) = {81};\n',
    'Line Loop(83) = {32, 49, -36, -52};\n',
    'Plane Surface(83) = {83};\n',
    'Line Loop(85) = {37, 54, -41, -53};\n',
    'Plane Surface(85) = {85};\n',
    'Line Loop(87) = {38, 55, -42, -54};\n',
    'Plane Surface(87) = {87};\n',
    'Line Loop(89) = {39, 56, -43, -55};\n',
    'Plane Surface(89) = {89};\n',
    'Line Loop(91) = {40, 53, -44, -56};\n',
    'Plane Surface(91) = {91};\n',
    'Line Loop(93) = {1, 18, -5, -17};\n',
    'Plane Surface(93) = {93};\n',
    'Line Loop(95) = {2, 19, -6, -18};\n',
    'Plane Surface(95) = {95};\n',
    'Line Loop(97) = {3, 20, -7, -19};\n',
    'Plane Surface(97) = {97};\n',
    'Line Loop(99) = {4, 17, -8, -20};\n',
    'Plane Surface(99) = {99};\n',
    'Line Loop(101) = {5, 22, -9, -21};\n',
    'Plane Surface(101) = {101};\n',
    'Line Loop(103) = {6, 23, -10, -22};\n',
    'Plane Surface(103) = {103};\n',
    'Line Loop(105) = {7, 24, -11, -23};\n',
    'Plane Surface(105) = {105};\n',
    'Line Loop(107) = {8, 21, -12, -24};\n',
    'Plane Surface(107) = {107};\n',
    'Line Loop(109) = {9, 26, -13, -25};\n',
    'Plane Surface(109) = {109};\n',
    'Line Loop(111) = {10, 27, -14, -26};\n',
    'Plane Surface(111) = {111};\n',
    'Line Loop(113) = {11, 28, -15, -27};\n',
    'Plane Surface(113) = {113};\n',
    'Line Loop(115) = {12, 25, -16, -28};\n',
    'Plane Surface(115) = {115};\n',
    'Surface Loop(117) = {72, 83, 77, 79, 81, 70};\n',
    'Volume(117) = {117};\n',
    'Surface Loop(120) = {101, 103, 105, 107, 66, 62, 87, 89, 91, 85};\n',
    'Volume(120) = {120};\n',
    'Surface Loop(122) = {99, 59, 93, 95, 97, 77, 79, 81, 83, 72, 62, 85, 87, 89, 91, 66, 109, 111, 113, 115, 69, 75};\n',
    'Volume(122) = {122};\n',
    'Physical Surface(126) = {75}; //Detector surface\n', 
    'Physical Surface(127) = {69};\n',
    'Physical Surface(128) = {70};\n',
    'Physical Surface(129) = {59};\n',
    'Physical Surface(130) = {113};\n',
    'Physical Surface(131) = {111};\n',
    'Physical Surface(132) = {115};\n',
    'Physical Surface(133) = {105};\n',
    'Physical Surface(134) = {103};\n',
    'Physical Surface(135) = {101};\n',
    'Physical Surface(136) = {107};\n',
    'Physical Surface(137) = {97};\n',
    'Physical Surface(138) = {95};\n',
    'Physical Surface(139) = {93};\n',
    'Physical Surface(140) = {99};\n',
    'Physical Surface(141) = {109};\n',
    'Physical Volume(123) = {117}; //Source volume\n',
    'Physical Volume(124) = {120}; //Wall\n',
    'Physical Volume(125) = {122}; //Void volume\n',
    '\n'])
    
    geometry.close()