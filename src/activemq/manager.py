from src.activemq.worker import ActiveMqWorker
import concurrent.futures

class ActivemqWorkerManager:
    def __init__(self, workers: list[ActiveMqWorker]) -> None:
        self.workers = workers
        self.threadpool = concurrent.futures.ThreadPoolExecutor(
            max_workers=len(self.workers)
            )
        
    def submit_threadpool(self):
        for worker in self.workers:
            self.threadpool.submit(worker.loop)

    def stop_threadpool(self):
        for worker in self.workers:
            worker.stop()
