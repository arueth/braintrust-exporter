#!/usr/bin/env python

import io
import json
import logging
import os
import pprint

import braintrust
import pandas as pd
import requests

API_URL = "https://api.braintrust.dev/v1"
BRAINTRUST_API_KEY = os.environ.get("BRAINTRUST_API_KEY")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "./braintrust_exports")
PROJECT_NAME = os.environ.get("PROJECT_NAME")
PROJECT_NAME_DIRECTORY = PROJECT_NAME.replace(" ", "-").lower()


auth_header = {"Authorization": f"Bearer {BRAINTRUST_API_KEY}"}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)


def export_experiments(project: dict[str, str]):
    """
    Fetches all experiments in a project and saves them as CSV files.
    """
    logger.info("Listing experiments for project '%s'", project["name"])

    experiments_response = requests.get(
        headers=auth_header,
        timeout=30,
        url=f"{API_URL}/experiment?project_name={project['name']}",
    )
    logger.debug(experiments_response)
    experiments_response.raise_for_status()

    experiments = experiments_response.json()["objects"]
    logger.debug(experiments)

    for experiment in experiments:
        logger.info("Exporting experiment: '%s'", experiment["name"])
        experiment_name_file = experiment["name"].replace(" ", "-").lower()
        try:
            logger.debug(experiment)
            current_experiment_response = requests.get(
                headers=auth_header,
                timeout=30,
                url=f"{API_URL}/experiment/{experiment['id']}/fetch",
            )
            logger.debug(current_experiment_response)
            current_experiment_response.raise_for_status()

            current_experiment = current_experiment_response.json()
            logger.debug(current_experiment)

            experiment_df = pd.read_json(io.StringIO(current_experiment_response.text))
            logger.debug(experiment_df)

            experiment_events_df = pd.DataFrame.from_records(experiment_df["events"])
            logger.debug(experiment_events_df)
            if len(experiment_events_df) > 0:
                experiment_events_df.drop(
                    axis=1,
                    columns=[
                        "_pagination_key",
                        "_xact_id",
                    ],
                    inplace=True,
                )
            logger.debug(experiment_events_df)

            with open(
                encoding="utf-8",
                file=f"{OUTPUT_DIR}/{PROJECT_NAME_DIRECTORY}/experiment_{experiment_name_file}.cvs",
                mode="w",
            ) as file:
                file.write(experiment_events_df.to_csv(index=False))
        except Exception as e:
            logger.error("Error exporting experiment '%s': %s", experiment["name"], e)
            raise e


def export_datasets(project: dict[str, str]):
    """
    Fetches all datasets in a project and saves them as CSV files.
    """
    logger.info("Listing datasets for project '%s'", project["name"])

    datasets_response = requests.get(
        headers=auth_header,
        timeout=30,
        url=f"{API_URL}/dataset?project_name={project['name']}",
    )
    logger.debug(datasets_response)
    datasets_response.raise_for_status()

    datasets = datasets_response.json()["objects"]
    logger.debug(datasets)

    for dataset in datasets:
        logger.info("Exporting dataset: '%s'", dataset["name"])
        dataset_name_file = dataset["name"].replace(" ", "-").lower()
        try:
            logger.debug(dataset)
            current_dataset_response = requests.get(
                headers=auth_header,
                timeout=30,
                url=f"{API_URL}/dataset/{dataset['id']}/fetch",
            )
            logger.debug(current_dataset_response)
            current_dataset_response.raise_for_status()

            current_dataset = current_dataset_response.json()
            logger.debug(current_dataset)

            dataset_events_df = pd.DataFrame.from_records(current_dataset["events"])
            logger.debug(dataset_events_df)
            if len(dataset_events_df) > 0:
                dataset_events_df.drop(
                    axis=1,
                    columns=[
                        "_pagination_key",
                        "_xact_id",
                    ],
                    inplace=True,
                )
            logger.debug(dataset_events_df)

            dataset_df = pd.read_json(io.StringIO(current_dataset_response.text))

            with open(
                encoding="utf-8",
                file=f"{OUTPUT_DIR}/{PROJECT_NAME_DIRECTORY}/dataset_{dataset_name_file}.cvs",
                mode="w",
            ) as file:
                file.write(dataset_events_df.to_csv(index=False))
        except Exception as e:
            logger.error("Error exporting dataset %s: %s", dataset, e)
            raise e


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # braintrust.login(api_key=BRAINTRUST_API_KEY)

    logger.info(
        "Export experiments and datasets from project '%s'(%s) to %s",
        PROJECT_NAME,
        PROJECT_NAME_DIRECTORY,
        OUTPUT_DIR,
    )

    try:
        logger.info("Searching for project '%s'", PROJECT_NAME)
        project_response = requests.get(
            headers=auth_header,
            timeout=30,
            url=f"{API_URL}/project?project_name={PROJECT_NAME}",
        )
        project_response.raise_for_status()
        project = project_response.json()["objects"][0]
        os.makedirs(f"{OUTPUT_DIR}/{PROJECT_NAME_DIRECTORY}", exist_ok=True)
    except IndexError as e:
        logger.error("Project '%s' was not found.", PROJECT_NAME)
        exit(1)
    except Exception as e:
        logger.error("An error occurred: %s", e)
        raise e

    export_experiments(project)
    export_datasets(project)

    logger.info(
        "Export to %s/%s complete",
        OUTPUT_DIR,
        PROJECT_NAME_DIRECTORY,
    )
