#!/usr/bin/env python

# -*- coding: utf-8 -*-

##    Description    eTOXlab component for runing a predictive model
##                   
##    Authors:       Manuel Pastor (manuel.pastor@upf.edu) 
##
##    Copyright 2013 Manuel Pastor
##
##    This file is part of eTOXlab.
##
##    eTOXlab is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation version 3.
##
##    eTOXlab is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with eTOXlab.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import getopt
import shutil

from utils import lastVersion
from utils import writeError
from utils import removefile
from utils import sandVersion

def view (endpoint, molecules, model, verID):
    """Top level view function

       molecules:  SDFile containing the collection of 2D structures to be predicted
       verID:      version of the model that will be used. Value -1 means the last one
       
    """
    
    # getMolecule
    if verID != -99:
        vv = lastVersion (endpoint, verID)
        
    va = sandVersion (endpoint)

    # if model was provided copy model to sandbox, either from argument or from version
    if model:
        #shutil.copy (model,va+'/imodel.py')
        shutil.copy (model,va+'/iview.py')
    else:
        shutil.copy (vv+'/imodel.py',va+'/iview.py')

##    if not molecules:
##        molecules = vv+'/training.sdf'

    # load model
    try:
        sys.path.append(va)
        from iview import imodel
        model = imodel (va)
    except:
        return (False, 'unable to load iview')

    if not model:
        return (False, 'unable to load iview')
    
    result = model.viewWorkflow (molecules)

    return (result)

    
def usage ():
    """Prints in the screen the command syntax and argument"""
    
    print 'view -e endpoint [-f filename.sdf][-v 1|last]'

def main ():

    endpoint = None
    ver = -99
    mol = None
    mod = None

    try:
       opts, args = getopt.getopt(sys.argv[1:], 'e:f:v:m:h')

    except getopt.GetoptError:
       writeError('Error. Arguments not recognized')
       usage()
       sys.exit(1)

    if args:
       writeError('Error. Arguments not recognized')
       usage()
       sys.exit(1)
        
    if len( opts ) > 0:
        for opt, arg in opts:

            if opt in '-e':
                endpoint = arg               
            elif opt in '-f':
                mol = arg
            elif opt in '-m':
                mod = arg
            elif opt in '-v':
                if 'last' in arg:
                    ver = -1
                else:
                    try:
                        ver = int(arg)
                    except ValueError:
                        ver = -99

            elif opt in '-h':
                usage()
                sys.exit(0)

    if not mol and ver==-99:
        usage()
        sys.exit(1)

    if not mod and ver==-99:
        usage()
        sys.exit(1)

    if mod and mol and ver!=-99:
        usage()
        sys.exit(1)
        
    if not endpoint:
        usage()
        sys.exit (1)


    result=view (endpoint, mol, mod, ver)

    print result

    sys.exit(0)
        
if __name__ == '__main__':
    
    main()