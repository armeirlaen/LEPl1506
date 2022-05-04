import coda_toolbox as coda
import glm_toolbox as glm
import pandas as pd

for Nsuj in [1,2,3,5,6]:
    for j in [1,2,3,4,5,6,7,8,9,10,11,12]:
        
        if j <10 :
            path = "GLM/S"+str(Nsuj)+"_00"+str(j)+".txt"
        else :
            path = "GLM/S"+str(Nsuj)+"_0"+str(j)+".txt"
        #makercadre = [1,2,3]
        #markermanip = [5,6,7,8]

        df = pd.read_csv(path,header = 0)
        #fd2 = glm.import_data(path2)
        base = df.LowAcc_X[0]
        for i in range(len(df.LowAcc_X)):
            df.LowAcc_X[i] -= base
        #print(df['LowAcc_X'])
        """
        #df.drop(columns=["Marker1_Visibility", "Marker2_Visibility","Marker3_Visibility",'Marker4_Visibility','Marker5_Visibility',
                         'Marker4_Visibility','Marker5_Visibility','Marker6_Visibility','Marker7_Visibility','Marker8_Visibility',
                         'Marker9_Visibility','Marker10_Visibility','Marker11_Visibility','Marker4_X', 'Marker4_Y', 'Marker4_Z',
                         'Marker9_X', 'Marker9_Y', 'Marker9_Z','Marker10_X','Marker10_Y', 'Marker10_Z',
                         'Marker11_X', 'Marker11_Y', 'Marker11_Z'], inplace = True)

        #df.rename(columns={'time': 'timec','Marker5_X' : 'Marker4_X','Marker5_Y' : 'Marker4_Y','Marker5_Z' : 'Marker4_Z',
                           'Marker6_X' : 'Marker5_X','Marker6_Y' : 'Marker5_Y','Marker6_Z' : 'Marker5_Z',
                           'Marker7_X' : 'Marker6_X','Marker7_Y' : 'Marker6_Y','Marker7_Z' : 'Marker6_Z',
                           'Marker8_X' : 'Marker7_X','Marker8_Y' : 'Marker7_Y','Marker8_Z' : 'Marker7_Z'}, inplace = True)
        """

        
        #
        
        if j < 10:
            df.to_csv("GLM/S"+str(Nsuj)+"_00"+str(j)+".txt",header  = True,index = False)
        else :
            df.to_csv("GLM/S"+str(Nsuj)+"_0"+str(j)+".txt",header  = True,index = False)

#file = open("Coda/S1_002.txt",'w')
#file.write(df.to_string())
#file.close()



