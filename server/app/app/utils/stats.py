def get_task_stats(taskList):
    statDict = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}

    for task in taskList:
        a = task.priority
        statDict[str(a.name)] += 1

    return list(statDict.values())
