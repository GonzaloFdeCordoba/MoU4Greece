#!/usr/bin/python
# -*- encoding: utf-8 -*-

import pylab as pl
import numpy as np
from scipy.optimize import fsolve
import timeit
from GreeceModelRBFOC import GreeceModelRBFOC

'''
This file calibrates the model explained in Public Debt Frontiers:
The Greek Case. Once calibrated it plots
The graph of the frontier at the calibration point.'''

tic=timeit.default_timer()
#%%
#Normalize GDP to 100 and fix macro data to that level
Y = 100
G = 0.45337099*Y
I = 0.2236*Y
C = Y-I
L = 57.50
H = 100
#Basic data and calibration for 2002-2006
RB = 0.0410 #Interest rate differential = 0%
RB1 = RB
tauk = 0.1640
taus = 0.3560
tauc = 0.1480
taul = 0.4100
taupi = 0.2500
beta = 1/(1+RB)   #Target RB=0.01
deltap = 0.0800
deltag = 0.0400
Ip = 0.8500*I
Ig = 0.1500*I
Lp = 0.8065*L  # Target Lg/Lp=0.24
Lg = 0.1935*L
Kp = Ip/deltap
Kg = Ig/deltag
R = (((1/beta)-1)/(1-tauk))+deltap
alphap = R*Kp/Y
alphag = (Kg/Kp)*alphap  #Target Rg=Rp
alphal = 1-alphap-alphag
eta = 0.477891259111057  #0.4326
mu = 0.6008
A = Y/(Kp**alphap*Kg**alphag*(mu*Lp**eta+(1-mu)*Lg**eta)**(alphal/eta))
rho = -1.0
Wp = (alphal*A*mu*Lp**(eta-1)*Kp**alphap*Kg**alphag* \
       (mu*Lp**eta+(1-mu)*Lg**eta)**(alphal/eta-1))/(1+taus)
Wprem = 1.4
Wg = Wprem*Wp
omega = 1/(1+(Wg/Lg)**rho)
pi_c = 1
theta1 = 0.4467
theta2 = Ig/G
theta3 = (1+taus)*Wg*Lg/G
theta4 = 1-theta1-theta2-theta3
Q = ((1-taul)/(1+tauc))*(H-Lp-Lg)*Wp
gamma = C/(C+Q)
#%%
#Get values from calibration
Ip = deltap*Kp
Ig = deltag*Kg
L = Lg+Lp
Y = A*Kp**alphap*Kg**alphag*(mu*Lp**eta+(1-mu)*Lg**eta)**(alphal/eta)
R = alphap*A*Kp**(alphap-1)*Kg**alphag*(mu*Lp**eta+(1-mu)*Lg**eta)**(alphal/eta)
PmKg = alphag*A*Kp**alphap*Kg**(alphag-1)* \
       (mu*Lp**eta+(1-mu)*Lg**eta)**(alphal/eta)
Wp = (alphal*A*mu*Lp**(eta-1)*Kp**alphap*Kg**alphag* \
        (mu*Lp**eta+(1-mu)*Lg**eta)**(alphal/eta-1))/(1+taus)
PmLg = (alphal*A*(1-mu)*Lg**(eta-1)*Kp**alphap*Kg**alphag* \
        (mu*Lp**eta+(1-mu)*Lg**eta)**(alphal/eta-1))/(1+taus)
Cg = theta1*G
Z = theta4*G
Cp = Y-Ip-Ig-Cg
C = Cp+pi_c*Cg
Wg = (omega/(1-omega))**(-1.0/(2.0*rho))*(theta3*G/(1+taus))**(1.0/2.0)
PI = Y-(1+taus)*Wp*Lp-R*Kp
IF = tauc*Cp+taul*(Wp*Lp+Wg*Lg)+tauk*(R-deltap)*Kp+taus*(Wp*Lp+Wg*Lg)+taupi*PI
B = (IF-G)/RB
#%%

#%Compute a steady state for each value of G/Y
init = 0.01    #%Lowest G/Y ratio
final = 0.65    # %Highest G/Y ratio
T = 1000    #%Density 1/T

def g(x):
    return GreeceModelRBFOC(x, param)

varNames = ["Kpss", "Kgss", "Lpss", "Lgss", "Bss", "Ipss", "Igss", "Lss", \
            "Yss", "Rss", "PmKg", "Wpss", "PmLg", "Gss", "Cgss", "Zss", \
            "Cpss", "Css", "Wgss", "PIss", "IFss", "ratGY"]

