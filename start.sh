if [ -n "$(docker ps -f "name=news_madlibs_container" -f "status=running" -q )" ]; then
    docker stop news_madlibs_container
fi
if [ $( docker ps -a -f name=news_madlibs_container | wc -l ) -eq 2 ]; then
    docker rm news_madlibs_container
fi

docker build -t news_madlibs .

docker run -it \
    --name news_madlibs_container \
    --network host \
    -v .:/app \
    news_madlibs

# docker exec -it news_madlibs_container /bin/bash # For debugging