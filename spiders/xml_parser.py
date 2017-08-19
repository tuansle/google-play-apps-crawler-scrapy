import os
from lxml import etree
import csv
import copy
import sys
from wordai.turing import TuringWordAi as wa
from spinrewriter import SpinRewriter
from langdetect import detect
import slugify
from misc import open_csv, randomDate, decode_str, decode_url
from datetime import datetime, timedelta
import random

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

    # print "seo key"
    # print item2[21][1].tag, item2[21][1].text

    s = etree.tostring(channel, pretty_print=True)
    # print s

    # # test cmt
    # print "comments"
    # for i in range(0, len(item2[89])):
    #     print item2[89][i].tag, item2[89][i].text, i
    # return tree


def find_etree_tag(ee):
    for i in range(0, len(ee)):
        print ee[i].tag


def csv_reader_test_genre(filepath):
    '''
    read csv file
    Returns
    -------
    a dict
    '''

    # open file
    genre = []
    for fil in os.listdir(filepath):
        if fil.endswith("csv"):
            reader = open_csv(os.path.join(filepath, fil))
            for row in reader:
                genre.append(row["Developer_ID"].replace("&", "and"))

    print set(genre)


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


def spinrewriter_spinner(filepath, download_min=99999000):
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

    rewriter = SpinRewriter('', '')

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
            row["Description"] = row["Description"].decode('unicode_escape').encode('ascii',
                                                                                    'ignore')  # stardardize string
            if len(row["Description"].split()) > 25 and len(row["Description"].split()) < 4000:
                try:
                    # only spin if download number >10000
                    if row["Downloads"] and int(
                            row["Downloads"].split(" - ", 1)[0].replace(",", "").replace(" ", "")) > download_min:
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
        print "spinning...", (len(to_spin.split(" ")) / 3900 + 2), "blocks of 3.8k words are going to be spinned"
        result_spin = ""
        # spin each 3800 words #TODO not working
        count_spinned = 0
        for i in range(1, (len(to_spin.split(" ")) / 3900 + 2)):
            splitted_words = unicode(" ".join(to_spin.split(" ")[3900 * (i - 1):3900 * i]), errors='replace')
            try:
                spinned = str(rewriter.unique_variation(splitted_words))
                if len(spinned) > 20:
                    result_spin += spinned
                else:
                    result_spin += splitted_words
                count_spinned += 1
            except Exception as e:
                print e
                result_spin += splitted_words
                count_spinned += 1
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
                            row["Downloads"].split(" - ", 1)[0].replace(",", "").replace(" ", "")) > download_min:
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


