"""
This script creates a predefined folder and file structure for a project.

📌 About `pathlib`:
- `pathlib` is a modern Python library for working with filesystem paths in an object-oriented way.
- It provides classes like `Path` to handle file and directory paths in a cleaner, cross-platform way.

📌 About `os`:
- The `os` module lets you interact with the operating system.
- Here, it’s used to:
    - Create directories (`os.makedirs`)
    - Check if files exist (`os.path.exists`)
    - Get file size (`os.path.getsize`)
    - Split file paths into directory and filename (`os.path.split`)
"""

import os
from pathlib import Path  # import Path from pathlib

# Define the main project folder name
project_name = "src"

# List of all files and folders we want to create
list_of_files = [
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/components/model_pusher.py",
    f"{project_name}/configuration/__init__.py",
    f"{project_name}/configuration/mongo_db_connection.py",
    f"{project_name}/configuration/aws_connection.py",
    f"{project_name}/cloud_storage/__init__.py",
    f"{project_name}/cloud_storage/aws_storage.py",
    f"{project_name}/data_access/__init__.py",
    f"{project_name}/data_access/proj1_data.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/entity/artifact_entity.py",
    f"{project_name}/entity/estimator.py",
    f"{project_name}/entity/s3_estimator.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/pipline/__init__.py",
    f"{project_name}/pipline/training_pipeline.py",
    f"{project_name}/pipline/prediction_pipeline.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",
    "app.py",
    "requirements.txt",
    "Dockerfile",
    ".dockerignore",
    "demo.py",
    "setup.py",
    "pyproject.toml",
    "config/model.yaml",
    "config/schema.yaml",
]

# Loop through all file paths and create them if they don't exist
for filepath in list_of_files:
    filepath = Path(filepath)  # Convert string path to a Path object
    filedir, filename = os.path.split(filepath)  # Split into directory and file name

    # If there is a directory in the path, create it
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)  # Create folders if not existing

    # Create empty file if it doesn't exist or is empty
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass  # Create an empty file
    else:
        print(f"File is already present at: {filepath}")
