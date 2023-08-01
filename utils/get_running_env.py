import boto3
from datetime import datetime
from settings import AWS_ACCESS_KEY, AWS_SECRET, AWS_SECRET_CONNECTED, AWS_ACCESS_KEY_CONNECTED


class AWS_ACCOUNTS:
    DEV = 'dev'
    CONNECTED = 'connected'


def get_running_custom_envs(account=AWS_ACCOUNTS.DEV):
    # if account == AWS_ACCOUNTS.CONNECTED:
    #     aws_key = AWS_ACCESS_KEY_CONNECTED
    #     aws_secret = AWS_SECRET_CONNECTED
    # else:
    #     aws_key = AWS_ACCESS_KEY
    #     aws_secret = AWS_SECRET
    #
    # running_instances = []
    # session = boto3.Session(region_name="us-west-2")
    # ec2 = session.resource(
    #     'ec2',
    #     aws_access_key_id=aws_key,
    #     aws_secret_access_key=aws_secret, verify=False
    # )
    # instances = ec2.instances.filter(
    #     Filters=[{'Name': 'tag:method', 'Values': ['automation']}])
    # for instance in instances:
    #     instance_details = {}
    #     instance_details["Name"] = filter_tag(instance.tags, "Name")
    #     instance_details["Instance"] = instance.id
    #     instance_details["Type"] = instance.instance_type
    #     instance_details["LaunchTime"] = datetime.strftime(instance.launch_time, "%Y-%m-%d %H:%M:%S")
    #     instance_details["State"] = instance.state["Name"]
    #     instance_details["Owner"] = filter_tag(instance.tags, "instance_owner")
    #     running_instances.append(instance_details)
    # # calculate up time
    # for instance in running_instances:
    #     a = datetime.fromisoformat(instance["LaunchTime"]).replace(tzinfo=None)
    #     b = datetime.now()
    #     diff = b - a
    #     instance["Running since (days)"] = int(diff.days)
    return [{
        "Name":"a",
        "Instance":"b",
        "Type":"c",
        "LaunchTime":"d",
        "State":"e",
        "Owner":"f",
        "Running since (days)":2


    },
        {
            "Name": "a",
            "Instance": "b",
            "Type": "c",
            "LaunchTime": "d",
            "State": "e",
            "Owner": "f",
            "Running since (days)": 3

        },
        {
            "Name": "a",
            "Instance": "b",
            "Type": "c",
            "LaunchTime": "d",
            "State": "e",
            "Owner": "f",
            "Running since (days)":4

        },
        {
            "Name": "a",
            "Instance": "b",
            "Type": "c",
            "LaunchTime": "d",
            "State": "e",
            "Owner": "f",
            "Running since (days)": 5

        }
    ]


def filter_tag(tag_list, key):
    for tag in tag_list:
        if tag["Key"] == key:
            return tag["Value"]


if __name__ == "__main__":
    result = get_running_custom_envs()
    print(result)
