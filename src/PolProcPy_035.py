#!usr/bin/python

"""
Version 0.3.5 for the Polonator Processor machine.
Major difference from previous:
- Added an "Open Project" dialog that doesn't work so well.
- Does not need to be in the same folder as the project.
Version 0.3.4 works stably by being in the same folder as the project.
"""

import os
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import ui_polonatorprocessor_03



class PolonatorProcessor(QMainWindow, ui_polonatorprocessor_03.Ui_MainWindow):
    """Main window of Polonator Processor GUI."""
    
    def __init__(self, parent=None):
        """Version, startup timer, connect buttons to Python functions."""
        super(PolonatorProcessor, self).__init__(parent)
        self.setupUi(self)

#===============================================================================
#       Software Version
        self.aboutVersion.setText("Version 0.3.5")
        self.aboutDate.setText("12/10/2010")
#===============================================================================
        global ImageViewer
        global currentDisplayCycle
        global softwarePath
        currentDisplayCycle = ""
        ImageViewer = "eog"
        softwarePath = str(os.getcwd())
        print "software path " + softwarePath
        
        self.outputTabs.setTabEnabled(2,False)
        self.outputTabs.setTabEnabled(3,False)
        
        self.timer1 = QTimer()
        QObject.connect(self.timer1, SIGNAL("timeout()"), self.timerUpdate)
        
        self.connect(self.polonator_initialize, SIGNAL("clicked()"), 
                     self.polonatorinitialize)
        
        self.connect(self.polonator_process, SIGNAL("clicked()"), 
                     self.polonatorprocess)
        
        self.connect(self.polonator_kill, SIGNAL("clicked()"), 
                     self.polonatorkill)
        
        self.connect(self.startQC, SIGNAL("clicked()"), 
                     self.start_QC)
        
        self.connect(self.objectDisplay, SIGNAL("clicked()"), 
                     self.object_Display)
        
        self.connect(self.rawDisplay, SIGNAL("clicked()"), 
                     self.raw_Display)
        
        self.connect(self.histogramDrawHistogram, SIGNAL("clicked()"), 
                     self.histogram_DrawHistogram)
        
        self.connect(self.histogramImportCutoffs, SIGNAL("clicked()"), 
                     self.histogram_ImportCutoffs)
        
        self.connect(self.histogramExportCutoffs, SIGNAL("clicked()"), 
                     self.histogram_ExportCutoffs)
        
        self.connect(self.histogramGenerateData, SIGNAL("clicked()"), 
                     self.histogram_GenerateData)
        
        self.connect(self.histogramSingleButton, SIGNAL("clicked()"), 
                     self.histogram_SingleButton)
        
        self.connect(self.histogramCycleButton, SIGNAL("clicked()"), 
                     self.histogram_CycleButton)
        
        self.connect(self.basecallerAddButton, SIGNAL("clicked()"), 
                     self.basecaller_AddButton)
        
        self.connect(self.basecallerRemoveButton, SIGNAL("clicked()"), 
                     self.basecaller_RemoveButton)
        
        self.connect(self.basecallerAddAllButton, SIGNAL("clicked()"), 
                     self.basecaller_AddAllButton)
        
        self.connect(self.basecallerUpButton, SIGNAL("clicked()"), 
                     self.basecaller_UpButton)
        
        self.connect(self.basecallerDownButton, SIGNAL("clicked()"), 
                     self.basecaller_DownButton)
        
        self.connect(self.basecallerRunBasecallerButton, SIGNAL("clicked()"), 
                     self.basecaller_RunBasecallerButton)
        
        self.connect(self.basecallerRunBasecallerResetButton, SIGNAL("clicked()"),
                     self.basecaller_RunBasecallerResetButton)
        
        self.connect(self.cycleListComplete, SIGNAL("itemSelectionChanged()"), 
                     self.cycle_ListComplete)
        
        self.connect(self.cycleListComplete, SIGNAL("clicked(QModelIndex)"),
                     self.switchTab)
        
        self.connect(self.basecallerDataKeepSlider, SIGNAL("valueChanged(int)"), 
                     self.basecaller_DataKeepSlider)
        
        self.connect(self.basecallerBackgroundSubtractSlider,
                     SIGNAL("valueChanged(int)"),
                     self.basecaller_BackgroundSubtractSlider)
        
        self.connect(self.FC_Hist, SIGNAL("clicked()"), self.viewFCHist)
        
        self.connect(self.FC_Map, SIGNAL("clicked()"), self.viewFCMap)
        
        self.connect(self.FC_RegX, SIGNAL("clicked()"), self.viewFCRegX)
        
        self.connect(self.FC_RegY, SIGNAL("clicked()"), self.viewFCRegY)

        self.connect(self.actionOpen, SIGNAL("triggered()"), self.menuOpen)


