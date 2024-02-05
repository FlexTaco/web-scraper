#!/bin/bash

#array for both 
ebay_files=()
hotTopic_files=()

while true;
do
    # counter for the output filenames
    counterEbay=1
    counterHotTopic=1

    if ls tagsoup-1.2.1.jar; then
        echo "tagsoup is in the current directory"
    else
       wget https://repo1.maven.org/maven2/org/ccil/cowan/tagsoup/tagsoup/1.2.1/tagsoup-1.2.1.jar
    fi

    # Read from the file and curl it and tagsoup
    while IFS= read -r url; do
        echo "Fetching content from: $url"
        output_file="ebay$counterEbay.html"
        curl "$url" -o "$output_file"
        echo "Content saved to: $output_file"
        echo "--------------------------------------"
        ebay_files+=("ebay$counterEbay.xhtml")
        java -jar tagsoup-1.2.1.jar --files $output_file
        ((counterEbay++))
    done < "$1"

    while IFS= read -r url; do
        echo "Fetching content from: $url"
        output_file="hotTopic$counterHotTopic.html"
        curl "$url" -o "$output_file"
        echo "Content saved to: $output_file"
        echo "--------------------------------------"
        hotTopic_files+=("hotTopic$counterHotTopic.xhtml")
        java -jar tagsoup-1.2.1.jar --files $output_file
        ((counterHotTopic++))
    done < "$2"


    echo "eBay files: ${ebay_files[@]}"
    echo "HotTopic files: ${hotTopic_files[@]}"
    #loop through both array and run python to insert data into sql table
    for ((i = 0; i< ${#ebay_files[@]}; i++)); do
        #change this to parser.py not parserTest.py
        python3 parser.py ${ebay_files[$i]} ${hotTopic_files[$i]}
        echo "-------------------------------------------"
    done

    #delete files; uncomment when done
    rm -f *.html *.xhtml

    #every 6 hours 
    sleep 21600

done
