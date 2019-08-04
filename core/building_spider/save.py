def save_file(file_name, queue):
    with open(file_name, 'w') as f:
        for _ in range(queue.qsize()):
            pro = queue.get()
            project = str(pro)
            f.write(project + '\n')
            queue.task_done()
