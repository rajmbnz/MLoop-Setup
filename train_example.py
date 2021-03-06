# Based on the official regression example:
# https://catboost.ai/docs/concepts/python-usages-examples.html#regression

import mlflow
from dotenv import load_dotenv
from catboost import CatBoostRegressor

load_dotenv()

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("kyle-test")

# Initialize data
train_data = [[1, 4, 5, 6], [4, 5, 6, 7], [30, 40, 50, 60]]
train_labels = [10, 20, 30]
eval_data = [[2, 4, 6, 8], [1, 4, 50, 60]]

# Initialize CatBoostRegressor
params = {
    "iterations": 2,
    "learning_rate": 1,
    "depth": 2,
    "allow_writing_files": False,
}
model = CatBoostRegressor(**params)

# Fit model
model.fit(train_data, train_labels)

# Log parameters and fitted model
with mlflow.start_run() as run:
    mlflow.log_params(params)
    mlflow.catboost.log_model(model, artifact_path="model")
    model_uri = mlflow.get_artifact_uri("model")

# Load model
loaded_model = mlflow.catboost.load_model(model_uri)

# Get predictions
preds = loaded_model.predict(eval_data)
print("predictions:", preds)