###########################################################
##
##	Written by Alexander Liptak (@ajulik1997)
##	Date: December 2017
##	E-Mail: Alexander.Liptak.2015@live.rhul.ac.uk
##	Phone: +44 7901 595107
##
##	Tested with McStas 2.4.1
##
###########################################################

######################### IMPORTS #########################

from PyQt4 import QtGui, QtCore
from glob import glob
from multiprocessing import cpu_count
from subprocess import check_call
from sympy import *
from time import sleep
import sys, os
import numpy as np
from shutil import rmtree
import SWINE_GUI, SWINE_GUI_cstinstr, SWINE_GUI_pselect, SWINE_GUI_prgbar
import MatplotlibWidget

######################### GLOBAL VARS #########################

cores = cpu_count()					## number of cores
environ = os.environ['PATH']		## envvar backup

mcstas_dir = ''						## McStas directory
mcrun = ''							## McRun path
mcstas = ''							## McStas path
mclib = ''							## McLib path
python_dir = ''						## Miniconda directory
gcc_dir = ''						## GCC directory

instr_dir = ''						## Instrument path
instr_params = ['']*6				## Instrument parameters
instr_pos = [0.0]*3					## Instrument positions

s1s2_sep = 0.0						## slit1-slit2 separation [mm]
s2samp_sep = 0.0					## slit2-sample separation [mm]

resolutionData = []					## holds resolution data matrix
intensityData = []					## holds intensity data matrix
perReslineData = []					## holds intensity data per resline
penumbraData = []		##??
highlightPoints = []	##??

experimentCalls = []				## McStas calls used for generating data

plotDatadir = ''

######################### WORKER THREADS #########################

class runSimulationThread(QtCore.QThread):
	def __init__(self, datafile):
		QtCore.QThread.__init__(self)
		self.datafile = datafile
		
	def __del__(self):
		self.wait()
	
	def run(self):
		global experimentCalls; global cores
		if os.path.exists(os.path.split(os.path.realpath(__file__))[0]+'\\temp'): rmtree(os.path.split(os.path.realpath(__file__))[0]+'\\temp')
		sleep(0.1)
		os.mkdir(os.path.split(os.path.realpath(__file__))[0]+'\\temp')
		self.emit(QtCore.SIGNAL('reset()'))
		self.emit(QtCore.SIGNAL('setText(QString)'), "Running simulations ...")
		for i in range(0,len(experimentCalls),cores):
			check_call(" | ".join([" ".join(p) for p in experimentCalls[i:i+cores]]))
			self.emit(QtCore.SIGNAL('setValue(int)'), int((i/len(experimentCalls))*100))
		
		global resolutionData; global intensityData; global instr_params; global instr_dir
		self.emit(QtCore.SIGNAL('reset()'))
		self.emit(QtCore.SIGNAL('setText(QString)'), "Analyzing data ...")
		for index, folder in enumerate(os.listdir(os.path.split(os.path.realpath(__file__))[0]+'\\temp')):
			with open(os.path.split(os.path.realpath(__file__))[0]+'\\temp'+'\\'+folder+'\\'+instr_params[5]+'.dat', 'r') as file:
				for line in file:
					if 'values:' in line:
						intensityData[int(folder[1:-1].split('][')[0]), int(folder[1:-1].split('][')[1])] = line.split(' ')[2]
						self.emit(QtCore.SIGNAL('setValue(int)'), int((index/len(os.listdir(os.path.split(os.path.realpath(__file__))[0]+'\\temp')))*100))
		
		np.savez_compressed(os.path.split(instr_dir[1:-1])[0]+'\\'+self.datafile, intensity=intensityData, resolution=resolutionData)
		rmtree(os.path.split(os.path.realpath(__file__))[0]+'\\temp')
		
