import threading

from setting import KEY_WORD


class FilterProject(threading.Thread):

    def __init__(self, project_queue, yes_queue, no_queue, FILTER, *args, **kwargs):
        super(FilterProject, self).__init__(*args, **kwargs)
        self.project_queue = project_queue
        self.yes_queue = yes_queue
        self.no_queue = no_queue
        self.filter = FILTER

    def run(self):
        if self.filter:
            while True:
                project = self.project_queue.get()
                if filter(project):
                    self.yes_queue.put(project)
                else:
                    self.no_queue.put(project)
                self.project_queue.task_done()



def filter(pro):
    if not KEY_WORD:
        return True
    a = [i for i in KEY_WORD if i in pro.title]
    if a:
        return True
    else:
        return False
