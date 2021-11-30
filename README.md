# Active Geo-replication demo
Active Geo-replication using ACRE and Python apps

**Introduction**
For the active geo replication demo, we will:
Deploy 2 ACRE clusters one each in Central India and South India, https://github.com/bestarch/re-aa
Deploy a sample user profile application built on Python, Flask, Bootstrap on VMs in each of these regions. https://github.com/bestarch/user-profile/tree/main

**Reference architecture**
The reference architecture looks something like this:

![active-active_demo drawio](https://user-images.githubusercontent.com/26322220/143983665-19d3bcd9-dc9d-4702-becc-0b705a3ad9d9.png)


**Procedure**
1. Create ACRE cluster with SKU E100, capacity can be anything. For this demo I have chosen 10. Deploy one cluster in Central India region and other deploy it in South India region. You may either do it from Azure Portal or do it using Azure Cli or Terraform. Terraform link is provided here https://github.com/bestarch/re-aa
![image](https://user-images.githubusercontent.com/26322220/143982955-381f77b0-33db-4eb1-93df-8819192d7ae2.png)

2. Test these clusters from your local environment so as to be sure everything is working as expected. You may use open source redis-cli or RedisInsight (Data visualization and monitoring tool from Redis(Company))

3. Note down the endpoint URL, Port (usually 10000 for ACRE) and primary key (password)

4. Next we will deploy the Python and Flask app to each of these regions. The idea is, each app should be connected to the cluster located at their respective regions. Refer the architecture diagram above.

5. For deploying our app, we will first spin-up two VMs in each of the regions and install the needed softwares to run our apps. Following are the steps needed for this:

    a. Create a VM with following details:
        OS: Ubuntu 18.04 
        Region: Central India
        Size: Standard D2s v3 (2 vcpus, 8 GiB memory)
        In the networking section, allow these ports: 22, 80,443, 5000 (custom port for Flask application)
        Enable public IP access
        Make everything else as default
        Note down the Public IP 
    b. Once the VM is up SSH into the terminal and execute these scripts:
        sudo apt-get update
        sudo apt-get -y install python3 python3-dev
        sudo apt install python3-pip
        sudo apt-get -y install nginx
        sudo apt-get -y install git
        git clone https://github.com/bestarch/user-profile.git
        cd user-profile

        sudo apt install python3-flask
        sudo apt install python3-pip
        pip3 install -r requirements.txt
        export FLASK_APP=server.py
        export URL=<URL> # From step 3 above
        export PORT=<PORT> # From step 3 above
        export PASSWORD=<Password> # From step 3 above
        flask run -h 0.0.0.0
    c.  Repeat the above steps for another region "South India"

6. Now we have deployed the active-active cluster along with the 2 VMs in each region. Let's test this.

7. Open the browser and enter http://<PUBLIC_IP_OF_CENTRAL_INDIA_REGION>:5000



