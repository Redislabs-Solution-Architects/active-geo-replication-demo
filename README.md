# Active Geo-replication demo
Active Geo-replication using a sample 'User Profile' application deployed in two different regions each pointing to their respective ACRE clusters.
The regions used here are:
1. Central India (Pune)
2. Southeast Asia (Singapore)


**Introduction** <br>

For the active geo replication demo, we will:
* Deploy 2 ACRE clusters one each in Central India and Southeast Asia. For this demo, I have used these Terraform scripts: https://github.com/bestarch/re-aa
* Deploy a sample user profile application built on Python, Flask, Bootstrap on Azure VMs in each of these regions. The application is present here: https://github.com/bestarch/user-profile

**Reference architecture**

The reference architecture looks something like this:

![A-A_ACRE_Demo drawio](https://user-images.githubusercontent.com/26322220/157703508-4d68d13a-bd40-4019-93a8-ad9900d621ad.png)



**Procedure** <br>
1. **Deployment of Redis Enterprise clusters with active geo-replication**: <br>
Create ACRE cluster with SKU E10, capacity can be anything. For this demo I have chosen 2. <br>
Deploy one cluster in Central India region and other in Southeast Asia region. You can achieve this either from Azure Portal, Azure Cli or Terraform scripts.<br> Terraform link is provided here https://github.com/bestarch/re-aa <br>

![image](https://user-images.githubusercontent.com/26322220/143982955-381f77b0-33db-4eb1-93df-8819192d7ae2.png)

Once complete, it looks something like this: <br>
![image](https://user-images.githubusercontent.com/26322220/157701062-7143bcba-5013-42fb-8fe3-87c06eeba2e0.png)


2. Test these clusters from your local environment so as to be sure everything is working as expected. You may use open source redis-cli or RedisInsight (Data visualization and monitoring tool from Redis

3. Note down the endpoint URL, Port (usually 10000 for ACRE) and primary key (password)

4. Next we will deploy the Python and Flask app to each of these regions. The idea is, each app should be connected to the cluster located in their respective region. Refer the architecture diagram above.

5. **Application Deployment**: <br>
For deploying our app, we will first spin-up two Azure VMs in each of the regions and install the needed softwares to run our apps.<br>
Following are the steps needed for this:

    a. Create a VM with following details:
    
        OS: Ubuntu 18.04 
        Region: Central India
        Size: Standard E2s v3 (2 vcpus, 16 GiB memory) 
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
        
    c.  Provision the sample user-profile application
    
        git clone https://github.com/bestarch/user-profile.git
        cd user-profile
        sudo apt install python3-flask
        sudo apt install python3-pip
        pip3 install -r requirements.txt
        
    d. Start the server
    
        cd user-profile
        export FLASK_APP=server.py
        export URL=<URL> # From step 3 above
        export PORT=<PORT> # From step 3 above
        export PASSWORD=<PASSWORD> # From step 3 above
        flask run -h 0.0.0.0

    e.  Repeat the above steps for another region "**Southeast Asia**"
    
    
For further reading on how to deploy python apps on Azure, please refer this link: https://docs.microsoft.com/en-us/azure-stack/user/azure-stack-dev-start-howto-vm-python?view=azs-2102
    
6. Now we have deployed the active-active cluster along with the 2 VMs in each region. The deployment looks something like this:
![image](https://user-images.githubusercontent.com/26322220/157700761-c992d6cf-b428-4ee7-8b57-df8113096c80.png)

Let's test this.

7. Open the browser and enter http://<PUBLIC_IP_OF_CENTRAL_INDIA_REGION>:5000
![image](https://user-images.githubusercontent.com/26322220/144080885-13372fa1-353a-42ca-9587-7f40eafc5843.png)

![image](https://user-images.githubusercontent.com/26322220/144081701-9dc03936-1343-4715-acb5-e6746b07dc0a.png)

8. **Testing** <br>
    Open http://<PUBLIC_IP_OF_CENTRAL_INDIA_REGION>:5000 and add details of a new user in the UI. 
    Now visit http://<PUBLIC_IP_OF_SOUTHEAST_ASIA_REGION>:5000, and check all the registered users.
    You should see the user added in Central India region. We can test this vice-versa as well by adding new user from Southeast asia region.
    
9. **Tear down** <br>
    Once the testing is done, tear down the ACRE clusters and the VMs in both the regions.


