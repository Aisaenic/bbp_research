package main

import (
	"fmt"
//	"encoding/json"
	"os"
	"io/ioutil"
)

type Tester struct {
        FirstName string
        LastName string
}

type Media struct {
        previewUrl string
        fullUrl string
        altText string
}

type Link struct {
        text string
        url string
        tcourl string
        indices string
}

type User struct {
        username string
	id string
	displayName string
	rawDescription string 
	renderedDescription string
	descriptionLinks string
	verified string
	created string
	followersCount string
	friendsCount string
	statusesCount string
	favoritesCount string
	listedCount string
	mediaCount string
	location string
	protected string 
	link Link
	profileImageUrl string
	profileBannerUrl string
	label string
	description string
	descriptionUrls string
	linkUrl string
	url string
}

type Tweet struct {
	url string
	date string
	rawContent string
	renderedContent string
	id string 
	user User
	replyCount string
	retweetCount string
	likeCount string
	quoteCount string
	conversationId string
	lang string 
	source string
	sourceUrl string
	sourceLabel string 
	link Link
	media Media
	retweetedTweet string
	quotedTweet string
	inReplyToTweetId string
	inReplyToUser string
	mentionedUsers string 
	coordinates string 
	place string
	hashtags string
	cashtags string 
	card string 
	viewCount string 
	vibe string 
	content string 
	outlinks string
	outlinksss string
	tcoutlinks string
	tcoutlinksss string 
	username string
	classification bool 
}

func parse_input(in_file string) {
	data, err := ioutil.ReadFile(in_file)
	if err != nil {
		fmt.Println("Cannot read file")
		os.Exit(1)
	}

	test_data_map := make(map[int]Tester)

	fmt.Println("File content is:")
	fmt.Println(string(data))
}

func main() {
	file_name := os.Args[1]
	fmt.Println("file name pulled first is", file_name)
	parse_input(file_name)
} 
