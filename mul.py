import multiprocessing

def worker(queue, value):
    queue.put(value)
    print(f"작업 {value} 완료")

if __name__ == '__main__':
    queue = multiprocessing.Queue()
    
    processes = []
    for i in range(3):
        process = multiprocessing.Process(target=worker, args=(queue, i))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    
    while not queue.empty():
        value = queue.get()
        print(f"작업 {value} 결과 확인")