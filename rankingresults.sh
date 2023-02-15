#! /bin/bash
################################################################################
# Help                                                                         #
################################################################################
Help()
{
   # Display Help
   echo "This bash Script will help return a ranked result of the matched documents for the input query"
   echo
   echo "Syntax: rankingresults.sh [-h|-q|-c|-d]"
   echo "options:"
   echo "h     Print the help manual"
   echo "q     input the query term"
   echo "c     return top 'c' ranked results"
   echo "d     index directory from which the results must be fetched."
   echo
}

################################################################################
################################################################################
# Main program                                                                 #
################################################################################
################################################################################

while getopts h:q:c:d: flag
do
    case "${flag}" in
        q) query=${OPTARG};;
        c) count=${OPTARG};;
        d) directory=${OPTARG};;
        \?) Help
            exit;;
    esac
done

if [[ $query && $directory ]] ; then
echo $query
python3 ranking.py -c $count -d $directory -q "'${query}'"
exit
else
Help
exit
fi