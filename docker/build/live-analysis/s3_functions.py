def list_bucket_s3(bucket):
    logger.log(15, 'Listing s3 bucket: '+str(bucket))

    s3bucket = boto3.resource('s3')
    my_bucket = s3bucket.Bucket(bucket)
    files = []
    for object in my_bucket.objects.all():
        files.append(object.key)
        logger.log(15, str(object.key))
    return files