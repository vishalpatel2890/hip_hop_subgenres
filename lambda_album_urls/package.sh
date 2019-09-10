#!/bin/bash
mkdir tmp

cp -f requirements.txt *.py .lambdaignore tmp

cd  tmp

pip install --upgrade --target ./ -r requirements.txt

cat .lambdaignore | xargs zip -9qyr lambda.zip  . -x
