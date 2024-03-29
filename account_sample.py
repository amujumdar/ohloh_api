#!/usr/bin/python

"""
This is an example of using the Ohloh API from Python.

Detailed information can be found at the Ohloh website:

     http://meta.ohloh.net/getting_started

This example uses the ElementTree library for XML parsing
(included in Python 2.5 and newer):

     http://effbot.org/zone/element-index.htm

This example retrieves basic Ohloh account information
and outputs it as simple name: value pairs.

Pass your Ohloh API key as the first parameter to this script.
Ohloh API keys are free. If you do not have one, you can obtain one
at the Ohloh website:

     http://www.ohloh.net/accounts/<your_login>/api_keys/new

Pass the email address of the account as the second parameter to this script.
"""

import sys, urllib, hashlib
# import ElementTree based on the python version
try:
  import elementtree.ElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET

# We pass the MD5 hash of the email address
email = hashlib.md5()
email.update(sys.argv[2])

# Connect to the Ohloh website and retrieve the account data.
params = urllib.urlencode({'api_key': sys.argv[1], 'v': 1})
url = "http://www.ohloh.net/accounts/%s.xml?%s" % (email.hexdigest(), params)
f = urllib.urlopen(url)

# Parse the response into a structured XML object
tree = ET.parse(f)

# Did Ohloh return an error?
elem = tree.getroot()
error = elem.find("error")
if error != None:
    print 'Ohloh returned:', ET.tostring(error),
    sys.exit()

# Output all the immediate child properties of an Account
for node in elem.find("result/account"):
    if node.tag == "kudo_score":
        print "%s:" % node.tag
        for score in elem.find("result/account/kudo_score"):
            print "\t%s:\t%s" % (score.tag, score.text)
    else:
        print "%s:\t%s" % (node.tag, node.text)
