## Project Links
- GitHub Repository: https://github.com/hammadwaheed1133/Project-Build-an-ML-Pipeline-Starter-03-07-25.git
- Weights & Biases Project: https://wandb.ai/hwahee2-western-governors-university/nyc_airbnb

## Project Status: COMPLETED ✓

This project has been successfully completed with a production-ready ML pipeline for NYC Airbnb price prediction.

### Final Results
- **Model Performance**: R² = 0.546, MAE = $34.40
- **Pipeline Status**: Fully operational end-to-end ML pipeline
- **Model Deployment**: Random Forest model with optimized hyperparameters
- **Data Validation**: Comprehensive data quality checks implemented
- **Experiment Tracking**: Full W&B integration for model versioning and artifact management

# Build an ML Pipeline for Short-Term Rental Prices in NYC

You are working for a property management company renting rooms and properties for short periods of 
time on various rental platforms. You need to estimate the typical price for a given property based 
on the price of similar properties. Your company receives new data in bulk every week. The model needs 
to be retrained with the same cadence, necessitating an end-to-end pipeline that can be reused.

This project implements a complete production-ready ML pipeline for this use case.

## Pipeline Architecture

The implemented pipeline includes the following components:

1. **Data Ingestion** (`download`): Automated data fetching from source
2. **Data Cleaning** (`basic_cleaning`): Outlier removal, data type conversion, geographic filtering
3. **Data Validation** (`data_check`): Comprehensive data quality tests including:
   - Row count validation
   - Price range verification
   - Column name validation
   - Geographic boundary checks
   - Statistical distribution comparisons
4. **Data Splitting** (`data_split`): Train/validation/test split with stratification
5. **Model Training** (`train_random_forest`): Random Forest model with optimized hyperparameters
6. **Model Testing** (`test_regression_model`): Production model evaluation on test set

## Optimized Model Configuration

The final model uses the following optimized hyperparameters:

```yaml
random_forest:
  n_estimators: 200
  max_depth: 10
  min_samples_split: 4
  min_samples_leaf: 3
  max_features: 0.5
  criterion: squared_error
  n_jobs: -1
  oob_score: true
```

## Table of contents