class dataCollectionThread(QtCore.QThread):
	def __init__(self, angle, pumbra, steps, neutrons):
		QtCore.QThread.__init__(self)
		self.angle = angle
		self.pumbra = pumbra
		self.steps = steps
		self.neutrons = neutrons
		
	def __del__(self):
		self.wait()
	
	def run(self):
		self.emit(QtCore.SIGNAL('reset()'))
		self.emit(QtCore.SIGNAL('setText(QString)'), "Preparing simulation...")
		
		S1 = symbols('S1')
		S2 = symbols('S2')
		penumbra = (2*((((s1s2_sep+s2samp_sep)*(S1+S2))/(2*s1s2_sep))-(S1/2)))/(sin(self.angle))
		resolution = ((atan((S1+S2)/(s1s2_sep)))/(2*tan(self.angle)))*100
		
		s1max = float(next(iter(solveset(Eq(penumbra.subs(S2,0),self.pumbra),S1))))
		s2max = float(next(iter(solveset(Eq(penumbra.subs(S1,0),self.pumbra),S2))))
			
		slitvals = [[],[]]
		for i in range(int(self.steps)+1):
			slitvals[0].append(i*(s1max/self.steps))
			slitvals[1].append(i*(s2max/self.steps))
			
		global resolutionData; resolutionData = np.zeros((int(self.steps)+1,int(self.steps)+1))
		global intensityData; intensityData = np.zeros((int(self.steps)+1,int(self.steps)+1))							## !!!
		global experimentCalls; experimentCalls = []
		
		for index1, item1 in enumerate(slitvals[0]):
			for index2, item2 in enumerate(slitvals[1]):
				penumbraCurrent = penumbra.subs([(S1,item1),(S2,item2)])
				resolutionCurrent = resolution.subs([(S1,item1),(S2,item2)])
				resolutionData[index1,index2] = resolutionCurrent
				self.emit(QtCore.SIGNAL('setValue(int)'), int((len(experimentCalls)/(len(slitvals[0])*len(slitvals[1])))*200))
				if ((penumbraCurrent <= self.pumbra) and (item1 != 0.0 and item2 != 0.0)):
					global instr_params
					experimentCalls.append([mcrun, instr_dir,
											'-d', os.path.split(os.path.realpath(__file__))[0]+'\\temp\\['+str(index1)+']['+str(index2)+']',
											'-n', str(int(self.neutrons)),
											instr_params[2]+'='+str(instr_pos[0]),instr_params[3]+'='+str(instr_pos[1]),
											instr_params[4]+'='+str(instr_pos[2]),
											instr_params[0]+'='+str(item1/1000), instr_params[1]+'='+str(item2/1000)])

class compileThread(QtCore.QThread):
	def __init__(self):
		QtCore.QThread.__init__(self)
	
	def __del__(self):
		self.wait()
	
	def run(self):
		INSTRtoC = mcstas, '-I', ' -I '.join(mclib), '-t', instr_dir.replace('\\','\\\\')
		CtoEXE = 'gcc', '-o', os.path.splitext(instr_dir)[0]+'.exe"', os.path.splitext(instr_dir)[0]+'.c"', '-g', '-O2','-lm'
		
		self.emit(QtCore.SIGNAL('reset()'))
		try:
			self.emit(QtCore.SIGNAL('setText(QString)'), "Compiling: instr -> c")
			check_call(' '.join(INSTRtoC))
			self.emit(QtCore.SIGNAL('setValue(int)'), 50)
		
			self.emit(QtCore.SIGNAL('setText(QString)'), "Compiling: c -> exe")
			check_call(' '.join(CtoEXE))
			self.emit(QtCore.SIGNAL('setValue(int)'), 100)
		except:
			self.emit(QtCore.SIGNAL('failed()'))
		self.emit(QtCore.SIGNAL('finished()'))

######################### DIALOG WINDOWS #########################

class LoadingBar(QtGui.QDialog, SWINE_GUI_prgbar.Ui_Dialog):
	def __init__(self, parent=None):
		super(LoadingBar, self).__init__(parent)
		self.setupUi(self)
	
	def reject(self):
		return
	
	def reset(self):
		self.prg.setValue(0)
		self.lbl.setText('')
	
	def setValue(self, value):
		self.prg.setValue(value)
	
	def setText(self, QString):
		self.lbl.setText(QString)

class PositionSelect(QtGui.QDialog, SWINE_GUI_pselect.Ui_Dialog):
	def __init__(self, parent=None):
		super(PositionSelect, self).__init__(parent)
		self.setupUi(self)
	
	def accept(self):
		global instr_pos;
		instr_pos[0] = self.spb_s1p.value()
		instr_pos[1] = self.spb_s2p.value()
		instr_pos[2] = self.spb_samp.value()
		global s1s2_sep; s1s2_sep = (instr_pos[1]-instr_pos[0])*1000
		global s2samp_sep; s2samp_sep = (instr_pos[2]-instr_pos[1])*1000
		self.parent().setEnabled()
		super(PositionSelect, self).accept()
	
	def reject(self):
		return

