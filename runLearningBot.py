import asyncio
import schedule

from slack import RTMClient, WebClient

import data.decoder as de 

__self_user_id = '' # Bot's user ID here

def send_simple_message(web_client, channel, text, thread_ts=None): ## not sure if this is in the right place...
    if web_client is not None and len(text) > 0:
        message_args = {
            'channel' : channel,
            'text' : text,
            'as_user' : True
        }
        
        if thread_ts is not None:
            message_args['thread_ts'] = thread_ts
    
    web_client.chat_postMessage(**message_args)
    return

def __should_handle(user=__self_user_id, text=''):
    return (user != __self_user_id
        and len(text) is not 0)

def handle_message(data, web_client):
    text = data['text']
    user = data['user']
    channel = data['channel']
    ts = data['ts']
    # message handling code here
    if data['text'] == "!test":
        send_simple_message(web_client, data['channel'],"test!")
        return
    return

def start_scheduler():
    # Add in any work you need to do to build your list of scheduled tasks here (birthdays, maintenance, whatever)
    return

if __name__ == '__main__':

    ###############################
    ###   Get the slack token   ###
    ###############################

    #de.MAIN_KEY = "/home/ubuntu/learningBot/data/learningbot" # prod location
    de.MAIN_KEY = "data/learningbot"
    __slack_token = de.getToken()

    ###############################
    ###   End the slack token   ###
    ###############################
    
    start_scheduler()

    __web_client = None

    def schedule_monitor():
        while True:
            schedule.run_pending()
            asyncio.sleep(15) # 15 seconds

    def main():
        @RTMClient.run_on(event='message')
        def handle(web_client=None, data=None, **kwargs):
            print(f'Message data: {data}')

            if __should_handle(user=data.get('user'), text=data.get('text')):
                handle_message(data, web_client)
        
        global __web_client

        __web_client = WebClient(token=__slack_token)
        __rtm_client = RTMClient(token=__slack_token)
        __rtm_future = None

        while True:
            try:
                __rtm_future = __rtm_client.start()
                print("Learning bot is connected!")
                break
            except Exception:
                print("Failed to connect to Slack; retrying in 5 seconds")
                await asyncio.sleep(5)
        
        await asyncio.gather(__rtm_future, schedule_monitor())

    asyncio.run(main())