#!/bin/bash

if [ ! -f config-trump ]; then
    echo "config-trump file required"
    exit 1
fi

set -ex

REPO_NAME=tbot
BRANCH=master
FILE=$BRANCH.zip
DIR=$REPO_NAME-$BRANCH
REPO=git@github.com:willrogers/$REPO_NAME.git
LINK=https://github.com/willrogers/$REPO_NAME/archive/$FILE
PHANTOM_FILE=phantomjs-2.0.0-linux-armv7l.tar.bz2
PHANTOM_TAR=https://github.com/mitghi/phantomjs-2.0.0-armv7/raw/master/$PHANTOM_FILE

wget $LINK
unzip $FILE

cd $DIR
virtualenv --no-site-packages venv
source venv/bin/activate
pip install -r requirements.txt

wget $PHANTOM_TAR
tar xjvf $PHANTOM_FILE phantomjs-2.0.0-linux-armv7l/bin/phantomjs
mv phantomjs-2.0.0-linux-armv7l/bin/phantomjs venv/bin/phantomjs
chmod +x venv/bin/phantomjs

echo
cat > trump.sh <<- EOM
#!/bin/bash
cd $(pwd)
source venv/bin/activate
python tweet.py trump
EOM

chmod +x trump.sh
echo "00 * * * * $(pwd)/trump.sh >> $(pwd)/trump.log 2>&1" > trump.cron
crontab trump.cron

cp ../config-trump .
