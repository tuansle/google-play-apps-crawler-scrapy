import os
from lxml import etree
import csv
from shutil import copyfile
from StringIO import StringIO
import copy

def parseXML(xmlFile):
    """
    Parse the xml
    """
    tree = etree.parse(xmlFile)
    return tree

def parseXML_test(xmlFile):
    """
    Parse the xml
    """


    tree = etree.parse(xmlFile)

    # channel = etree.SubElement(tree, 'channel')
    root = tree.getroot()
    channel = root[0]




    item = channel[10]
    item2 = copy.deepcopy(item)


    # modify item2
    item2[0].text = "test"
    item2[37][1].text = "2"



    channel.remove(item)
    channel.append(item2)





    tree_out = etree.ElementTree(root)
    tree_out.write('outputsss.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")


    for i in range(0, len(item2)):
        print item2[i].tag, item2[i].text, i

    print "fasdfads"
    print item2[37][1].tag, item2[37][1].text



    s = etree.tostring(channel, pretty_print=True)
    # print s
    return tree

def find_etree_tag(ee):
    for i in range(0, len(ee)):
        print ee[i].tag

def xml_writer(filepath='', unit="static/unit.xml", start_id=0):
    '''
    Function to read csv file and convert to wp-importable xml file
    Returns
    -------

    '''

    # field definition
    fieldnames = ['Video_URL',
                  'Author',
                  'Content_rating',
                  'Version',
                  'Filesize',
                  'screenshots',
                  'Updated',
                  'Description',
                  'Review_number',
                  'Downloads',
                  'Link',
                  'Genre',
                  'Developer_badge',
                  'Item_name',
                  'Rating_value',
                  'package_name',
                  'IAP',
                  'Physical_address',
                  'Author_link',
                  'Compatibility',
                  'Developer_ID',
                  'cover_image',
                  'Price']


    # parse template
    tree = etree.parse(unit) # element tree object
    root = tree.getroot()
    channel = root[0]

    #take dummy item template
    item = channel[10]
    #remove dummy
    channel.remove(item)

    # open file
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=' ', quotechar='|',)

        for row in reader:
            # print row

            #item manipulation
            # copy new instance of item
            item_new = copy.deepcopy(item)
            #title
            item_new[0].text = row['Item_name']
            #link
            item_new[1].text = item_new[1].text.replace("facebook-copy", row['Item_name'].lower().replace(" ","-"))
            #pubdate
            # item_new[2].text =
            #guid
            item_new[4].text = item_new[4].text.replace("343453", str(start_id)) #append startid to link
            #desc
            item_new[5].text = row['Description']
            # downloadbox
            item_new[6].text = item_new[6].text.replace("com.facebook.katana", row['package_name'])
            # post id
            item_new[8].text = str(start_id)
            #post name
            item_new[13].text = row['Item_name'].lower().replace(" ","-")

            #TODO: fetch category




            # append to channel
            channel.append(item_new)

            # increase start_id
            start_id += 1
            # for i in range(0, len(item_new)):
            #     print item_new[i].tag, item_new[i].text
            # print item_new

    # write to xmlfile
    # tree_out = etree.ElementTree(root)
    # tree_out.write(filepath + ".xml", pretty_print=True, xml_declaration=True, encoding="utf-8")

if __name__ == "__main__":
    # xml_writer(filepath="/home/tuan/Code/google-play-apps-crawler-scrapy/csvfile/1.csv")
    parseXML_test("static/unit.xml")