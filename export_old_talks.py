""" Scrapes old seminar talks from http://www.cs.iit.edu/~mbilgic/seminar/index.html . The output is then transfered to a Google Sheet and Google Calendar.

This fails on the "Who we are..." talks, so I've just ignored them.

I also made no attempt to scrape the actual abstract and bio.
"""
import codecs
import re
import requests
import sys

from BeautifulSoup import BeautifulSoup as bs


sys.stdout = codecs.getwriter('utf8')(sys.stdout)

soup = bs(requests.get('http://www.cs.iit.edu/~mbilgic/seminar/index.html').text)
for table in soup.findAll('table'):
    for tr in table.findAll('tr'):
        event = []
        for i, td in enumerate(tr.findAll('td')):
            text = re.sub('\s+', ' ', td.text).strip()
            if i == 0:  # date
                text = text.split()[1]
                # print 'date=', text
                event.append(text)
            elif i == 1:  # time
                parts = text.split(' - ')
                # print 'parts=', parts
                if len(parts) == 2:
                    event.extend(parts)
            else:
                event.append(text)
        if len(event) == 6:
            print '%s\t%s\t%s\t%s\t%s\t%s' % (event[0],
                                                 event[5],
                                                 event[1],
                                                 event[2],
                                                 event[3],
                                                 event[4])
