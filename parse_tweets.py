#!/usr/bin/env python3 

import argparse
import json 
import csv

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("all_data")
    parser.add_argument("tagged_data")
    args = parser.parse_args()
    all_data = args.all_data
    tagged_data = args.tagged_data
    return [all_data, tagged_data]

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

def ingest_tags(file):
    tags = []
    openf = open(file)
    for line in openf:
        line = line.replace("\n", "")
        line = line.split(",")
        id_val = line[0]
        tag = line[1]
        tag_dict = {"id": id_val, "tag": tag}
        tags.append(tag_dict)
    return tags

def connect_tags(all_data, tagged_data):
    good_data = []
    for val in all_data:
        del val["_type"]
        del val["user"]["_type"]
        del val["user"]["link"]
        del val["links"]
        del val["outlinks"]
        del val["tcooutlinks"] 

        for elt in val["user"]:
            fieldName = "user_" + elt
            val[fieldName] = val["user"][elt]
        del val["user"] 
        
        if type(val["media"]) is list:
            val["altText"] = val["media"][0]["altText"]
            del val["media"]

        curr_id = val["id"]
        
        for num in tagged_data:
            temp_id = int(num["id"])
            if curr_id == temp_id:
                val["tag"] = num["tag"] 
        
        good_data.append(val)
    return good_data

def write_to_csv(data):
    with open('full_dataset.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field_names = data[0].keys()
        writer.writerow(field_names) 

        for line in data:
            vals = []
            for elt in line:
                vals.append(line[elt])
            print(vals)
            writer.writerow(vals) 

def main():
    files = parse_args()
    all_tweets = ingest_file(files[0])
    tags = ingest_tags(files[1])
    tweets = unique_tweets(all_tweets)
    parsed_data = connect_tags(tweets, tags)
    write_to_csv(parsed_data) 

main()
