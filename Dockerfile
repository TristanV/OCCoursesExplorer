FROM python:3.10-bullseye

RUN pip install jupyterlab notebook voila
EXPOSE 8080

WORKDIR /usr/src/app
COPY src ./
COPY voila.json ./

RUN pip3 install -r requirements.txt

CMD [ "voila", "OCCoursesExplorer.ipynb" ]
