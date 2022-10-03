# Exam 1

### Deploy with docker

```
    cd exam_1/docker
    docker-compose up -d
```

#### Environment of monitor srvice

(__Set environment variable in exam_1/docker/monitor/.env__)

||Name|Description|
|----|-----|------|
|1|slack_token| Slack's token to authentication and notify|
|2|channel|Channel Id to recevice notification from chat bot|
|3|time_sleep| The time to re-check total block|
|4|threshold_block| The threshold block|
|5|my_node| address of my node|
|6|another_node| address of another node to compare|

### Deploy with k8s

```
    cd exam_1
    kubectl apply -f k8s/
```

# Exam 2

### Prequires

#### Package

Refer: https://stedolan.github.io/jq/download/

- jq 1.5 is in the official Debian and Ubuntu repositories. Install using `sudo apt-get install jq`.

- jq 1.5 is in the official Fedora repository. Install using `sudo dnf install jq`.

### Environment variable

||Name|Description|
|-|---|-----------|
|1|SLACK_TOKEN|slack token in order to authen and post message via api|
|2|SLACK_CHANNEL| channel's Id to recevice notication from chat bot|
|3|TIME_SLEEP| The time to re-check the price of token|


