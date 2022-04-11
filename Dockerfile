FROM python:3
ADD bintest.py /
RUN pip install pip install websocket-client
CMD [ "python", "./bintest.py" ]
