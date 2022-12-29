FROM python:3
ENV PYTHONUNBUFFERED 1
COPY . /code/web_monitoring/
WORKDIR /code/web_monitoring
RUN chmod +x /code/web_monitoring/run_web_monitor.sh
RUN chmod +x /code/web_monitoring/run_data_handler.sh
COPY requirements.txt /code/
RUN pip install -r requirements.txt