from django.db.migrations.state import ModelState
from django.db.migrations import operations
from django.db.migrations.migration import Migration
from django.db import connections
from django.db.migrations.state import ProjectState

def get_create_sql_for_model(model):
    model_state = ModelState.from_model(model)

    table_name = model.objects.model._meta.db_table

    # Create a fake migration with the CreateModel operation
    cm = operations.CreateModel(name=model_state.name, fields=model_state.fields.items())
    migration = Migration("fake_migration", "app")
    migration.operations.append(cm)
    print(cm.describe())
    # Let the migration framework think that the project is in an initial state
    state = ProjectState()

    # Get the SQL through the schema_editor bound to the connection
    connection = connections['default']
    with connection.schema_editor(collect_sql=True, atomic=migration.atomic) as schema_editor:
        try:
            state = migration.apply(state, schema_editor, collect_sql=True)
        except:
            ... 
    sqls = schema_editor.collected_sql
    items = []
    for sql in sqls:
        if sql.startswith('--'):
            continue
        items.append(sql)

    return table_name,items