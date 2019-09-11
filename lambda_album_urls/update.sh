#!/bin/bash
#run to update zipfile 
cp -f requirements.txt *.py .lambdaignore tmp

cd  tmp

cat .lambdaignore | xargs zip -9qyr lambda.zip  . -x
