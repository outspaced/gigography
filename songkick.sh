#!/bin/bash
for i in `seq 0 10`;
do
	curl -G -d "page=$i&apikey=$SONGKICK_API_KEY" https://api.songkick.com/api/3.0/users/outspaced/gigography.xml > $i.xml
done    
