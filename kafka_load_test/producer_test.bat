@echo off

set "topics=test1"
set "record_size=4096"
set "num_records=1000"
set "throughput=10"

REM 멀티프로세스 실행
for %%t in (%topics%) do (
    start C:/kafka_2.13-3.5.1/bin/windows/kafka-producer-perf-test.bat ^
--producer-props bootstrap.servers=34.22.67.163:29092 ^
--print-metric ^
--record-size %record_size% --num-records %num_records% --throughput %throughput% ^
--topic %%t

)

echo now: %time%