import os
import sys
import csv


def standardize_string(in_str):
    '''
    Standardize string, remove special characters
    Parameters
    ----------
    in_str str

    Returns
    -------

    '''
    try:
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
        return in_str.encode("utf-8").replace("\n", "\|/")
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
    return in_str.replace("\|/", "\n")

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

    with open(csv_path, 'w') as csvfile:
        spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=' ', quotechar='|', )
        spamwriter.writeheader()
        spamwriter.writerows(list_to_write)
        csvfile.close()
        spamwriter = None

if __name__ == "__main__":
    csvfile = open_csv("/home/tuan/Code/google-play-apps-crawler-scrapy/csvfile/old/1.csv")
    print csvfile