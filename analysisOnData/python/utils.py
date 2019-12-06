def get_LHEScaleWeight_meaning(wid=0):
    if wid==0:
        return 'muR1_muF1'
    elif wid==1:
        return 'muR1_muF2'
    elif wid==2:
        return 'muR1_muF0p5'
    elif wid==3:
        return 'muR2_muF1'
    elif wid==4:
        return 'muR2_muF2'
    elif wid==5:
        return 'muR2_muF0p5'
    elif wid==6:
        return 'muR0p5_muF1'
    elif wid==7:
        return 'muR0p5_muF2'
    elif wid==8:
        return 'muR0p5_muF0p5'

def get_LHEPdfWeight_meaning(wid=0):
    if wid<100:
        return 'NNPDF_'+str(wid)+'replica'
    elif wid==100:
        return 'NNPDF_alphaSDown'
    elif wid==101:
        return 'NNPDF_alphaSUp'
    else:
        return 'NNPDF_XXXreplica'
        

