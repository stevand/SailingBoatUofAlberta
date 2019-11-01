"""
@author: eqgui
"""

import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from euler_sim2 import EulerSimulator
import json

def setup(frame):
    state = frame.state
    control = frame.control
    env = frame.env

    global ax1, ax2, ax3
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

    ds=control.s_angle
    Rs=np.array([[np.cos(ds),-np.sin(ds)],[np.sin(ds) ,np.cos(ds)]])

    r_pos=np.array([[0,a/2],[0,0]])
    dr=-control.r_angle
    Rr=np.array([[np.cos(dr),-np.sin(dr)],[np.sin(dr) ,np.cos(dr)]])

    ra=state.theta
    Rb=np.array([[np.cos(ra),-np.sin(ra)],[np.sin(ra) ,np.cos(ra)]])
    xbr=np.zeros((len(xb),1))
    ybr=np.zeros((len(xb),1))
    for i in range(len(xb)):
        xbr[i][0]=Rb[0][0:2].dot(np.array([[xb[i]],[yb[i]]]))+state.x
        ybr[i]=Rb[1][0:2].dot(np.array([[xb[i]],[yb[i]]]))+state.y
    s_r=Rs.dot(s_pos)+np.array([[a*0.75,a*0.75],[0,0]])
    s_r_r=Rb.dot(s_r)
    r_r=Rr.dot(r_pos)+np.array([[-a/2,-a/2],[0,0]])
    r_r_r=Rb.dot(r_r)
    ax1.axis(np.array([-r*1.1,r*1.1,-r*1.1,r*1.1]))
    ax1.fill(np.array([-r*1.1,r*1.1,r*1.1,-r*1.1]),np.array([-r*1.1,-r*1.1,r*1.1,r*1.1]),"g")
    ax1.fill(x,y,'b')
    ax1.fill(xbr,ybr,'tab:orange')
    ax1.plot(s_r_r[0]+state.x,s_r_r[1]+state.y,'k',r_r_r[0]+state.x,r_r_r[1]+state.y,'k')

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
    ax4.set_xticklabels(['N','NW','W','SW','S','SE','E','NE'])
    ax4.set_yticklabels([])
    ax4.set_frame_on('True')
    ax4.arrow(-180/360*np.pi*2,env.V,180/360*np.pi*2,0,head_width=-0.075,shape='right')
    ax4.arrow(-180/360*np.pi*2,env.V,180/360*np.pi*2,0,head_width=0.075,shape='left')
    plt.subplots_adjust(wspace=0, hspace=0)
    return fig
    #

def updplot(frame):
    state = frame.state
    control = frame.control

    theta=np.linspace(0.0,2.0*np.pi,100)
    c=0.1
    a=0.1
    e=0.95
    xb=c+np.cos(theta)*a*(1-e**2)/(1+e*np.cos(theta))
    yb=np.sin(theta)*a*(1-e**2)/(1+e*np.cos(theta))
    s_pos=np.array([[0,-a*0.75],[0,0]])
    
    
    ds=control.s_angle
    Rs=np.array([[np.cos(ds),-np.sin(ds)],[np.sin(ds) ,np.cos(ds)]])
    
    r_pos=np.array([[0,a/2],[0,0]])
    dr=-control.r_angle
    Rr=np.array([[np.cos(dr),-np.sin(dr)],[np.sin(dr) ,np.cos(dr)]])
    
    ra=state.theta
    Rb=np.array([[np.cos(ra),-np.sin(ra)],[np.sin(ra) ,np.cos(ra)]])
    xbr=np.zeros((len(xb),1))
    ybr=np.zeros((len(xb),1))
    for i in range(len(xb)):
        xbr[i][0]=Rb[0][0:2].dot(np.array([[xb[i]],[yb[i]]]))+state.x
        ybr[i]=Rb[1][0:2].dot(np.array([[xb[i]],[yb[i]]]))+state.y
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
    
def transtwopi(x):
    y=x-2*np.pi*np.floor(x/(2*np.pi))
    return y