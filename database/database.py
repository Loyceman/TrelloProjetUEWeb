import yaml
from pathlib import Path
from database.models import db


def init_database():
    db.drop_all()
    db.create_all()
    populate_database()


def populate_database():
    # Load mock data from YAML file
    mock_data_path = Path(__file__).parent / 'mock_data.yaml'
    with open(mock_data_path, 'r') as file:
        mock_data = yaml.safe_load(file)

    # Get all model classes from the SQLAlchemy metadata
    model_classes = {}

    for mapper in db.Model.registry.mappers:
        cls = mapper.class_
        classname = cls.__name__
        if not classname.startswith('_'):
            tblname = cls.__tablename__
            model_classes[tblname] = cls
    for table_name, table_data in mock_data.items():
        # Find the model class corresponding to the table name
        model_class = next((cls for cls in model_classes.values() if cls.__tablename__ == table_name), None)
        print(model_class)
        if model_class:
            print(table_data)
            for item_data in table_data:
                print(item_data)
                # Create an instance of the model class with the provided data
                instance = model_class(**item_data)
                db.session.add(instance)
        else:
            print(f"Warning: No model found for table '{table_name}'")
    db.session.commit()