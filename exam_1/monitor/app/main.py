import logging, os, time
from slack_sdk import WebClient

channel = os.getenv('channel')
token   =  os.getenv('slack_tone')
time_sleep = os.getenv('time_sleep')

client = WebClient(token=token)
logger = logging.getLogger(__name__)

def notification():

    message = [
    {
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Security Testing  "
			}
		},
		{
			"type": "divider"
		},
        {
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Site* "
				},
				{
					"type": "mrkdwn",
					"text": "*Information*"
				}
			]
		}
    ]

    response = client.chat_postMessage(blocks=message, channel=channel)
    logger.info(response)
    
if __name__ == "__main__":
    notification()