import requests
import json
import urlparse
import posixpath

import config

class MemeError(Exception): pass

def _image_id_for_url(image_url):
    '''
    Given a memegenerator.net image url, finds the image ID
    '''
    u = urlparse.urlparse(image_url)
    basename = posixpath.basename(u.path)
    image_id = posixpath.splitext(basename)[0]
    return image_id

def get_meme(name):
    '''
    Returns the best guess for the meme of a given name
    '''
    url = "http://version1.api.memegenerator.net/Generators_Search"
    params = {'q':name,
            'pageIndex':'0',
            'pageSize':'12'}

    response = requests.get(url, params=params)
    
    json_payload = response.json()
    if not json_payload['success']:
        return None

    memes = sorted(json_payload['result'],
            key=lambda x:x['instancesCount'],
            reverse = True)
    if not memes:
        return []
    return memes[0]

def create_meme(meme, text_elems):
    '''
    Given a meme, creates an instance of that meme with the given text elements
    from text_elems (should be a two item list)
    '''
    url = "http://version1.api.memegenerator.net/Instance_Create"
    params = {'username':config.memegen_username,
            'password':config.memegen_password,
            'language_code':'en',
            'generatorID':meme['generatorID'],
            'imageID':_image_id_for_url(meme['imageUrl']),
            'text0':text_elems[0],
            'text1':text_elems[1]}
    response = requests.get(url, params=params)
    ''' EXAMPLE RESPONSE
    {u'result': {u'generatorID': 1323, u'displayName': u'Ancient Aliens', u'instanceID': 54589988, u'imageUrl': u'http://cdn.meme.li/images/400x/627067.jpg', u'instanceImageUrl': u'http://cdn.meme.li/instances/400x/54589988.jpg', u'text0': None, u'text1': u'Cheese Diets', u'totalVotesScore': 0, u'urlName': u'Ancient-Aliens', u'instanceUrl': u'http://memegenerator.net/instance/54589988'}, u'success': True}
    '''

    json_response = response.json()
    
    if not json_response['success']:
        raise MemeError(json_response['errorMessage'])
    
    return json_response['result']['instanceImageUrl']