class CustomInstr(QtGui.QDialog, SWINE_GUI_cstinstr.Ui_Dialog):
	def __init__(self, parent=None):
		super(CustomInstr, self).__init__(parent)
		self.setupUi(self)

		self.btn_select.clicked.connect(self.getInstr)
	
	def getInstr(self):
		path = QtGui.QFileDialog.getOpenFileName(self, "Select instrument file", os.path.split(os.path.realpath(__file__))[0], "*.instr")
		if path:
			global instr_dir; instr_dir = '"'+os.path.normpath(path)+'"'
			self.lbl_btn.setText(instr_dir.split('\\')[-1][:-1])
			for item in [self.txt_s1w, self.txt_s2w, self.txt_s1p, self.txt_s2p, self.txt_sp, self.txt_psd]:
				item.setEnabled(True)

	def accept(self):
		self.parent().rdb_cust.setChecked(True)
		temp = []
		for item in [self.txt_s1w, self.txt_s2w, self.txt_s1p, self.txt_s2p, self.txt_sp, self.txt_psd]:
			temp.append(item.text())
		if '' in temp:
			QtGui.QMessageBox.warning(self, "Instrument parameters invalid", "Make sure no instrument parameter fields are left empty!", QtGui.QMessageBox.Retry)
			return 0;
		if not all(param in open(instr_dir[1:-1]).read() for param in temp):
			QtGui.QMessageBox.warning(self, "Instrument parameters invalid", "These parameters don't exist in the instrument file!", QtGui.QMessageBox.Retry)
			return 0;
		global instr_params; instr_params = temp[:]
		super(CustomInstr, self).accept()
		self.parent().getSlitPositions()
	
	def reject(self):
		self.parent().rdb_cust.setChecked(False)
		self.parent().setDisabled()
		super(CustomInstr, self).reject()

######################### MAIN APP #########################

