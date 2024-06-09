#!/bin/bash

# Function to ask yes/no questions
ask_question() {
    local question="$1"
    local default="$2"
    local response
    while true; do
        read -p "$question [$default]: " response
        response=${response:-$default}
        case "$response" in
            [Yy]*) return 0 ;;
            [Nn]*) return 1 ;;
            *) echo "Please answer yes or no." ;;
        esac
    done
}

# Ask questions and execute corresponding actions
if ask_question "Do you want to init your db" "N"; then
    python /app/lib/db_init.py
fi

if ask_question "Do you want to fill the data with TMDB API" "N"; then
    python /app/processing.py
fi

if ask_question "Do you want to run the dashboard" "N"; then
    python /app/dahsboard.py
fi
