# An example on how to use and nest TaskSets

from locust import HttpUser, TaskSet, task, between

# 当类里面的任务请求有先后顺序时，继承SequentialTaskSet类
# 没有先后顺序，可以继承TaskSet类

class ForumThread(TaskSet):
    pass


class ForumPage(TaskSet):
    # wait_time can be overridden for individual TaskSets
    wait_time = between(10, 300)

    # TaskSets can be nested multiple levels
    tasks = {
        ForumThread: 3
    }

    @task(3)
    def forum_index(self):
        pass

    @task(1)
    def stop(self):
        self.interrupt()


class AboutPage(TaskSet):
    pass


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    # We can specify sub TaskSets using the tasks dict
    tasks = {
        ForumPage: 20,
        AboutPage: 10,
    }

    # We can use the @task decorator as well as the
    # tasks dict in the same Locust/TaskSet
    @task(10)
    def index(self):
        pass
#


import os
from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    def on_start(self):

        self.client.post("/login", {
            "username": "test_user",
            "password": ""
        })

    @task(10)
    def index(self):
        self.client.get("/")
        self.client.get("/static/assets.js")

    @task(5)
    def about(self):
        self.client.get("/about/")

if __name__ == "__main__":
    os.system("locust -f filename.py --host=http://localhost")