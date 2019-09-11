#!/bin/bash

#run for first time or when new packages are added

mkdir tmp

cp -f requirements.txt *.py .lambdaignore tmp

cd  tmp

pip install --upgrade --target ./ -r requirements.txt

cat .lambdaignore | xargs zip -9qyr lambda.zip  . -x
