aws lambda create-function \
--function-name ${FUNCTIONNAME} \
--runtime python3.6 \
--role arn:aws:iam::${ACCOUNT_ID}:role/${ROLENAME} \
--handler lambda_function.lambda_handler \
--zip-file fileb://tmp/lambda.zip
