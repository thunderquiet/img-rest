

FROM python
WORKDIR /app
ADD ./img-rest/ .
ADD ./img-rest/app .
ADD ./config.py .
RUN pip install -r requirements.txt
CMD python ./runner.py
EXPOSE 80

