from flask_sqlalchemy import SQLAlchemy
import yaml
import pathlib

db = SQLAlchemy()


def init_database():
    db.drop_all()
    db.create_all()
    populate_database()


def populate_database():
    import database.models
    do_populate = True
    if not do_populate:
        return

    database_folder = str(pathlib.Path(__file__).parent.absolute())
    mock_data_file = database_folder + "/mock_data.yaml"
    with open(mock_data_file) as f:
        mock_data = yaml.safe_load(f)
        for mock_object_key, mock_object_dict in mock_data.items():
            if mock_object_key == "_classes":
                continue
            model_class_name = mock_object_dict.get("class")
            print("Model class name :")
            print(model_class_name)
            model_class = getattr(database.models, model_class_name)
            model_object = model_class()

            for attribute_name, attribute_name_value in mock_object_dict.items():
                setattr(model_object, attribute_name, attribute_name_value)

            db.session.add(model_object)
        db.session.commit()
