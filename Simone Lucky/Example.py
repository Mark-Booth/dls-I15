#Definisco una funzione che mi calcola la funzione di Planck (Ideale) fornendo
#la temperatura che voglio utilizzare (T) e la lunghezza d'onda (x). 
def Planck(T,x):
    a=numpy.expm1(0.0144043/(x*10**(-9))/T)
    P=1/(x*10**(-9))**5*3.74691*10**(-16)*1/(a-1)
    return P

 #Programma che carica un file di temperatura (raw) lo normalizza e me lo 
#grafica in un plot per ottenere la mia funzione di Planck   
import numpy
import matplotlib.pyplot as plt
import math
#mi carica la colonna x ed y dal mio file .txt e le tiene in memoria
x,y=numpy.loadtxt('T_40_1.txt',unpack=True)
xC,yC=numpy.loadtxt('Calib.txt',unpack=True)

P=Planck(2436,x)
y2=y*10
Norm=y/yC*P


    
fig = plt.figure()

ax1 = fig.add_subplot(111)

#stile del grafico che plotto
ax1.set_title("Raw data")    
ax1.set_xlabel('wavelength (nm)')
ax1.set_ylabel('Intensity')


ax1.plot(x,Norm, 'r', label='the data')
#ax1.plot(x,y, 'r',x,y2,'bs', label='the data')

leg = ax1.legend()

plt.show()



#figure(1)
#plot(x,y,'k-', linewidth=2)
#xlabel('Incident angle (deg)',fontsize=18)
#ylabel('Attenuation length ($\mu m$)',fontsize=18)
