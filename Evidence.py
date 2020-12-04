from bs4 import BeautifulSoup
import requests
import json
import secrets # file that contains your API key
import pdb

CACHE_FILE_NAME = 'cache.json'
CACHE_DICT = {} 
baseurlSoup = 'https://www.internationalstudent.com/school-search/usa'
baseurlAPI = 'http://www.mapquestapi.com/search/v2/radius'


'''
url = 'https://www.internationalstudent.com/school-search/480/usa/michigan/university-of-michigan-ann-arbor'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser') # get the text
searching_ul = soup.find('div',{'id':'school-info-student-faculty'}) # find ul, which has 'dropdwon-menu SearchBar-keywordSearch' class
text = searching_ul.find('div',{'class':'col pl-1 small'})
text_num = searching_ul.find('div',{'class':'col-3 text-right'})
print("Number of the " + text.text + " is " + text_num.text)
'''

class university:
    '''An University 

    Instance Attributes
    -------------------
    states: string
        States of USA
    name: string
        name of the university
    address: string
        address of the university
    zipcode: string
        zip-code of the university
    phone: string
        phone of the university
    male_tot, male_intl, female_tot, female_intl: string
        number of the male total, male international, female total, female international respectively
    '''
    def __init__(self): #initialize empty attributes
        self.states = [] # states in US
        self.name = [] # name of the university
        self.male_tot = [] # total num of male students
        self.male_intl = [] # num of international male students
        self.female_tot = [] # total num of female students
        self.female_intl = [] # num of international female students
        self.address = [] # address of the university
        self.zipcode = [] # zip code of the university
        self.phone = [] # phone of the university
        self.url = [] # url of the university

    def info(self):
        return self.name + ' : ' + self.address + ' [' + self.zipcode + ']'

    pass

class restaurant:
    '''A restaurant

    Instance Attributes
    -------------------
    name: string
        name of the restaurnat
    address: string
        address of the restaurnat
    zipcode: string
        zip-code of the restaurnat
    '''
    def __init__(self): #initialize empty attributes
        self.name = [] # address of the restaurant
        self.address = [] # address of the restaurant
        self.zipcode = [] # zip code of the restaurant

    def info(self):
        return self.name + ' : ' + self.address + ' [' + self.zipcode + ']'

    pass

def loadCache(): 
    ''' Load cache if exists 

    Parameters
    ----------
    None

    Returns
    -------
    cache
        jason format, if the cache exists
        empty, if the cache does not exist
    '''

    try: # Try to get cache 
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except: # if no cache 
        cache = {}
    return cache

# Load the cache, save in a global variable
CACHE_DICT = loadCache()

def saveCache(cache):
    ''' save cache

    Parameters
    ----------
    cache : dict

    Returns
    -------
    None
    '''
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()

