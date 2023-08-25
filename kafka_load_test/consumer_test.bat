@echo off

set "topics=test1"
set "message=10000"
set "num_records=1000"
set "interval=100"
set "repeat_count=1"

REM 멀티프로세스 실행
for /l %%i in (1,1,%repeat_count%) do (

start C:/kafka_2.13-3.5.1/bin/windows/kafka-consumer-perf-test.bat ^
--broker-list 34.146.29.164:29092 ^
--topic %topics% ^
--messages %message% ^
--show-detailed-stats ^
--reporting-interval %interval% ^
--group g1

)

