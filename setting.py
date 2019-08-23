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

# 筛选项目标题的关键词, 例如学校，公司。。,空表示为所有都可以
# KEYWORDS = ["学校", "公司", "食堂", ...]
KEYWORDS = [
    '小学', '中学', '大学', '专科',
    '学校', '技校', '学院', '职业',
    '体育', '初等', '高等', '宿舍',
    '宿舍', '食堂', '图书馆', '实验',
    '高中', '初中', '院校', '幼儿',
    '师范', '教学'
]

# 目标项目保存文件名
YES_FILE = "./temp/yes.txt"
# 不要的项目文件名
NO_FILE = "./temp/no.txt"

# 设置request的请求超时时间
TIMEOUT = 30
IS_PROXY = True
