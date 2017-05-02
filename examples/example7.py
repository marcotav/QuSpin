from __future__ import print_function, division

import sys,os
import argparse

qspin_path = os.path.join(os.getcwd(),"../")
sys.path.insert(0,qspin_path)

from quspin.operators import ops_dict,hamiltonian,exp_op
from quspin.basis import spin_basis_1d
from quspin.tools.measurements import obs_vs_time
import numpy as np
import matplotlib.pyplot as plt



def drive(L,S,blocks,omega,nT):

	# user defined generator
	# generates stroboscopic dynamics 
	def psi_t(psi0,U1,U2,nT):
		yield psi0
		for i in range(nT):
			psi0 = U2.dot(psi0)
			psi0 = U1.dot(psi0)
			psi0 = U2.dot(psi0)
			yield psi0

	T = 2*np.pi/omega

	basis = spin_basis_1d(L,S=S,pauli=False,**blocks)
	print "S = {S:3s}, L = {L:2d}, Size of H-space: {Ns:d}".format(S=S,L=L,Ns=basis.Ns)
	
	s = (basis.sps-1)/2.0

	Jzz = [[-1.0,i,(i+1)%L] for i in range(L)]
	hx  = [[-1.0,i] for i in range(L)]

	no_checks = dict(check_symm=False,check_herm=False)

	H1 = hamiltonian([["zz",Jzz]],[],basis=basis,dtype=np.float64,**no_checks)
	H2 = hamiltonian([["+",hx],["-",hx]],[],basis=basis,dtype=np.float64,**no_checks)

	E_i,psi = H1.eigsh(k=1,which="SA")
	psi = psi.ravel()

	U1 = exp_op(H1,a=-1j*T/2)
	U2 = exp_op(H2,a=-1j*T/4)

	times = np.arange(0,nT+1,1)*T

	Obs_t = obs_vs_time(psi_t(psi,U1,U2,nT),times,dict(E=H1),disp=True)

	plt.plot(times,(Obs_t["E"]+L*(s**2))/(2*(s**2)*L),marker='.',markersize=5)




blocks = dict(kblock=0,pblock=1,zblock=1)


systems = [("1/2",20),("1",12),("3/2",10),("2",8)]

for S,L in systems:
	drive(L,S,blocks,1.0/np.pi,100)




plt.show()

