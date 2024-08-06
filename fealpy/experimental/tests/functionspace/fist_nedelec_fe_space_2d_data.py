import numpy as np

# 定义多个典型的 FirstNedelecDof2d 对象
# mesh = TriangleMesh.from_box(nx = 1,ny =1)
# p =  10
init_mesh_data = [
    {
        "edof":5,
        "cdof":20,
        "gdof":65,
        "cell2dof":np.array([[10, 11, 12, 13, 14,  9,  8,  7,  6,  5, 20, 21, 22, 23, 24, 25,
                              26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
                              42, 43, 44],
                             [14, 13, 12, 11, 10, 19, 18, 17, 16, 15,  0,  1,  2,  3,  4, 45,
                              46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61,
                              62, 63, 64]],dtype=np.int32)
    

        
    }
]
