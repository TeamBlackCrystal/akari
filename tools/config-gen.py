import configparser
import json
import os

config = configparser.ConfigParser()
config.read('./example-config.ini', 'utf-8')

BOT_TOKEN = os.environ.get('BOT_TOKEN')
BOT_URL = os.environ.get('BOT_URL')
BOT_OWNERS = os.environ.get('BOT_OWNERS')

if BOT_TOKEN is None or BOT_URL is None or BOT_OWNERS is None:
    raise ValueError('BOT_TOKEN, BOT_URL, BOT_OWNERSのいずれかが定義されていません')
raw_config = config.__dict__['_sections']
print(raw_config)
raw_config['BOT']['token'] = BOT_TOKEN
raw_config['BOT']['url'] = BOT_URL
raw_config['BOT']['owner_ids'] = json.loads(BOT_OWNERS)

with open('./config.ini', mode='w', encoding='utf-8') as f:
    config.write(f)
