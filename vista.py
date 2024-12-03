import pyvista as pv

a=1
def visu(a):
    
    if a ==1:
        
        pl = pv.Plotter()
        
        pl.import_vrml('gate_visu.wrl')
        
        pl.show()
        
    else: return 0
    
    
if __name__ == "__main__":
    a=1
    visu(a)
    
    
