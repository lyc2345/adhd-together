# from selenium import webdriver
import sys
# from urllib2 import urlopen
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import time

class Route:
  def __init__(self, busId, back, forward):
    self.busId = busId
    self.back = back
    self.forward = forward

def bus_tracker(busId):
  url = 'http://apidata.tycg.gov.tw/OPD-io/bus4/GetEstimateTime.xml?routeIds=' + busId
  soup = BeautifulSoup(urllib.request.urlopen(url), 'lxml')
  # print(soup.prettify())

  route_xml = soup.route

  goForward = []
  goBack = []

  for stop in route_xml:
    if stop['goback'] == '1':
      goBack.append(stop)
    else:
      goForward.append(stop)

  return Route(busId, goBack, goForward)

def getBusInformation(text):
  route = bus_tracker(text)

  # reload(sys)
  # sys.setdefaultencoding('utf-8')
  time_format = '%H:%M'

  nowDate = datetime.now()
  nowStr = str(nowDate.hour) + ':' + str(nowDate.minute)
  now = datetime.strptime(nowStr, time_format)
  # print(now)

  busInfo = 'Back' + '\n'
  for b in route.back:
    ct = datetime.strptime(str(b['cometime']), time_format)
    # print('cometime: ', ct)
    timegap = (ct - now).seconds
    if (timegap > 0 and timegap < 300):
      busInfo += '* '
    busInfo += str(b['cometime']) + ' - ' + str(b['stopname']) + ' \n'
    # print('back: ', b)
  busInfo += '*****************************' + '\n'
  busInfo += 'Forward' + '\n'
  for f in route.forward:
    busInfo += str(f['cometime']) + ' - ' + str(f['stopname']) + ' \n'
    # print('forward: ', f)
  return busInfo
