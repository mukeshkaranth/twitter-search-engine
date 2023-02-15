#! /bin/bash
################################################################################
# Help                                                                         #
################################################################################
Help()
{
   # Display Help
   echo "This bash Script will help crawl twitter data based on the search query term and number of tweets provided."
   echo
   echo "Syntax: crawler.sh [-h|l|c]"
   echo "options:"
   echo "h     Print this Help."
   echo "l     hashtag or query term"
   echo "c     number of tweets"
   echo
}

################################################################################
################################################################################
# Main program                                                                 #
################################################################################
################################################################################

while getopts h:l:c: flag
do
    case "${flag}" in
        l) hashtag=${OPTARG};;
        c) count=${OPTARG};;
        \?) Help
            exit;;
    esac
done

if [[ $hashtag && $count ]] ; then
python3 TweetCrawler.py -l $hashtag -c $count
exit
else
Help
exit
fi