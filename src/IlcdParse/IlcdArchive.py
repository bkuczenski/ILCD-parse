'''
Created on Jul 24, 2015

@author: Brandon
'''

import os
import uuid
from .IlcdEntity import IlcdEntity


class IlcdArchive(object):
    '''
    Stores a reference to an ILCD archive directory structure.
    '''
    root="."
    
    typeDirs={'Process':'processes',
              'Flow':'flows',
              'LCIAMethod':'lciamethods',
              'FlowProperty':'flowproperties',
              'UnitGroup':'unitgroups',
              'Source':'sources',
              'Contact':'contacts'
              }
    
    def dataPath(self, datatype):
        return os.path.join(self.root,'ILCD',self.typeDirs[datatype])
    
    def listFiles(self, datatype):
        Fs = os.listdir(self.dataPath(datatype))
        #for f in Fs:
        #    print f
        return Fs
            
        
    def createLciaFromTemplate(self,template='lcia-template.xml'):
        T=IlcdEntity(template)
        if T.dataType() != 'LCIAMethod':
            print 'Input file is not an LCIAMethod data set'
            return []
        my_uuid=uuid.uuid4() # create new random UUID
        T.uuid(my_uuid)
        return T

    def saveIlcdEntity(self, T):
        fname = str(T.uuid()) + '.xml'
        savepath = os.path.join(self.dataPath(T.dataType()),fname)
        try: 
            T.write(savepath)
        except:
            print 'error encountered saving to ' + savepath
            return False
            
        print T.dataType() + ' file ' + fname + ' written.'
        return True


    def findUuid(self, uid):
        """
        uid is either a UUID or a string that should represent a valid UUID
        """
        matches = []
        name = str(uid)+'.xml'
        for path in self.typeDirs.iterkeys():
            if name in os.listdir(self.dataPath(path)):
                matches.append(os.path.join(self.dataPath(path), name))
        
        if len(matches)==1:
            return IlcdEntity(matches[0])
        else:
            print '{0} matches found.'.format(len(matches))
            return []

            
            
                
        
    
    def __init__(self, root):
        '''
        Constructor
        '''
        # first validate that root points to an ILCD archive
        if os.path.exists(os.path.join(root,'ILCD'))==True:
            self.root=root
            print "ILCD archive found at root path"
        else: 
            print "root path does not appear to be an ILCD archive."
            
        
    # def getProcesses(self):
    #  return 
        