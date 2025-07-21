import json, mlflow, tempfile, os, wandb, hydra, time
from omegaconf import DictConfig
from hydra.core.config_store import ConfigStore

_steps = [
    "download",
    "basic_cleaning",
    "data_check",
    "data_split",
    "train_random_forest",
    # NOTE: We do not include this in the steps so it is not run by mistake.
    # You first need to promote a model export to "prod" before you can run this,
    # then you need to run this step explicitly
#    "test_regression_model"
]

# This automatically reads in the configuration
@hydra.main(version_base=None, config_path=".", config_name="config")
def go(config: DictConfig):
    print("Starting continuous pipeline processing. Press Ctrl+C to stop.")
    
    while True:  # Continuous loop
        try:
            # Setup the wandb experiment. All runs will be grouped under this name
            os.environ["WANDB_PROJECT"] = config["main"]["project_name"]
            os.environ["WANDB_RUN_GROUP"] = config["main"]["experiment_name"]

            # Steps to execute
            steps_par = config['main']['steps']
            active_steps = steps_par.split(",") if steps_par != "all" else _steps

            print(f"\nStarting new pipeline run at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Move to a temporary directory
            with tempfile.TemporaryDirectory() as tmp_dir:
                if "download" in active_steps:
                    print("Executing download step...")
                    _ = mlflow.run(
                        "https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter.git#components/get_data",  #  FIXED
                        "main",  # FIXED - Added entry point
                        parameters={
                            "sample": config["etl"]["sample"],
                            "artifact_name": "sample.csv",
                            "artifact_type": "raw_data",
                            "artifact_description": "Raw_file_as_downloaded"
                        },
                        env_manager="conda"
                    )

                if "basic_cleaning" in active_steps:
                    print("Executing basic cleaning step...")
                    _ = mlflow.run(
                        "src/basic_cleaning",  # Use local path instead of GitHub URL
                        "main",
                        parameters={
                            "input_artifact": "sample.csv:latest",
                            "output_artifact": "clean_sample.csv",
                            "output_type": "clean_sample",
                            "output_description": "Data_with_outliers_and_null_values_removed",
                            "min_price": config['etl']['min_price'],
                            "max_price": config['etl']['max_price']
                        },
                        env_manager="conda"
                    )

                if "data_check" in active_steps:
                    print("Executing data check step...")
                    _ = mlflow.run(
                        "https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter.git#src/data_check",
                        "main",
                        parameters={
                            "csv": "clean_sample.csv:latest",
                            "ref": "clean_sample.csv:reference",
                            "kl_threshold": config['data_check']['kl_threshold'],
                            "min_price": config['etl']['min_price'],
                            "max_price": config['etl']['max_price']
                        },
                        env_manager="conda"
                    )

                if "data_split" in active_steps:
                    print("Executing data split step...")
                    _ = mlflow.run(
                        "https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter.git#components/train_val_test_split",
                        "main",
                        parameters={
                            "input": "clean_sample.csv:latest",
                            "test_size": config['modeling']['test_size'],
                            "random_seed": config['modeling']['random_seed'],
                            "stratify_by": config['modeling']['stratify_by']
                        },
                        env_manager="conda"
                    )

                if "train_random_forest" in active_steps:
                    print("Executing random forest training step...")
                    # NOTE: we need to serialize the random forest configuration into JSON
                    rf_config = os.path.abspath("rf_config.json")
                    with open(rf_config, "w+") as fp:
                        json.dump(dict(config["modeling"]["random_forest"].items()), fp)  # DO NOT TOUCH

                    _ = mlflow.run(
                        "src/train_random_forest",  #  FIXED - Use local version!
                        "main",
                        parameters={
                            "trainval_artifact": "trainval_data.csv:latest",
                            "val_size": config['modeling']['val_size'],
                            "random_seed": config['modeling']['random_seed'],
                            "stratify_by": config['modeling']['stratify_by'],
                            "rf_config": rf_config,
                            "max_tfidf_features": config['modeling']['max_tfidf_features'],
                            "output_artifact": "random_forest_export"
                        },
                        env_manager="conda"
                    )

                if "test_regression_model" in active_steps:
                    print("Executing model testing step...")
                    _ = mlflow.run(
                        "https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter.git#components/test_regression_model",  # ✅ Fixed path
                        "main",
                        parameters={
                            "mlflow_model": "random_forest_export:prod",
                            "test_dataset": "test_data.csv:latest"  # Will verify if this should be test_artifact
                        },
                        env_manager="conda"
                    )

            print(f"Pipeline run completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("Waiting for next run (60 minutes)...")
            # Wait for 60 minutes before the next run
            time.sleep(3600)  # 3600 seconds = 1 hour

        except KeyboardInterrupt:
            print("\nPipeline execution stopped by user.")
            break
        except Exception as e:
            print(f"\nError occurred: {str(e)}")
            print("Retrying in 5 minutes...")
            time.sleep(300)  # Wait 5 minutes before retrying

if __name__ == "__main__":
    go()

# Weigts and Bias = ce60b5cc9a6920374682b3535ee98207edf80e36