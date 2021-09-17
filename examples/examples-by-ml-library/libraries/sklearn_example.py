from modelstore.model_store import ModelStore
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from libraries.util.datasets import load_diabetes_dataset
from libraries.util.domains import DIABETES_DOMAIN


def _train_example_model() -> Pipeline:
    X_train, X_test, y_train, y_test = load_diabetes_dataset()

    # Train a model using an sklearn pipeline
    params = {
        "n_estimators": 250,
        "max_depth": 4,
        "min_samples_split": 5,
        "learning_rate": 0.01,
        "loss": "ls",
    }
    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("regressor", GradientBoostingRegressor(**params)),
        ]
    )
    pipeline.fit(X_train, y_train)
    results = mean_squared_error(y_test, pipeline.predict(X_test))
    print(f"🔍  Trained model MSE={results}.")
    return pipeline


def train_and_upload(modelstore: ModelStore) -> dict:
    # Train a scikit-learn model
    model = _train_example_model()

    # Upload the model to the model store
    print(
        f'⤴️  Uploading the catboost model to the "{DIABETES_DOMAIN}" domain.'
    )
    meta_data = modelstore.upload(DIABETES_DOMAIN, model=model)
    return meta_data


def load_and_test(modelstore: ModelStore, model_id: str):
    # Load the model back into memory!
    print(
        f'⤵️  Loading the catboost "{DIABETES_DOMAIN}" domain model={model_id}'
    )
    model = modelstore.load(DIABETES_DOMAIN, model_id)

    # Run some example predictions
    _, X_test, _, y_test = load_diabetes_dataset()
    results = mean_squared_error(y_test, model.predict(X_test))
    print(f"🔍  Loaded model MSE={results}.")