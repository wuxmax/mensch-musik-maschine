

class ModuleLogger:
    def __init__(self):
        self.logs = []

    def log(self, module, log):
        self.logs.append([module, log])

    def get_logs(self):
        print('get log')
        print(self.logs)
        logs = self.logs
        self.logs = []
        return logs