def constructUniqueKey(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''
    key_value_temp = [] # empty string
    connector = "_"
    for i in params.keys(): # get all of values in params
        key_value_temp.append(f'{i}_{params[i]}')
    key_value_temp.sort() # sort string in alphabat order
    unique_key = baseurl + connector + connector.join(key_value_temp)
    return unique_key

def requestResponseText(url):
    ''' request response text of the url

    Parameters
    ----------
    url: string

    Returns
    -------
    response.text
    '''
    if (url in CACHE_DICT.keys()): 
        print("Using cache")
    else:
        print("Fetching")
        response = requests.get(url)
        CACHE_DICT[url] = response.text 
        saveCache(CACHE_DICT)
    return CACHE_DICT[url]

def extractUniInfo(url):
    '''Extract an university info and
    make an instance that contains the info
    
    Parameters
    ----------
    url: string
        The URL for an university
    
    Returns
    -------
    instance
        an university instance
    '''

    Uni = university() # call the class
    
    response_text = requestResponseText(url)
    soup = BeautifulSoup(response_text, 'html.parser') # get the text
    Uni.url = url
    ## some universities have no information
    try:
        Uni.name = soup.find('div',{'class':'card card-body mb-3 p-3'}).h1.text # name
    except:
        pass
    try:
        Uni.state = soup.find_all('li',{'class':'breadcrumb-item'})[2].a.text
    except:
        pass
    try:
        Uni.male_tot = soup.find_all('strong',{'class':'f-12'})[1].text
    except:
        pass
    try:
        Uni.male_intl = soup.find_all('strong',{'class':'f-12'})[4].text
    except:
        pass
    try:
        Uni.female_tot = soup.find_all('strong',{'class':'f-12'})[2].text
    except:
        pass
    try:
        Uni.female_intl = soup.find_all('strong',{'class':'f-12'})[5].text
    except:
        pass
    try:
        fullAddress = soup.find('ul',{'class':'fa-ul'}).li.text.strip()
    except:
        pass
    try:
        Uni.address = fullAddress[:-6]
    except:
        pass
    try:
        Uni.zipcode = fullAddress[-5:]
    except:
        pass
    try:
        Uni.phone = soup.find('ul',{'class':'fa-ul'}).a.text
    except:
        pass
    
    return Uni

def printUniInfo(Uni):
    '''Print an university info and
    make an instance that contains the info
    
    Parameters
    ----------
    Uni: instance
    
    Returns
    -------
    None
    '''

    print("Name: " + Uni.name)
    print("Address: " + Uni.address + ', ' + Uni.zipcode)
    print("Phone Number: " + Uni.phone)
    print("# of male students: " + Uni.male_tot)
    print("# of female students: " + Uni.female_tot)
    print("# of male international students: " + Uni.male_intl)
    print("# of female international students: " + Uni.female_intl)
    
    pass

def extractUnis(url, lists):
    '''Extract university urls and
    make a dict containing the uni name and corresponding url
    
    Parameters
    ----------
    url: string
        The URL of the state
    lists: empty list
    
    Returns
    -------
    lists
        appended lists
    '''

    response_text = requestResponseText(url)
    soup = BeautifulSoup(response_text, 'html.parser') # get the text

    isnext = soup.find('li',{'class':'btn btn-sm btn-link next'})
    
    if not(isnext == None):
        url_new = 'https://www.internationalstudent.com' + isnext.a['href']
        extractUnis(url_new, lists)

        return lists.append(soup.find_all('li',{'class':'list-group-item d-flex justify-content-between font-bitter h6'}))
    
    return lists.append(soup.find_all('li',{'class':'list-group-item d-flex justify-content-between font-bitter h6'}))

def getUniList(url):
    '''Make a list of university instances from a state url
    
    Parameters
    ----------
    url: string
        A URL for a state
    
    Returns
    -------
    dictUniInsatnce: Dict
        keys: uniName, value: uni instance
    '''
    
    li_list = []
    dictUniInsatnce = {}

    extractUnis(url,li_list)
    for i in range(len(li_list)):
        h = len(li_list) - 1 - i # li_list has a reverse order
        for j in range(len(li_list[h])):
            uniName = li_list[h][j].a.text.strip()
            uniURL = 'https://www.internationalstudent.com' + li_list[h][j].a['href']
            dictUniInsatnce[uniName] = extractUniInfo(uniURL)

    return dictUniInsatnce

def printUniList(dictUniInsatnce):
    '''Print the extracted uni info list in the terminal
    
    Parameters
    ----------
    dictUniInsatnce: university instances in dict format
    
    Returns
    -------
    pass
    '''
    for uniName in dictUniInsatnce.keys():
        print(uniName)
    pass

def extractStates():
    '''Extract state urls and
    make a dict containing the state name and corresponding url
    
    Parameters
    ----------
    None
    
    Returns
    -------
    dict
        state name : state url
    '''

    stateNameURL = {}
    response_text = requestResponseText(baseurlSoup)
    soup = BeautifulSoup(response_text, 'html.parser') # get the text

    for i in range(3):
        ultag = soup.find_all('ul',{'class':'list-unstyled col-md mb-0 d-flex flex-column justify-content-between'})[i+3]
        for litag in ultag.find_all('li'):
            stateName = litag.a.text.strip()
            stateURL = 'https://www.internationalstudent.com' + litag.a['href']
            stateNameURL[stateName] = stateURL

    for keys in stateNameURL.keys():
        print(keys)

    return stateNameURL

def requestAPI(url, params):
    ''' request API and retrun the output in the json format

    Parameters
    ----------
    url: Strings
    params: dictionary

    Returns
    -------
    json
    '''
    response = requests.get(baseurl, params=params) # oauth is defined globally
    return response.json()

def printNearbyRestaurants(uni):
    '''Obtain API data from MapQuest API.
    
    Parameters
    ----------
    uni: Insatnce
        an instance of an university
    
    Returns
    -------
    dict
        a converted API return from MapQuest API
    '''

    
    params = {"key":secrets.API_KEY, "origin":uni.zipcode, "radius":10, "maxMatches":10, "ambiguities":"ignore"}
    unique_key = constructUniqueKey(baseurl=baseurlAPI, params= params)

    if unique_key in CACHE_DICT.keys(): # if the unique key is in cache
        print("Using Cache")
    else: # if the unique key is not in cache
        print("Fetching")
        CACHE_DICT[unique_key] = requestAPI(url=baseurlAPI, params=params) #request new one
        saveCache(CACHE_DICT) # save the current state

    results = CACHE_DICT[unique_key]

    ## To do: extract 10 restaurants
    '''
    for i in range(len(results)):
        dsfsfsdf
    '''
    pass

if __name__=="__main__":
    #url = 'https://www.internationalstudent.com/school-search/480/usa/michigan'
    #dict_michigan = getUniList(url)
    #printUniList(dict_michigan)
    stateNameURL = extractStates()
    print("--------------------------------------")
    stateName = input("Type one of the states mentioned above: ")
    print("University lists in the chosen state")
    uniNameURL = getUniList(stateNameURL[stateName])
    printUniList(uniNameURL)
    print("--------------------------------------")
    uniName = input("Type one of the universities mentioned above: ")
    printUniInfo(extractUniInfo(uniNameURL[uniName].url))


    pdb.set_trace()