for name in varNames:
    globals()[name] = np.zeros(T)
    
x0 = [Kp, Kg, Lp, Lg, B]
for t in range(T):
    ratGY[t] = init+(final-init)*t/(T-1)
    param = [alphap, alphag, RB1, deltap, deltag, gamma, rho, theta1, \
             theta2, theta3, pi_c, mu, eta, omega, tauc, taul, tauk, taus, \
             taupi, H, A, ratGY[t], RB]
      
    crit = 1e-10
    maxit = 1000
    sol = fsolve(g, x0, xtol=1.e-06)
    Kpss[t] = sol[0]
    Kgss[t] = sol[1]
    Lpss[t] = sol[2]
    Lgss[t] = sol[3]
    Bss[t] = sol[4]
    Ipss[t] = deltap*Kpss[t]
    Igss[t] = deltag*Kgss[t]
    Lss[t] = Lgss[t]+Lpss[t]
    Yss[t] = A*Kpss[t]**alphap*Kgss[t]**alphag*(mu*Lpss[t]**eta+ \
            (1-mu)*Lgss[t]**eta)**(alphal/eta)
    Rss[t] = alphap*A*Kpss[t]**(alphap-1)*Kgss[t]**alphag*(mu*Lpss[t]** \
            eta+(1-mu)*Lgss[t]**eta)**(alphal/eta)
    PmKg[t] = alphag*A*Kpss[t]**alphap*Kgss[t]**(alphag-1)*(mu*Lpss[t]**eta+ \
            (1-mu)*Lgss[t]**eta)**(alphal/eta)
    Wpss[t] = (alphal*A*mu*Lpss[t]**(eta-1)*Kpss[t]**alphap*Kgss[t]**alphag* \
            (mu*Lpss[t]**eta+(1-mu)*Lgss[t]**eta)**(alphal/eta-1))/(1+taus)
    PmLg[t] = (alphal*A*(1-mu)*Lgss[t]**(eta-1)*Kpss[t]**alphap*Kgss[t]** \
            alphag*(mu*Lpss[t]**eta+(1-mu)*Lgss[t]**eta)** \
            (alphal/eta-1))/(1+taus)
    Gss[t] = ratGY[t]*Yss[t]
    Cgss[t] = theta1*Gss[t]
    Zss[t] = theta4*Gss[t]
    Cpss[t] = Yss[t]-Ipss[t]-Igss[t]-Cgss[t]-RB*Bss[t]
    Css[t] = Cpss[t]+pi_c*Cgss[t]
    Wgss[t] = (omega/(1-omega))**(-1.0/(2.0*rho))*(theta3*Gss[t]/(1+taus))**(1.0/2.0)
    PIss[t] = Yss[t]-(1+taus)*Wpss[t]*Lpss[t]-Rss[t]*Kpss[t]
    IFss[t] = tauc*Cpss[t]+(taul+taus)*(Wpss[t]*Lpss[t]+Wgss[t]*Lgss[t])+ \
              tauk*(Rss[t]-deltap)*Kpss[t]+taupi*PIss[t]
    tb = t
    if Bss[t] <= 0:
        break
    x0 = [Kpss[t], Kgss[t], Lpss[t], Lgss[t], Bss[t]]
    
toc=timeit.default_timer()
print "time=%f" % (toc - tic )

dataGreece = np.array([[2002, 45.1, 101.7],
                       [2003, 44.7, 97.4],
                       [2004, 45.5, 98.6],
                       [2005, 44.6, 100],
                       [2006, 45.3, 106.1],
                       [2007, 47.5, 105.4],
                       [2008, 50.6, 110.7],
                       [2009, 54, 129.7],
                       [2010, 51.5, 148.3],
                       [2011, 51.8, 170.6]])
    
pl.figure(figsize=(8, 8))
pl.xlim(40,55)
#pl.xticks([0,50,100])
pl.ylim(35,160)
#pl.yticks([180,200,220,240])
pl.plot(100*Gss/Yss, 100*Bss/Yss)
pl.title('Debt and Expenditures')
pl.plot(dataGreece[:,1], dataGreece[:,2], 'ro')
pl.ylabel('Debt to GDP')
pl.xlabel('Expenditures to GDP')

pl.show()