#===============================================================================
# QProcess
#===============================================================================
    def proc_start(self, cmd):
        """Start QProcess and make connections."""
        print "proc_start"
        print cmd
        global proc
        cmd = QString(cmd)
        proc = QProcess()
        proc.setProcessChannelMode(1)
        proc.start(cmd)
        self.connect(proc, SIGNAL("readyRead()"), self.proc_readyRead)
        self.connect(proc, SIGNAL("finished(int)"), self.proc_finished)

    def proc_readyRead(self):
        """Append standard output line to QTextEdit."""
        print "proc_readyRead"
        outtext = (str(proc.readAllStandardOutput()).rstrip('\n'))
        outWin.append(outtext)
        outWin.ensureCursorVisible()
        print(outtext)
        log = open("PolonatorProcessorLog.txt",'a')
        log.write(outtext)
        log.close()
        
    def proc_finished(self):
        """
        When QProcess is finished, print error, close process, perform
        post-process commands, and go to next function.
        """
        print "proc_finished 1"
        log = open("PolonatorProcessorLog.txt",'a')
        finishedoutput = str(proc.readAllStandardOutput())
        finishederror = str(proc.readAllStandardError())
        outWin.append(finishedoutput)
        outWin.append(finishederror)
        print "proc_finished 2"
        outWin.append("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        log.write(finishedoutput)
        log.write(finishederror)
        log.close()
        print "proc_finished 3"
        proc.close()
        print "proc_finished 4"
        for arg in args:
            exec(arg)
            print "done arg " + str(args.index(arg)) + ": " + arg
        print "proc_finished 5"
        eval(nextFunc)
        print "proc_finished 6"

    def proc_pass(self):
        """End of a set of QProcesses."""
        print "proc_pass"
        return


#===============================================================================
# Timer Update
#===============================================================================
    def timerUpdate(self):
        """Load data and do a bunch of stuff on startup."""
        print "timerUpdate"

#        os.system("chmod 666 *")
#        os.system("chmod 777 *.py")
#        os.system("chmod 777 src/*.py")
#        os.system("chmod 777 display_*")
#        os.system("chmod 777 disp_*")
    #    os.system("chmod 777 )
        
        self.tab_2.setEnabled(False)
        self.tab_4.setEnabled(False)
        self.tab_5.setEnabled(False)
        self.tab_6.setEnabled(False)
        self.tab_7.setEnabled(False)
        self.polonator_initialize.setEnabled(False)
        self.polonator_process.setEnabled(False)
        self.updateQualityLists()
        self.updateBasecallerAvailableList()
        self.initializeHistogramCutoffFields([])
        
        self.updateHistogramCutoffs([])
        self.updateHistogramFileList()
        global conds
        conds = ['self.tab_1.setEnabled(True)', 'self.tab_2.setEnabled(True)',
                 'self.tab_4.setEnabled(True)', 'self.tab_5.setEnabled(True)',
                 'self.tab_6.setEnabled(True)', 'self.tab_7.setEnabled(True)']
        self.updateProcesses1()


#===============================================================================
# Polonator tab
#===============================================================================
    # Initialize Button
    def polonatorinitialize(self):
        """'Initialize' button in Polonator tab."""
        self.outputTabs.setCurrentIndex(0)
        self.statusbar.showMessage("Initialize processor")
        self.polonator_initializestatus.setText(QApplication.translate("MainWindow",
                                                                       "RUNNING"))
        cmd = "python "+softwarePath+"/PolonatorTab/initialize_processor.py"
        self.polonator_initialize.setEnabled(False)
        self.polonator_process.setEnabled(False)
        global nextFunc
        global args
        global conds
        global outWin
        nextFunc = "self.updateProcesses1()"
        args = ['self.polonator_initialize.setEnabled(False)',
                'self.polonator_process.setEnabled(False)']
        conds = ['pass']
        outWin = self.polonator_textarea
        self.proc_start(cmd)

    #Process images button
    def polonatorprocess(self):
        """'Process Images' button in Polonator tab."""
        self.outputTabs.setCurrentIndex(0)
        cmd = 'python '+softwarePath+'/PolonatorTab/processor.py'
        self.polonator_processorstatus.setText(QApplication.translate("MainWindow",
                                                                      "RUNNING"))
        self.polonator_initialize.setEnabled(False)
        self.polonator_process.setEnabled(False)
        global nextFunc
        global args
        global conds
        global outWin
        nextFunc = "self.updateProcesses1()"
        args = ['self.polonator_initialize.setEnabled(False)',
                'self.polonator_process.setEnabled(False)']
        conds = ['pass']
        outWin = self.polonator_textarea
        self.proc_start(cmd)

    #STOP ALL PROCESSING SOFTWARE button
    def polonatorkill(self):
        """'STOP ALL PROCESSING SOFTWARE' button in Polonator tab."""
        cmd = 'python '+softwarePath+'/PolonatorTab/process_kill.py'
        global nextFunc
        global args
        global conds
        global outWin
        nextFunc = "self.updateProcesses1()"
        args = ['pass']
        conds = ['self.tab_1.setEnabled(True)', 'self.tab_2.setEnabled(True)',
                 'self.tab_4.setEnabled(True)',
                 'self.tab_5.setEnabled(True)', 'self.tab_6.setEnabled(True)',
                 'self.tab_7.setEnabled(True)']
        outWin = self.polonator_textarea
        self.proc_start(cmd)


#===============================================================================
# Cycle Quality tab
#===============================================================================
    #QC button
    def start_QC(self):
        """
        'QC' button in Cycle Quality tab.
        
        This section needs to be modified so that the proc_finished() section
        doesn't loop.  Probably can't just make a new qprocess section because
        it would still limit the number of selected objects in cycleListPending.
        """
        self.process = QProcess(self)
        self.process.setProcessChannelMode(1)
        self.connect(self.process, SIGNAL("finished(int)"), self.finished_QC)
        self.connect(self.process, SIGNAL("readyRead"), self.readyRead_QC)
        global cmdlistQC
        global cycleQC
        global cycleQCitem
        global outWin
        pendlistQC = []
        cmdlistQC = []
        cycleQC = []
        cycleQCitem = []
        outWin = self.polonator_textarea
        self.outputTabs.setCurrentIndex(0)
        if self.cycleListPending.selectedItems() == []:
            outWin.append("No pending cycles selected.")
            return
        cnt = self.cycleListPending.count()
        print "# in Pending Cycle list " + str(cnt)
        if cnt == 0:
            self.outputTabs.setCurrentIndex(0)
            outWin.append("There are no pending cycles. Nothing to do.")
            return
        for i in xrange(cnt):
            if self.cycleListPending.isItemSelected(self.cycleListPending.item(i)):
                pendlistQC.append(self.cycleListPending.item(i))
        self.startQC.setEnabled(False)
        self.cycleListPending.setEnabled(False)
        for item in pendlistQC:
            seltext = str(item.text())
            cycleQCitem.append('pass')
            cycleQCitem.append(item)
            cycleQC.append('pass')
            cycleQC.append(seltext)
            cmdQC1 = (["python "+softwarePath+"/CycleQualityTab/disp_delta.py tetrahedra/" + seltext +
                    "-QC.delta QC-" + seltext + "-delta"])
            cmdQC2 = ["python "+softwarePath+"/CycleQualityTab/disp_regQC.py " + seltext]
            cmdlistQC.append(cmdQC1)
            cmdlistQC.append(cmdQC2)
        cmdQC = cmdlistQC[0]
        self.process.start(cmdQC[0])
        return


    def readyRead_QC(self):
        log = open("PolonatorProcessorLog.txt",'a')
        outtext = (str(self.process.readAllStandardOutput()).rstrip('\n'))
        self.polonator_textarea.append(outtext)
        self.polonator_textarea.ensureCursorVisible()
        self.polonator_textarea.append("still going!")
        print(outtext)
        log.write(outtext)
        log.close()

    def finished_QC(self, rv):
        if cycleQCitem[0] != 'pass':
            pendlocation = "GUI-data/qc_cycle_list_processing-done.dat"
            complocation = "GUI-data/qc_cycle_list_QC-done.dat"
            try:
                pendfilein = open(pendlocation,"r")
                compfilein = open(complocation,"r")
                pendlines = pendfilein.readlines()
                complines = compfilein.readlines()
                for i in xrange(len(pendlines)-1):
                    if cycleQC[0] in pendlines[i]:
                        del pendlines[i]
                        complines.append(cycleQC[0])
                pendfilein.close()
                compfilein.close()
                
                pendfileout = open(pendlocation,'w')
                compfileout = open(complocation,'w')
                for pendline in pendlines:
                    print >> pendfileout, pendline
                for compline in complines:
                    print >> compfileout, compline
                pendfileout.close()
                compfileout.close()
                
                compcyclerow = self.cycleListPending.row(cycleQCitem[0])
                compcycle = self.cycleListPending.takeItem(compcyclerow)
                self.cycleListComplete.addItem(compcycle)
                self.cycleListComplete.sortItems()

            except IOError:
                errormsg = "ERROR:\tCan't find either %(pendlocation)s or %(complocation)s." %vars()
                self.polonator_textarea.append(errormsg)
                log = open("PolonatorProcessorLog.txt",'a')
                log.write(errormsg)
                log.close()

        del cycleQC[0]
        del cycleQCitem[0]
        cmdQC = cmdlistQC[0]
        del cmdlistQC[0]
        if cmdlistQC != []:
            cmdQC = cmdlistQC[0]
        else:
            self.process = None
            self.startQC.setEnabled(True)
            self.cycleListPending.setEnabled(True)
            self.polonator_textarea.append("QC done.")
            log = open("PolonatorProcessorLog.txt",'a')
            log.write("QC done.")
            log.close()
            return
        self.polonator_textarea.append("Still going...")
        log = open("PolonatorProcessorLog.txt",'a')
        log.write("Still going...")
        log.close()
        self.process.start(cmdQC[0])

    def switchTab(self):
        """
        Switches right tab when clicking an item
        in the Complete Cycle list."""
        if self.ImageSwitchButton.isChecked():
            print "ImageSwitchButton is Checked!"
            self.outputTabs.setCurrentIndex(1)

    def cycle_ListComplete(self):
        """
        Display images in "Images" tab when item is selected
        in the Complete Cycles list in Cycle Quality tab.
        """
        global currentDisplayCycle

        currentDisplayCycle = ""
        print currentDisplayCycle
        n = self.cycleListComplete.currentRow()
        scene0 = QGraphicsScene()
        scene0.setSceneRect(0, 0, 250, 310)
        scene1 = QGraphicsScene()
        scene1.setSceneRect(0, 0, 250, 310)
        scene2 = QGraphicsScene()
        scene2.setSceneRect(0, 0, 250, 310)
        scene3 = QGraphicsScene()
        scene3.setSceneRect(0, 0, 250, 310)
        if n != -1:
            selitem = self.cycleListComplete.item(n)
            if currentDisplayCycle != selitem.text():
                currentDisplayCycle = str(selitem.text())
                print currentDisplayCycle
                
                fchistFilename = ("GUI-data/QC/QC-" + currentDisplayCycle +
                                  "-deltahist-cycle01.png")
                print fchistFilename
                self.statusbar.showMessage("Loading image " + fchistFilename)
                pic = QPixmap(fchistFilename).scaled(270,330,1,1)
                scene0.addItem(QGraphicsPixmapItem(pic))
                view0 = self.imageJPanel1
                view0.setScene(scene0)
                view0.setRenderHint(QPainter.Antialiasing)
                view0.show()

                fcmapFilename = ("GUI-data/QC/QC-" + currentDisplayCycle +
                                 "-deltafcmap-cycle01.png")
                self.statusbar.showMessage("Loading image " + fcmapFilename)
                pic = QPixmap(fcmapFilename).scaled(270,330,1,1)
                scene1.addItem(QGraphicsPixmapItem(pic))
                view1 = self.imageJPanel2
                view1.setScene(scene1)
                view1.setRenderHint(QPainter.Antialiasing)
                view1.show()
                
                fcregXFilename = ("GUI-data/QC/" + currentDisplayCycle +
                                  "_regQC-X.png")
                self.statusbar.showMessage("Loading image " + fcregXFilename)
                pic = QPixmap(fcregXFilename).scaled(270,330,1,1)
                scene2.addItem(QGraphicsPixmapItem(pic))
                view2 = self.alignXImageJPanel
                view2.setScene(scene2)
                view2.setRenderHint(QPainter.Antialiasing)
                view2.show()
                
                fcregYFilename = ("GUI-data/QC/" + currentDisplayCycle +
                                  "_regQC-Y.png")
                self.statusbar.showMessage("Loading image " + fcregYFilename)
                pic = QPixmap(fcregYFilename).scaled(270,330,1,1)
                scene3.addItem(QGraphicsPixmapItem(pic))
                view3 = self.alignYImageJPanel
                view3.setScene(scene3)
                view3.setRenderHint(QPainter.Antialiasing)
                view3.show()

#===============================================================================
# Image Viewing buttons
#===============================================================================
    def viewFCHist(self):
        """
        Displays FC Hist image in EOG popup window when
        button in Images tab is clicked."""
        print "FC Hist CLICKED!"
        if currentDisplayCycle == "":
            scene = QGraphicsScene()
            scene.addText("There is no image loaded.\n\n" +
                          "Choose an item from the Complete Cycles\n" + 
                          "list in the Cycle Quality tab.")
            view = self.imageJPanel1
            view.setScene(scene)
            view.show()
            return
        else:
            filename = ("GUI-data/QC/QC-" + currentDisplayCycle + "-deltahist-cycle01.png")
            QProcess.startDetached(ImageViewer + " " + filename)

    def viewFCMap(self):
        """
        Displays FC Map image in EOG popup window when
        button in Images tab is clicked."""
        print "FC Map CLICKED!"

        if currentDisplayCycle == "":
            scene = QGraphicsScene()
            scene.addText("There is no image loaded.\n\n" +
                          "Choose an item from the Complete Cycles\n" + 
                          "list in the Cycle Quality tab.")
            view = self.imageJPanel2
            view.setScene(scene)
            view.show()
            return
        else:
            filename = ("GUI-data/QC/QC-" + currentDisplayCycle + "-deltafcmap-cycle01.png")
            QProcess.startDetached(ImageViewer + " " + filename)
        
    def viewFCRegX(self):
        """
        Displays FC Reg-X image in EOG popup window when
        button in Images tab is clicked."""
        print "FC RegX CLICKED!"
        if currentDisplayCycle == "":
            scene = QGraphicsScene()
            scene.addText("There is no image loaded.\n\n" +
                          "Choose an item from the Complete Cycles\n" + 
                          "list in the Cycle Quality tab.")
            view = self.alignXImageJPanel
            view.setScene(scene)
            view.show()
            return
        else:
            filename = ("GUI-data/QC/" + currentDisplayCycle + "_regQC-X.png")
            QProcess.startDetached(ImageViewer + " " + filename)
        
    def viewFCRegY(self):
        """
        Displays FC Reg-Y image in EOG popup window when
        button in Images tab is clicked."""
        print "FC RegY CLICKED!"
        if currentDisplayCycle == "":
            scene = QGraphicsScene()
            scene.addText("There is no image loaded.\n\n" +
                          "Choose an item from the Complete Cycles\n" + 
                          "list in the Cycle Quality tab.")
            view = self.alignYImageJPanel
            view.setScene(scene)
            view.show()
            return
        else:
            filename = ("GUI-data/QC/" + currentDisplayCycle + "_regQC-Y.png")
            QProcess.startDetached(ImageViewer + " " + filename)


#===============================================================================
# Object Finder tab
#===============================================================================
    #Display Objects button
    def object_Display(self):
        """'Display Objects' button in Object Finder tab."""
        positionMax = 2179
        self.outputTabs.setCurrentIndex(0)
        if self.objectPosition.value() <= positionMax:
            cmd = ("."+softwarePath+"/ObjectFinderTab/run_display_objects.sh " +
                   "/opt/MATLAB/MATLAB_Component_Runtime/v77/ " +
                   str(self.objectFC.currentText()) + " " +
                   str(self.objectLane.currentText()) + " " +
                   str(self.objectPosition.value()))
            print cmd
            global nextFunc
            global args
            global outWin
            nextFunc = "self.proc_pass()"
            args = ['pass']
            outWin = self.polonator_textarea
            self.proc_start(cmd)


#===============================================================================
# Raw Images tab
#===============================================================================
    #Display Color Overlay button
    def raw_Display(self):
        """'Display Color Overlay' button in Raw Images tab."""
        self.outputTabs.setCurrentIndex(0)
        red = str(self.rawRed.currentText())
        green = str(self.rawGreen.currentText())  
        blue = str(self.rawBlue.currentText())
        filename1 = "none"
        filename2 = "none"
        filename3 = "none"
        rawImageValue = self.rawImage.value()
        image_string = "%(rawImageValue)04d" %vars()
        i = self.rawCycleList.currentRow()
        selection = self.rawCycleList.item(i)
        seltext = selection.text()
        if red != "None" or green != "None" or blue != "None":
            rExist = 1
            gExist = 1

            bExist = 1
            if red != "None":
                filename1 = ("GUI-data/images/" +
                             str(self.rawFlowcell.currentText()) + seltext +
                             "_" + red + "/" +
                             str(self.rawLane.currentText()) + "_" +
                             image_string + ".raw")
                print "red filename: " + filename1
                if not os.path.isfile(filename1):
                    self.polonator_textarea.append("ERROR:\t" + filename1 +
                                                   " does not exist.")
                    log = open("PolonatorProcessorLog.txt",'a')
                    log.write("ERROR:\t" + filename1 + " does not exist.")
                    log.close()
                    rExist = 0
            if green != "None":
                filename2 = ("GUI-data/images/" +
                             str(self.rawFlowcell.currentText()) + seltext +
                             "_" + green + "/" +
                             str(self.rawLane.currentText()) + "_" +
                             image_string + ".raw")
                print "green filename: " + filename2
                if not os.path.isfile(filename2):
                    self.polonator_textarea.append("ERROR:\t" + filename2 +
                                                   " does not exist.")
                    log = open("PolonatorProcessorLog.txt",'a')
                    log.write("ERROR:\t" + filename2 + " does not exist.")
                    log.close()
                    gExist = 0
            if blue != "None":
                filename3 = ("GUI-data/images/" +
                             str(self.rawFlowcell.currentText()) + seltext +
                             "_" + blue + "/" +
                             str(self.rawLane.currentText()) + "_" +
                             image_string + ".raw")
                print "blue filename: " + filename3
                if not os.path.isfile(filename3):
                    self.polonator_textarea.append("ERROR:\t" + filename3 +
                                                   " does not exist.")
                    log = open("PolonatorProcessorLog.txt",'a')
                    log.write("ERROR:\t" + filename3 + " does not exist.")
                    log.close()
                    bExist = 0

            if rExist == 0 or gExist == 0 or bExist == 0:
                return
            cmd = ("."+softwarePath+"/RawImagesTab/run_display_color_raw.sh " +
                   "/opt/MATLAB/MATLAB_Component_Runtime/v77/ " + str(filename1) +
                   " " + str(filename2) + " " + str(filename3))

            print "Executing " + cmd
            global nextFunc
            global args
            global outWin
            nextFunc = "self.proc_pass()"
            args = ['pass']
            outWin = self.polonator_textarea
            self.proc_start(cmd)
        else:
            self.polonator_textarea.append("ERROR:\tRed, Green, and Blue " +
                                           'dropdowns are all set to "None."\n' + 
                                           "\tNothing to show.")
            log = open("PolonatorProcessorLog.txt",'a')
            log.write("ERROR:\tRed, Green, and Blue " +
                      'dropdowns are all set to "None."\n' + 
                      "\tNothing to show.")
            log.close()


#===============================================================================
# Histogram tab
#===============================================================================
    #Display Histogram button
    def histogram_DrawHistogram(self):
        """'Display Histogram' button in Histogram tab."""
        if self.histogramCycleButton.isChecked() == True:
            subcmd = "python "+softwarePath+"/HistogramTab/histogram4.py"
        else:
            subcmd = "python "+softwarePath+"/HistogramTab/histogram.py"
        i = self.histogramFileList.currentRow()
        self.outputTabs.setCurrentIndex(0)
        if i != -1:
            self.histogramDrawHistogram.setEnabled(False)
            selection = self.histogramFileList.item(i)
            seltext = str(selection.text())
            threshText = str(self.histogramThreshold.text())
            if threshText == "":
                threshText = "0"
                self.histogramThreshold.setText("0")
            cmd = (subcmd + " " + seltext + " " +
                   str(self.histogramFlowcell.currentText()) + " " +
                   str(self.histogramLane.currentText()) + " " +
                   threshText)
            global nextFunc
            global args
            global outWin
            outWin = self.polonator_textarea
            nextFunc = "self.proc_pass()"
            args = ['self.histogramDrawHistogram.setEnabled(True)']
            self.proc_start(cmd)
        else:
            self.polonator_textarea.append("Nothing selected in the Histogram File List.")
            log = open("PolonatorProcessorLog.txt",'a')
            log.write("Nothing selected in the Histogram File List.")
            log.close()

    #LOAD CUTOFFS button
    def histogram_ImportCutoffs(self):
        """'Import Cutoffs' button in Histogram tab."""
        histogramCutoffArray = list()
        self.updateHistogramCutoffs(histogramCutoffArray)
        self.outputTabs.setCurrentIndex(0)
        self.histogramCutoff0_0.setText(histogramCutoffArray[0])
        self.histogramCutoff0_1.setText(histogramCutoffArray[1])
        self.histogramCutoff0_2.setText(histogramCutoffArray[2])
        self.histogramCutoff0_3.setText(histogramCutoffArray[3])
        self.histogramCutoff0_4.setText(histogramCutoffArray[4])
        self.histogramCutoff0_5.setText(histogramCutoffArray[5])
        self.histogramCutoff0_6.setText(histogramCutoffArray[6])
        self.histogramCutoff0_7.setText(histogramCutoffArray[7])
        self.histogramCutoff1_0.setText(histogramCutoffArray[8])
        self.histogramCutoff1_1.setText(histogramCutoffArray[9])
        self.histogramCutoff1_2.setText(histogramCutoffArray[10])
        self.histogramCutoff1_3.setText(histogramCutoffArray[11])
        self.histogramCutoff1_4.setText(histogramCutoffArray[12])
        self.histogramCutoff1_5.setText(histogramCutoffArray[13])
        self.histogramCutoff1_6.setText(histogramCutoffArray[14])
        self.histogramCutoff1_7.setText(histogramCutoffArray[15])
        self.polonator_textarea.append("-------------------------------------" +
                                       "-----------------------------")
        
        
    # SET CUTOFFS button
    def histogram_ExportCutoffs(self):
        """'Export Cutoffs' button in Histogram tab."""
        histogramCutoffArray = []
        self.outputTabs.setCurrentIndex(0)
        self.initializeHistogramCutoffFields(histogramCutoffArray)
        self.writeHistogramCutoffs(histogramCutoffArray)
        self.polonator_textarea.append("Cutoffs saved to primer_thresholds.dat.")
        log = open("PolonatorProcessorLog.txt",'a')
        log.write("Cutoffs saved to primer_thresholds.dat.")
        log.close()
    
    #GENERATE DATA button
    def histogram_GenerateData(self):
        """'Generate Data' button in Histogram tab."""
        a = self.histogramFileList.currentRow()
        self.outputTabs.setCurrentIndex(0)
        if a!=-1:
            self.tabWidget.setTabEnabled(5, False)
            aa = self.histogramFileList.item(a)
            selectedFile = aa.text()
            cmd = "python "+softwarePath+"/HistogramTab/makePrimerFile.py " + str(selectedFile)
            global nextFunc
            global args
            nextFunc = "self.proc_pass()"
            args = ['self.tabWidget.setTabEnabled(5, True)']
            outWin = self.polonator_textarea
            self.proc_start(cmd)

    #Single radio button
    def histogram_SingleButton(self):
        """'Single' radio button in Histogram tab."""
        self.updateHistogramFileList()
        self.histogramGenerateData.setEnabled(False)
    
    #Cycle radio button
    def histogram_CycleButton(self):
        """'Cycle' radio button in Histogram tab."""
        self.updateHistogramFileList()
        self.histogramGenerateData.setEnabled(True)
        

#===============================================================================
# Basecaller tab
#===============================================================================
    #ADD --> button
    def basecaller_AddButton(self):
        """
        Move selected item from Available Cycles to Read Order.
        
        The "TO DO" section was in the original Java code.
        """
        # TO DO:
        # add handling code here
        i = self.basecallerAvailCyclesList.currentRow()
        selection = self.basecallerAvailCyclesList.takeItem(i)
        self.basecallerReadOrderList.addItem(selection)
        if self.basecallerReadOrderList.count() == 1:
            self.basecallerReadOrderList.setCurrentRow(0)
        
    #<-- Remove button
    def basecaller_RemoveButton(self):
        """Move selected item from Read Order to Available Cycles."""
        i = self.basecallerReadOrderList.currentRow()
        selection = self.basecallerReadOrderList.takeItem(i)
        self.basecallerAvailCyclesList.addItem(selection)
        self.basecallerAvailCyclesList.sortItems(0)
        if self.basecallerAvailCyclesList.count() == 1:
            self.basecallerAvailCyclesList.setCurrentRow(0)
        
    #Add All --> button
    def basecaller_AddAllButton(self):
        """Move all items in Available Cycles to Read Order."""
        i = self.basecallerAvailCyclesList.count()
        while i >= 0:
            selection = self.basecallerAvailCyclesList.takeItem(i)
            self.basecallerReadOrderList.addItem(selection)
            i = i-1
        self.basecallerReadOrderList.sortItems(0)

    #Up button
    def basecaller_UpButton(self):
        """Move selected item in Read Order up one space."""
        i = self.basecallerReadOrderList.currentRow()
        selection = self.basecallerReadOrderList.takeItem(i-1)
        self.basecallerReadOrderList.insertItem(i, selection)
    
    #Down button
    def basecaller_DownButton(self):
        """Move selected item in Read Order down one space."""
        i = self.basecallerReadOrderList.currentRow()
        selection = self.basecallerReadOrderList.takeItem(i+1)
        self.basecallerReadOrderList.insertItem(i, selection)
    
    #Percent Data To Keep slider
    def basecaller_DataKeepSlider(self, value):
        """
        'Percent Data To Keep' slider in Basecaller tab.
        
        The 'To Do' section was in the original Java GUI.
        """
        position = str(value)
        self.basecallerPercentToKeepLabel.setText(position)
        # TO DO:
        # add handling code here
        
    #Percent Background Subtract slider
    def basecaller_BackgroundSubtractSlider(self, value):
        """
        'Percent Background Subtract' slider in Basecaller tab.
        
        The 'To Do' section was in the original Java GUI.
        """
        position = str(value)
        self.basecallerPercentBGSubtractLabel.setText(position)
        # TO DO:
        # add handing code here
        
    #RUN BASECALLER button
    def basecaller_RunBasecallerButton(self):
        """'Run Basecaller' button in Basecaller tab."""
        histogramCutoffArray = []
        self.initializeHistogramCutoffFields(histogramCutoffArray)
        self.writeHistogramCutoffs(histogramCutoffArray)
        self.outputTabs.setCurrentIndex(0)
        self.basecallerRunBasecallerButton.setEnabled(False)
        self.basecallerRunBasecallerResetButton.setEnabled(True)
        cmd1 = "./GUI-data/readspec"
        try:
            outfile = open(cmd1, "w")
            i = 0
            length = self.basecallerReadOrderList.count()
            while i < length:
                selitem = self.basecallerReadOrderList.item(i)
                value = selitem.text()
                outfile.write(value)
                outfile.write("\n")
                self.polonator_textarea.append('wrote "' + str(value) +
                                                   '" to "' + cmd1 + '"' )
                log = open("PolonatorProcessorLog.txt",'a')
                log.write('wrote "' + str(value) +'" to "' + cmd1 + '"' )
                log.close()
                i = i+1
            outfile.close()
        except IOError:
            self.polonator_textarea.append('"' + cmd1 + '" failed ')
            log = open("PolonatorProcessorLog.txt",'a')
            log.write('"' + cmd1 + '" failed ')
            log.close()
            
        cmd2 = ("python "+softwarePath+"/BasecallerTab/basecall.py " + str(self.basecallerReadfileFN.text()) +
                " " + str(self.basecallerPercentToKeepLabel.text()) + " " + 
                str(self.basecallerPercentBGSubtractLabel.text()))
        global nextFunc
        global args
        global outWin
        nextFunc = "self.proc_pass()"
        args = ['self.basecallerRunBasecallerButton.setEnabled(True)',
                'self.basecallerRunBasecallerResetButton.setEnabled(False)']
        outWin = self.polonator_textarea
        self.proc_start(cmd2)

    #Reset button
    def basecaller_RunBasecallerResetButton(self):
        """
        If the "Run Basecaller" has been interrupted, this will turn it back on."""
        proc.kill()
        outWin.append("\n\nBasecaller process killed.")
        self.basecallerRunBasecallerButton.setEnabled(True)
        self.basecallerRunBasecallerResetButton.setEnabled(False)


#===============================================================================
# Update functions
#===============================================================================

    #update Processes
    def updateProcesses1(self):
        """
        One of the things that runs on startup,
        along with a few buttons in Polonator tab.
        """
        print "updateProcesses1"
        cmd2 = "python "+softwarePath+"/UpdateFunctions/find_running_processes.py"
        path = os.path.realpath("")
        self.polonator_experiment.setText(path)
        self.polonator_textarea.append(path)
        log = open("PolonatorProcessorLog.txt",'a')
        log.write(path)
        log.close()
        global nextFunc
        global args
        global outWin
        nextFunc = "self.updateProcesses2()"
        args = ['self.polonator_process.setEnabled(True)',
                'self.polonator_initialize.setEnabled(True)',
                'self.polonator_processorpath.setText("")',
                'self.polonator_processorstatus.setText("NOT RUNNING")',
                'self.polonator_initializepath.setText("")',
                'self.polonator_initializestatus.setText("NOT RUNNING")']
        outWin = self.polonator_textarea
        for cond in conds:
            args.append(cond)
        print "args: " + str(args)
        self.proc_start_2(cmd2)
        return 

    def updateProcesses2(self):
        """Continuation of updateProcesses1."""
        print "updateProcesses2"
        cmd3 = "/home/polonator/PROCESS_STATUS"
        self.polonator_process.setEnabled(False)
        self.polonator_initialize.setEnabled(False)
        try:
            print "updateProcesses2 Try1"
            r3 = open(cmd3)
            out3 = r3.readlines()
            worked = True
            r3.close()
        except IOError:
            print "updateProcesses2 Except"
            self.polonator_textarea.append('"' + cmd3 + '" failed to open')
            log = open("PolonatorProcessorLog.txt",'a')
            log.write('"' + cmd3 + '" failed to open')
            log.close()
            worked = False
        if worked == True:
            print "updateProcesses2 Worked"


            print str(out3)
            for line in out3:
                line = line.rstrip("\n")
                if line.startswith("P") == True:
                    self.startswithP(line)
                    #initialize_clicked=False
                    #processor_clicked=False
                if line.startswith("R") or line.startswith("I"):
                    self.startswithRI(line)
                    #initialize_clicked=False
                    #processor_clicked=False
        else: print "r3 if loop off"
        self.polonator_process.setEnabled(True)
        self.polonator_initialize.setEnabled(True)

    def startswithP(self, line):
        """When a line in the file from updateProcesses3 starts with P."""
        print "startswithP"
        self.polonator_processorpath.setText(line[2])
        self.polonator_processorstatus.setText("RUNNING")
        self.polonator_processorpath.setStyleSheet(QApplication.translate("MainWindow",
                                                                          "background-color: rgb(102,255,102);",
                                                                          None, QApplication.UnicodeUTF8))

        
    def startswithRI(self, line):
        """When a line in the file from updateProcesses3 starts with R or I."""
        print "startswithRI"
        self.polonator_initializepath.setText(line[2])
        self.polonator_initializestatus.setText("RUNNING")
        self.polonator_initializepath.setStyleSheet(QApplication.translate("MainWindow",
                                                                           "background-color: rgb(102,255,102);",
                                                                           None, QApplication.UnicodeUTF8))

    #Custom QProcess Set for updateProcesses1
    def proc_start_2(self, cmd):
        """
        This QProcess set is specifically for self.updateProcesses1().
        Otherwise it is identical to the first QProcess set.
        Start QProcess and make connections.
        """
        print "proc_start_2"
        print cmd
        global proc_2
        cmd = QString(cmd)
        proc_2 = QProcess()
        proc_2.start(cmd)
        self.connect(proc_2, SIGNAL("readyRead()"), self.proc_readyRead_2)
        self.connect(proc_2, SIGNAL("finished(int)"), self.proc_finished_2)

    def proc_readyRead_2(self):
        """Append standard output line to QTextEdit."""
        print "proc_readyRead_2"
        log = open("PolonatorProcessorLog.txt",'a')
        outWin.append(str(proc_2.readLine()).rstrip('\n'))
        log.write(str(proc_2.readLine()).rstrip('\n'))
        log.close()
        
    def proc_finished_2(self):
        """
        When QProcess is finished, print error, close process, perform
        post-process commands, and go to next function.
        """
        print "proc_finished_2 1"
        log = open("PolonatorProcessorLog.txt",'a')
        outWin.append(QString(proc_2.readAllStandardError()))
        print "proc_finished_2 2"
        outWin.append("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        log.write(str(proc_2.readAllStandardError()))
        log.close()
        print "proc_finished_2 3"
        proc_2.close()
        print "proc_finished_2 4"
        for arg in args:
            exec(arg)
            print "done arg " + str(args.index(arg)) + ": " + arg
        print "proc_finished_2 5"
        eval(nextFunc)
        print "proc_finished_2 6"

    def proc_pass_2(self):
        """End of a set of QProcesses."""
        print "proc_pass_2"
        return

    #update BasecallerAvailableList
    def updateBasecallerAvailableList(self):
        """Update Available List in Basecaller tab."""
        if self.basecallerAvailCyclesList.currentRow() == -1:
            i = 0
        else:
            i = self.basecallerAvailCyclesList.currentRow()
        self.basecallerAvailCyclesList.clear()
        cmd = "GUI-data/qc_cycle_list.dat"
        r = open(cmd)
        tries = 0
        while tries < 5:
            try:
                out = r.readlines()
                for line in out:
                    line = line.rstrip("\r\n")
                    item = QListWidgetItem(line)
                    self.basecallerAvailCyclesList.addItem(item)
                    self.polonator_textarea.insertPlainText(line + ", ")
                self.polonator_textarea.textCursor().deletePreviousChar()
                self.polonator_textarea.textCursor().deletePreviousChar()
                self.polonator_textarea.append('"' + cmd + '" success\n')
                log = open("PolonatorProcessorLog.txt",'a')
                log.write('"' + cmd + '" success\n')
                log.close()
                tries = 6
            except IOError:
                tries += 1
                self.polonator_textarea.append('"' + cmd + '" failed ' +
                                               str(tries) + " times")
                log = open("PolonatorProcessorLog.txt",'a')
                log.write('"' + cmd + '" failed ' + str(tries) + " times")
                log.close()
        r.close()

        if self.basecallerAvailCyclesList.item(0):
            if self.basecallerAvailCyclesList.item(0).text() == '':
                self.basecallerAvailCyclesList.takeItem(0)
        self.basecallerAvailCyclesList.sortItems()

        if i > self.basecallerAvailCyclesList.count()-1:
            i = self.basecallerAvailCyclesList.count()-1
        self.basecallerAvailCyclesList.setCurrentRow(i)
    

    #Initialize Histogram Cutoff Fields
    def initializeHistogramCutoffFields(self, histogramCutoffArray = list()):
        """Create the histogram cutoff list to be saved."""
        histogramCutoffArray.append(int(self.histogramCutoff0_0.text()))
        histogramCutoffArray.append(int(self.histogramCutoff0_1.text()))
        histogramCutoffArray.append(int(self.histogramCutoff0_2.text()))
        histogramCutoffArray.append(int(self.histogramCutoff0_3.text()))
        histogramCutoffArray.append(int(self.histogramCutoff0_4.text()))
        histogramCutoffArray.append(int(self.histogramCutoff0_5.text()))
        histogramCutoffArray.append(int(self.histogramCutoff0_6.text()))
        histogramCutoffArray.append(int(self.histogramCutoff0_7.text()))
        histogramCutoffArray.append(int(self.histogramCutoff1_0.text()))
        histogramCutoffArray.append(int(self.histogramCutoff1_1.text()))
        histogramCutoffArray.append(int(self.histogramCutoff1_2.text()))
        histogramCutoffArray.append(int(self.histogramCutoff1_3.text()))
        histogramCutoffArray.append(int(self.histogramCutoff1_4.text()))
        histogramCutoffArray.append(int(self.histogramCutoff1_5.text()))
        histogramCutoffArray.append(int(self.histogramCutoff1_6.text()))
        histogramCutoffArray.append(int(self.histogramCutoff1_7.text()))
        return histogramCutoffArray

    def writeHistogramCutoffs(self, histogramCutoffArray):
        """Save the list created in initializeHistogramCutoffFields()."""
        try:
            outfile = open('GUI-data/primer_thresholds.dat','w')
            i = 0
            while i < 16:
                if histogramCutoffArray[i] >= 0 and histogramCutoffArray[i] < 16384:
                    outfile.write(str(histogramCutoffArray[i]) + "\n")
                else:
                    outfile.write("0\n")
                    histogramCutoffArray[i] = 0
                i = i+1
            outfile.close()
        except IOError:
            print "can't write to file GUI-data/primer_thresholds.dat"
        
    #update Histogram Cutoffs
    def updateHistogramCutoffs(self, histogramCutoffArray):
        """Update histogram cutoff list."""
        cmd = "GUI-data/primer_thresholds.dat"
        try:
            r = open(cmd)
            tries = 0
            while tries < 5:
                try:
                    out = r.readlines()
                    for line in out:
                        line = line.rstrip("\n")
                        histogramCutoffArray.append(line)
                        self.polonator_textarea.insertPlainText(line + ", ")
                    if len(histogramCutoffArray) < 16:
                        i = len(histogramCutoffArray)-1
                        while i < 15:
                            histogramCutoffArray.append('0')
                            i = i+1
                    tries = 6
                except IOError:
                    tries += 1
                    self.polonator_textarea.append('"' + cmd + '" failed ' +
                                                   str(tries) + " times")
                    log = open("PolonatorProcessorLog.txt",'a')
                    log.write('"' + cmd + '" failed ' + str(tries) + " times")
                    log.close()
            r.close()
            self.polonator_textarea.textCursor().deletePreviousChar()
            self.polonator_textarea.textCursor().deletePreviousChar()
            self.polonator_textarea.append('"' + cmd + '" success \n')
            log = open("PolonatorProcessorLog.txt",'a')
            log.write('"' + cmd + '" success \n')
            log.close()
        except IOError:
            self.polonator_textarea.append('"' + cmd + '" does not exist.\n')
            log = open("PolonatorProcessorLog.txt",'a')
            log.write('"' + cmd + '" does not exist.\n')
            log.close()
            histogramCutoffArray = list()
            for i in xrange(15):
                histogramCutoffArray.append('0')
        return histogramCutoffArray
    
    #update Histogram File List
    def updateHistogramFileList(self):
        """Update the Histogram File List field."""
        i = self.histogramFileList.currentRow()
        if True:
            print("Histogram Single Button checked " +
                  str(self.histogramSingleButton.isChecked()))
            print("Histogram Cycle Button checked " + 
                  str(self.histogramCycleButton.isChecked()))
            histogramFileListData = list()
            if self.histogramSingleButton.isChecked() == True:
                self.histogramCycleButton.setChecked(False)
                children = os.listdir('GUI-data/beads')
                if children == []:
                    self.polonator_textarea.append("Nothing in path 'GUI-data/beads'")
                    log = open("PolonatorProcessorLog.txt",'a')
                    log.write("Nothing in path 'GUI-data/beads'")
                    log.close()
                    pass
                else:
                    for child in children:
                        if ".beadsums_full" in child:
                            filename = child
                            cstring = filename[2:filename.index(".beadsums_full")]
                            histogramFileListData.append(cstring)
                        
            if self.histogramCycleButton.isChecked() == True:
                self.histogramSingleButton.setChecked(False)
                cmd = "GUI-data/qc_cycle_list.dat"
                r=open(cmd)
                tries = 0
                while tries < 5:
                    try:
                        out = r.readlines()
                        for line in out:
                            line = line.rstrip("\r\n")
                            histogramFileListData.append(line)
                        tries = 6
                        self.polonator_textarea.append('"' + cmd + '" success')
                        log = open("PolonatorProcessorLog.txt",'a')
                        log.write('"' + cmd + '" success')
                        log.close()
                    except IOError:
                        tries += 1
                        self.polonator_textarea.append('"' + cmd + '" failed ' +
                                                       str(tries) + " times")
                        log = open("PolonatorProcessorLog.txt",'a')
                        log.write('"' + cmd + '" failed ' + str(tries) + " times")
                        log.close()
                r.close()

            if self.histogramFileList.item(0):
                if self.histogramFileList.item(0).text() == '':
                    self.histogramFileList.takeItem(0)

            histogramFileListData.sort()
            self.histogramFileList.clear()
            for value in histogramFileListData:
                self.histogramFileList.addItem(value)
            if self.histogramFileList.item(0):
                if self.histogramFileList.item(0).text() == '':
                    self.histogramFileList.takeItem(0)
            flen = len(histogramFileListData)
            if i == -1:
                i = 0
            if flen <= (i+1):
                self.histogramFileList.setCurrentRow(flen-1)
            else:
                self.histogramFileList.setCurrentRow(i)

            
    def procImageVerifier(self):
        """This was blank in the original java gui also."""
        pass
    
    def updateQualityLists(self):
        """
        Update the lists in the Complete Cycles,
        Pending Cycles, and In Progress.
        """
        completedListData = list()
        pendingListData = list()
        inprogressListData = list()
        currentSelection = self.cycleListComplete.currentRow()
        currentSelection2 = self.rawCycleList.currentRow()
        currentSelection3 = self.cycleListPending.currentRow()
        if currentSelection2 == -1:
            currentSelection2 = 0

        """Complete Cycles list"""
        cmd1 = "GUI-data/qc_cycle_list_QC-done.dat"
        r1 = open(cmd1)
        tries1 = 0
        while tries1 < 5:
            try:
                out1 = r1.readlines()
                for line in out1:
                    line = line.rstrip("\n")
                    TorF = line in completedListData
                    if TorF == False:
                        completedListData.append(line)
                    self.polonator_textarea.insertPlainText(line + ", ")
                self.polonator_textarea.textCursor().deletePreviousChar()
                self.polonator_textarea.textCursor().deletePreviousChar()
                completedListData.sort()
                self.cycleListComplete.clear()
                self.rawCycleList.clear()
                for value in completedListData:
                    self.cycleListComplete.addItem(value)
                    self.cycleListComplete.setCurrentRow(currentSelection)
                    self.rawCycleList.addItem(value)
                    self.rawCycleList.setCurrentRow(currentSelection2)
                
                self.polonator_textarea.append('"' + cmd1 + '" success \n')
                log = open("PolonatorProcessorLog.txt",'a')
                log.write('"' + cmd1 + '" success \n')
                log.close()
                tries1 = 6
            except IOError:
                tries1 += 1
                self.polonator_textarea.append('"' + cmd1 + '" failed ' +
                                               str(tries1) + " times")
                log = open("PolonatorProcessorLog.txt",'a')
                log.write('"' + cmd1 + '" failed ' + str(tries1) + " times")
                log.close()
        r1.close()
        if self.cycleListComplete.item(0):
            if self.cycleListComplete.item(0).text() == '':
                self.cycleListComplete.takeItem(0)
        if self.rawCycleList.item(0):
            if self.rawCycleList.item(0).text() == '':
                self.rawCycleList.takeItem(0)
        
        """Pending Cycles list"""
        cmd2 = "GUI-data/qc_cycle_list_processing-done.dat"
        r2 = open(cmd2)
        tries2 = 0
        while tries2 < 5:
            try:
                out2 = r2.readlines()
                for line in out2:
                    line = line.rstrip("\r\n")
                    TorF = line in completedListData
                    if TorF == False:
                        pendingListData.append(line)
                    self.polonator_textarea.insertPlainText(line + ", ")
                self.polonator_textarea.textCursor().deletePreviousChar()
                self.polonator_textarea.textCursor().deletePreviousChar()
                self.cycleListPending.clear()
                self.cycleListPending.addItems(pendingListData)
                self.polonator_textarea.append('"' + cmd2 + '" success \n')
                log = open("PolonatorProcessorLog.txt",'a')
                log.write('"' + cmd2 + '" success \n')
                log.close()
                tries2 = 6
                self.cycleListPending.setCurrentRow(currentSelection3)
            except IOError:
                tries2 += 1
                self.polonator_textarea.append('"' + cmd2 + '" failed ' +
                                               str(tries2) + " times")
                log = open("PolonatorProcessorLog.txt",'a')
                log.write('"' + cmd2 + '" failed ' + str(tries2) + " times")
                log.close()
        r2.close()
        if self.cycleListPending.item(0):
            if self.cycleListPending.item(0).text() == '':
                self.cycleListPending.takeItem(0)

        """Cycles In Progress list"""
        cmd3 = "GUI-data/qc_cycle_list.dat"
        r3 = open(cmd3)
        tries3 = 0
        while tries3 < 5:
            try:
                out3 = r3.readlines()
                for line in out3:
                    line = line.rstrip("\r\n")
                    compLD = line in completedListData
                    pendLD = line in pendingListData
                    if compLD == False or pendLD == False:
                        inprogressListData.append(line)
                    self.polonator_textarea.insertPlainText(line + ", ")
                self.polonator_textarea.textCursor().deletePreviousChar()
                self.polonator_textarea.textCursor().deletePreviousChar()
                self.cycleListInProgress.clear()
                self.cycleListInProgress.addItems(inprogressListData)
                self.cycleListInProgress.sortItems()
                self.polonator_textarea.append('"' + cmd3 + '" success')
                log = open("PolonatorProcessorLog.txt",'a')
                log.write('"' + cmd3 + '" success')
                log.close()
                tries3 = 6
            except IOError:
                tries3 += 1
                self.polonator_textarea.append('"' + cmd3 + '" failed ' +
                                               str(tries3) + " times")
                log = open("PolonatorProcessorLog.txt",'a')
                log.write('"' + cmd3 + '" failed ' + str(tries3) + " times")
                log.close()
        r3.close()
        if self.cycleListInProgress.item(0):
            if self.cycleListInProgress.item(0).text() == '':
                self.cycleListInProgress.takeItem(0)
        

#===============================================================================
# Menu Bar
#===============================================================================
    def menuOpen(self):
        """Open a folder containing a project.
        
        There are currently no checks in place to make sure the folder is a
        legitimate project folder.  You will just get errors saying files
        don't exist."""
        print "Open command clicked!"
        openDialog = QFileDialog()
        projectPath = str(openDialog.getExistingDirectory(self,
                      self.tr("Open a folder containing a project."),
                      QDir.homePath()))
        print projectPath
        os.chdir(projectPath)
        self.timer1.singleShot(1, self.timerUpdate)
        self.timer1.start(60000)
        
        
#===============================================================================
# The End
#===============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = PolonatorProcessor()
    myapp.show()
    sys.exit(app.exec_())
