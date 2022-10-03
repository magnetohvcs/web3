#!/bin/bash

# Global variable
[ -z $SLACK_TOKEN ] && SLACK_TOKEN=xoxb-4030150203985-4184537502672-UyJhyffwNj4sTs9kXcQjNvWh
[ -z $SLACK_CHANNEL ] && SLACK_CHANNEL=C0402U1LSRM
[ -z $TIME_SLEEP ] && TIME_SLEEP=30
data='{ "array": [] }'

function notification(){
    TOKEN=$1
    PRICE=$2
    # Logging to debug

    printf "\n------------------------------\n${TOKEN} tokeb with \$${PRICE} is being expected\n------------------------------\n"

    SLACK_ATTACHMENT=$(jq -n \
        --arg ch "$SLACK_CHANNEL" \
        --arg msg "The *$TOKEN*'s price is *\$$PRICE* at `date +%y/%m/%d-%H:%M`" \
        '{channel: $ch, "blocks":[{type: "section", text: {type: "mrkdwn", text: $msg}}]}' )

    response=$(curl -X POST \
        -H 'Content-type: application/json; charset=utf-8'  \
        -H "Authorization: Bearer ${SLACK_TOKEN}" \
        --data "$SLACK_ATTACHMENT"\
        https://slack.com/api/chat.postMessage 2>/dev/null)
    
    if [ $(jq -r '.ok' <<<$response) == false ]
    then
        echo "Can not notify due to" 
        jq <<<$response
        exit 1
    fi
}

function isNumber(){
    number=$1
    if [[ ! "$number" =~ ^-?[0-9]+$ ]]; then
        printf "${number} is not an integer.\nPlease input the expected price is integer!!" 
        exit 1
    fi   
}


function init_data(){
    read -p "Would you like look up the price of token? (The list tokens are splited by ','). They are: " tokens
    index=0

    for token in $(echo $tokens | sed 's/ //g' | tr "," "\n")
    do
        read -p "The expected price of $token is $" price
        # Sanitize space in variable
        price=$(echo $price | sed 's/ //g')
        # Validate variable is integer or not
        isNumber $price
        # Append element with token and price 
        data=$(jq ".array[${index}] += {\"token\" : \"${token}\", \"price\":${price}}" <<<$data)
        # Increase count variable
        index=$((index+=1))
    done
}

function check_price(){
    for element in $(jq -r '.array[] | @base64' <<<$data)
    do

        # Get element in array
        _tmp=$(echo $element | base64 -d) 
        # Get value from key token
        token=$(jq -r .token <<<$_tmp)
        # Get value from key price
        price=$(jq -r .price <<<$_tmp)

        # Get current price from api
        _price=$(curl -X 'GET' \
                    "https://api.coingecko.com/api/v3/simple/price?ids=${token}&vs_currencies=usd" \
                    -H 'accept: application/json' 2>/dev/null | jq -r .${token}.usd )  

        # Compare it is null or not
        if [ $_price == "null"  ]
        then
            echo "Don't found the price of ${token} token"
            exit 1
        fi

        # Logging to debug 
        echo "The price of $token is \$$_price at `date +%y/%m/%d-%H:%M`"

        # Parse to int in order to comparse the current price and the expected price, ignore stderr due to it will raise the expection about 'printf: 1330.82: invalid number'
        if [ $(printf "%d" "$_price" 2>/dev/null) -gt $price ]
        then
            notification $token $_price
        fi
    done
}

init_data

while :
do
    check_price
    # Wait 30s to refesh session check price
    sleep $TIME_SLEEP
done