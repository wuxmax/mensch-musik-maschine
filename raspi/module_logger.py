

class ModuleLogger:
    def __init__(self):
        self.logs = []

    def log(self, module, log):
        self.logs.append([module, str(log)])

    def get_logs(self):
        logs = self.logs
        self.logs = []
        return logs
