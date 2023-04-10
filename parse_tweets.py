#!/usr/bin/env python3 

import argparse
import json 
import csv

#Parses command line args, two command line args exist, json file with all data and csv file with data tags
#Input: None 
#Output: list with json file all_data and csv file tagged_data
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("all_data")
    parser.add_argument("tagged_data")
    args = parser.parse_args()
    all_data = args.all_data
    tagged_data = args.tagged_data
    return [all_data, tagged_data]

#Parses all tweet data 
#Input: json file
#Output: List of tweets, where each tweet is represented as a multidimensional dict
def ingest_file(file):
    tweets = []
    openf = open(file)
    for line in openf: 
        data = json.loads(line)
        tweets.append(data)
    return tweets 

#Removes repeat tweets 
#Input: list of tweets 
#Output: list of tweets with any duplicate tweets removed
def unique_tweets(tweets): 
    id_list = []
    unique_tweets = []
    for val in tweets:
        if val["id"] not in id_list:
            id_list.append(val["id"])
            unique_tweets.append(val)
    return unique_tweets

#Isolates specific elements of a tweet
#Input: list of tweets 
#Output: N/A 
def key_parts(tweets): 
    #currently isolates tweet content, that can be changed 
    for val in tweets: 
        content = val["content"]
        print(content.replace("\n", " "))

#Processes the data tags 
#Input: csv file 
#Output: list of tags, where each element in list is dictionary with id/tag pairs 
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

#Cleans and prepares data for classification
#Adds tag to its corresponding data, removes extraneous fields, and replaces NaN values with 0
#Input: list of tweets, list of tags 
#Output: list where each element is a dictionary representing fully cleaned tweets 
def connect_tags(all_data, tagged_data):
    good_data = []
    for val in all_data:
        #delete extraneous fields
        del val["_type"]
        del val["user"]["_type"]
        del val["user"]["link"]
        del val["links"]
        del val["outlinks"]
        del val["tcooutlinks"] 

        #flatten three dimensional user field 
        for elt in val["user"]:
            fieldName = "user_" + elt
            val[fieldName] = val["user"][elt]
        del val["user"] 
        
        #flatten three dimensional media field 
        if type(val["media"]) is list:
            val["altText"] = val["media"][0]["altText"]
            del val["media"]

        curr_id = val["id"]
        
        #add the proper tag to its corresponding tweet 
        for num in tagged_data:
            temp_id = int(num["id"])
            if curr_id == temp_id:
                if num["tag"] == "FALSE":
                    val["tag"] = 0 
                elif num["tag"] == "TRUE":
                    val["tag"] = 1
       
        #change NaN data to ints with 0 
        for elt in val: 
            if type(val[elt]) is not str and type(val[elt]) is not int and type(val[elt]) is not bool:
                val[elt] = 0 
        good_data.append(val)
    return good_data

#Write cleaned data to csv 
#Input: list of cleaned tweets 
#Output: N/A 
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
