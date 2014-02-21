#!/bin/bash

DEPLOY_DIR=/var/www/tangthuvien.vn
CURRENT_DIR=$DEPLOY_DIR/current

cd $CURRENT_DIR
cd socket.io
exec node app.js
