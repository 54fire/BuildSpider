from queue import Queue


PROJECT_CLASS = ''

# 定义需要的队列
company_queue = Queue()
company_code_queue = Queue()
project_queue = Queue()
detail_queue = Queue()
# 过滤后的队列
yes_queue  = Queue()
no_queue = Queue()
# 代理ip的队列
proxy_queue = Queue()
post_proxy_queue = Queue()

# 筛选项目标题的关键词, 例如学校，公司。。
# KEY_WORD = ["学校", "公司", "食堂", ...]
KEY_WORD = []

# 目标项目保存文件名
YES_FILE = "./temp/yes.txt"
# 不要的项目文件名
NO_FILE = "./temp/no.txt"
