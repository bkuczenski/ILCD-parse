'''
Created on Aug 16, 2015

@author: Brandon
'''

from .IlcdArchive import IlcdArchive
import lxml.etree as ET
import sys
import os


impactCategories = [ 'Abiotic resource depletion',
'Acidification',
'Aquatic eco-toxicity',
'Aquatic Eutrophication',
'Biotic resource depletion',
'Cancer human health effects',
'Climate change',
'Ionizing radiation',
'Land use',
'Non-cancer human health effects',
'Ozone depletion',
'Photochemical ozone creation',
'Respiratory inorganics',
'Terrestrial Eutrophication',
'other' ]

indicatorTypes = [ 'Area of Protection damage indicator',
'Combined single-point indicator',
'Damage indicator',
'Mid-point indicator']

def getReferenceFlow(flow,nsmap):
    """
    flow is an IlcdEntity of type flow
    """
    _id = int(flow.El('referenceToReferenceFlowProperty').text)
    rfp = flow.El('flowProperties').getchildren()[_id]
    return nonemap(rfp,'referenceToFlowPropertyDataSet').attrib['refObjectId']

def selectFromList(lst):
    choices = dict((i, f) for i, f in enumerate(f for f in lst))
    for choice in sorted(choices.items()):
        print '[%s] %s' % choice
    select = None
    while select is None:
        select = choices.get(int(raw_input('Enter selection: ')))
        if not select:
            print 'Please make a valid selection!'
    return select
    

def nonemap(x,el):
    return x.find('{0}{1}'.format('{'+x.nsmap[None]+'}',el))

def convertProcessToLcia(O,p):
    """
    O is ILCD Archive
    p is process file
    """
    
    # the players
    P = O.findUuid(os.path.splitext(p)[0])
    print 'Importing: ' + P.El('baseName').text
    L = O.createLciaFromTemplate()
    
    lcia_ns = L.getroot().nsmap
    
    # the basic data
    L.El('name','common').text = P.El('baseName').text
    L.El('methodology').text = 'TRACI 2.0'
    L.El('impactCategory').text = selectFromList(impactCategories)
    L.El('impactIndicator').text = raw_input('Impact Indicator: ')
    L.El('referenceYear').text = P.El('referenceYear','common').text
    L.El('duration').text = 'indefinite'
    L.El('interventionLocation').text = 'US'
    L.El('impactLocation').text = 'US'

    L.El('typeOfDataSet').text = selectFromList(indicatorTypes)
    L.El('normalisation').text= 'false'
    L.El('weighting').text = 'false'
    
    QR=L.El('quantitativeReference')
    CF=L.El('characterisationFactors')
    
    # the exchanges
    Xs = P.El('exchanges').getchildren()
    for x in Xs:
        flow_el = nonemap(x,'referenceToFlowDataSet')
        flow_uuid = flow_el.attrib['refObjectId']
        flow_comment = flow_el.getchildren()[0]
        if nonemap(x, 'exchangeDirection').text == 'Input':
            # Input exchange = reference flow
            ref_uuid = getReferenceFlow(O.findUuid(flow_uuid), nsmap = lcia_ns)
            RQ = ET.Element('referenceQuantity',
                            attrib = {'type':'flow property data set',
                                      'refObjectId':ref_uuid,
                                      'uri':'../flowproperties/{0}.xml'.format(ref_uuid)},
                            nsmap = lcia_ns)
            RQ.append(flow_comment)
            QR.append(RQ)
            print 'reference flow: {0} {1}'.format(ref_uuid,flow_comment.text)
            
        else:
            # Output exchange = new factor
            mean_value = 1 / float(nonemap(x, 'resultingAmount').text) # note inversion!
            F = ET.Element('factor',nsmap = lcia_ns)
            FL = ET.Element('referenceToFlowDataSet', 
                          attrib={'type':'flow data set',
                                  'refObjectId':flow_uuid,
                                  'uri':'../flows/{0}.xml'.format(flow_uuid)},
                          nsmap = lcia_ns)
            FL.append(flow_comment)
            F.append(FL)
            ET.SubElement(F, 'exchangeDirection',nsmap = lcia_ns).text='Output'
            ET.SubElement(F, 'meanValue', nsmap = lcia_ns).text = str( mean_value ) 
            CF.append(F)
            print 'exchange: {0} {1}'.format(flow_uuid,flow_comment.text)

    return L
            
def main(argv):
    O = IlcdArchive(argv[0])
    Ps = O.listFiles('Process')
    if len(argv)>1:
        Ps = Ps[argv[1] - 1 : argv[1] ] # slice so that we still end up with a list
    for p in Ps:
        print '=='+p+'=='
        L = convertProcessToLcia(O, p)
    O.saveIlcdEntity(L)
    return L

if __name__ == '__main__':
    """
    Positional parameters:
    process2lcia [ILCD archive root path] [index to convert (optional)]
    """
    main(sys.argv[1:])
    pass