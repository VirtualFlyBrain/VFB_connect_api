FROM python:3.6.2

RUN mkdir /code /code/src /code/vfb_connect_api
ADD requirements.txt run.sh setup.py logging.conf /code/

RUN chmod 777 /code/run.sh
RUN pip install -r /code/requirements.txt
# copy except __init__.py file and test folder
ADD src/vfb_connect_api/endpoints /code/vfb_connect_api/endpoints
ADD src/vfb_connect_api/exception /code/vfb_connect_api/exception
ADD src/vfb_connect_api/app.py src/vfb_connect_api/settings.py src/vfb_connect_api/restplus.py /code/vfb_connect_api/

WORKDIR /code

RUN cd /code && python3 setup.py develop
RUN ls -l /code && ls -l /code/vfb_connect_api

ENTRYPOINT bash -c "cd /code; python3 vfb_connect_api/app.py"