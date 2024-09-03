#!/bin/bash

# 로그 디렉토리 설정
LOG_DIR="/home/eppioen/Desktop/workspace/purse_etl/logs"

# Airflow 웹 서버 백그라운드 실행
nohup airflow webserver -p 8080 > "$LOG_DIR/airflow_webserver.out" 2>&1 &

# Airflow 스케줄러 백그라운드 실행
nohup airflow scheduler > "$LOG_DIR/airflow_scheduler.out" 2>&1 &