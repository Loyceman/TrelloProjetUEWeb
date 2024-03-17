import yaml
from pathlib import Path
from database.models import db
from sqlalchemy import inspect
import os


def init_database():
    if os.path.exists("database/database.db"):
        os.remove("database/database.db")
    db.drop_all()
    db.create_all()
    populate_database()
    print("\n")


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

        print("    Mapped " + str(classname) + " class")
    print("    Model classes : " + str(model_classes))
    print("Classes mapping complete !\n")

    print("Importing items from the mock data...")
    previous_model_class = None
    for table_name, table_data in mock_data.items():
        # Find the model class corresponding to the table name
        model_class = model_classes.get(table_name)
        if model_class != previous_model_class:
            previous_model_class = model_class
            print("    Importing " + str(
                [class_name for class_name, mapped_class in model_classes.items() if mapped_class == model_class][
                    0]) + " class items")
            print("        Table data :")
            print("            " + str(table_data))
        if model_class:
            print("        Model class :")
            print("            " + str(inspect(model_class).columns.keys()))
            debug_counter = 1
            for item_data in table_data:
                print("        Item " + str(debug_counter) + " :")
                # Create an instance of the model class with the provided data
                print("            Item data : " + str(item_data))
                instance = create_instance(model_class, item_data)
                print("            Instance created")
                db.session.add(instance)

                for relationship_name, related_items in item_data.items():
                    if not isinstance(related_items, list):
                        continue
                    related_objects = []
                    for related_item in related_items:
                        related_objects.append(related_item)
                    linked_class = model_classes[relationship_name[:-1]]
                    print("            Found relationship with class " + str(
                        linked_class) + " and with items with id : " + str(related_objects))
                    for related_object in related_objects:
                        getattr(instance, relationship_name).append(
                            get_object_by_type_and_id(linked_class, related_object))
                print("            Item successfully added to the database !")
                debug_counter += 1
        else:
            print(f"Warning: No model found for table '{table_name}'")
        print("    All items in the class imported !\n")
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


def get_object_by_type_and_id(model_class, object_id):
    try:
        obj = model_class.query.get(object_id)
        return obj
    except Exception as e:
        print(f"Error: {e}")
        return None
