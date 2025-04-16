"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 10/02/2025
"""

from sqlalchemy.orm import class_mapper

from sqlalchemy.orm import class_mapper, relationships


def model_to_dict(model, recursive=True, exclude_none=False, exclude=[]):
    """
    Converts an SQLAlchemy model instance to a dictionary.

    Args:
        model: SQLAlchemy model instance.
        recursive (bool): If True, also converts nested relationships.
        exclude_none (bool): If True, excludes keys with None values.
        exclude (list): List of attribute names to exclude.

    Returns:
        dict: Dictionary representation of the SQLAlchemy model.
    """
    if model is None:
        return None

    result = {}

    # Extract column attributes
    for column in class_mapper(model.__class__).columns:
        key = column.name
        if key in exclude:
            continue
        value = getattr(model, key)
        if exclude_none and value is None:
            continue
        result[key] = value

    if recursive:
        # Extract relationships (e.g., ForeignKey fields)
        for rel in class_mapper(model.__class__).relationships:
            key = rel.key
            if key in exclude:
                continue
            value = getattr(model, key)
            if value is None:
                continue

            if rel.uselist:  # One-to-Many or Many-to-Many
                result[key] = [model_to_dict(child, recursive, exclude_none, exclude) for child in value]
            else:  # One-to-One
                result[key] = model_to_dict(value, recursive, exclude_none, exclude)

    return result
