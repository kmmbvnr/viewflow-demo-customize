def task_owner(task_name):
    """
    Returns same process finished task owner
    """
    def get_task_owner(process):
        flow_cls = process.flow_cls

        task_node = flow_cls._meta.node(task_name)
        task = flow_cls.task_cls.objects.get(
            process=process,
            flow_task=task_node,
            status=flow_cls.task_cls.STATUS.FINISHED)
        return task.owner
    return get_task_owner
