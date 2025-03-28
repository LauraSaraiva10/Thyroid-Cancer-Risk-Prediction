import os
import importlib
from models.base_model import Base

def import_models():
    model_dir = 'models'

    for filename in os.listdir(model_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Strip .py extension
            importlib.import_module(f'models.{module_name}')

    # After importing, ensure all tables are in Base.metadata
    assert Base.metadata.tables, "No tables were found in Base.metadata. Ensure models inherit from Base."
