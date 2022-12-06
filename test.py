from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import sys

name = sys.argv[1]
pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-e076c408-faa9-11e5-8916-0619f8945a4f'
pnconfig.publish_key = 'pub-c-3d779a5c-675d-411b-b23d-9265381dce0a'
pnconfig.user_id = name
pubnub = PubNub(pnconfig)

class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        print(message.publisher, ':', message.message)


pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('my_channel').execute()

while True:
    pubnub.publish().channel('my_channel').message(input()).sync()
