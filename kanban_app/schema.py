import graphene
from graphene_django.types import DjangoObjectType
from .models import Task, Column

class TaskType(DjangoObjectType):
    class Meta:
        model = Task

class ColumnType(DjangoObjectType):
    class Meta:
        model = Column

class CreateTask(graphene.Mutation):
    class Arguments:
        text = graphene.String(required=True)
        description = graphene.String()
        category_id = graphene.ID()
        date = graphene.String()  # Add this line

    task = graphene.Field(TaskType)

    def mutate(self, info, text, description=None, category_id=None, date=None):  # Update this line
        task = Task.objects.create(
            text=text,
            description=description,
            category_id=category_id,
            date=date  # Add this line
        )
        return CreateTask(task=task)

class UpdateTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        text = graphene.String()
        description = graphene.String()
        category_id = graphene.ID()
        date = graphene.String()  # Add this line

    task = graphene.Field(TaskType)

    def mutate(self, info, id, text=None, description=None, category_id=None, date=None):  # Update this line
        task = Task.objects.get(id=id)
        if text is not None:
            task.text = text
        if description is not None:
            task.description = description
        if category_id is not None:
            task.category_id = category_id
        if date is not None:  # Add this line
            task.date = date  # Add this line
        task.save()
        return UpdateTask(task=task)

class DeleteTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    task = graphene.Field(TaskType)

    def mutate(self, info, id):
        task = Task.objects.get(id=id)
        task.delete()
        return DeleteTask(task=task)

class CreateColumn(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        date = graphene.String()  # Add this line

    column = graphene.Field(ColumnType)

    def mutate(self, info, name, date=None):  # Update this line
        column = Column.objects.create(name=name, date=date)  # Update this line
        return CreateColumn(column=column)

class UpdateColumn(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        date = graphene.String()  # Add this line

    column = graphene.Field(ColumnType)

    def mutate(self, info, id, name=None, date=None):  # Update this line
        column = Column.objects.get(id=id)
        if name is not None:
            column.name = name
        if date is not None:  # Add this line
            column.date = date  # Add this line
        column.save()
        return UpdateColumn(column=column)

class DeleteColumn(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    column = graphene.Field(ColumnType)

    def mutate(self, info, id):
        column = Column.objects.get(id=id)
        column.delete()
        return DeleteColumn(column=column)

class Query(graphene.ObjectType):
    all_tasks = graphene.List(TaskType)
    all_columns = graphene.List(ColumnType)

    def resolve_all_tasks(self, info, **kwargs):
        return Task.objects.all()

    def resolve_all_columns(self, info, **kwargs):
        return Column.objects.all()

class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()
    create_column = CreateColumn.Field()
    update_column = UpdateColumn.Field()
    delete_column = DeleteColumn.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
