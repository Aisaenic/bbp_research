#!/usr/bin/env python3 

import argparse
import json 

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    file = args.file
    return file

def ingest_file(file):
    tweets = []
    openf = open(file)
    for line in openf: 
        data = json.loads(line)
        tweets.append(data)

    return tweets 

def unique_tweets(tweets): 
    id_list = []
    unique_tweets = []
    for val in tweets:
        if val["id"] not in id_list:
            id_list.append(val["id"])
            unique_tweets.append(val)
    return unique_tweets

def key_parts(tweets): 
    for val in tweets: 
        content = val["content"]
        print(content.replace("\n", " "))

def main():
    file = parse_args()
    all_tweets = ingest_file(file)
    tweets = unique_tweets(all_tweets)
    key_parts(tweets) 

main()