def xml_writer(filepath=None, unit="static/unit.xml", start_id=0, start_cmt_id=0):
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

    # open CSV file
    reader = open_csv(filepath)

    #take current time
    ctime = datetime.now()

    for row in reader:
        # print row

        # item manipulation

        # split author link:
        try:
            row["Author_site"], row["Author_email"] = row["Author_link"].split("https://www.google.com/url?q=")[
                1].split("mailto:")
        except:
            row["Author_site"] = row["Author_link"]
            row["Author_email"] = ''
            pass

        # copy new instance of item
        item_new = copy.deepcopy(item)
        # title
        item_new[0].text = unicode(row['Item_name'].title(), errors="replace")  # e.g faceBook Messenger => Facebook Messenger
        # link
        item_new[1].text = item_new[1].text.replace("facebook-copy", slugify.slugify(unicode(item_new[0].text.lower())))
        # pubdate
        # pubdate = currentdate - 3
        time_pub = ctime - timedelta(days=3)
        item_new[2].text = item_new[2].text.replace("08 Aug 2017 16:48:47", time_pub.strftime('%Y %b %d %H:%M:%S'))
        # guid
        item_new[4].text = item_new[4].text.replace("343453", str(start_id))  # append startid to link
        # desc
        # item_new[5].text = decode_str(row['Description'])
        # downloadbox
        item_new[6].text = decode_str(row['Description']) + "\n" \
                           + '<a href="' + row['Link'] + ' target="_blank"' + '">Source</a>' + "\n" \
                           + item_new[6].text.replace("com.facebook.katana", row['package_name'])
        # post id
        item_new[8].text = str(start_id)

        #post date and postdate gmt = time pub
        #post date
        item_new[9].text = item_new[9].text.replace("2017-08-08 16:48:47", time_pub.strftime('%Y-%m-%d %H:%M:%S'))
        #post date gmt
        item_new[10].text = item_new[9].text

        # post name: slug
        item_new[13].text = slugify.slugify(unicode(item_new[0].text.lower()))

        # IMPORTANT: index init
        #wp meta index start (the first {http://wordpress.org/export/1.2/}postmeta  in parsexmltest)
        wp_first_meta_index = 20
        #copy tag
        index_cat_apps = 41 # the index of "category Apps 82" run parsexmltest

        # yoast wp seo keywords
        item_new[wp_first_meta_index][1].text = item_new[wp_first_meta_index][1].text.replace("download", item_new[0].text + " APK Download")

        # custom screenshots
        item_new[wp_first_meta_index + 3][1].text = item_new[wp_first_meta_index + 3][1].text.replace("screenshots", decode_url(row["screenshots"]))

        # date release
        item_new[wp_first_meta_index + 4][1].text = item_new[wp_first_meta_index + 4][1].text.replace("2014-09-02", row['Updated'])

        # author name
        item_new[wp_first_meta_index + 5][1].text = item_new[wp_first_meta_index + 5][1].text.replace("Facebook", decode_str(row["Author"]))

        #version
        item_new[wp_first_meta_index + 7][1].text = item_new[wp_first_meta_index + 7][1].text.replace("3.1.1", row["Version"])

        # app icon
        item_new[wp_first_meta_index + 8][1].text = item_new[wp_first_meta_index + 8][1].text.replace("appicontest", decode_url(row["cover_image"]))

        # yoast wp seo snipet #
        item_new[wp_first_meta_index + 15][1].text = item_new[wp_first_meta_index + 15][1].text.replace("testdescription", "1-Click Download " + item_new[0].text + " APK for Android devices. " + item_new[0].text + " Android App for Samsung, Huawei, OPPO, Sony, Google smartphones and tablets.")

        # port-version (app version)
        if row["Version"]:
            item_new[wp_first_meta_index + 16][1].text = item_new[wp_first_meta_index + 16][1].text.replace("1", row["Version"])

        # port-requirement (android requirement)
        if row["Compatibility"]:
            item_new[wp_first_meta_index + 17][1].text = item_new[wp_first_meta_index + 17][1].text.replace("2.3 and up", row["Compatibility"])

        # custom meta field: content rating
        if row["Content_rating"]:
            item_new[wp_first_meta_index + 18][1].text = item_new[wp_first_meta_index + 18][1].text.replace("Everyone", row["Content_rating"])
        # custom meta field:downloads
        if row["Downloads"]:
            item_new[wp_first_meta_index + 18][1].text = item_new[wp_first_meta_index + 18][1].text.replace("100,000 - 500,000", row["Downloads"])
        # custom meta field: author info
        if row["Author_site"]:
            item_new[wp_first_meta_index + 18][1].text = item_new[wp_first_meta_index + 18][1].text.replace("Hidden on request", row["Author_site"] + "\n" + row["Author_email"])

        # COMMENTS
        for i in range(1,5):
            if row["review_star" + str(i)] and len(row["review_star" + str(i)]) > 10:
                comment = copy.deepcopy(item_new[index_cat_apps + 8])
                #remove old comment
                # item_new.remove(item_new[90]) #temporary not remove predefined comment
                # add infor for comment
                #comment id
                comment[0].text = str(start_cmt_id)

                #comment author
                comment[1].text = row["review_username" + str(i)]

                #comment date: in range (last 3 days)
                comment[5].text = comment[5].text.replace("2017-05-25 18:08:01", randomDate(time_pub.strftime('%Y-%m-%d %H:%M:%S'), ctime.strftime('%Y-%m-%d %H:%M:%S'), random.random()))
                #comment date_gmt
                comment[6].text =  comment[5].text

                #comment content
                comment[7].text = row["review_content" + str(i)]

                #comment userid = comment id
                comment[11].text = comment[0].text
                #comment rating
                comment[12][1].text = filter(str.isdigit, row["review_star" + str(i)])

                # append item
                item_new.append(comment)

                # + 1 to comment id
                start_cmt_id += 1

        # CATEGORY
        #copy category
        cat_genre = copy.deepcopy(item_new[index_cat_apps + 7])
        cat_genre.text = cat_genre.text.replace("Games", row["Genre"])
        cat_genre.attrib['nicename'] = slugify.slugify(unicode(row["Genre"]))
        item_new.append(cat_genre)

        # if there is genre2
        if row["Genre2"]:
            cat_genre2 = copy.deepcopy(item_new[index_cat_apps + 7])
            cat_genre2.text = cat_genre2.text.replace("Games", row["Genre"])
            cat_genre2.attrib['nicename'] = slugify.slugify(unicode(row["Genre"]))
            item_new.append(cat_genre2)



        #content rating tag
        rating = copy.deepcopy(item_new[index_cat_apps])
        rating.text = rating.text.replace("Apps", row["Content_rating"])
        rating.attrib['nicename'] = slugify.slugify(unicode(row["Content_rating"]))
        item_new.append(rating)

        #genre tag
        genre = copy.deepcopy(item_new[index_cat_apps])
        genre.text = genre.text.replace("Apps", row["Genre"])
        genre.attrib['nicename'] = slugify.slugify(unicode(row["Genre"]))
        item_new.append(genre)

        # if there is genre2
        if row["Genre2"]:
            genre2 = copy.deepcopy(item_new[index_cat_apps])
            genre2.text = genre2.text.replace("Apps", row["Genre"])
            genre2.attrib['nicename'] = slugify.slugify(unicode(row["Genre"]))
            item_new.append(genre2)

        #name tag
        name = copy.deepcopy(item_new[index_cat_apps])
        name.text = name.text.replace("Apps", row["Item_name"])
        name.attrib['nicename'] = slugify.slugify(unicode(row["Item_name"]))
        item_new.append(name)

        #download tag
        download = copy.deepcopy(item_new[index_cat_apps])
        download.text = download.text.replace("Apps", row["Downloads"])
        download.attrib['nicename'] = slugify.slugify(unicode(row["Downloads"]))
        item_new.append(download)

        #author tag
        author = copy.deepcopy(item_new[index_cat_apps])
        author.text = author.text.replace("Apps", row["Author"])
        author.attrib['nicename'] = slugify.slugify(unicode(row["Author"]))
        item_new.append(author)

        #price tag
        price = copy.deepcopy(item_new[index_cat_apps])
        if "Buy" in row["Price"]:
            price.text = price.text.replace("Apps", "Paid App")
            price.attrib['nicename'] = "paid-app"
        else:
            price.text = price.text.replace("Apps", "Free App")
            price.attrib['nicename'] = "free-app"
        item_new.append(price)

        #badge tag
        if row["Developer_badge"]:
            badge = copy.deepcopy(item_new[index_cat_apps])
            badge.text = badge.text.replace("Apps", row["Developer_badge"])
            badge.attrib['nicename'] = slugify.slugify(unicode(row["Developer_badge"]))
            item_new.append(badge)

        #remove old category
        for i in range(index_cat_apps, index_cat_apps + 8):
            item_new.remove(item_new[index_cat_apps])


        # #debug
        # for i in range(0,21):
        #     print item_new[i].tag, item_new[i].text

        # append to channel
        channel.append(item_new)

        # increase start_id
        start_id += 1

    # remove first error item
    channel.remove(channel[10])
    # write to xmlfile

    tree_out = etree.ElementTree(root)
    tree_out.write(filepath + ".xml", pretty_print=True, xml_declaration=True, encoding="utf-8")

#generate xml for the whole folder
def gen_xml_folder(folder_path, unit="../static/unit.xml",  start_id=1000):
    for fil in os.listdir(folder_path):
        xml_writer(filepath=os.path.join(folder_path, fil),unit=unit, start_id=start_id, start_cmt_id=start_id)
        start_id += 2000


if __name__ == "__main__":
    #generate xml for the whole folder
    # gen_xml_folder("/home/tuan/Code/google-play-apps-crawler-scrapy/csvfile/newest", unit= "static/unit.xml", start_id=1000)

    # xml_writer(filepath="/home/tuan/Code/google-play-apps-crawler-scrapy/csvfile/newest/1.csv",start_id=10000, start_cmt_id=10000)
    parseXML_test("static/unit.xml")

    # spinrewriter_spinner("/home/tuan/Code/google-play-apps-crawler-scrapy/csvfile/1.csv")
    # csv_reader_test_genre("/home/tuan/Code/google-play-apps-crawler-scrapy/csvfile/old")
    # csv_reader_test_genre("/home/tuan/Code/google-play-apps-crawler-scrapy/csvfile/newest")
    #
