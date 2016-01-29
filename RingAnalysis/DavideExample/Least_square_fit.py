#===============================================================================
# IMPORT EXPERIMENT SCAN
#===============================================================================
from dlstools import dataloader
d=dataloader.dlsloader('')

#===============================================================================
# DEFINITIONS OF THE FITTING FUNCTION: LORENTZIAN = LINEAR BACKGROUND
#===============================================================================
def one_lorentz_linear(x,a,x0,FWHM,x_1,x_0):
    return a*1/(1+((x-x0)/(FWHM/2))**2)+x_1*x+x_0


#===============================================================================
# MAIN PROGRAM
#===============================================================================
first_scan=538330
last_scan=538366
parameters_list=[1,1,1,1,1] #Initial guess for the parameters of the fitting function
for scan_num in arange(first_scan,last_scan+1,1):
    d(scan_num)
    fit_parameters,cov_matrix=curve_fit(one_lorentz_linear,d.eta,d.APD,p0=parameters_list) #Least square fitting routine