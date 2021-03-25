
FROM python
WORKDIR /app
ADD ./img-engine/ .
ADD ./img-engine/app .
ADD ./config.py .
RUN pip install -r requirements.txt
CMD python ./runner.py
EXPOSE 5555

