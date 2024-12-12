# Delete Offline GitLab Runners

This script deletes all the offline GitLab runners that are created by the Kubernetes executor for a project in GitLab.

## Installation

Install the required dependencies:

    pip install -r requirements.txt

## Generate a Project Access Token
Generate a Project Access Token with api scope from the repository settings:

Navigate to GitLab -> Project Repository -> Settings -> Access Tokens.
Create a new token with api scope.

## Usage
    List all runners for a project

        python delete_runners.py <access_token> -g <group_id> -p <project_id> --no-act --gitlab <gitlab_url>

    Delete all runners for a project

        python delete_runners.py <access_token> -g <group_id> -p <project_id> --gitlab <gitlab_url>