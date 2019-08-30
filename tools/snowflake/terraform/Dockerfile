# Use an official Python runtime as a parent image
FROM python:3.7-stretch

#RUN mkdir /app

# Set the working directory to /app
WORKDIR /mnt/disks

# Copy the current directory contents into the container at /app
COPY . /mnt/disks

RUN git clone git@github.com:monobinab/professional-services.git

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r ../source/requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
#ENV NAME World

# Run app.py when the container launches
CMD ["python", "../source/main.py"]