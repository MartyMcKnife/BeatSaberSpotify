import pyyoutube

api = pyyoutube.Api(api_key='AIzaSyApqowLWESOEORFMzsHQKM74zgBZH8juzc')

playlist_json = api.get_playlist_item_by_id(playlist_item_id=
    'https://www.youtube.com/watch?v=Xdsg_0fhT5Y&list=PLhNeRwBqkeSUtIeUSuYtDpLuXFdKUz0-W')

print(playlist_json)
