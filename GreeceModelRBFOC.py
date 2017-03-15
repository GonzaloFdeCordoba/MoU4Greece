#!/usr/bin/python

def GreeceModelRBFOC(x0, param):
    alphap = param[0]
    alphag = param[1]
    RB1 = param[2]
    deltap = param[3]
    deltag = param[4]
    gamma = param[5]
    rho = param[6]
    theta1 = param[7]
    theta2 = param[8]
    theta3 = param[9]
    pi_c = param[10]
    mu = param[11]
    eta = param[12]
    omega = param[13]
    tauc = param[14]
    taul = param[15]
    tauk = param[16]
    taus = param[17]
    taupi = param[18]
    H = param[19]
    A = param[20]
    ratGY = param[21]
    RB = param[22]
    
    Kpss = x0[0]
    Kgss = x0[1]
    Lpss = x0[2]
    Lgss = x0[3]
    Bss = x0[4]
    f = [i for i in range(5)]

    Ipss = deltap*Kpss
    Igss = deltag*Kgss
    Yss = A*Kpss**alphap*Kgss**alphag*(mu*Lpss**eta+(1-mu)*Lgss**eta)** \
    ((1-alphap-alphag)/eta)
    Rss = alphap*A*Kpss**(alphap-1)*Kgss**alphag*(mu*Lpss**eta+(1-mu)* \
    Lgss**eta)**((1-alphap-alphag)/eta)
    Wpss = ((1-alphap-alphag)*A*mu*Lpss**(eta-1)*Kpss**alphap*Kgss**alphag* \
    (mu*Lpss**eta+(1-mu)*Lgss**eta)**((1-alphap-alphag)/eta-1))/(1+taus)
    Gss = ratGY*Yss
    Cgss = theta1*Gss
    Cpss = Yss-Ipss-Igss-Cgss-RB*Bss
    Css = Cpss+pi_c*Cgss
    Wgss = (omega/(1-omega))**(-1.0/(2.0*rho))*(theta3*Gss/(1+taus))**(1.0/2.0)
    PIss = Yss-(1+taus)*Wpss*Lpss-Rss*Kpss
    IFss = tauc*Cpss+(taul+taus)*(Wpss*Lpss+Wgss*Lgss)+tauk*(Rss-deltap)* \
       Kpss+taupi*PIss

    f[0] = Gss+RB*Bss-IFss
    f[1] = Igss-theta2*Gss
    f[2] = Css*((1-gamma)/gamma)-((1-taul)/(1+tauc))*(H-Lpss-Lgss)*Wpss
    f[3] = (Rss-deltap)*(1-tauk)-RB1
    f[4] = Lgss-(omega/(1-omega))**(1.0/(2.0*rho))* \
           (theta3*Gss/(1+taus))**(1.0/2.0)
    return f




