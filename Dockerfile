FROM python:3
ENV PYTHONUNBUFFERED 1
COPY . /code/web_monitoring/
WORKDIR /code/web_monitoring
ENV COMPOSE_FILE=.env
RUN chmod +x /code/web_monitoring/run_web_monitor_dev.sh
RUN chmod +x /code/web_monitoring/run_data_handler_dev.sh
RUN chmod +x /code/web_monitoring/run_web_monitor_prod.sh
RUN chmod +x /code/web_monitoring/run_data_handler_prod.sh
COPY requirements.txt /code/
RUN pip install -r requirements.txt