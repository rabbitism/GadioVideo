import json
import os
import re
import sys
import urllib.request

import requests
from bs4 import BeautifulSoup

api = "https://www.gcores.com/gapi/v1/radios/112068?include=category,user,media,djs,media.timelines"

