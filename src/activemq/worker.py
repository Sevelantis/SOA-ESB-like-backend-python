import logging
import stomp.connect as connect
import time

class ActiveMqWorker:
    def __init__(
        self, 
        connection: connect.StompConnection11, 
        sub_id: int,
        queue: str
        ) -> None:
        self.conn = connection
        self.sub_id = sub_id
        self.queue = queue
        self.stopped = False
        self.__subscribe()
    
    def __subscribe(self):
        self.conn.subscribe(
            destination=self.queue,
            id=self.sub_id,
            ack='auto',
        )
    
    def loop(self) -> None:
        while self.conn.is_connected():
            time.sleep(.5)
            if self.stopped:
                break
    
    def stop(self) -> None:
        self.stopped = True
