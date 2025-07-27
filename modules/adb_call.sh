#!/bin/bash

# Check if a number was provided
if [ -z "$1" ]; then
    echo "Usage: ./adb_call.sh <phone_number>"
    exit 1
fi

number="$1"

# Execute ADB call
adb shell am start -a android.intent.action.CALL -d tel:$number