class MainApp(QtGui.QMainWindow, SWINE_GUI.Ui_MainWindow):

	def __init__(self, parent=None):
		super(MainApp, self).__init__(parent)
		self.setupUi(self)

		QtGui.QMessageBox.information(self, "Path warning", "Make sure no paths you use in this application include a space. \nSpaces are not handled well by McStas and GCC and you will receive an error and/or obtain incorrect results.", QtGui.QMessageBox.Ok)

		self.customInstrDialog = CustomInstr(self)
		self.instrPosDialog = PositionSelect(self)
		self.loadingBar = LoadingBar(self)
		
		self.btn_mcstas.clicked.connect(self.getMcstasDir)
		self.rdb_cust.clicked.connect(self.setCustomInstrument)
		self.rdb_def.clicked.connect(self.setDefaultInstrument)
		self.btn_gendata.clicked.connect(self.generateData)
		self.btn_data.clicked.connect(self.loadData)
		self.btn_plot.clicked.connect(self.plot1)
		self.btn_plot_2.clicked.connect(self.plot2)
	
	def getMcstasDir(self):
		directory = QtGui.QFileDialog.getExistingDirectory(self, "Select location on McStas")
		if directory:
			if ('mcstas-' in directory.split('\\')[-1]):
				if float(directory.split('\\')[-1].split('-')[1][0:3]) >= 2.4:
					self.lbl_mcstas.setText('McStas Version: ' + directory.split('\\')[-1])
					
					global mcstas_dir; mcstas_dir = '"'+directory+'"'
					global mcrun; mcrun = '"'+directory+'\\bin\\mcrun.bat'+'"'
					global mcstas; mcstas = '"'+directory+'\\bin\\mcstas.exe'+'"'
					global mclib; mclib = glob(directory+'\\lib\\*'); mclib = ['"'+i+'"' for i in mclib]
					global gcc_dir; gcc_dir = '"'+glob(directory+'\\miniconda*\\Library\\mingw-w64\\bin\\')[0]+'"'
					global python_dir; python_dir = '"'+glob(directory+'\\miniconda*\\')[0]+'"'
					
					global environ
					os.environ['PATH']=environ+';'+gcc_dir+';'+python_dir

					for item in [self.lbl_instr, self.rdb_cust, self.rdb_def]:
						item.setEnabled(True)
				else:
					QtGui.QMessageBox.warning(self, "Invalid McStas directory", "Incompatible McStas installation!", QtGui.QMessageBox.Retry)
			else:
				QtGui.QMessageBox.warning(self, "Invalid McStas directory", "This is not a McStas directory!", QtGui.QMessageBox.Retry)
		
	def setDefaultInstrument(self):
		self.rdb_cust.setChecked(False)
		self.rdb_def.setChecked(True)
		global instr_dir; instr_dir = '"'+os.path.split(os.path.realpath(__file__))[0]+'\\default.instr'+'"'
		global instr_params;
		instr_params[0] = 'slit1_width'
		instr_params[1] = 'slit2_width'
		instr_params[2] = 'slit1_pos'
		instr_params[3] = 'slit2_pos'
		instr_params[4] = 'sample_pos'
		instr_params[5] = 'sample_psd'
		self.getSlitPositions()

	def setCustomInstrument(self):
		self.rdb_def.setChecked(False)
		self.rdb_cust.setChecked(True)
		if self.customInstrDialog.show() == 0:
			self.setCustomInstrument()

	def getSlitPositions(self):
		self.instrPosDialog.show()
		if self.rdb_cust.isChecked():
			self.instrPosDialog.spb_s1p.setValue(0)
			self.instrPosDialog.spb_s2p.setValue(0)
			self.instrPosDialog.spb_samp.setValue(0)
		if self.rdb_def.isChecked():
			self.instrPosDialog.spb_s1p.setValue(8.58)
			self.instrPosDialog.spb_s2p.setValue(13.63)
			self.instrPosDialog.spb_samp.setValue(14.03)
	
	def setEnabled(self):
		for item in [self.lbl_data, self.lbl_angle, self.lbl_penumbra, self.lbl_steps, self.lbl_neutrons,
					 self.box_angle, self.box_penumbra, self.box_steps, self.box_neutrons, self.btn_gendata, self.txt_description_2]:
			item.setEnabled(True)
		self.recompile()
	
	def setDisabled(self):
		for item in [self.lbl_data, self.lbl_angle, self.lbl_penumbra, self.lbl_steps, self.lbl_neutrons,
					 self.box_angle, self.box_penumbra, self.box_steps, self.box_neutrons, self.btn_gendata, self.txt_description_2]:
			item.setEnabled(False)
						
	def recompile(self):		
		self.loadingBar.show()
		self.compilation = compileThread()
		self.connect(self.compilation, QtCore.SIGNAL('reset()'), self.loadingBar.reset)
		self.connect(self.compilation, QtCore.SIGNAL('setText(QString)'), self.loadingBar.setText)
		self.connect(self.compilation, QtCore.SIGNAL('setValue(int)'), self.loadingBar.setValue)
		self.connect(self.compilation, QtCore.SIGNAL('finished()'), self.loadingBar.hide)
		self.connect(self.compilation, QtCore.SIGNAL('failed()'), self.compileFailed)
		self.compilation.start()

	def compileFailed(self):
		QtGui.QMessageBox.critical(self, "Compilation error", "An error has occurred during compilation", QtGui.QMessageBox.Abort)
	
	def generateData(self):
		if self.txt_description_2.text() == '':
			QtGui.QMessageBox.warning(self, "Invalid data path", "Please enter filename where data will be saved", QtGui.QMessageBox.Retry)
		else:
			self.loadingBar.show()
			self.dataCollection = dataCollectionThread(angle = self.box_angle.value(),
													   pumbra = self.box_penumbra.value(),
													   steps = self.box_steps.value(),
													   neutrons = self.box_neutrons.value())
			self.connect(self.dataCollection, QtCore.SIGNAL('reset()'), self.loadingBar.reset)
			self.connect(self.dataCollection, QtCore.SIGNAL('setText(QString)'), self.loadingBar.setText)
			self.connect(self.dataCollection, QtCore.SIGNAL('setValue(int)'), self.loadingBar.setValue)
			self.connect(self.dataCollection, QtCore.SIGNAL('finished()'), self.runSimulations)
			self.dataCollection.start()
	
	def runSimulations(self):
		self.loadingBar.show()
		self.simulation = runSimulationThread(datafile = self.txt_description_2.text())
		self.connect(self.simulation, QtCore.SIGNAL('reset()'), self.loadingBar.reset)
		self.connect(self.simulation, QtCore.SIGNAL('setText(QString)'), self.loadingBar.setText)
		self.connect(self.simulation, QtCore.SIGNAL('setValue(int)'), self.loadingBar.setValue)
		self.connect(self.simulation, QtCore.SIGNAL('finished()'), self.loadingBar.hide)
		self.simulation.start()
	
	def loadData(self):
		global plotDatadir;
		plotDatadir = QtGui.QFileDialog.getOpenFileName(self, "Select data file", os.path.split(os.path.realpath(__file__))[0], "*.npz")
		if plotDatadir:
			self.lbl_dataset.setText('Data set: ' + os.path.basename(plotDatadir))
			self.plt_widget.setEnabled(True)
	
	def plot1(self):
		global plotDatadir;
		if plotDatadir == '':
			QtGui.QMessageBox.warning(self, "Data not selected", "You have not loaded any data to plot!", QtGui.QMessageBox.Retry)
		else:
			self.plt_widget.figure.clear()
			ax = self.plt_widget.figure.add_subplot(111)
			ax.set_title(self.txt_description.text())
			
			data = np.load(plotDatadir)['intensity']
			heatmap = ax.imshow(data, cmap='hot', interpolation='nearest')
			colorbar = self.plt_widget.figure.colorbar(heatmap)
			self.plt_widget.figure.canvas.draw()
	
	def plot2(self):
		global plotDatadir;
		if plotDatadir == '':
			QtGui.QMessageBox.warning(self, "Data not selected", "You have not loaded any data to plot!", QtGui.QMessageBox.Retry)
		else:
			data = np.load(plotDatadir)['resolution']

######################### LAUNCHER #########################

def main():
	app = QtGui.QApplication(sys.argv)
	form = MainApp()
	form.show()
	app.exec_()

if __name__ == '__main__':
	main()