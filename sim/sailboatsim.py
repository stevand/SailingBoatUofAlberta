#Author: Shou Zhang

import math
import numpy as np
import matplotlib.pyplot as plt
import time

class Sim_Boat:
    Jz=10000
    beta=0.05
    p8=2.0
    p3=6000
    m=300.0
    p2=0.2
    p7=1
    alphar=2000
    p6=1.0
    alphas=1000.0
    q=1
    zeta=math.pi/4
    dt=0.1

    def __init__(self,x,y,theta,v,omega,a,psi):
        self.x=[x]
        self.y=[y]
        self.theta=[theta]
        self.v=[v]
        self.omega=[omega]
        self.a=a
        self.psi=psi

    def controller(self):
         wx_ap=self.a*math.cos(self.psi-self.theta[-1])-self.v[-1]
         wy_ap=self.a*math.sin(self.psi-self.theta[-1])
         psi_ap=math.atan2(wy_ap,wx_ap)
         a_ap=math.sqrt(wx_ap*wx_ap+wy_ap*wy_ap)

         if math.cos(math.atan2(-self.y[-1],-self.x[-1])-self.psi)+math.cos(self.zeta)<0:
            if math.cos(self.theta[-1])*math.cos(self.psi+self.zeta)+math.sin(self.theta[-1])*math.sin(self.psi+self.zeta)-math.cos(self.theta[-1])*math.cos(self.psi-self.zeta)-math.sin(self.theta[-1])*math.sin(self.psi-self.zeta)>0:
                self.q=2
            else:
                self.q=3
         else:
            self.q=1

         if self.q==1: thetabar=math.atan2(-self.y[-1],-self.x[-1])
         if self.q==2: thetabar=math.pi+self.psi-self.zeta
         if self.q==3: thetabar=math.pi+self.psi+self.zeta

         rudder=(math.pi/4)*math.sin(self.theta[-1]-thetabar);
         if math.cos(self.theta[-1]-thetabar)<0:
             rudder=(math.pi/4)*np.sign(rudder)
         sail1=(math.pi/2)*0.5*(math.cos(psi_ap)+1);
         return rudder, sail1

    def boatModel(self,rudder,sail1):         
         wx_ap=self.a*math.cos(self.psi-self.theta[-1])-self.v[-1]
         wy_ap=self.a*math.sin(self.psi-self.theta[-1])
         psi_ap=math.atan2(wy_ap,wx_ap)
         a_ap=math.sqrt(wx_ap*wx_ap+wy_ap*wy_ap)
         if math.cos(psi_ap)+math.cos(sail1)<0:
             sail=math.atan(math.tan(psi_ap))
         else:
             sail=-np.sign(math.sin(psi_ap))*sail1
         fr = -self.alphar*self.v[-1]*math.sin(rudder)
         fs = self.alphas*a_ap*math.sin(sail-psi_ap)

         x_t=self.x[-1]+(self.v[-1]*math.cos(self.theta[-1])+self.beta*self.a*math.cos(self.psi))*self.dt
         y_t=self.y[-1]+(self.v[-1]*math.sin(self.theta[-1])+self.beta*self.a*math.sin(self.psi))*self.dt
         theta_t=self.theta[-1]+self.omega[-1]*self.dt
         v_t=self.v[-1]+(1/self.m)*(math.sin(sail)*fs+math.sin(rudder)*fr-self.p2*self.v[-1]*self.v[-1])*self.dt
         omega_t=self.omega[-1]+(1/self.Jz)*((self.p6-self.p7*math.cos(sail))*fs+self.p8*math.cos(rudder)*fr-self.p3*self.omega[-1]*self.v[-1])*self.dt;
         self.x.append(x_t)
         self.y.append(y_t)
         self.theta.append(theta_t)
         self.v.append(v_t)
         self.omega.append(omega_t)

if __name__=='__main__':
    x=-200
    y=100
    theta=0
    v=1
    omega = 0
    a=4
    psi=0
    myboat=Sim_Boat(x,y,theta,v,omega,a,psi)

    N=10000    
    for i in range(N):
        rudder, sail1=myboat.controller()
        myboat.boatModel(rudder,sail1)
        
    plt.plot(myboat.x,myboat.y)
    plt.xlim([-300,300])
    plt.ylim([-300,300])
    plt.title('boat path')
    plt.xlabel('x/m')
    plt.ylabel('y/m')
    plt.quiver(-100,-100,math.cos(myboat.psi),math.sin(myboat.psi),scale=8)
    plt.text(-100,-150,'wind')
    plt.grid()
    plt.show()