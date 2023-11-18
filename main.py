from src.events.queue_observer import QueueObserver
from src.events.event_queue import EventQueue
from src.graphical_ui.maze_activity import MazeActivity


from src.maze_parameters.maze_parameters import MazeParameters
from src.maze_parameters.maze_type import MazeType
from src.maze_parameters.parameters_querier import ParametersQuerier
from src.maze_parameters.log_instructions import log_instructions
from src.maze_generation.maze_generator import MazeGenerator
from src.graphical_ui.graphical_ui import GraphicalUI
from src.maze_solving.maze_solver import MazeSolver


class MazeProgram:
    def __init__(self) -> None:
        self.event_queue = EventQueue()
        self.event_observer = QueueObserver(self.event_queue)
        self.graphical_ui = None
        self.maze_generator = None
        self.maze_solver = None
        self.maze = None

    def run(self):
        # log_instructions()
        # querier = ParametersQuerier()
        # parameters = querier.get_parameters()
        parameters = MazeParameters(4, MazeType.SINGLE)
        self.maze_generator = MazeGenerator(parameters)

        self.maze_generator.attach_observer(self.event_observer)

        self.graphical_ui = GraphicalUI(
            parameters.size,
            self.event_queue,
            self._perform_activity,
        )

    def _perform_activity(self, activity: MazeActivity, parameters):
        print(f"Performing activity {activity}")
        if activity == MazeActivity.GENERATE:
            self._generate_maze(with_event_dispatching=parameters)
        elif activity == MazeActivity.GET_MAZE:
            maze = self._get_generated_maze()
            self.maze = maze
            return maze
        elif activity == MazeActivity.SOLVE_WALL_FOLLOWER:
            self._setup_solver()
            self.maze_solver.solve_with_wall_follower()
        else:
            raise ValueError("Unknown activity")

    def _generate_maze(self, with_event_dispatching):
        self.maze_generator.generate(with_event_dispatching)
        # maze = self.maze_generator.get_finished_maze()
        # self.graphical_ui.set_maze(maze)

    def _get_generated_maze(self):
        return self.maze_generator.get_finished_maze()

    def _setup_solver(self):
        if self.maze_solver is None:
            self.maze_solver = MazeSolver(self.maze)
            self.maze_solver.attach_observer(self.event_observer)


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
