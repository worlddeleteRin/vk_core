import requests
import json
import time

from httpx import Client



class VkClient():
    http: Client
    access_token: str
    api_v: str
    api_url: str
    app_id: int

    def __init__(self,
            access_token: str,
            api_v: str = '5.126',
            api_url: str = 'https://api.vk.com/method',
            app_id: int = 7709111
        ):
        self.api_v = api_v
        self.api_url = api_url
        self.access_token = access_token
        # init httpx Client
        self.http = Client(
            base_url = self.api_url,
            params = {
                'access_token': self.access_token,
                'v': self.api_v
            }
        )


    def request_token_url(self, app_id=7709111):
        return f'https://oauth.vk.com/authorize?client_id={app_id}&redirect_uri=https://oauth.vk.com/blank.html&display=popup&scope=notify+friends+photos+status+wall+offline+groups+stats+email+market&response_type=token&revoke=1'
    def default_params(self):
        return f"&access_token={self.access_token}&v={self.api_v}"


class VkWall():
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
        response = requests.get(request_url).json()
        if 'error' in response.keys():
            print('error while get post \n', response)
            return None
        else:
            for post in response['response']['items']:
                current_post = VkGroupPost(self.client, post)
                posts.append(current_post)
            return posts
    def post(self, post):
        method = 'wall.post'
        params = f"?owner_id=-{self.owner_id}"\
        f"&from_group={post.from_group}"\
        f"&attachments={post.get_attachments_str()}"\
        + self.client.default_params()
        if post.message:
            params += f"&message={post.message}"
        request = self.client.api_url + method + params
        response = requests.get(request).json()
        print('add post response is', response)
    def delete_post(self, post_id):
        method = 'wall.delete'
        params = f'?owner_id={self.group_id}'\
        f'&post_id={post_id}'\
        + self.client.default_params()
        request = self.client.api_url + method + params
        response = requests.get(request).json()
        if 'error' in response:
            print('error when delete post', response)


class Post():
    attachments = []
    from_group = 1 # 1 - from group, 0 - from user
    def __init__(self, message = None):
        self.message = message
        self.attachmets = []
    def get_attachments_str(self):
        return ','.join(self.attachments)

class VkGroupPost():
    # create vk group post object from post_response    
    def __init__(self, client, post_response):
        self.response = post_response
        self.client = client
        self.id = post_response['id']
        self.from_id = post_response['from_id']
        self.owner_id = post_response['owner_id']
        # self.group info owner_id_clean = abs(self.owner_id)
        self.date = post_response['date']
        self.marked_as_ads = post_response['marked_as_ads']
        self.type = post_response['post_type']
        self.text = post_response['text']
        if 'can_pin' in post_response:
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
        response = requests.get(request_url).json()
        print('response repost is: \n', response)
    def download_attachments(self):
        if not self.attachments:
            return None
        photos = []
        for attachment in self.attachments:
            if attachment["type"] == "photo":
                attachment_url = attachment["photo"]["sizes"][-1]["url"]
                current_photo = requests.get(attachment_url).content
                photos.append(current_photo)
        return photos

class VkGroups():
    group_id = None
    sort = None

    def __init__(self, client):
        self.client = client
    def getMembers(self, offset = 0):
        method = 'groups.getMembers'
        params = f"?group_id={self.group_id}"\
        f"&sort={self.sort}"\
        f"&offset={offset}"\
        + self.client.default_params()
        request = self.client.api_url + method + params
        response = requests.get(request).json()
        if 'error' in response:
            print('error while get groups Members, response is', response)
            return None
        return response["response"]["items"]
    def getMembersAll(self, members_limit=1000):
        members_count = self.getMembersCount()
        need_requests = int(members_count / members_limit)
        offset = 0
        group_members = []
        print('group members count:', members_count)
        for i in range(0, need_requests):
            print('request index: ', i, 'offset:', offset)
            current_members = self.getMembers(offset = offset)
            if current_members:
                group_members += current_members
                offset += members_limit
                time.sleep(2)
            else:
                print('no current members')
                return None
        return group_members

    def getMembersCount(self):
        info = self.getById()
        if info:
            return info["members_count"]
        return None
    def getById(self, fields="members_count"):
        method = 'groups.getById'
        params = f"?group_id={self.group_id}"\
        f"&fields={fields}"\
        + self.client.default_params()
        request = self.client.api_url + method + params
        response = requests.get(request).json()
        if 'error' in response:
            print('erorr while get group info by id, response is', response)
            return None
        return response["response"][0]


class Photos():
    group_id = None
    # image path or url
    photo_src = None
    upload_url = None
    upload_response = None
    photo_owner_id = None
    photo_id = None

    def __init__(self, client):
        self.client = client

    def get_attachment_str(self):
        return 'photo' + str(self.photo_owner_id) + '_' + str(self.photo_id)
    def upload_wall_photo(self):
        if not self.group_id:
            print('specify group_id to load photo')
            return None
        if not self.photo_src:
            print('specify photo_content to load photo')
            return None
        self.getWallUploadServer()
        if not self.upload_url:
            return None
        self.uploadWallUploadServer()
        self.saveWallPhoto()

    def get_photo_by_src(self):
        if not self.photo_src:
            print('specify photo src')
            return None
        if isinstance(self.photo_src, bytes):
            photo_content = self.photo_src
        elif 'http' in self.photo_src:
            photo_content = requests.get(self.photo_src).content
        else:
            photo_content = open(self.photo_src, 'rb').read()
        return photo_content


    def saveWallPhoto(self):
#       save photo after successful load it on server
        upload_response = self.upload_response
        method = 'photos.saveWallPhoto'
        params = f'?group_id={self.group_id}&photo={upload_response["photo"]}&server={upload_response["server"]}&hash={upload_response["hash"]}' + self.client.default_params()
        request = self.client.api_url + method + params
        response = requests.get(request).json()
        if 'error' in response:
            print('error when save wall photo, response is', response)
        else:
            self.photo_id = response["response"][0]["id"]
            self.photo_owner_id = response["response"][0]["owner_id"]

    def getWallUploadServer(self):
#   method returns server address (url) to upload photo 
        method = 'photos.getWallUploadServer'
        params = f'?group_id={abs(self.group_id)}' + self.client.default_params()
        request = self.client.api_url + method + params
        response = requests.get(request).json()
        if 'error' in response:
            print('error while get photo upload url, response is', response)
        self.upload_url = response["response"]["upload_url"]

    def uploadWallUploadServer(self):
        current_photo = self.get_photo_by_src()
        image_file = ('file.png', current_photo, 'multipart/form-data')
        response = requests.post(self.upload_url, files = {"photo": image_file }).json()
        self.upload_response = response
