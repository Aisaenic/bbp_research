package main

import (
	"fmt"
	"encoding/json"
	"os"
	"io/ioutil"
)

type Tester struct {
	FirstName string `json:"FirstName"`
	LastName string `json:"LastName"`
}

type Media struct {
	PreviewUrl string `json:"previewUrl"`
	FullUrl string `json:"fullUrl"`
	AltText string `json:"altText"`
}

type Link struct {
	Text string `json:"text"`
	Url string `json:"url"`
	Tcourl string `json:"tcourl"`
	Indices string `json:"indices"`
}

type User struct {
	Username string `json:"username"`
	Id string `json:"id"`
	DisplayName string `json:"displayname"`
	RawDescription string `json:"rawDescription"`
	RenderedDescription string `json:"renderedDescription"`
	DescriptionLinks string `json:"descriptionLinks"`
	Verified string `json:"verified"`
	Created string `json:"created"`
	FollowersCount string `json:"followersCount"`
	FriendsCount string `json:"friendsCount"`
	StatusesCount string `json:"statusesCount"`
	FavoritesCount string `json:"favoritesCount"`
	ListedCount string `json:"listedCount"`
	MediaCount string `json:mediaCount"`
	Location string `json:"location"`
	Protected string `json:"protected"`
	Link Link `json:"link"`
	ProfileImageUrl string `json:"profileImageUrl"`
	ProfileBannerUrl string `json:"profileBannerUrl"`
	Label string `json:"label"`
	Description string `json:"description"`
	DescriptionUrls string `json:"descriptionUrls"`
	LinkTcourl string `json:"linkTcourl"`
	LinkUrl string `json:"linkUrl"`
	Url string `json:"url"`
}

type Tweet struct {
	Url string `json:"url"`
	Date string `json:"date"`
	RawContent string `json:"rawContent"`
	RenderedContent string `json:"renderedContent"`
	Id string `json:"id"`
	User User `json:"user"`
	ReplyCount string `json:"replyCount"`
	RetweetCount string `json:"retweetCount"`
	LikeCount string `json:"likeCount"`
	QuoteCount string `json:"quoteCount"`
	ConversationId string `json:"conversationId"`
	Lang string `json:"lang"`
	Source string `json:"source"`
	SourceUrl string `json:"sourceUrl"`
	SourceLabel string `json:"sourceLabel"`
	Links Link `json:"links"`
	Media Media `json:"media"`
	RetweetedTweet string `json:"retweetedTweet"`
	QuotedTweet string `json:"quotedTweet"`
	InReplyToTweetId string `json:"inReplyToTweetId"`
	InReplyToUser string `json:"inReplyToUser"`
	MentionedUsers string `json:"mentionedUsers"`
	Coordinates string `json:"coordinates"`
	Place string `json:"place"`
	Hashtags string `json:"hashtags"`
	Cashtags string `json:"cashtags"`
	Card string `json:"card"`
	ViewCount string `json:"viewCount"`
	Vibe string `json:"vibe"`
	Content string `json:"content"`
	Outlinks string `json:"outlinks"`
	Outlinksss string `json:"outlinksss"`
	Tcoutlinks string `json:"tcoutlinks"`
	Tcoutlinksss string `json:"tcoutlinksss"`
	Username string `json:"username"`
	Classification bool 
}

//Tweets struct which contains an array of Tweets
type Tweets struct {
	Tweets []Tweet 
}

type Testers struct {
	Testers []Tester
}

func parse_input(in_file string) {
	jsonFile, err := os.Open(in_file)
	if err != nil {
		fmt.Println("Cannot read file", err)
		os.Exit(1)
	}

	defer jsonFile.Close()

	byteValue, _ := ioutil.ReadAll(jsonFile)
	var tweets Tweets 
	json.Unmarshal(byteValue, &tweets)
	fmt.Println(tweets)
} 

func test_parse_input(in_file string) {
	jsonFile, err := os.Open(in_file)
	if err != nil {
		fmt.Println("Cannot read file", err)
		os.Exit(1)
	}

	fmt.Println("Successfully opened", in_file)

	defer jsonFile.Close()

	byteValue, _ := ioutil.ReadAll(jsonFile)

	var testers Testers 

	json.Unmarshal(byteValue, &testers)

	fmt.Println(testers) 

//	for i := 0; i < len(tweets.Tweets); i++ {
//		fmt.Println("content: " + tweets.Tweets[i].content)
//	}

}

func main() {
	file_name := os.Args[1]
	fmt.Println("file name pulled first is", file_name)
	parse_input(file_name)
} 
