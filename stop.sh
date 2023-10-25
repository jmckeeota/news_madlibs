if [ -n "$(docker ps -f "name=news_madlibs_container" -f "status=running" -q )" ]; then
    docker stop news_madlibs_container
fi
if [ $( docker ps -a -f name=news_madlibs_container | wc -l ) -eq 2 ]; then
    docker rm news_madlibs_container
fi