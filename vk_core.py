import requests
import json
import pandas as pd
import time
import random
import sys


class VkClient():
    api_v = 5.126
    api_url = "https://api.vk.com/method/"
    access_token = None

    def __init__(self):
        pass
    def request_token_url(self):
        app_id = 7709111
        return f'https://oauth.vk.com/authorize?client_id={app_id}&redirect_uri=https://oauth.vk.com/blank.html&display=popup&scope=notify+friends+photos+status+wall+offline+groups+stats+email+market&response_type=token&revoke=1'
    def configure(self, access_token):
        self.access_token = access_token
    def default_params(self):
        return f"&access_token={self.access_token}&v={self.api_v}"


class VkGroup():
    owner_id = None
    group_id = None

    def __init__(self, client, owner_id, group_id):
        self.client = client
        self.owner_id = owner_id
        self.group_id = group_id
    def get_posts(self, count):
        posts = []
        method = "wall.get?"
        params = f"owner_id=-{self.owner_id}&count={count}&filter=owner" + self.client.default_params()
        request_url = self.client.api_url + method + params
        print('request url is', request_url)
        response = requests.get(request_url).json()
        if 'error' in response.keys():
            print('error while get post \n', response)
            # return None
        else:
            for post in response['response']['items']:
                current_post = VkGroupPost(self.client, post)
                posts.append(current_post)
            return posts

class VkGroupPost():
	# create vk group post object from opst_response	
    def __init__(self, client, post_response):
        self.client = client
        self.id = post_response['id']
        self.from_id = post_response['from_id']
        self.owner_id = post_response['owner_id']
        self.owner_id_clean = abs(self.owner_id)
        self.date = post_response['date']
        self.marked_as_ads = post_response['marked_as_ads']
        self.type = post_response['post_type']
        self.text = post_response['text']
        self.can_pin = post_response['can_pin']
        if 'attachments' in post_response.keys():
            self.attachments = post_response['attachments']
        else:
            self.attachments = None
    def like(self):
        method = "likes.add?"
        params = f"type={self.type}&owner_id={self.owner_id}&item_id={self.id}" + self.client.default_params()
        request_url = self.client.api_url + method + params
        response = requests.get(request_url).json()
        print('response like is: \n', response)
    def repost(self, 
        message = None, group_id = None, mark_as_ads = 0):
        method = "wall.repost?"
        params = f"object=wall{self.owner_id}_{self.id}&mark_as_ads={mark_as_ads}" + self.client.default_params()
        if message:
            params += f'&message={message}'
        if group_id:
            params += f'&group_id={group_id}'
        request_url = self.client.api_url + method + params
        print('request url reply is \n ', request_url)
        response = requests.get(request_url).json()
        print('response repost is: \n', response)


    

