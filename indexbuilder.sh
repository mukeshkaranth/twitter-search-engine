#! /bin/bash
################################################################################
# Help                                                                         #
################################################################################
Help()
{
   # Display Help
   echo "This bash Script will help index the stored data to the given directory location using standard analyser"
   echo
   echo "Syntax: indexbuilder.sh [-h|-d]"
   echo "options:"
   echo "h     Print the help manual"
   echo "d     destination directory in the format: indexing_directory_name/"
   echo
}

################################################################################
################################################################################
# Main program                                                                 #
################################################################################
################################################################################

while getopts h:d: flag
do
    case "${flag}" in
        d) directory=${OPTARG};;
        \?) Help
            exit;;
    esac
done

if [ $directory ] ; then
python3 indexing.py -d $directory
exit
else
Help
exit
fi