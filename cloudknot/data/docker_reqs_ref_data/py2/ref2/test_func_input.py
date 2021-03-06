import boto3
import cloudpickle
import os
import pickle
from argparse import ArgumentParser
from functools import wraps


def pickle_to_s3(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        s3 = boto3.client("s3")
        bucket = os.environ.get("CLOUDKNOT_JOBS_S3_BUCKET")
        key = '/'.join([
            'cloudknot.jobs',
            os.environ.get("CLOUDKNOT_S3_JOBDEF_KEY"),
            os.environ.get("AWS_BATCH_JOB_ID"),
            '{0:3d}'.format(int(os.environ.get("AWS_BATCH_JOB_ATTEMPT"))),
            'output.pickle'
        ])
        pickled_result = cloudpickle.dumps(f(*args, **kwargs))
        s3.put_object(Bucket=bucket, Body=pickled_result, Key=key)

    return wrapper


@pickle_to_s3
def unit_testing_func(name=None, no_capitalize=False):
    """Test function for unit testing of cloudknot.DockerImage

    Import statements of various formats are deliberately scattered
    throughout the function to test the pipreqs components of
    clouknot.DockerImage
    """
    import sys  # noqa: F401
    import boto3.ec2  # noqa: F401
    if name:
        from docker import api  # noqa: F401
        from os.path import join  # noqa: F401

        if not no_capitalize:
            import pytest as pt  # noqa: F401
            import h5py.utils as h5utils  # noqa: F401

            name = name.title()

        return 'Hello {0}!'.format(name)

    from six import binary_type as bt  # noqa: F401
    from dask.base import curry as dbc  # noqa: F401

    return 'Hello world!'


if __name__ == "__main__":
    description = ('Download input from an S3 bucket and provide that input '
                   'to our function. On return put output in an S3 bucket.')

    parser = ArgumentParser(description=description)

    parser.add_argument(
        'bucket', metavar='bucket', type=str,
        help='The S3 bucket for pulling input and pushing output.'
    )

    parser.add_argument(
        '--starmap', action='store_true',
        help='Assume input has already been grouped into a single tuple.'
    )

    args = parser.parse_args()

    s3 = boto3.client('s3')
    bucket = args.bucket
    key = '/'.join([
        'cloudknot.jobs',
        os.environ.get("CLOUDKNOT_S3_JOBDEF_KEY"),
        os.environ.get("AWS_BATCH_JOB_ID"),
        'input.pickle'
    ])

    response = s3.get_object(Bucket=bucket, Key=key)
    input = pickle.loads(response.get('Body').read())

    if args.starmap:
        unit_testing_func(*input)
    else:
        unit_testing_func(input)
