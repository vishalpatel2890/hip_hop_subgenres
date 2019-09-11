#!/bin/bash
#run to update function on lambdaignore

aws lambda update-function-code \
--function-name ${FUNCTIONNAME} \
--zip-file fileb://tmp/lambda.zip
