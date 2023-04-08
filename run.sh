set -xe

VERSION=1.3.33

docker build -t URL:$VERSION .
docker push URL:$VERSION
