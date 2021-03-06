# Active Geo-replication demo
Active Geo-replication using User Profile application deployed in two different regions each pointing to their respective ACRE clusters.


**Introduction**

For the active geo replication demo, we will:
* Deploy 2 ACRE clusters one each in East US and Central US. For this demo, I have used these Terraform scripts: https://github.com/Redislabs-Solution-Architects/re-aa
* Deploy a sample user profile application built on Python, Flask, Bootstrap on VMs in each of these regions. The application is present in this repo.

**Reference architecture**

The reference architecture looks something like this:

![active-active_demo drawio](https://user-images.githubusercontent.com/26322220/144104403-a4b1cc7f-9bcb-4a5c-aebb-311240a5105f.png)


**Procedure**
1. **Deployment of Redis Enterprise clusters with active geo-replication**: Create ACRE cluster with SKU E100, capacity can be anything. For this demo I have chosen 10. Deploy one cluster in East US region and other deploy it in Central US region. You may either do it from Azure Portal or do it using Azure Cli or Terraform. Terraform link is provided here https://github.com/Redislabs-Solution-Architects/re-aa
![image](https://user-images.githubusercontent.com/26322220/143982955-381f77b0-33db-4eb1-93df-8819192d7ae2.png)
Once complete, it looks something like this:
![image](https://user-images.githubusercontent.com/26322220/144082884-6ebeb6fa-8d9b-4470-ae68-56a41a09579e.png)


2. Test these clusters from your local environment so as to be sure everything is working as expected. You may use open source redis-cli or RedisInsight (Data visualization and monitoring tool from Redis(Company))

3. Note down the endpoint URL, Port (usually 10000 for ACRE) and primary key (password)

4. Next we will deploy the Python and Flask app to each of these regions. The idea is, each app should be connected to the cluster located at their respective regions. Refer the architecture diagram above.

5. **Application Deployment**: For deploying our app, we will first spin-up two VMs in each of the regions and install the needed softwares to run our apps. Following are the steps needed for this:

    a. Create a VM with following details:
        OS: Ubuntu 18.04 
        Region: East US
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
        git clone https://github.com/Redislabs-Solution-Architects/active-geo-replication-demo.git
        cd user-profile

        sudo apt install python3-flask
        sudo apt install python3-pip
        pip3 install -r requirements.txt
        export FLASK_APP=server.py
        export URL=<URL> # From step 3 above
        export PORT=<PORT> # From step 3 above
        export PASSWORD=<PASSWORD> # From step 3 above
        flask run -h 0.0.0.0

    c.  Repeat the above steps for another region "Central US"
    
    For further reading on how to deploy python apps on Azure, please refer this link: https://docs.microsoft.com/en-us/azure-stack/user/azure-stack-dev-start-howto-vm-python?view=azs-2102
    
6. Now we have deployed the active-active cluster along with the 2 VMs in each region. The deployment looks something like this:
![image](https://user-images.githubusercontent.com/26322220/144066272-4628370d-ba1d-4567-a1be-ceb1436e547f.png)
Let's test this.

7. Open the browser and enter http://<PUBLIC_IP_OF_EAST_US_REGION>:5000
![image](https://user-images.githubusercontent.com/26322220/144080885-13372fa1-353a-42ca-9587-7f40eafc5843.png)

![image](https://user-images.githubusercontent.com/26322220/144081701-9dc03936-1343-4715-acb5-e6746b07dc0a.png)

8. **Testing**: 
Open http://<PUBLIC_IP_OF_EAST_US_REGION>:5000, enter the details of the new user. 
Now visit  http://<PUBLIC_IP_OF_CENTRAL_US_REGION>:5000, and check all the registered users.
You should see the user added in East US region. 
We can test this vice-versa as well by adding new user from central region.



