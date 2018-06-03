# Review Checker

List applicants that has not yet been reviewed by someone.

## Setup Enviornment Variables

```sh
export ASANA_TOKEN='your asana token'
export PROJECT_ID='your project id'
```

## Usage
```sh
python review_checker.py [-h] [-a] [-t] reviewer_name
```

- positional arguments:
    - reviewer_name      Name of target reviewer

- optional arguments:
    - -h, --help         show this help message and exit
    - -a, --audit        Check audit tasks
    - -t, --take-course  Check take course tasks

### Using pipenv

#### Setup
```sh
pipenv install
```

### Using pip
#### Setup
```sh
pip install -r requirements.txt
```

## Authors
[Lee-W](https://github.com/Lee-W)
