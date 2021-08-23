from celery import Celery
from vk_api.utils import get_random_id
import vk_api
from settings import VK_TOKEN


vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()

app = Celery('tasks', broker='redis://redis:6379')


@app.task
def send_to_user(message, user):
    try:
        vk.messages.send(user_id=user,
                         message=message,
                         random_id=get_random_id())
        return f'message: {message} sended to {user}'
    except BaseException as e:
        return f'ERROR sending to {user}: {e}'
