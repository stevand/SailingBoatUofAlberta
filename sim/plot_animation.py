# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 11:09:36 2019

@author: eqgui
"""

import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import euler_simplified2 as e1
import json

with open('sim_params.json', mode='r') as param_file:
    sim_params = json.load(param_file)
print(sim_params)

dt=0.0025
sim_time=0.5
simsteps = round(sim_time // dt)
Sim1=e1.EulerSimulator(**sim_params)
"""Sim1.V=1
Sim1.beta=0.5
Sim1.fric_a=0.05
Sim1.fric_t=0.5
Sim1.J=0.01
Sim1.l=1
Sim1.m=1
Sim1.r_lift=0.1
Sim1.r_r=1
Sim1.r_s=1
Sim1.s_lift=0.2"""
Sim1.state.omega=0
Sim1.state.r_angle=30/360*np.pi*2
Sim1.state.s_angle=-30/360*np.pi*2
Sim1.state.theta=45/360*np.pi*2
Sim1.state.v=0
Sim1.state.x=-0.5
Sim1.state.y=2

state=Sim1.state
fig=plt.figure(figsize=(21,7))
ax1 = plt.subplot(1, 3, 1)
r=2.5
theta=np.linspace(0.0,2.0*np.pi,100)
x=r*np.cos(theta)
y=r*np.sin(theta)
c=0.1
a=0.1
e=0.95
xb=c+np.cos(theta)*a*(1-e**2)/(1+e*np.cos(theta))
yb=np.sin(theta)*a*(1-e**2)/(1+e*np.cos(theta))
s_pos=np.array([[0,-a*0.75],[0,0]])


ds=state.s_angle
Rs=np.array([[np.cos(ds),-np.sin(ds)],[np.sin(ds) ,np.cos(ds)]])

r_pos=np.array([[0,a/2],[0,0]])
dr=-state.r_angle
Rr=np.array([[np.cos(dr),-np.sin(dr)],[np.sin(dr) ,np.cos(dr)]])

ra=state.theta
Rb=np.array([[np.cos(ra),-np.sin(ra)],[np.sin(ra) ,np.cos(ra)]])
xbr=np.zeros((len(xb),1))
ybr=np.zeros((len(xb),1))
for i in range(len(xb)):
    xbr[i][0]=Rb[0][0:2].dot(np.array([[xb[i]],[yb[i]]]))+state.x;
    ybr[i]=Rb[1][0:2].dot(np.array([[xb[i]],[yb[i]]]))+state.y;
s_r=Rs.dot(s_pos)+np.array([[a*0.75,a*0.75],[0,0]])
s_r_r=Rb.dot(s_r)
r_r=Rr.dot(r_pos)+np.array([[-a/2,-a/2],[0,0]])
r_r_r=Rb.dot(r_r)
ax1.axis(np.array([-r*1.1,r*1.1,-r*1.1,r*1.1]))
ax1.fill(np.array([-r*1.1,r*1.1,r*1.1,-r*1.1]),np.array([-r*1.1,-r*1.1,r*1.1,r*1.1]),"g")
ax1.fill(x,y,'b')
ax1.fill(xbr,ybr,'tab:orange')
ax1.plot(s_r_r[0]+state.x,s_r_r[1]+state.y,'k',r_r_r[0]+state.x,r_r_r[1]+state.y,'k')
#ax1.get_children()[2].set_xy(np.column_stack([xbr,ybr]))


ax2 = plt.subplot(2, 3, 5,projection='polar')
ax2.set_theta_direction(-1)
ax2.set_theta_zero_location("N")
ax2.set_thetamin(-45.1)
ax2.set_thetamax(45.1)
ax2.set_thetagrids([-45,-30,-15,0,15,30,45])
ax2.set_rticks([])
ax2.set_title('Rudder Angle')
ax2.title.set_position([0.5,0.95])
ax2.set_rlim([0,1])
ax2.plot([0,-dr],[0,1])


ax3 = plt.subplot(2, 3, 2,projection='polar')
ax3.set_theta_zero_location("S")
ax3.set_thetamin(-90.1)
ax3.set_thetamax(90.1)
ax3.set_thetagrids([-90.1,-60,-30,0,30,60,90.1])
ax3.set_rticks([])
ax3.set_title('Sail Angle')
ax3.title.set_position([0.5,0.75])
ax3.set_rlim([0,1])
ax3.plot([0,ds],[0,1])
ax3.set_frame_on('True')

ax4 = plt.subplot(1, 3, 3,projection='polar')
ax4.set_theta_zero_location("N")

ax4.title.set_position([0.5,-0.1])
ax4.set_title('Wind Direction and Velocity')
ax4.set_rlim([0,1])
#ax4.plot([(30+180)/360*np.pi*2,30/360*np.pi*2],[1,1])
ax4.set_xticklabels(['N','NW','W','SW','S','SE','E','NE'])
ax4.set_yticklabels([])
ax4.set_frame_on('True')
#ax4.annotate("", xy=(0.5, 0.5), xytext=(0, 0),arrowprops=dict(arrowstyle="->"))
ax4.arrow(-180/360*np.pi*2,Sim1.V,180/360*np.pi*2,0,head_width=-0.075,shape='right')
ax4.arrow(-180/360*np.pi*2,Sim1.V,180/360*np.pi*2,0,head_width=0.075,shape='left')
#ax4.arrow((45+180)/360*np.pi*2,0.5,180/360*np.pi*2,0,head_width=1,shape='full')
plt.subplots_adjust(wspace=0, hspace=0)

#
def updplot(state):
    theta=np.linspace(0.0,2.0*np.pi,100)
    c=0.1
    a=0.1
    e=0.95
    xb=c+np.cos(theta)*a*(1-e**2)/(1+e*np.cos(theta))
    yb=np.sin(theta)*a*(1-e**2)/(1+e*np.cos(theta))
    s_pos=np.array([[0,-a*0.75],[0,0]])
    
    
    ds=state.s_angle
    Rs=np.array([[np.cos(ds),-np.sin(ds)],[np.sin(ds) ,np.cos(ds)]])
    
    r_pos=np.array([[0,a/2],[0,0]])
    dr=-state.r_angle
    Rr=np.array([[np.cos(dr),-np.sin(dr)],[np.sin(dr) ,np.cos(dr)]])
    
    ra=state.theta
    Rb=np.array([[np.cos(ra),-np.sin(ra)],[np.sin(ra) ,np.cos(ra)]])
    xbr=np.zeros((len(xb),1))
    ybr=np.zeros((len(xb),1))
    for i in range(len(xb)):
        xbr[i][0]=Rb[0][0:2].dot(np.array([[xb[i]],[yb[i]]]))+state.x;
        ybr[i]=Rb[1][0:2].dot(np.array([[xb[i]],[yb[i]]]))+state.y;
    s_r=Rs.dot(s_pos)+np.array([[a*0.75,a*0.75],[0,0]])
    s_r_r=Rb.dot(s_r)
    r_r=Rr.dot(r_pos)+np.array([[-a/2,-a/2],[0,0]])
    r_r_r=Rb.dot(r_r)
    ax1.get_children()[2].set_xy(np.column_stack([xbr,ybr]))
    ax1.get_children()[3].set_xdata(s_r_r[0]+state.x)
    ax1.get_children()[3].set_ydata(s_r_r[1]+state.y)
    ax1.get_children()[4].set_xdata(r_r_r[0]+state.x)
    ax1.get_children()[4].set_ydata(r_r_r[1]+state.y)
    
    ax2.get_children()[0].set_xdata([0,-dr])
    ax2.get_children()[0].set_ydata([0,1])
    
    ax3.get_children()[0].set_xdata([0,ds])
    ax3.get_children()[0].set_ydata([0,1])


#    #ax4.annotate("", xy=(0.5, 0.5), xytext=(0, 0),arrowprops=dict(arrowstyle="->"))    
#    #ax4.arrow((45+180)/360*np.pi*2,0.5,180/360*np.pi*2,0,head_width=1,shape='full')
#    plt.subplots_adjust(wspace=0, hspace=0)
#    return fig
#

root= tk.Tk()
#
#sim_time=1
#simsteps = round(sim_time // dt)
#
def animate(i):
    px=Sim1.state.x
    py=Sim1.state.y
    Sim1.state.s_angle=-90/360*np.pi*2*np.cos(i*dt*10)
    Sim1.state.r_angle=45/360*np.pi*2*np.cos(i*dt*10)
#    Sim1.V=(1+np.sin(i*dt*10))/2
#    ax4.get_children()[0].set_xy(np.column_stack([[-180/360*np.pi*2,180/360*np.pi*2],[np.sin(i*dt*10),0]]))
#    ax4.get_children()[1].set_xy(np.column_stack([[-180/360*np.pi*2,180/360*np.pi*2],[Sim1.V,0]]))
    Sim1.simulate(i*dt)
#    temp=transtwopi(np.arctan(Sim1.state.y/Sim1.state.x))
#    print(transtwopi(Sim1.state.theta))
#    print(temp)
    if (Sim1.state.x**2+Sim1.state.y**2>(r**2)*1.01):
        Sim1.state.v=0
        Sim1.state.x=px
        Sim1.state.y=py
    updplot(Sim1.state)
    
def transtwopi(x):
    y=x-2*np.pi*np.floor(x/(2*np.pi))
    return y

plotcanvas = FigureCanvasTkAgg(fig, root)
plotcanvas.get_tk_widget().grid(column=1, row=1)
ani = animation.FuncAnimation(fig, animate, interval=simsteps, blit=False)
root.mainloop()
#
#
#

