###############################################################################
# Dockerfile to build unit_testing_func application container
# Based on python 3
###############################################################################

# Use official python base image
FROM python:3

# Install python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Create a default user. Available via runtime flag `--user cloudknot-user`.
# Add user to "staff" group.
# Give user a home directory.
RUN useradd cloudknot-user \
    && addgroup cloudknot-user staff \
    && mkdir /home/cloudknot-user \
    && chown -R cloudknot-user:staff /home/cloudknot-user

ENV HOME /home/cloudknot-user

# Copy the python script
COPY unit_testing_func.py /home/cloudknot-user/

# Set working directory
WORKDIR /home/cloudknot-user

# Set entrypoint
ENTRYPOINT ["python", "/home/cloudknot-user/unit_testing_func.py"]
