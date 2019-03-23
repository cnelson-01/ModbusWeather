# import threading
#
# prompt = '''q = quit
# choice: '''
#
#
# class InputHandler:
#     def __init__(self):
#         self.keepRunning = True
#         self.start()
#
#     def start(self):
#         self.thread = threading.Thread(target=self.runThread)
#         self.thread.start()
#
#     def runThread(self):
#         while keepRunning:
#             command = input(prompt)
#
#             if command == 'q':
#