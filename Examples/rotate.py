#!/usr/bin/env python
"""-----------------------------------------------------------------
  Python file for plotting Finesse ouput rotate.out
  created automatically Sat Mar  4 20:41:36 2017

  Run from command line as: python rotate.py
  Load from python script as: import rotate
  And then use:
  rotate.run() for plotting only
  x,y=rotate.run() for plotting and loading the data
  x,y=rotate.run(1) for only loading the data
-----------------------------------------------------------------"""

__author__ = "Finesse, http://www.gwoptics.org/finesse"

import numpy as np
import matplotlib
BACKEND = 'Qt4Agg'
matplotlib.use(BACKEND)
from matplotlib import rc
import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LogNorm

def convert3D(X,Y,Z):
	row,col=Z.shape
	nxp=len(np.nonzero(np.equal(Y,Y[0]))[0])
	nyp=row/nxp
	y=Y[0:nyp]
	x=X[0:row:nyp]#note the order
	M=np.zeros((nyp,nxp,col))
	for i in range(col):
		M[:,:,i]=np.reshape(Z[:,i],(nyp,nxp),order='F')
	return (x,y,M)

formatter = matplotlib.ticker.EngFormatter(unit='')
formatter.ENG_PREFIXES[-6] = 'u'
def run(noplot=None):
	data = np.loadtxt('rotate.out',comments='%')
	rows,cols=data.shape
	X=data[:,0]
	Y=data[:,1]
	Z=data[:,2:cols]
	x,y,z=convert3D(X,Y,Z)
	mytitle='rotate                Sat Mar  4 20:41:36 2017'
	if (noplot==None):
		# setting default font sizes
		rc('font',**pp.font)
		rc('xtick',labelsize=pp.TICK_SIZE)
		rc('ytick',labelsize=pp.TICK_SIZE)
		rc('text', usetex=pp.USETEX)
		rc('axes', labelsize = pp.LABEL_SIZE)
		fig=plt.figure()
		fig.set_size_inches(pp.fig_size)
		fig.set_dpi(pp.FIG_DPI)
		ax3 = fig.add_subplot(111)
		xm,ym=np.meshgrid(x,y)
		surf=ax3.pcolor(xm,ym,z[:,:,0],cmap=cm.jet,linewidth=0, label = 'b1 n4 (wx0=10m, wy0=10m)')
		surf.set_rasterized(True) # set this for mixed-mode rendering
		ax3.set_ylim(-4e-05,4e-05)
		ax3.set_ylabel('xbeta [rad] (bs1)')
		ax3.xaxis.set_major_formatter(formatter)
		ax3.yaxis.set_major_formatter(formatter)
		ax3.set_xlim(-5,5)
		ax3.set_xlabel('x [x/wx0] (b1)')
		fig.colorbar(surf)
		if pp.PRINT_TITLE:
			plt.title(mytitle)
		if pp.SCREEN_TITLE:
			fig.canvas.manager.set_window_title(mytitle)
		else:
			fig.canvas.manager.set_window_title('')
	return (x,y)
class pp():
	# set some gobal settings first
	BACKEND = 'Qt4Agg' # matplotlib backend
	FIG_DPI=90 # DPI of on sceen plot
	# Some help in calculating good figure size for Latex
	# documents. Starting with plot size in pt,
	# get this from LaTeX using \showthe\columnwidth
	fig_width_pt = 484.0
	inches_per_pt = 1.0/72.27  # Convert TeX pt to inches
	golden_mean = (np.sqrt(5)-1.0)/2.0   # Aesthetic ratio
	fig_width = fig_width_pt*inches_per_pt  # width in inches
	fig_height = fig_width*golden_mean      # height in inches
	fig_size = [fig_width,fig_height]
	# some plot options:
	LINEWIDTH = 1 # linewidths of traces in plot
	AA = True # antialiasing of traces
	USETEX = False # use Latex encoding in text
	SHADOW = False # shadow of legend box
	GRID = True # grid on or off
	# font sizes for normal text, tick labels and legend
	FONT_SIZE = 10 # size of normal text
	TICK_SIZE = 10 # size of tick labels
	LABEL_SIZE = 10 # size of axes labels
	LEGEND_SIZE = 10 # size of legend
	# font family and type
	font = {'family':'sans-serif','size':FONT_SIZE}
	DPI=300 # DPI for saving via savefig
	# print options given to savefig command:
	print_options = {'dpi':DPI, 'transparent':True, 'bbox_inches':'tight', 'pad_inches':0.1}
	# for Palatino and other serif fonts use:
	#font = {'family':'serif','serif':['Palatino']}
	SCREEN_TITLE = True # show title on screen?
	PRINT_TITLE = False # show title in saved file?

if __name__=="__main__":
	run()
