#import required resources
import boto3 
import time 
s3= boto3.client('s3') 
#uploads the specified image to the specified s3 bucket. 
s3.upload_file('image1.jpg','my-bucket2024472','image1.jpg')
#causes the uploading process to stop for 30 seconds
time.sleep(30) 
s3.upload_file('image2.png','my-bucket2024472','image2.png') 
time.sleep(30) 
s3.upload_file('image3.jpg','my-bucket2024472','image3.jpg') 
time.sleep(30)
s3.upload_file('image4.jpg','my-bucket2024472','image4.jpg') 
time.sleep(30)
s3.upload_file('image5.jpg','my-bucket2024472','image5.jpg')