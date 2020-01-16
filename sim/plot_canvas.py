"""
@author: eqgui
"""

import numpy as np
import matplotlib.pyplot as plt
from time import clock

def setup(frame):
    env = frame.env

    global ax1, ax2, ax3
    global fig
    fig=plt.figure(figsize=(27,9))
    ax1 = plt.subplot(1, 3, 1)
    # Size of the "water" (distance from the origin (0,0))
    r=4
    
#    Use this for a circular map
#    theta=np.linspace(0.0,2.0*np.pi,100)
#    x=r*np.cos(theta)
#    y=r*np.sin(theta)
    
#    Use this for a squared map
    x=[r,r,-r,-r]
    y=[r,-r,-r,r]
    
    #Sets the axis for the "map"
    ax1.axis(np.array([-r*1.1,r*1.1,-r*1.1,r*1.1]))
    #Plots the "land"
    ax1.fill(np.array([-r*1.1,r*1.1,r*1.1,-r*1.1]),np.array([-r*1.1,-r*1.1,r*1.1,r*1.1]),"g")
    #Plots the water
    ax1.fill(x,y,'b')
    #Creates a fill object for the boat (to be updated in "updplot")
    ax1.fill([],[],'tab:orange')
    #Creates line objects for the sail and rudder (to be updated in "updplot")
    ax1.plot([],[],'k',[],[],'k')
    ax1.plot([],[],'.r',markersize=2)

    #Creates the rudder angle polar plot
    ax2 = plt.subplot(3, 3, 5,projection='polar')
    ax2.set_theta_direction(-1)
    ax2.set_theta_zero_location("N")
    #Sets the max and min values
    ax2.set_thetamin(-45.1)
    ax2.set_thetamax(45.1)
    #Sets the interval values to be labeled
    ax2.set_thetagrids([-45,-30,-15,0,15,30,45])
    #No radius values for this plot
    ax2.set_rticks([])
    ax2.set_rlim([0,1])
    #Title and its position
    ax2.set_title('Rudder Angle',rotation='vertical',x=-0.3,y=0.2)
    #Creates a line object for the rudder position (to be updated in "updplot")    
    ax2.plot([],[])   
    

    #Creates the sail angle polar plot
    ax3 = plt.subplot(3, 3, 2,projection='polar')
    ax3.set_theta_zero_location("S")
    #Sets the max and min values
    ax3.set_thetamin(-90.1)
    ax3.set_thetamax(90.1)
    #Sets the interval values to be labeled
    ax3.set_thetagrids([-90.1,-60,-30,0,30,60,90.1])
    #No radius values for this plot
    ax3.set_rticks([])
    ax3.set_rlim([0,1])
    #Title and its position
    ax3.set_title('Sail Angle',rotation='vertical',x=-0.3,y=0.2)
    #Creates a line object for the sail position (to be updated in "updplot") 
    ax3.plot([],[])

    #Creates the wind direction and speed polar plot
    ax4 = plt.subplot(3, 3, 8,projection='polar')
    ax4.set_theta_zero_location("N")
    #Title and its position
    ax4.set_title('Wind Direction\n' + r'and Velocity',rotation='vertical',x=-0.3,y=0.2)
    ax4.set_rlim([0,1])
    #ax4.plot([(30+180)/360*np.pi*2,30/360*np.pi*2],[1,1])
    #Sets the interval labels to be displayed 
    ax4.set_xticklabels(['N','NW','W','SW','S','SE','E','NE'])
    ax4.set_yticklabels([])
    ax4.arrow(-180/360*np.pi*2,env.V,180/360*np.pi*2,0,head_width=-0.075,shape='right')
    ax4.arrow(-180/360*np.pi*2,env.V,180/360*np.pi*2,0,head_width=0.075,shape='left')
    plt.subplots_adjust(wspace=0, hspace=0)
    updplot(frame)
    return fig
    #

def updplot(frame):
    fig.canvas.draw()
    state = frame.state
    control = frame.control
    #print(clock())
    #Creates the boat curves
    theta=np.linspace(0.0,2.0*np.pi,100)
    c=0.1
    a=0.1
    e=0.95
    xb=c+np.cos(theta)*a*(1-e**2)/(1+e*np.cos(theta))
    yb=np.sin(theta)*a*(1-e**2)/(1+e*np.cos(theta))
    #Creates the line that represents the sail
    s_pos=np.array([[0,-a*0.75],[0,0]])
    
    #Gets the sail angle and creates the sail rotation matrix
    ds=control.s_angle
    Rs=np.array([[np.cos(ds),-np.sin(ds)],[np.sin(ds) ,np.cos(ds)]])
    
    #Creates the line that represents the rudder
    r_pos=np.array([[0,a/2],[0,0]])
    #Gets the rudder angle and creates the rudder rotation matrix
    dr=-control.r_angle
    Rr=np.array([[np.cos(dr),-np.sin(dr)],[np.sin(dr) ,np.cos(dr)]])
    
    #Gets the boat angle and creates the boat rotation matrix
    ra=state.theta
    Rb=np.array([[np.cos(ra),-np.sin(ra)],[np.sin(ra) ,np.cos(ra)]])
    #Rotates the boat
    xbr=np.zeros((len(xb),1))
    ybr=np.zeros((len(xb),1))
    for i in range(len(xb)):
        xbr[i][0]=Rb[0][0:2].dot(np.array([[xb[i]],[yb[i]]]))+state.x
        ybr[i]=Rb[1][0:2].dot(np.array([[xb[i]],[yb[i]]]))+state.y
    #Rotates the sail regarding its angle
    s_r=Rs.dot(s_pos)+np.array([[a*0.75,a*0.75],[0,0]])
    #Rotates the sail regarding the boat's angle
    s_r_r=Rb.dot(s_r)
    #Rotates the ruddder regarding its angle
    r_r=Rr.dot(r_pos)+np.array([[-a/2,-a/2],[0,0]])
    #Rotates the rudder regarding the boat's angle
    r_r_r=Rb.dot(r_r)
    
    #Plots the current boat/rudder/sail states
    ax1.get_children()[2].set_xy(np.column_stack([xbr,ybr]))
    ax1.get_children()[3].set_xdata(s_r_r[0]+state.x)
    ax1.get_children()[3].set_ydata(s_r_r[1]+state.y)
    ax1.get_children()[4].set_xdata(r_r_r[0]+state.x)
    ax1.get_children()[4].set_ydata(r_r_r[1]+state.y)

    #Gets the data from previous steps
    xc=ax1.get_children()[5].get_xdata()
    yc=ax1.get_children()[5].get_ydata()
    #Appends the current data and plots it          
    xc=np.append(xc,state.x)
    yc=np.append(yc,state.y)
    ax1.get_children()[5].set_xdata(xc)
    ax1.get_children()[5].set_ydata(yc)
    
    #Plots the current rudder state
    ax2.get_children()[0].set_xdata([0,-dr])
    ax2.get_children()[0].set_ydata([0,1])
    
    #Plots the current sail state
    ax3.get_children()[0].set_xdata([0,ds])
    ax3.get_children()[0].set_ydata([0,1])
    
def transtwopi(x):
    #Function to get an angle between 0 to 2*pi (360)
    y=x-2*np.pi*np.floor(x/(2*np.pi))
    return y