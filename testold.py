from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import sys


name = sys.argv[1]
pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-e076c408-faa9-11e5-8916-0619f8945a4f'
pnconfig.publish_key = 'pub-c-3d779a5c-675d-411b-b23d-9265381dce0a'
pnconfig.user_id = name
pubnub = PubNub(pnconfig)

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass
        #print('   sending: success')
    else:
        print('   sending: fail')

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel('my_channel').message('Hello world!').pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        # Handle new message stored in message.message
        print(message.message)

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('my_channel').execute()

while True:
    a = input()
    pubnub.publish().channel('my_channel').message(name + ': ' + a).pn_async(my_publish_callback)
