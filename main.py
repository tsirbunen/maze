from maze_activity import MazeActivity
from src.events.queue_observer import QueueObserver
from src.events.event_queue import EventQueue


from src.maze_parameters.maze_parameters import MazeParameters
from src.maze_parameters.maze_type import MazeType
from src.maze_parameters.parameters_querier import ParametersQuerier
from src.maze_parameters.log_instructions import log_instructions
from src.maze_generation.maze_generator import MazeGenerator
from src.graphical_ui.graphical_ui import GraphicalUI


# event_queue = EventQueue()


# # # log_instructions()
# # parameters = ParametersQuerier().get_parameters()
# parameters = MazeParameters(3, MazeType.SINGLE)
# maze_generator = MazeGenerator(parameters)
# # maze_generator.attach_observer(event_queue)
# maze_generator.generate()
# graphical_ui = GraphicalUI(parameters.size, event_queue)

# maze_generator.attach_observer(graphical_ui)
# maze_connection = maze_generator.get_finished_maze()


# while not event_queue.is_empty():
#     event = event_queue.next_event()
#     # print(event)
#     print(f"Event: {event.event_type} {event.to_node} {event.from_node}")
class MazeProgram:
    def __init__(self) -> None:
        # self.event_queue = EventQueue()
        self.event_queue = EventQueue()
        self.event_observer = QueueObserver(self.event_queue)

    def run(self):
        # log_instructions()
        # querier = ParametersQuerier()
        # parameters = querier.get_parameters()
        parameters = MazeParameters(3, MazeType.SINGLE)
        self.maze_generator = MazeGenerator(parameters)

        self.maze_generator.attach_observer(self.event_observer)

        graphical_ui = GraphicalUI(
            parameters.size,
            self.event_queue,
            self._perform_activity,
        )

    def _perform_activity(self, activity: MazeActivity):
        if activity == MazeActivity.GENERATE:
            self._generate_maze()
        else:
            raise ValueError("Unknown activity")

    def _generate_maze(self):
        self.maze_generator.generate()


maze_program = MazeProgram()
maze_program.run()

# # # https://superfastpython.com/thread-queue/


# # # SuperFastPython.com
# # # example of using a queue with a limited capacity
# # from time import sleep
# # from random import random
# # from threading import Thread
# # from queue import Queue


# # # generate work
# # def producer(queue):
# #     print("Producer: Running")
# #     # generate work
# #     for i in range(10):
# #         # generate a value
# #         value = random()
# #         # block
# #         sleep(value)
# #         # add to the queue
# #         queue.put(value)
# #     print("Producer: Done")


# # # consume work
# # def consumer(queue):
# #     print("Consumer: Running")
# #     # consume work
# #     while True:
# #         # get a unit of work
# #         item = queue.get()
# #         # report
# #         print(f">got {item}")
# #         # mark as completed
# #         queue.task_done()
# #     # all done
# #     print("Consumer: Done")


# # # create the shared queue
# # queue = Queue(2)
# # # start the consumer
# # consumer = Thread(target=consumer, args=(queue,), daemon=True)
# # consumer.start()
# # # start 5 producers
# # producers = [Thread(target=producer, args=(queue,)) for _ in range(5)]
# # for producer in producers:
# #     producer.start()
# # # wait for all producers to finish
# # for producer in producers:
# #     producer.join()
# # # wait for all work to be processed
# # queue.join()

# import threading
# import queue

# q = queue.Queue()


# def worker():
#     while True:
#         item = q.get()
#         print(f"Working on {item}")
#         print(f"Finished {item}")
#         q.task_done()


# # Turn-on the worker thread.
# # threading.Thread(target=worker, daemon=True).start()

# # Send thirty task requests to the worker.
# for item in range(3):
#     q.put(item)
# # worker()
# # Block until all tasks are done.
# q.join()
# print("All work completed")
