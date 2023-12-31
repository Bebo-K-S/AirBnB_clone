#!/usr/bin/python3
"""
The basemodel module file

Contains the class BaseModel and it's functions & attributes
"""
from datetime import datetime
import uuid
import models


class BaseModel:
    """class BaseModel

    Attributes:
        id (string): A unique generated id that identifes the instance
                     of the class.
        created_at (datetime): Assigned with the time the instance was created
                               at.
        updated_at (datetime): Initially assigned with the created time and
                               the date when the instance is updated.
    """
    id = None
    created_at = None
    updated_at = None

    def __init__(self, *args, **kwargs):
        """__init__

        The BaseModel constructor.
        """
        if kwargs:
            for key, val in kwargs.items():
                # If the key is the time change it from string to datetime
                if key in ('created_at', 'updated_at'):
                    val = datetime.strptime(val, "%Y-%m-%dT%H:%M:%S.%f")

                if key != '__class__':
                    setattr(self, key, val)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """__str__

        Returns a special message when printing the class.
        """
        return "[{:s}] ({:s}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
            )

    def save(self):
        """save

        A method that updates the piblic instaance attribute `updated_at`
        with the current datetime.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """to_dict

        A method that returns a dictionary containing all keys/values
        of __dict__ of the instance.

        Return:
            (dict): The keys/values of the __dict__ instance.
        """

        class_dict = self.__dict__.copy()
        class_dict['__class__'] = self.__class__.__name__
        class_dict['created_at'] = self.created_at.isoformat()
        class_dict['updated_at'] = self.updated_at.isoformat()

        return class_dict
