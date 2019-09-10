FROM lambci/lambda:build-python3.6

COPY . /var/task

RUN pip3 install -r /var/task/requirements.txt

RUN rm /var/runtime/awslambda/runtime.cpython-36m-x86_64-linux-gnu.so

COPY runtime-mock.py /var/runtime/awslambda/runtime.py

ENTRYPOINT ["/var/lang/bin/python3.6", "/var/runtime/awslambda/bootstrap.py"]
