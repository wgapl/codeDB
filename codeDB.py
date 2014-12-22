#! /usr/bin/env python

from pymongo import MongoClient
from datetime import datetime
from pprint import pprint

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-n", "--name", help="The name of the project.")
parser.add_argument("-l", "--location",
    help="The location of the code in the filesystem.")
parser.add_argument("-u", "--url", help="The url of the project.")
parser.add_argument("-r", "--remove", help="Remove a project from codeDB.")
parser.add_argument("-d", "--display",
    help="Show the contents of codeDB.", action="store_true")

head_width = 60
args = parser.parse_args()
header = "#" * head_width


def arg_check(args):
    """Go through and check the arguments in args. Raise an InputError if
    none of the necessary input is provided.
    """
    if args.display:
        display_codeDB()
        return True, None, None

    if args.remove != None:
        code = get_code()
        check = remove_project(args.remove, code)
        return None, check, args.remove

    if args.name != None:
        name = args.name
    else:
        msg = "Please enter a project name!"
        print msg
        return

    if args.location != None:
        location = args.location
    else:
        msg = "Please enter the location of the project on the local filesystem."
        print msg
        return

    if args.url != None:
        url = args.url
    else:
        msg = "Please enter the URL of the project."
        print msg
        return



    return name, location, url

def display_codeDB():
    import math
    code = get_code()
    codeDB_label = " codeDB Project List "
    prefill = "#" * int(math.floor((head_width + 0. - len(codeDB_label))/2))
    postfill =  "#" * int(math.ceil((head_width +0. - len(codeDB_label))/2))
    print
    print header
    print ''.join([prefill,codeDB_label,postfill])
    print header
    print

    for x in code.find():
        print "Name:      "+x["name"]
        print "Location:  "+x["location"]
        print "URL:       "+x["url"]
        print
        print header


def get_code():
    """Get the "code" collection from the wgapl database.
    """
    client = MongoClient()
    wgapl = client["wgapl"]
    code = wgapl["code"]
    return code

def insert_project(name, loc, url, collection):
    """Insert the name, location, and url of a code project into
    the collection.
    """
    entry = {
        "name": name,
        "location": loc,
        "url": url,
        "date":datetime.utcnow()
        }

    collection.insert(entry)

def remove_project(name, collection):
    if collection.find_one({"name":name}) == None:
        msg = "There is no project with that name to be removed."
        print msg
        return False
    else:
        collection.remove({"name":name})
        return True

def test_basics():
    """Test the progress being made
    """
    code = get_code()

    insert_project(
        "Test Proj", # Name of test project
        "/home/wg",  # location of the project on the local file system
        "https://github.com/testus/test", # URL of project on web
        code # collection to insert this data into
        )

    for x in code.find():
        pprint.pprint(x)

    code.remove({"name":"Test Proj"})

    assert code.count() == 0


def test_args():
    code = get_code()
    name, loc, url = arg_check(args)

    if not all([name,loc,url]):
        if loc:
            print "The project %s was removed" % url
            return
        else:
            return

    if code.find_one({"name":name}) != None:
        print "There is already a project with this name in the database."
        return

    else:
        insert_project(name, loc, url, code)
        entry = code.find_one({"name":name})
        assert entry["location"] == loc

def main():

    code = get_code()
    name, loc, url = arg_check(args)
    if not all([name,loc,url]):
        if name == True:
            return
        if loc:
            name = url
            print "The project %s was removed." % name
            return
        else:
            return

    if code.find_one({"name":name}) != None:
        print "There is already a project with this name in the database."
        return
    else:
        insert_project(name, loc, url, code)
        entry = code.find_one({"name":name})
        print "The following entry has been added to codeDB:"
        pprint(entry)



if __name__ == "__main__":
    main()