- [Preliminary steps](#preliminary-steps)
  * [Fork the Starter Kit](#fork-the-starter-kit)
  * [Create environment](#create-environment)
  * [Get API key for Weights and Biases](#get-api-key-for-weights-and-biases)
  * [The configuration](#the-configuration)
  * [Running the entire pipeline or just a selection of steps](#Running-the-entire-pipeline-or-just-a-selection-of-steps)
  * [Pre-existing components](#pre-existing-components)

## Preliminary steps

### Supported Operating Systems

This project is compatible with the following operating systems:

- **Ubuntu 22.04** (Jammy Jellyfish) - both Ubuntu installation and WSL (Windows Subsystem for Linux)
- **Ubuntu 24.04** - both Ubuntu installation and WSL (Windows Subsystem for Linux)
- **macOS** - compatible with recent macOS versions

Please ensure you are using one of the supported OS versions to avoid compatibility issues.

### Python Requirement

This project requires **Python 3.10**. Please ensure that you have Python 3.10 installed and set as the default version in your environment to avoid any runtime issues.

### Fork the Starter kit
Go to [https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter](https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter)
and click on `Fork` in the upper right corner. This will create a fork in your Github account, i.e., a copy of the
repository that is under your control. Now clone the repository locally so you can start working on it:

```
git clone https://github.com/[your github username]/Project-Build-an-ML-Pipeline-Starter.git
```

and go into the repository:

```
cd Project-Build-an-ML-Pipeline-Starter
```
Commit and push to the repository often while you make progress towards the solution. Remember 
to add meaningful commit messages.

### Create environment
Make sure to have conda installed and ready, then create a new environment using the ``environment.yaml``
file provided in the root of the repository and activate it:

```bash
> conda env create -f environment.yml
> conda activate nyc_airbnb_dev
```

### Get API key for Weights and Biases
Let's make sure we are logged in to Weights & Biases. Get your API key from W&B by going to 
[https://wandb.ai/authorize](https://wandb.ai/authorize) and click on the + icon (copy to clipboard), 
then paste your key into this command:

```bash
> wandb login [your API key]
```

You should see a message similar to:
```
wandb: Appending key for api.wandb.ai to your netrc file: /home/[your username]/.netrc
```

### The configuration
As usual, the parameters controlling the pipeline are defined in the ``config.yaml`` file defined in
the root of the starter kit. We will use Hydra to manage this configuration file. 
Open this file and get familiar with its content. Remember: this file is only read by the ``main.py`` script 
(i.e., the pipeline) and its content is
available with the ``go`` function in ``main.py`` as the ``config`` dictionary. For example,
the name of the project is contained in the ``project_name`` key under the ``main`` section in
the configuration file. It can be accessed from the ``go`` function as 
``config["main"]["project_name"]``.

NOTE: do NOT hardcode any parameter when writing the pipeline. All the parameters should be 
accessed from the configuration file.

### Running the entire pipeline or just a selection of steps

#### Full Pipeline Execution
To run the complete pipeline:

```bash
> mlflow run . -P steps=download,basic_cleaning,data_check,data_split,train_random_forest
```

#### Individual Step Execution
When developing it is useful to be able to run one step at the time. Say you want to run only
the ``download`` step:

```bash
> mlflow run . -P steps=download
```
If you want to run the ``download`` and the ``basic_cleaning`` steps:
```bash
> mlflow run . -P steps=download,basic_cleaning
```

#### Testing the Production Model
To test the production model (requires model to be promoted to 'prod' in W&B):

```bash
> mlflow run . -P steps=test_regression_model
```

#### Parameter Override
You can override any other parameter in the configuration file using the Hydra syntax:

```bash
> mlflow run . \
  -P steps=download,basic_cleaning \
  -P hydra_options="modeling.random_forest.n_estimators=10 etl.min_price=50"
```

### Pre-existing components
In order to simulate a real-world situation, we are providing you with some pre-implemented
re-usable components. While you have a copy in your fork, you will be using them from the original
repository by accessing them through their GitHub link, like:

```python
_ = mlflow.run(
                f"{config['main']['components_repository']}/get_data",
                "main",
                version='main',
                env_manager="conda",
                parameters={
                    "sample": config["etl"]["sample"],
                    "artifact_name": "sample.csv",
                    "artifact_type": "raw_data",
                    "artifact_description": "Raw file as downloaded"
                },
            )
```
where `config['main']['components_repository']` is set to 
[https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter/tree/main/components](https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter/tree/main/components).

Available components:
- `get_data`: downloads the data. [MLproject](https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter/blob/main/components/get_data/MLproject)
- `train_val_test_split`: segregate the data (splits the data) [MLproject](https://github.com/udacity/Project-Build-an-ML-Pipeline-Starter/blob/main/components/train_val_test_split/MLproject)
- `test_regression_model`: tests production model against test set

## Implementation Details

### Data Processing
- **Price filtering**: $10 - $350 range
- **Geographic filtering**: NYC boundaries (longitude: -74.25 to -73.50, latitude: 40.5 to 41.2)
- **Data validation**: Comprehensive test suite ensuring data quality
- **Feature engineering**: Date features, TF-IDF text processing

### Model Features
- **Preprocessing pipeline**: Handles categorical, numerical, and text features
- **Random Forest**: Optimized for price prediction task
- **Performance metrics**: R² score and Mean Absolute Error
- **Artifact management**: Model versioning with W&B

## In case of errors

### Environments
When you make an error writing your `conda.yml` file, you might end up with an environment for the pipeline or one
of the components that is corrupted. Most of the time `mlflow` realizes that and creates a new one every time you try
to fix the problem. However, sometimes this does not happen, especially if the problem was in the `pip` dependencies.
In that case, you might want to clean up all conda environments created by `mlflow` and try again. In order to do so,
you can get a list of the environments you are about to remove by executing:

```
> conda info --envs | grep mlflow | cut -f1 -d" "
```

If you are ok with that list, execute this command to clean them up:

**_NOTE_**: this will remove *ALL* the environments with a name starting with `mlflow`. Use at your own risk

```
> for e in $(conda info --envs | grep mlflow | cut -f1 -d" "); do conda uninstall --name $e --all -y;done
```

This will iterate over all the environments created by `mlflow` and remove them.

### MLflow & Wandb

If you see any error while running the command:

```
> mlflow run .
```

Please, make sure all steps are using **the same** python version and that you have **conda installed**. Additionally, *mlflow* and *wandb* packages are crucial and should have the same version.

## Project Structure

```
├── config.yaml                 # Pipeline configuration with optimized hyperparameters
├── main.py                     # Main pipeline orchestrator
├── environment.yml             # Conda environment specification
├── src/                        # Source code for pipeline steps
│   ├── basic_cleaning/         # Data cleaning step
│   ├── data_check/            # Data validation tests
│   └── train_random_forest/    # Model training step
└── components/                 # Reusable pipeline components
    ├── get_data/              # Data ingestion
    ├── train_val_test_split/  # Data splitting
    └── test_regression_model/ # Model testing
```

## License

[License](LICENSE.txt)