import os
import sys
import json
import shutil
import joblib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from from_root import from_root

from src.exception import MyException
from src.logger import logging

class ModelRegistry:
    """
    Handles saving, versioning, and comparing ML models locally.
    Stores:
        - Models as .pkl
        - Metrics as .json
    """

    def __init__(self):
        """
         Folder path to store models and metrics
        """
        self.model_dir = 'models'
        self.model_dir_path = os.path.join(from_root(), self.model_dir)
        os.makedirs(self.model_dir_path ,exist_ok=True)
        self.run_time = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
        self.model_version = os.path.join(self.model_dir_path, self.run_time)
        os.makedirs(self.model_version,exist_ok=True)

        ''' Folder for store best model and that use in prediction'''
        self.best_model_dir = "predictive_model"
        self.best_model_dir_path =os.path.join(from_root() ,self.best_model_dir)
        os.makedirs(self.best_model_dir_path ,exist_ok=True)

        # self.best_model_dir = self.registry_dir / "best_model"
        # self.versions_dir = self.registry_dir / "versions"

        # self.best_model_dir.mkdir(exist_ok=True)
        # self.versions_dir.mkdir(exist_ok=True)

    def save_model(self, model: Any, metrics: Dict[str, float],model_name='model' ,metrics_name='metrics') -> str:
        """
        Save a model and metrics to a versioned folder.
        Returns path to saved model folder.
        """
        try:
            logging.info("Saving new model and metrics to versioned folder.")

            # Save model
            model_paths = f"{model_name}.pkl"
            model_path = os.path.join(self.model_version ,model_paths)
            joblib.dump(model ,model_path)

            # Save metrics
            metrics_path = f"{metrics_name}.json"
            metrix_path = os.path.join(self.model_version ,metrics_path)

            with open(metrix_path, "w") as f:
                json.dump(metrics, f, indent=4)

            logging.info(f"Model and metrics saved at {self.model_version}")
            return str(self.model_version)

        except Exception as e:
            raise MyException(e, sys) from e

    def _load_metrics(self, folder: Path ,metrics_name = 'metrics') -> Dict[str, float]:
        # metrics_path = os.path.join(folder , f"{metrics_name}.json")
        try:
            folder_path = Path(folder)
            json_file = next(folder_path.glob("*.json"), None) # find first file with json extension in folder
            
            if json_file is None:
                return {}
            with open(json_file, "r") as f:
                return json.load(f)
        except Exception as e:
            raise MyException(e, sys) from e


    def compare_and_update_best(self, new_model: Any, new_metrics: Dict[str, float], metric_key: str = '0', model_name='model' , metrics_name ='metrics'):
        """
        Compare a new model to the current best model using a chosen metric (default: accuracy).
        If better, replace the best model.
        """
        try:
            # Save model to versions folder first (for history)
            new_model_path = self.save_model(new_model, new_metrics ,model_name ,metrics_name)
            print(new_model_path)

            # Check if best model exists
            try:
                folder = Path(self.best_model_dir_path)
                best_folder = next((p for p in folder.iterdir() if p.is_dir()),'')
            except Exception as e:
                raise MyException(e, sys) from e
            
            # getting metrics of best or predictive model
            folder = os.path.join(self.best_model_dir_path ,best_folder)
            best_metrics = self._load_metrics(best_folder)


            if not best_metrics:
                logging.info("No best model found. Setting current model as best.")
                self._update_best_model(new_model_path)
                return True

            # Compare metric
            old_score = best_metrics.get(metric_key, 0.0)
            new_score = new_metrics.get(metric_key, 0.0)
            logging.info(f"Old best {metric_key}: {old_score}, New {metric_key}: {new_score}")

            if new_score > old_score:
                logging.info("New model is better. Updating best model.")
                self._update_best_model(new_model_path)
                return True
            else:
                logging.info("New model is NOT better. Keeping old best model.")
                return False

        except Exception as e:
            raise MyException(e, sys) from e

    def _update_best_model(self, source_folder: str):
        """
        Replace best model folder with contents from source folder.
        """
        try:
           
            if os.path.exists(self.best_model_dir_path):
                shutil.rmtree(self.best_model_dir_path)    # delete all existing file into a folder

            dir_path=os.path.join(self.best_model_dir_path ,self.run_time)
            os.makedirs(dir_path ,exist_ok=True)
            shutil.copytree(source_folder, dir_path ,dirs_exist_ok=True)
            logging.info("Best model updated successfully.")
        except Exception as e:
            raise MyException(e, sys) from e
    

    def load_best_model(self) -> Any:
        """
        Load the best model from the best_model folder.
        :return: Best model object.
        """
        try:
            folder = Path(self.best_model_dir_path)
            best_model = next((p for p in folder.iterdir() if p.is_dir()), '')
        except Exception as e:
            raise MyException(e, sys) from e

        try:
            # Path to the folder containing the pkl file
            model_folder_path = os.path.join(self.best_model_dir_path, best_model)
            # Get first .pkl file
            model_pkl = next(Path(model_folder_path).glob("*.pkl"), None)

            if model_pkl is None:
                #raise FileNotFoundError("No best model found yet.")
                return None

            # Load the pickle file
            print(model_pkl)
            print(os.path.isfile(model_pkl))  # must be True
            print(os.path.getsize(model_pkl)) # must not be 0

            with open(model_pkl, "rb") as f:
                model = joblib.load(f)
            return model
            

        except Exception as e:
            raise MyException(e, sys) from e



# used for testing purpuse

# ex = ModelRegistry()

# from sklearn.ensemble import RandomForestClassifier
# # 1. Create an untrained RandomForestClassifier
# model = RandomForestClassifier(n_estimators=100, random_state=42)

# # 3. Create a fake metrics dictionary (normally you'd get this after training)
# metrics = {
#     "accuracy": 13,   # None since we didn't train
#     "precision": 1,
#     "recall": 1
# }

# ex.compare_and_update_best(model ,metrics ,'accuracy','1','1')


# model=ex.load_best_model()
# print(model.get_params())

