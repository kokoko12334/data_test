import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("ka_per.csv", index_col=0)

df_m = pd.read_csv('kafka_performance_results/memory.csv')


cols = df.columns
t = ['1','cpu 사용률','디스크 읽기 처리량(Mib/s)','디스크 쓰기 처리량(Mib/s)','네트워크 수신량(Mib/s)','네트워크 송신량(Mib/s)']
for i in range(1,len(cols)):
    
    mean = round(df[cols[i]].mean(),2)
    plt.plot(df['time'], df[cols[i]], label='cpu_사용률')
    df.plot(x='time',y=cols[i],title=t[i])
    plt.axhline(y=mean, color='r', linestyle='--', label=f'평균:{mean}')
    plt.legend()
    plt.show()

mean = round(df_m['memory_utilization'].mean(),2)
plt.plot(df_m['time'], df_m['memory_utilization'], label='메모리사용률')
df_m.plot(x='time',y='memory_utilization',title='메모리 사용률')
plt.axhline(y=mean, color='r', linestyle='--', label=f'평균:{mean}')
plt.legend()
plt.show()





