# -*- coding: utf-8 -*-
import os

from plugins import DataPlugin

# Import PyQt5 classes
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebKit import *
from PyQt5.QtNetwork import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtPrintSupport import *


import utils
import csv
import xml.etree.cElementTree as et
from collections import defaultdict

import numpy as np

import ui, db
from data import DataSet

class ImportMetabolights( ui.ImportDataView ):

    import_filename_filter = "All compatible files (*.csv);;Comma Separated Values (*.csv);;All files (*.*)"
    import_description =  "Open experimental data from Metabolights experimental datasets"

    def __init__(self, plugin, parent, **kwargs):
        super(ImportTextView, self).__init__(plugin, parent, **kwargs)

       
    # Data file import handlers (#FIXME probably shouldn't be here)
        
    def load_datafile(self, filename):
        self.load_metabolights()
        
    def load_metabolights(self, filename, id_col=0, name_col=4, data_col=18): # Load from csv with experiments in COLUMNS, metabolites in ROWS
        print "Loading Metabolights..."
        
        #sample	1	2	3	4
        #class	ADG10003u_007	ADG10003u_008	ADG10003u_009	ADG10003u_010   ADG19007u_192
        #2-oxoisovalerate	0.3841	0.44603	0.45971	0.40812
        reader = csv.reader( open( filename, 'rU'), delimiter='\t', dialect='excel')
    
        # Sample identities from top row ( sample labels )
        hrow = reader.next()
        sample_ids = hrow[1:]    

        # Sample classes from second row; crop off after u_
        hrow = reader.next()
        classes = hrow[1:]    
        classes = [ c.split('u_')[0] for c in classes]

        metabolites = []
        metabolite_data = []
        # Read in metabolite data n.b. can have >1 entry / metabolite so need to allow for this
        for row in reader:
            metabolites.append( row[0] )
            metabolite_data.append( row[1:] )
            
        ydim = len( classes )
        xdim = len( metabolites )
        
        dso = self.data.o['output']
        dso.empty(size=(ydim, xdim))

        dso.labels[0] = sample_ids
        dso.classes[0] = classes 

        dso.labels[1] = metabolites

        for n,md in enumerate(metabolite_data):
            dso.data[:,n] = np.array(md)
        

class ImportMetabolights(DataPlugin):

    def __init__(self, **kwargs):
        super(ImportMetabolights, self).__init__(**kwargs)
        self.register_app_launcher( self.app_launcher )

    def app_launcher(self):
        #self.load_data_file()
        self.instances.append( ImportMetabolightsView( self, self.m ) )

    

