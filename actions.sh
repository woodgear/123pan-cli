#!/bin/bash

function p123-gen-token() {
  mkdir -p ~/.p123
  local token=$(curl -q -s 'https://open-api.123pan.com/api/v1/access_token' \
    -H 'Content-Type: application/json' \
    -H 'Platform: open_platform' \
    -d "{
        \"ClientID\": \"$P123_CLIENT_ID\",
        \"ClientSecret\": \"$P123_CLIENT_SECRET\"
    }" | jq -r .data.accessToken)
  echo "$token" >~/.p123/token
}

function p123-hash() {
  export PAN_123_ACCESS_TOKEN=$(cat ~/.p123/token)
  python3 ./cli.py | tee ./123.out
}
