FROM python:3.8

RUN pip install --upgrade pip

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY CostBHKcb.py /
COPY Model_cb /

EXPOSE 8501

CMD ["streamlit", "run", "./CostBHKcb.py","--server.fileWatcherType", "none", "--server.port=8501", "--server.address=0.0.0.0"]