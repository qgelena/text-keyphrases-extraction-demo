FROM tallestman/gensim:latest

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./templates *.py SmartStoplist.txt ./
CMD [ "python", "./backend.py" ]