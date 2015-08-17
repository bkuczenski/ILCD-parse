'''
Created on Aug 16, 2015

@author: Brandon
'''

import lxml.etree as ET
import re
import uuid

class IlcdEntity(object):
    '''
    classdocs
    '''
    
    def dataType(self):
        """extracts the data type from the XML root element"""
        R=self.getroot()
        return re.sub(r'{([^}]+)}(.*)DataSet$',r'\2',R.tag, count=1)

    def El(self, el, ns=None):
        R=self.getroot()
        return R.find('.//{0}{1}'.format('{' + R.nsmap[ns] + '}',el))

    def Els(self, el, ns=None):
        R=self.getroot()
        return R.findall('.//{0}{1}'.format('{' + R.nsmap[ns] + '}',el))

    def commonEl(self, el):
        return self.El(el, 'common')

    def uuid(self, my_uuid=None):
        """ 
        without an argument, query and return the UUID
        with an argument, set the UUID
        """
        uel = self.commonEl('UUID')
        if my_uuid==None:
            return uuid.UUID(uel.text)
        elif isinstance(my_uuid,uuid.UUID):
            uel.text = str(my_uuid)
            return my_uuid
        else:
            try:
                val = uuid.UUID(my_uuid,)
            except:
                print my_uuid
                print 'Not a valid UUID'
                return False

            uel.text = str(val)
            return val

    def version(self, my_version=[]):
        R=self.getroot()
        if len(my_version)==0:
            return R.find('.//common:dataSetVersion', R.nsmap).text.split('.')
        else:
            while len(my_version)<3:
                my_version.append('0')
            v = [int(k) for k in my_version]
            v_str='{0:02}.{0:02}.{0:03}'.format(v[0],v[1],v[2])
            R.find('.//common:dataSetVersion', R.nsmap).text = v_str
            return my_version

    def tickMajorVersion(self):
        """ increase the major version XX.00.000 by 1 count"""
        R=self.getroot()
        ver = R.find('.//common:dataSetVersion', R.nsmap).text.split('.')
        ver[0]='{0:02}'.format(int(ver[0])+1)
        R.find('.//common:dataSetVersion', R.nsmap).text = '.'.join(ver)

    def tickMinorVersion(self):
        """ increase the minor version 00.XX.000 by 1 count"""
        R=self.getroot()
        ver = R.find('.//common:dataSetVersion', R.nsmap).text.split('.')
        ver[1]='{0:02}'.format(int(ver[1])+1)
        R.find('.//common:dataSetVersion', R.nsmap).text = '.'.join(ver)

    def tickVersionRev(self):
        """ increase the version rev-number 00.00.XXX by 1 count"""
        R=self.getroot()
        ver = R.find('.//common:dataSetVersion', R.nsmap).text.split('.')
        ver[2]='{0:03}'.format(int(ver[2])+1)
        R.find('.//common:dataSetVersion', R.nsmap).text = '.'.join(ver)

    def getroot(self):
        return self.xmlfile.getroot()
    
    def write(self, savepath):
        with open(savepath, 'wb') as f:
            self.xmlfile.write(f, pretty_print=True)

    def __init__(self, filepath, datatype=None):
        """
        Instantiate a new ILCD entity from an XML file.
        Optionally specify expected data type and return error if types don't match
        """
        parser = ET.XMLParser(remove_blank_text=True)
        self.xmlfile = ET.parse(filepath,parser)
        if datatype != None:
            if self.dataType() != datatype:
                raise ValueError
        
        
        