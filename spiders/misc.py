import os
import sys
import csv
import random
import time
import unicodedata


def standardize_string(in_str, unicode = True):
    '''
    Standardize string, remove special characters
    Parameters
    ----------
    in_str str

    Returns
    -------

    '''
    try:
        if unicode:
            if unicodedata.normalize('NFKD', in_str).encode('ascii', 'ignore') == None:
                print in_str
            return unicodedata.normalize('NFKD', in_str).encode('ascii', 'ignore')
        else:
            return in_str.decode('unicode_escape').encode('ascii','ignore')
    except:
        pass

def encode_str(in_str):
    '''
    Encode string to store in string
    Parameters
    ----------
    in_str str

    Returns
    -------

    '''
    try:
        return in_str.encode("utf-8").replace("\n", ".xd.")
    except:
        pass

def decode_str(in_str):
    '''
    Decode string from string to display
    Parameters
    ----------
    in_str str

    Returns
    -------

    '''
    try:
        return in_str.replace(".xd.", "\n")
    except:
        pass

def decode_url(in_str):
    '''
    Decode url
    Parameters
    ----------
    in_str str

    Returns
    -------

    '''
    out_str = in_str.replace("rw//lh", "rw\nhttps://lh")
    if out_str[:1] == "\n":
        out_str = out_str[1:]
    elif out_str[:2] == "//":
        out_str = "https:" + out_str
    out_str = out_str.replace("rwhttps", "rw\nhttps")
    return out_str

def open_csv(csv_path):
    '''
    Open csv file as a dict
    Parameters
    ----------
    csv_path

    Returns
    -------
    a list of rows

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
                  'Genre2',
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
                  'Price',
                  'review_username1',
                  'review_username2',
                  'review_username3',
                  'review_username4',
                  'review_star1',
                  'review_star2',
                  'review_star3',
                  'review_star4',
                  'review_content1',
                  'review_content2',
                  'review_content3',
                  'review_content4']

    result_list = []

    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=' ', quotechar='|', )
        for row in reader:
            result_list.append(row)

    return result_list


def write_csv(csv_path, list_to_write):
    '''
    write csv file
    Parameters
    ----------
    csv_path str

    list_to_write str
        list of string to write to csv

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
                  'Genre2',
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
                  'Price',
                  'review_username1',
                  'review_username2',
                  'review_username3',
                  'review_username4',
                  'review_star1',
                  'review_star2',
                  'review_star3',
                  'review_star4',
                  'review_content1',
                  'review_content2',
                  'review_content3',
                  'review_content4']

    with open(csv_path, 'w') as csvfile:
        spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=' ', quotechar='|', )
        spamwriter.writeheader()
        spamwriter.writerows(list_to_write)
        csvfile.close()
        spamwriter = None


def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    '''
    generate random time between two timeframe
    Parameters
    ----------
    start
    end
    prop

    Returns
    -------

    '''
    return strTimeProp(start, end, '%Y-%m-%d %H:%M:%S', prop)

if __name__ == "__main__":
    # csvfile = open_csv("/home/tuan/Code/google-play-apps-crawler-scrapy/csvfile/old/1.csv")
    # print csvfile
    # print randomDate("2015-10-20 00:00:00", "2016-10-20 00:00:00", random.random())
    # a = decode_url("//lh3.googleusercontent.com/qeJZcsvxIPD992xKgpGeAZEMAIWJYhdaJDHmEjlu91dFtNgNn_YxpFoTiyZ_k3wofbg=h900-rw//lh3.googleusercontent.com/Tk-niI8FSAHaF30-BoQLcmwTaeceq0FjS_q0ehtZpecw591iB3ftGYxgmaQFgfI4fw=h900-rw//lh3.googleusercontent.com/Ra3O7pqy6fyBuwnC62H2e-6q-ogt81P4Af9LRMwqUJk4VJAnv0bs3ntNLZH_1grlXg=h900-rw//lh3.googleusercontent.com/vh6HewgxXjjmdPCzvXs6xWkb6QxUsVMCjscKaG2zH_UivuvkysKzsX-Pm__vN3zVNLY=h900-rw//lh3.googleusercontent.com/vAPt9F2sJ3KbqCLysO24Gp66w0kGmW0iksf6AzvNjpe8AaVqRO0MygiGO2PP-uW4=h900-rw//lh3.googleusercontent.com/Kc0fbk3sWDhyRxZKtgFDHOz3oq3DkQmIXkf9V1iI16ff7RFsvUvN7Er-XpJqyqcWCN0=h900-rw//lh3.googleusercontent.com/MO8Xoe2rigvS2Z4KOdyIOqfak49urWuWt4EQF_CZPRb_c4uS26RHNNwKyAtZ7tJLpw=h900-rw//lh3.googleusercontent.com/vJ0MIUv5UhFkDw1SD4CipI_UvCgMK_Bx7DJJ7S9hbsRFlec4QxGM1hu2Yxy5vopwheE=h900-rw//lh3.googleusercontent.com/uEVUWdNStCIpLISUJjrpU7d9PvRH_-jl7pYE-Klz7mX7wvBi-N0b4gORtsl0RGrZimg=h900-rw//lh3.googleusercontent.com/QDDtniyN-h738-zJgqBgP21ua_o4XbVXIpW4sWpBJwEkf3faRS9SGmbcCI9Fm719Pw=h900-rw//lh3.googleusercontent.com/07QldCJ4adY25Lqm4X6WWpFmwj6kM1Lcf2ahWWc-5BypOSdVBqDOmJVPV1Tak_uRrl8=h900-rw//lh3.googleusercontent.com/AM1Pi_iCgF68Zi1SVFFp-xQUzoHD3SCUuib_uCkjkRWcU8AjltOTiUPmzp8O2qMd2Snd=h900-rw")
    # print a

    print standardize_string(u"Mit 5 von f\xfcnf Sternen bewertet")