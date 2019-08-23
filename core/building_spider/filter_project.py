import threading

from setting import KEYWORDS

def keywords_juste(sentences, keywords=KEYWORDS):
    '''
    :param keywords: 关键词
    :param sentences: 需要判断的句子
    :return: 如果句子中包含关键词就返回true，反之返回false
    '''
    if not KEYWORDS:
        return True
    for keyword in keywords:
        if keyword in sentences:
            return True
    return False

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
                if keywords_juste(project):
                    self.yes_queue.put(project)
                else:
                    self.no_queue.put(project)
                self.project_queue.task_done()

