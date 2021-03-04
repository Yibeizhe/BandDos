import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator
class Band():
    def __init__(self, band):
        with open(band) as f:
            self.band = f.readlines()
            # n kpoints in each bands
            self.nks = int(self.band[1].split()[-2])
            # The number of bands
            self.nbands = int(self.band[1].split()[-1])
            print('There are {} bands, and in each band there are {} kpoints'.format(self.nbands, self.nks))
        self.bands=np.loadtxt(band)
        # K points
        self.kps = self.bands[0:self.nks, 0]
    def band_plot(self,color='grey',la='Total'):
        #Use the first band to plot legend
        plt.plot(self.kps,self.bands[0:self.nks,1],linewidth=0.2, linestyle="-",color=color,label=la)
        for i in range(1,self.nbands):
            # Energy of each band
            energy = self.bands[i * self.nks:(i + 1) * self.nks, 1]
            kpoints = self.bands[i * self.nks:(i + 1) * self.nks, 0]
            plt.plot(kpoints, energy, linewidth=0.2, linestyle="-", color=color)
    def band_up_down(self,linewidth=0.5,color1='black',color2='red'):
        #plot spin-up
        plt.plot(self.kps,self.bands[0:self.nks,1],linewidth=linewidth, linestyle="-",color=color1,label='UP')
        for i in range(1,self.nbands):
            # Energy of each band
            energy = self.bands[i * self.nks:(i + 1) * self.nks, 1]
            kpoints = self.bands[i * self.nks:(i + 1) * self.nks, 0]
            plt.plot(kpoints, energy, linewidth=linewidth, linestyle="-", color=color1)
        #plot spin-down
        plt.plot(self.kps,self.bands[0:self.nks,2],linewidth=linewidth, linestyle="-",color=color2,label='DW')
        for i in range(1,self.nbands):
            # Energy of each band
            energy = self.bands[i * self.nks:(i + 1) * self.nks, 2]
            kpoints = self.bands[i * self.nks:(i + 1) * self.nks, 0]
            plt.plot(kpoints, energy, linewidth=linewidth, linestyle="-", color=color2)
    def pband_plot(self,color,label):
        for i in range(self.nbands):
            # Energy of each band
            energy = self.bands[i * self.nks:(i + 1) * self.nks, 1]
            kpoints = self.bands[i * self.nks:(i + 1) * self.nks, 0]
            plt.scatter(kpoints, energy, self.bands[i * self.nks:(i + 1) * self.nks, 11]**2*10, alpha=0.7,
                        marker='o', color=color, edgecolors=color, linewidths=0.7)
        #The projected legend marker.
        maxindex = np.argmax(self.bands[:,11])
        #Find which band has the maximum projected value
        mp=int(maxindex)//self.nks
        print("The maximum of project band is {}".format(maxindex))
        energy1=self.bands[mp*self.nks:(mp+1)*self.nks,1]
        kpoints=self.bands[mp*self.nks:(mp+1)*self.nks,0]
        plt.scatter(kpoints, energy1, self.bands[mp*self.nks:(mp+1)*self.nks,11], alpha=0.7,
                    marker='o', color=color, edgecolors=color, linewidths=0.7,label=label)

def k_name_coor(kname='KLABELS',kcoor='KLINES.dat'):
    '''
    Getting the high symmetry K points' name and value from KLABELS and KLINES.dat files,respectively.
    '''
    # Mark the symmetry Kpoints and Fermi level
    # Read the K-points name and coordinates from KLABELS.
    kps = np.loadtxt(kname, dtype='str', skiprows=1, comments="*")
    # The first column is the K high-symmetry points' names.
    k_name = list(kps[:, 0])
    k_name[0]=r'$\Gamma$'
    k_name[-1]=r'$\Gamma$'
    # The K high-symmetry points' coordinates must be read from the KLINES.dat.
    kl = np.loadtxt(kcoor)
    k_coor = np.floor(np.array(sorted(set(kl[:, 0])), dtype=float) * 1000) / 1000
    print('High symmetry K points name: {} and values:{}'.format(k_name,k_coor))
    plt.xticks(k_coor, k_name)
    for i in k_coor:
        plt.axvline(x=i, color='grey', linewidth=0.5, linestyle='--', alpha=0.5)
def pband():
    '''Only for ploting the Cr and I projected band'''
    up_dw = str(input("Enter 'UP' for spin up, 'DW' for spin down projects band: "))
    Cr = Band('PBAND_Cr_{}.dat'.format(up_dw))
    I = Band('PBAND_I_{}.dat'.format(up_dw))
    Cr.band_plot(la=up_dw)
    Cr.pband_plot(color='blue', label='Cr')
    # I.band_plot()
    I.pband_plot(color='red', label='I')
    plt.legend(loc='upper right', fontsize=8, framealpha=0.5, frameon=False)
    plt.xlim(Cr.kps[0], Cr.kps[-1])


fig = plt.figure(figsize=(3, 4), dpi=300)
band_choose=int(input('Enter 1 for band_without_spin 2 for band_with_spin 3 for pband:'))
if band_choose ==1:
    bands = Band('BAND.dat')
    bands.band_plot()
    plt.xlim(bands.kps[0], bands.kps[-1])
elif band_choose ==2:
    bands = Band('BAND.dat')
    bands.band_up_down()
    plt.xlim(bands.kps[0], bands.kps[-1])
elif band_choose==3:
    pband()
else:
    print('Enter wrongly')


plt.legend(loc='upper right',fontsize=8,framealpha=0.5,frameon=False)
#Mark the high symmetry points on axis.
k_name_coor()

#plot fermi level
plt.axhline(y=0,linestyle='--',color='grey',linewidth=0.7)

y_major_locator=MultipleLocator(1)
ax=plt.gca()
ax.yaxis.set_major_locator(y_major_locator)
ylim_b=float(input("Enter the bottom energy: "))
ylim_t=float(input("Enter the top energy: "))
plt.ylim(ylim_b,ylim_t)
tit=input('Enter the title of picture: ')
plt.title(tit,fontsize=8)
plt.ylabel('Energy(eV)',fontsize=8)
plt.tick_params(axis='both',direction='in',labelsize=8)
figname=input('Enter figure name: ')
plt.savefig(figname)
plt.show()

