import os
from lxml import etree
import csv
from shutil import copyfile
from StringIO import StringIO
import copy
import sys
from wordai.turing import TuringWordAi as wa
from spinrewriter import SpinRewriter
from langdetect import detect
from collections import OrderedDict


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


def csv_reader(filepath):
    '''
    read csv file
    Returns
    -------
    a dict
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

    # open file
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=' ', quotechar='|', )

    return reader


def csv_reader_test(filepath):
    '''
    read csv file
    Returns
    -------
    a dict
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

    # open file
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=' ', quotechar='|', )
        for row in reader:
            print row["Downloads"], len(row["Downloads"])
            print row["Downloads"].split(" - ", 1)[0].replace(",", "").replace(" ", "")
    return reader


def wordai_spinner(filepath):
    '''
    wordai content spinner api
    Parameters
    ----------
    dict
    username
    password

    Returns
    -------

    '''
    reload(sys)
    sys.setdefaultencoding('utf8')

    wordai = wa('username', 'password')

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

    # open file
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=' ', quotechar='|', )
        for row in reader:
            try:
                row["Description"] = str(wordai.unique_variation(row["Description"].replace("\n", "|"))).replace("|",
                                                                                                                 "\n")
            except Exception as e:
                print e
                continue

            print row["Description"]


def spinrewriter_spinner(filepath):
    '''
    wordai content spinner api
    Parameters
    ----------
    dict
    username
    password

    Returns
    -------

    '''
    reload(sys)
    sys.setdefaultencoding('utf8')


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

    # decide what to spin, add to "to_spin"
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=' ', quotechar='|', )
        to_spin = ""
        for row in reader:
            if len(row["Description"].split()) > 25 and len(row["Description"].split()) < 4000:
                try:
                    # only spin if download number >10000
                    if row["Downloads"] and int(
                            row["Downloads"].split(" - ", 1)[0].replace(",", "").replace(" ", "")) > 99000:
                        # only spin if it is English. temporary turn off
                        # print row["Description"]
                        # if detect(unicode(row["Description"].split(".", 1)[0], errors='ignore')) == 'en':  # only take the first sentence
                        to_spin += str(row["Description"]).replace("\n", "\|/") + "||||||||"
                        # print countx
                except Exception as e:
                    print e
                    # if str(e) == "No features in text.":
                    #     to_spin += str(row["Description"]).replace("\n", "\|/") + "||||||||"
                    continue

        # print to_spin
        result_spin = ""
        # spin each 3800 words #TODO not working
        count_spinned = 0
        for i in range(1, (len(to_spin.split(" ")) / 3800 + 2)):
            splitted_words = unicode(" ".join(to_spin.split(" ")[3800 * (i - 1):3800 * i]), errors='replace')
            try:
                spinned = str(rewriter.unique_variation(splitted_words))
                # spinned = splitted_words   + "SPINNEDDDDDDDDDDDDD" # for testing
                if len(spinned) > 20:
                    result_spin += spinned
                else:
                    result_spin += splitted_words
                count_spinned += 1
            except Exception as e:
                print e
                result_spin += splitted_words
                count_spinned +=1
                if str(e) == "Error!!!,  Quota limit for API calls reached.":
                    break
                else:
                    continue

            print count_spinned, "blocks per ", (len(to_spin.split(" ")) / 3800 + 2), "completed"



        # for i in range(0,len(result_spin.split("----------"))):
        #     print result_spin.split("----------")[i]

        print len(result_spin.split("||||||||"))

    result = []
    with open(filepath) as csvfile:
        count = 0
        count2 = 0
        count3 = 0
        reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=' ', quotechar='|', )

        for row in reader:
            # print row
            count3 += 1
            print count3
            if len(row["Description"].split()) > 25 and len(row["Description"].split()) < 4000:
                try:
                    # only spin if download number >10000
                    if row["Downloads"] and int(
                            row["Downloads"].split(" - ", 1)[0].replace(",", "").replace(" ", "")) > 99000:
                        # only spin if it is English. temporary turn off
                        # if detect(unicode(row["Description"].split(".", 1)[0], errors='ignore')) == 'en':  # only take the first sentence
                        print row["Description"]
                        row["Description"] = result_spin.split("||||||||")[count].replace("\|/", "\n")
                        print row["Description"]
                        count += 1
                        print "count1,", count
                        # spinned_content = str(rewriter.unique_variation(row["Description"].replace("\n", "|"))).replace("|", "\n")
                        # if len(spinned_content) > 20: # to debug: if an error return, skip
                        #     row["Description"] = spinned_content + ".."
                except Exception as e:
                    print "Error!!!, ", e
                    continue

            result.append(row)
            count2 += 1
            print "count2,", count2

            # number of spinned 3.8k for testing
            # print "result spin block", result_spin.count("SPINNEDDDDDDDDDDDDD")

            with open(filepath + "_spinned", 'w') as csvfile:
                spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=' ', quotechar='|', )
                # spamwriter.writeheader()
                for row in result:
                    spamwriter.writerow(row)
                csvfile.close()
                spamwriter = None


def xml_writer(dict=None, unit="static/unit.xml", start_id=0):
    '''
    Function to read csv file and convert to wp-importable xml file
    Returns
    -------

    '''

    # parse template
    tree = etree.parse(unit)  # element tree object
    root = tree.getroot()
    channel = root[0]

    # take dummy item template
    item = channel[10]
    # remove dummy
    channel.remove(item)

    for row in dict:
        # print row

        # item manipulation
        # copy new instance of item
        item_new = copy.deepcopy(item)
        # title
        item_new[0].text = row['Item_name']
        # link
        item_new[1].text = item_new[1].text.replace("facebook-copy", row['Item_name'].lower().replace(" ", "-"))
        # pubdate
        # item_new[2].text =
        # guid
        item_new[4].text = item_new[4].text.replace("343453", str(start_id))  # append startid to link
        # desc
        item_new[5].text = row['Description']
        # downloadbox
        item_new[6].text = item_new[6].text.replace("com.facebook.katana", row['package_name'])
        # post id
        item_new[8].text = str(start_id)
        # post name
        item_new[13].text = row['Item_name'].lower().replace(" ", "-")

        # TODO: fetch category




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
    # parseXML_test("static/unit.xml")

    spinrewriter_spinner("/home/tuan/Code/google-play-apps-crawler-scrapy/csvfile/1.csv")
    # csv_reader_test("/home/tuan/Code/google-play-apps-crawler-scrapy/csvfile/1.csv")
    #
