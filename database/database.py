import yaml
from pathlib import Path
from database.models import db
import logging
from sqlalchemy import inspect


def init_database():
    db.drop_all()
    db.create_all()
    populate_database()


def populate_database():
    print("\n\n===== CREATING THE DATABASE =====\n")
    # Load mock data from YAML file
    mock_data_path = Path(__file__).parent / 'mock_data.yaml'
    with open(mock_data_path, 'r') as file:
        mock_data = yaml.safe_load(file)

    # Get all model classes from the SQLAlchemy metadata
    model_classes = {}

    print("Mapping classes...")
    for mapper in db.Model.registry.mappers:
        cls = mapper.class_
        classname = cls.__name__
        model_classes[classname.lower()] = cls

        print("    Mapped", classname, "class")
    print("    Model classes :", model_classes)
    print("Classes mapping complete !\n")

    print("Importing items from the mock data...")
    previous_model_class = None
    for table_name, table_data in mock_data.items():
        print("    Table data :")
        print("       ", table_data)
        # Find the model class corresponding to the table name
        model_class = model_classes.get(table_name)
        if model_class != previous_model_class :
            previous_model_class = model_class
            print("    Importing", [class_name for class_name, mapped_class in model_classes.items() if mapped_class == model_class][0], "class items")
        if model_class:
            print("        Model class columns :")
            print("           ", inspect(model_class).columns.keys())
            print("        Relationship columns :")
            print("           ", get_relationship_names(model_class))
            debug_counter = 1
            for item_data in table_data:
                print("        Item", debug_counter, ":")
                # Create an instance of the model class with the provided data
                print("            Item data :", item_data)
                instance = create_instance(model_class, item_data)
                print("            Instance created")
                for relationship_name, related_items in item_data.items():
                    if not isinstance(related_items, list):
                        continue
                    related_objects = []
                    for related_item in related_items:
                        related_objects.append(related_item)
                    print("Instance :", instance)
                    print("Relationship name :", relationship_name)
                    linked_class = model_classes[relationship_name[:-1]]
                    print("Linked class :", linked_class)
                    print("Related objects :", related_objects)
                    for related_object in related_objects:
                        getattr(instance, relationship_name).append(get_object_by_type_and_id(linked_class, related_object))
                db.session.add(instance)
                print("            Item successfully added to the database")
                debug_counter += 1
        else:
            print(f"Warning: No model found for table '{table_name}'")
    db.session.commit()
    print("All imports successful !")


def get_relationship_names(model_class):
    relationship_names = []
    for relationship in model_class.__mapper__.relationships:
        relationship_names.append(relationship.key)
    return relationship_names



def create_instance(model, data):
    instance = model()
    relationships = get_relationship_names(model)
    for key, value in data.items():
        if hasattr(model, key) and key not in relationships:
            setattr(instance, key, value)
    return instance

def get_object_by_type_and_id(model_class, id):
    try:
        # Query the model for the object with the given ID
        obj = model_class.query.get(id)
        return obj
    except Exception as e:
        print(f"Error: {e}")
        return None
