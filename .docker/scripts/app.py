#!/usr/bin/python3
import os
import docker

client = docker.from_env()

def apps_active_list():
    pass

def app_is_active(container_name):
    list_of_active_containers = client.containers.list()
    def containers_equal(container: docker.models.containers.Container, test_string: str):
        if container.id == test_string:
            return True
        elif container.name == test_string:
            return True
        elif container.short_id == test_string:
            return True

    for container in list_of_active_containers:
        pass
    print(list_of_active_containers)

if __name__ == "__main__":
    app_is_active("asdf")
