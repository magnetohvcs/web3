import os, time
from slack_sdk import WebClient
from web3 import Web3, HTTPProvider
import requests

# Init data
channel = os.getenv('channel')
token = os.getenv('slack_token')
time_sleep = int(os.getenv('time_sleep'))
client = WebClient(token=token)
myNode = os.getenv('my_node')
anotherNode = os.getenv('another_node')
threshold = int(os.getenv('threshold_block'))

def getBlockNumber(node):
    # https://www.quicknode.com/docs/ethereum/eth_blockNumber
	w3 = Web3(HTTPProvider(f"http://{node}:8545"))
	total = w3.eth.blockNumber
	print(f"The number block of {node} is {total}")
	return total


def notification(myTotal, anotherTotal):
    message = [
    {
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "My node is slower than another node"
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
					"text": f"My blocks: `{myTotal}` \nAnother blocks: `{anotherTotal}`"
				}
			]
		}
    ]

    client.chat_postMessage(blocks=message, channel=channel)

    
if __name__ == "__main__":
	retry = 1
	while True:
		try:
			myTotal = getBlockNumber(myNode)
			anotherTotal = getBlockNumber(anotherNode)
   
			if (anotherTotal - myTotal) > threshold:
				notification(myTotal, anotherTotal)

			time.sleep(time_sleep)
   
		except requests.exceptions.ConnectionError as e:
			print(f"Retry connect #{retry} due to\n", e)
			time.sleep(2)
			retry += 1
   
		except Exception as e:
			print(e)
			break
