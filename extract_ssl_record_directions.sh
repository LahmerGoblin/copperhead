p1=45;
p2=40;
packet_count=0;

tshark -r $1 -z follow,ssl,hex,1 -Tfields -e ip.src -e ip.dst -e ssl.record.length > /tmp/ssl_record

while read row; do
    if [[ $row == 1* ]] 
        then 
        wordc=0
        for word in $row; do
            wordc=$((wordc+1))
        done
        if [[ $wordc == 3 ]]
            then
            if [[ $row == 134.169.109.25* ]]
                then
                echo 1
            else
                packet_count=$((packet_count+1))
                if [[ $packet_count -le $p2 ]]
                    then 
                    echo -1
                else
                    packet_count=$((packet_count-p2))
                fi
            fi
        fi
    fi
done </tmp/ssl_record
