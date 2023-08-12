import pandas as pd
import matplotlib.pyplot as plt


df_cpu = pd.read_csv("kafka_performance_results/3-3/cpu.csv")
df_rb = pd.read_csv("kafka_performance_results/3-3/disk_rb.csv")
df_wb = pd.read_csv("kafka_performance_results/3-3/disk_wb.csv")
df_rby = pd.read_csv("kafka_performance_results/3-3/received_bytes.csv")
df_sby = pd.read_csv("kafka_performance_results/3-3/sent_bytes.csv")
df_m = pd.read_csv("kafka_performance_results/3-3/memory.csv")


df = pd.merge(df_cpu,df_rb, on='time')
df = pd.merge(df,df_wb,on='time')
df = pd.merge(df,df_rby,on='time')
df = pd.merge(df,df_sby,on='time')
df

df['cpu_utilization'] = df['cpu_utilization']*100
df['disk_rb'] = df['disk_rb']/1000000
df['disk_wb'] = df['disk_wb']/1000000
df['received_bytes'] = df['received_bytes']/1000000
df['sent_bytes'] = df['sent_bytes']/1000000


lst = []
for i in df['time']:
    lst.append(i.split()[4])
df['time'] = lst

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

cols = df.columns
t = ['1','cpu 사용률','디스크 읽기 처리량(Mib/s)','디스크 쓰기 처리량(Mib/s)','네트워크 수신량(Mib/s)','네트워크 송신량(Mib/s)']
for i in range(1,len(cols)):
    
    mean = round(df[cols[i]].mean(),2)
    plt.plot(df['time'], df[cols[i]], label='cpu_사용률')
    df.plot(x='time',y=cols[i],title=t[i])
    plt.axhline(y=mean, color='r', linestyle='--', label=f'평균:{mean}')
    plt.legend()
    plt.show()




lst = []
for i in df_m['time']:
    lst.append(i.split()[4])
df_m['time'] = lst

mean = round(df_m['memory_utilization'].mean(),2)
plt.plot(df_m['time'], df_m['memory_utilization'], label='메모리사용률')
df_m.plot(x='time',y='memory_utilization',title='메모리 사용률')
plt.axhline(y=mean, color='r', linestyle='--', label=f'평균:{mean}')
plt.legend()
plt.show()





