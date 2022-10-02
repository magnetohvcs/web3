import logging, os, time
from slack_sdk import WebClient
from web3 import Web3, HTTPProvider

channel = os.getenv('channel')
token = os.getenv('slack_tone')
time_sleep = os.getenv('time_sleep')

client = WebClient(token=token)
logger = logging.getLogger(__name__)


def getBlockNumber(node):
    # https://www.quicknode.com/docs/ethereum/eth_blockNumber
    
	w3 = Web3(HTTPProvider(f"http://{node}:8545"))
	total = w3.eth.blockNumber
	logging.info(f"The number block of {node} is {total}")
	return total



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
    getBlockNumber("my_node")