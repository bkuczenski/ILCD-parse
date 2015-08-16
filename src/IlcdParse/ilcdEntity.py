'''
Created on Aug 16, 2015

@author: Brandon
'''

import lxml.etree as ET
import re
import uuid

class ilcdEntity(ET):
    '''
    classdocs
    '''
    def dataType(self):
        """extracts the data type from the XML root element"""
        R=self.getroot()
        return re.sub(r'{([^}]+)}(.*)DataSet$',r'\2',R.tag, count=1)

    def uuid(self, my_uuid=''):
        """ 
        without an argument, query and return the UUID
        with an argument, set the UUID
        """
        R=self.getroot()
        if my_uuid.empty():
            return uuid.UUID(R.find('.//common:UUID', R.nsmap).text)
        else:
            try:
                val = uuid.UUID(my_uuid)
            except:
                print 'Not a valid UUID'
                return False

            R.find('.//common:UUID', R.nsmap).text = str(val)
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

        