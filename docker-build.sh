IMAGE_NAME=j7p
HUB_NAME=newtondotcom/j7p:0.0.2
docker build . -f Dockerfile -t $IMAGE_NAME
docker tag $IMAGE_NAME $HUB_NAME
docker push $HUB_NAME