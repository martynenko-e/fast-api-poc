import os
import httpx


def read_files(path):
    # Get a list of all files and directories in the given path
    entries = os.listdir(path)

    for entry in entries:
        # Get the full path of the entry
        full_path = os.path.join(path, entry)

        if os.path.isdir(full_path):
            # If the entry is a directory, recursively call this function on it
            read_files(full_path)
        else:
            # If the entry is a file, read its contents and send it to the API
            if "__pycache__" in full_path or ".git" in full_path or "scripts" in full_path:
                continue
            with open(full_path, 'rb') as file:
                # print(full_path[4:])
                content = file.read()
                send_to_api(full_path[4:], content)


def send_to_api(full_path, content):
    username = 'yevm'
    token = os.environ.get("PA_TOKEN")
    host = 'www.pythonanywhere.com'

    files = {'content': content}

    with httpx.Client() as client:
        response = client.post(
            f'https://{host}/api/v0/user/{username}/files/path/home/{username}/fast_api_poc/{full_path}',
            files=files,
            headers={'Authorization': f'Token {token}'}
        )
        if response.status_code == 201:
            print(f'File {full_path} created')
        elif response.status_code == 200:
            print(f'File {full_path} updated')
        else:
            print(
                f'Got unexpected status code {response.status_code}: {response.content!r}')


# Call the read_files function with the path of the directory you want to read
read_files('./.')
