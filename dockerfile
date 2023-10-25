FROM python:3.9.17-slim
ENV PYTHONPATH "${PYTHONPATH}: /app"
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

# Additional dependencies for TextBlob
RUN python -m textblob.download_corpora


# ENTRYPOINT ["tail", "-f", "/dev/null"] # For Debugging
CMD [ "python", "./news_madlibs.py"]