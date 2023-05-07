from app.schemas.task import TaskWithDepdend, TaskDependency


def topo_sort_task(taskList):
    graph = {}
    in_degrees = {}

    for task in taskList:
        task_id = task.id
        depend_on = task.depends_on

        if task_id not in graph:
            graph[task_id] = set()

        if task_id not in in_degrees:
            in_degrees[task_id] = 0

        for dependency in depend_on:
            depend_on_task_id = dependency.depend_on_task_id

            if depend_on_task_id not in graph:
                graph[depend_on_task_id] = set()

            if depend_on_task_id not in in_degrees:
                in_degrees[depend_on_task_id] = 0

            graph[depend_on_task_id].add(task_id)
            in_degrees[task_id] += 1

    result = []
    queue = []

    for task_id, in_degree in in_degrees.items():
        if in_degree == 0:
            queue.append(task_id)

    print(graph)

    while queue:
        task_id = queue.pop(0)
        # print(task_id)
        result.append(task_id)

        for dependent_task_id in graph[task_id]:
            in_degrees[dependent_task_id] -= 1

            if in_degrees[dependent_task_id] == 0:
                queue.append(dependent_task_id)

    tasks_dict = {task.id: task for task in taskList}
    sorted_tasks = [tasks_dict[task_id] for task_id in result]
    return sorted_tasks
