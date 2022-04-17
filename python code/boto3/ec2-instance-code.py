#imports required resources 
import boto3

# low-level client represents the ec2 with region set to virginia USA
client = boto3.client('ec2', region_name='us-east-1')

# launches instances with specified details
response = client.run_instances(
   # Defines ESB volumes
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {

                'DeleteOnTermination': True,
                'VolumeSize': 8,
                'VolumeType': 'gp2'
            },
        },
    ],
    # The id which is required for the instace to launch
    ImageId='ami-0c02fb55956c7d316',
    # Determines the performance and can effect cost of running the instance. 
    InstanceType='t3.micro',
    MaxCount=1,
    MinCount=1,
    
    KeyName = 'vockey',
    Monitoring={
        'Enabled': False
    },
)