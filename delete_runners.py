import requests
import argparse

def get_runners(gitlab_url, project_id, headers):
    runners = []
    page = 1
    per_page = 100
    while True:
        url = f"{gitlab_url}/api/v4/projects/{project_id}/runners?page={page}&per_page={per_page}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        runners.extend(data)
        page += 1
    return runners

def remove_runner(gitlab_url, runner_id, headers):
    url = f"{gitlab_url}/api/v4/runners/{runner_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 403:
        print(f"Permission denied to remove runner ID: {runner_id}. Response: {response.text}")
        return False
    response.raise_for_status()
    return response.status_code == 204

def main():
    parser = argparse.ArgumentParser(description="Delete all inactive or offline GitLab runners in a specific project.")
    parser.add_argument("token", help="GitLab personal access token")
    parser.add_argument("-g", "--group", type=int, required=True, help="Group ID")
    parser.add_argument("-p", "--project", type=int, required=True, help="Project ID")
    parser.add_argument("--no-act", action="store_true", help="Dry run, show all inactive or offline runners")
    parser.add_argument("--gitlab", required=True, help="GitLab URL")
    
    args = parser.parse_args()
    
    headers = {"PRIVATE-TOKEN": args.token}
    runners = get_runners(args.gitlab, args.project, headers)
    
    inactive_runners = [runner for runner in runners if runner['status'] in ['offline', 'paused']]
    
    if args.no_act:
        print("Dry run mode. The following inactive or offline runners would be deleted:")
        for runner in inactive_runners:
            print(f"Runner ID: {runner['id']}, Description: {runner['description']}, Status: {runner['status']}")
    else:
        for runner in inactive_runners:
            if remove_runner(args.gitlab, runner['id'], headers):
                print(f"Removed runner ID: {runner['id']}, Description: {runner['description']}, Status: {runner['status']}")
            else:
                print(f"Failed to remove runner ID: {runner['id']}, Description: {runner['description']}, Status: {runner['status']}")

if __name__ == "__main__":
    main()