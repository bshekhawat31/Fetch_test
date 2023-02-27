# Fetch_test
# Pre requisites:
-Docker
-Python
-Postgresql
-AWScli Local

# Language used: Python

# Steps to run the code:
-Download the project in your local computer
-Assuming the executor has all the pre requistes, read the docker images given in the test doc into your docker
-Run ```docker-compose up``` command in your terminal from the path where the code is downloaded
-Then again in your terminal run ```python test.py``` command to run the main code file(where the logic to read the queue messages sits)
-Using your terminal again run ```psql``` and the postgres terminal will open
-Run ```Select * from user_logins``` to view the inserted data 

# About the files in this project:
docker-compose.yml::
-- This is a config file where the configurations for SQS and Postgres are defined

test.py::
-We establish connection with postgres using 'pycopg2' and connection to SQS is established using boto3 in python
-The JSON data containing user login behavior from an AWS SQS Queue, that is made available via a custom localstack image that has the data pre loaded is first read and then inserted into Postgres
- recieve_message and delete_message are used to read and delete incomming data from SQS queue

# Next Steps:
- The code architecture can be imporved to handle multiple consumers. Currently it caters to only one Consumer
- Analytics for individual operations can be performed to provide latency, throughput etc
- More secure cryptographic encrytions could be used to mask the data more securely
- If time had permitted we could have tested the usability on a actual server

# Answers to the test Questions:
Q1. -We would first need to do Q/A testing for this application to make sure this is fit to be deployed into production.
-We would then need a automation deployment software like Jenkins/Codefresh etc and create a CI/CD pipeline to connect github repository(where the code sits) to production servers. 
-We would have to make endpoint connections from our application to the production server in a .yml file(if using cloud services) which will be used for deployment
-Then use the CI/CD pipeline to test the code in lower production levels and then deploy it to production server
- Maintain and troubleshoot if needed

Q2. - We can  created splunk dasboards to monitor the software application(success calls, error calls etc) and store log file which will help in trouble         shooting
   - We can have other dashboards like in new relic to monitor traffic, infrastructure health etc
   - There should be proper logging done in the code dso that it can be used to create and store log files which will help in troubleshooting

Q3. - To tackle growing datasets we can have two ways: one, we can use sharding to partition the database onto multiple servers or second, We can have a primary and a secondary database on a single server(if DB size is to business needs) and run timely replication batch files to make sure data on both DBs is always same. The Primary DB will be the real time customer using Db and will have data only upto a certain time and after that it will be truncated. The secondary DB will have archival data until legal policy rules demand and the size of this will be bigger than the primary DB.  
 - Serveral instances of this applications can be deployed on multiple severs. We can always have a primary and a secondary server as a backup.
 - A load balancer can be used to distribute the load of the grwoing dataset across multiple servers.

Q4. I have used base64 encoding to mask the data so to recover it we can use base64 decoding method.
Q5. -For the DB attribute app_version we assumed that the hard business rule is to store it as a integer and therefore we had to change to format of the version number to store it as a int in the database. If we had to store the version number as it looks then we could have stored it as string to accomodate the '.' 
