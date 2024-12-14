# 3-Tier-VPC-AWS
This is a repo to build a 3-tier-WebApp in VPC on AWS

This guide will walk you through the process of creating a 3-tier Virtual Private Cloud (VPC) in Amazon Web Services (AWS) and This project demonstrates the deployment and hosting of a web application on AWS, utilizing various services and components to ensure high availability, scalability, security, and fault tolerance.


# ARCHITECTURE :
![image](https://github.com/user-attachments/assets/8e8007a3-5557-4ba2-b86e-6d18593d94d0)



This diagram shows the key components of our setup, including:

  Public and Private subnets across two Availability Zones
  Internet Gateway for public internet access
  NAT Gateways for outbound internet access from private subnets
  Application Load Balancer in the public subnets
  EC2 instances in each tier
  RDS instance in the private subnet

As we progress through this guide, we'll set up each of these components step by step.

## Table of Contents
1. [Overview of a 3-Tier](#overview)









# Overview of a 3-Tier Architecture <a name="overview"></a>
when the user wants to access any application, it needs the UI to interact, User Interface is called as presentation layer. Once the user started accessing the UI, application needs to respond to the user according to the business need. So the Business logic operations happens at business layer. Finally, application needs some kind of persistent storage to interact with user, This layer is called as data layer.

Three Layers are
  Presentation Layer [UI]
  Business Layer [Business logic]
  Data Layer [Data]

**Why we need three tier application ?**
  If you look at the above points, we are separating the application into multiple layer which helps to scale and secure independently and main modularity . These layers are physically separated, with each running on its own infrastructure.

  The architecture presented in this article is one of many possible ways to design a three-tier system and is specifically tailored to meet the goals of availability, security, scalability, and performance.
    
  In this article, We will build Secure, Scalable and Resilient 3-tiered Web application in AWS Cloud.


Let's Start building it!

**Why we need it ?**
AWS by default provides the default VPC, but if you are creating the resources or running your workload in default VPC, your application might get access to external world and it's not safe to build the application in default VPC.

In order to protect your resources, you will be building your own network space in cloud and you will be having the control such as inbound and outbound traffic for the VPC.


# VPC COMPONENTS:
what is subnets ?
Subnet is network portion in your VPC, just think VPC is the full pizza and subnet is one slice of complete pizza.

![image](https://github.com/user-attachments/assets/ba3b1e08-4c4d-4d16-8639-1549b96be3de)


**why we need subnet ?**
  We can create the network portion in VPC such as private and public subnets and we can set the rules such as only the resources in the public subnet can access the internet and resources in private subnet shouldn't access it.
  
**Internet gateway : [IGW]**
  It is the one of the AWS component in VPC, with the help of IGW, your VPC can access to the internet. So, without creating and attaching the IGW to VPC, your VPC can't access to the internet world.
  
**NAT Gateway : [NAT GW]**
  It is the one of the AWS component in VPC. NAT GW helps private instance resources to talk to internet. For Ex., Your private instances need to get the patch, in this case your private resources will talk with internet via NAT gateway. NAT Gateway will be present in Public subnet and acts as a proxy for your private instances.
  
**CREATE VPC :**
  As this article is quite big to follow up, I have created the VPC and its component in the other article which is mentioned below. Please refer the below mentioned article and come back here to create the Security groups.

https://medium.com/@tojanasg/aws-build-a-secure-scalable-and-resilient-3-tier-web-application-c763a2a3ebb6

## Security Groups Configuration:**
Security Groups are virtual firewalls for controlling inbound and outbound traffic for your EC2 instances.

1. **Web Server-SG (for the Web Server):**

1.Navigate to Security Groups in the VPC Dashboard.
2.Click Create Security Group.
3.Name: WebServer-SG.

**Inbound Rules:**

  HTTP (80): Allow from 0.0.0.0/0 (or your IP range).
  HTTPS (443): Allow from 0.0.0.0/0.
  SSH (22): Allow from your IP address only (to enable EC2 Instance Connect).
  
**Outbound Rules: Allow all traffic (default).**
  Attach this security group to your EC2 Web Server instance later.

2. **AppServer-SG (for the Application Server):**
Repeat the process for another security group.
Name: AppServer-SG.

Inbound Rules:
  Allow HTTP (port 5000 or custom app port) traffic from WebServer-SG.
  Outbound Rules: Allow all traffic.

**3. Database-SG (for RDS):**
Create a new security group named Database-SG.

**Inbound Rules:**
  MySQL/Aurora (3306): Allow traffic only from AppServer-SG.
  Outbound Rules: Allow all traffic (default).

**Outcome**
  A VPC with the following configuration:
  Public Subnet: Hosts your Web Server.
  Private Subnet: Hosts your App Server and RDS.

**If you have noticed, we have created the security group chaining, Security group of App Server only allows traffic from webserver. SG of Database will allow traffic from App Server. So, Here we are creating the secured network between subnets.**

--------------------------------------------------------------------------------

## Phase 2: Launch the Web Server
  In this phase, we will launch an EC2 instance for the web server in the public subnet created in Phase 1. The web server will serve as the front end of the e-commerce platform.
Step-by-Step Process

**1. Launch an EC2 Instance**
  2.Go to the EC2 Dashboard in the AWS Management Console.
  3. Click Launch Instance.
  4. Choose an Amazon Machine Image (AMI):
  5. Select Amazon Linux 2023 (free tier eligible).
  6.Choose an Instance Type:
  7.Select t2.micro (free tier eligible).
  8.Configure the Network Settings:
  9.Select the VPC you created earlier (e.g., ECommerce-VPC).
  10.Select a Public Subnet (e.g., 10.0.1.0/24).
  11. Ensure Auto-assign Public IP is enabled.


![image](https://github.com/user-attachments/assets/0d95bea1-8a1d-444e-8d95-0cf41a43f16d)

**2. Attach a Security Group:**
  Select the WebServer-SG created in Phase 1.

  ![image](https://github.com/user-attachments/assets/b33c6568-652a-4d13-a25c-f73517dba536)

**3. Add Storage:**
  Use the default root volume (e.g., 8 GiB of General Purpose SSD).

**4. Add Tags:**
  Key: Name, Value: WebServer.

**Click Launch Instance.**

![image](https://github.com/user-attachments/assets/c1a4c64f-3dd0-4e63-8794-15c66ec30e83)


# 2. Access the Instance
  1.Go to the Instances section in the EC2 Dashboard.
  2.Locate your Web Server instance.
  3.Click Connect.
  4. Under EC2 Instance Connect, click Connect to access the instance terminal.

  ![image](https://github.com/user-attachments/assets/4b6c8c1b-c60d-40f5-8017-70582ddb3e1a)

# 3. Install a Web Server
Run the following commands in the EC2 terminal to update the instance and install Apache:

![image](https://github.com/user-attachments/assets/864a1d46-7c3e-4239-a10e-36a6b4ba59fa)

# 4. Add a Test Web Page
Create a simple test web page:

**echo "Welcome to the E-Commerce Platform Web Server" | sudo tee /var/www/html/index.html**

![image](https://github.com/user-attachments/assets/85a4aff5-ddac-4d9b-a7df-9eaea36843dc)


# 5. Test the Web Server
  Copy the Public IP Address of your EC2 instance from the EC2 Dashboard.
  Open a web browser and paste the Public IP. You should see the message:

    **Welcome to the E-Commerce Platform Web Server**

    ![image](https://github.com/user-attachments/assets/f41da71b-91c1-48f2-8bcd-fae0ebabde6a)

--------------------------------------------------------------------------------

## Phase 3: Deploy Application Logic (App Server)
  In this phase, we will launch an EC2 instance in the private subnet created in Phase 1 to host the application logic. This Application Server will process user requests and communicate with the Database layer.

  Follow the same procedure for creating the instance but make sure of selecting the private subnet in network settings
    1. Configure the Network Settings:
    2. Select the VPC you created earlier (e.g., ECommerce-VPC).
    3. Select a Private Subnet (e.g., 10.0.2.0/24).
    4. Disable Auto-assign Public IP (since this is a private instance).

    ![image](https://github.com/user-attachments/assets/b2665b2f-3d7d-4d49-a3ff-ebbf8bc58f75)


# 2. Access the Instance Using EC2 Instance Connect
    1. Go to the Instances section in the EC2 Dashboard.
    2. Locate your App Server instance.
    3. Since it's in a private subnet, create a temporary SSH tunnel via the Web Server:
    
    4. Open the Web Server's EC2 Instance Connect and log in.
    5. From the Web Server's terminal, connect to the private App Server using its private IP address:
          bash Copy code
          ssh ec2-user@<Private-IP-of-AppServer>
          Replace <Private-IP-of-AppServer> with the App Server's private IP (visible in the EC2 Dashboard).

--------------------------------------------------------------------------------

  ## Phase 3: Install Application Dependencies
    **1. **Web Server Setup****

Once connected to the WebServer: Run the below script to install and run webserver.
            **sudo yum update -y
            sudo yum install -y httpd
            sudo systemctl start httpd
            sudo systemctl enable httpd
            echo "<h1>Welcome to the E-Commerce Platform - Web Server</h1>" | sudo tee /var/www/html/index.html**

  **2. App Server setup:**
Run the command for installing the dependencies of php and mysql in the App server
            **sudo yum update -y
            sudo yum install -y php php-mysqlnd**


          ![image](https://github.com/user-attachments/assets/347f407e-1150-4d1d-b071-ba9bd1dd13ab)
          
--------------------------------------------------------------------------------

## Phase 4: Setting Up the Database with RDS
  In this phase, we will set up an Amazon RDS (MySQL) instance for the backend database to store product details, user data, and order details.
Launch an RDS Instance:
    1. Navigate to the RDS Dashboard.
    2. Click Create database.
    3. Choose Standard Create.
    4. Database Engine: Select MySQL.
    5. Version: Choose the latest available MySQL version.
    6. Templates: Select Free Tier.
    7. Instance Configuration:

   ** DB instance identifier: EcommerceDB.
    Master username: admin.
    Master password: Set and confirm a strong password (e.g., Admin1234!)**

    8.DB Instance Size: Choose db.t2.micro (Free Tier eligible).
    9.Allocated storage: Leave at the default (20 GiB).

**3. Connectivity:**
    VPC: Select EcommerceVPC.
    Subnet group: Leave the default.
    Public access: No (RDS should not be directly accessible from the internet).
    VPC security group: Choose an existing group or create a new one:
    Name the security group RDS-SG.
    Add Inbound Rules:
    MySQL/Aurora, Port 3306, Source: AppServerSG.

Leave other settings as default and click Create database.
Verify Database Status:

Go to Databases and ensure the status is Available.

![image](https://github.com/user-attachments/assets/66e95989-e7f4-4cc1-86ae-32fa68917b26)

![image](https://github.com/user-attachments/assets/42612c7e-0713-42bd-b2e9-4d0a6f8b5a9b)


## Connect App Server to RDS:
    1. Connect to the App server instance using SSH, and run the below command to install MYSQL Client in App server and connect to it

 **sudo dnf update -y
 sudo dnf install mariadb105**
    2. Connect to the MySQL DB instance. For example, enter the following command. This action lets you connect to the MySQL DB instance using the MySQL client.

Substitute the DB instance endpoint (DNS name) for endpoint, and substitute the master username that you used for admin. Provide the master password that you used when prompted for a password.
  **mysql -h endpoint -P 3306 -u admin -p**

  ![image](https://github.com/user-attachments/assets/67ca4757-4dff-4833-9ca1-d0eeb0ef109f)


# 3. Set Up the Database Schema:
Once connected to the RDS database, create tables by executing the below SQL script
    **CREATE DATABASE EcommerceDB;
    USE EcommerceDB;
    CREATE TABLE Products (
     ProductID INT AUTO_INCREMENT PRIMARY KEY,
     Name VARCHAR(255) NOT NULL,
     Description TEXT,
     Price DECIMAL(10, 2) NOT NULL
    );
    CREATE TABLE Users (
     UserID INT AUTO_INCREMENT PRIMARY KEY,
     Name VARCHAR(255) NOT NULL,
     Email VARCHAR(255) UNIQUE NOT NULL,
     Password VARCHAR(255) NOT NULL
    );
    CREATE TABLE Orders (
     OrderID INT AUTO_INCREMENT PRIMARY KEY,
     UserID INT,
     TotalAmount DECIMAL(10, 2),
     OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );**

Once Executed, confirm whether the table is created or not.

![image](https://github.com/user-attachments/assets/3d5b7003-dce1-469c-bbbc-7a08066e16ee)

--------------------------------------------------------------------------------

## Phase 7: Adding Scalability with Load Balancer
1. Create the Application Load balancer and target it to the Web server for the scalability and route traffic across AZs 
2. Create the Security Group which allows all traffic as inbound.
3. Create the Target group ans target to the web server group.

 ![image](https://github.com/user-attachments/assets/2cb35429-a3b3-4bfc-b0fd-05b88c2d58d5)
 ![image](https://github.com/user-attachments/assets/98d69797-51bc-40d9-b7da-547d347d92c6)

![image](https://github.com/user-attachments/assets/27973c87-3603-4323-bc70-024562aabf63)

--------------------------------------------------------------------------------

## Phase 8 :Insert Data into RDS from App Server and Enable Web Server to Call the App Server
  Log in to the App Server using EC2 Instance Connect.
  Install Required Software:

  **Please refer app.py code for the code snippet**

  3. Start the Flask App:
      Run the below command

     **python3 app.py**

     The application will now listen on port 5000 of the App Server.

     ![image](https://github.com/user-attachments/assets/7d358dfa-d4d1-446e-9498-13462b32d265)

# Test the App Server API:
  1. Insert the data to RDS DB using POSTMAN
  2. POST to add a new product
       URL: http://<App-Server-Public-IP>:5000/add-product
        Method: POST
        Body (JSON)
        
        { "name": "Tablet", "price": 299.99, "stock": 15 }
 
 **Verify:**
  The product is added to the RDS database.
  Run SELECT * FROM Products; on your RDS database to confirm.

--------------------------------------------------------------------------------

## Phase 9 : Connect the Web Server to the App Server

1. **Update the Web Server Code:**

On the Web Server instance, create a new file named index.html.
Paste the below html file to show the values from RDS.

![image](https://github.com/user-attachments/assets/2a26cbfe-5cd2-4a2c-b644-0843ccaa65bd)

### End Result
**Web Server:** Serves the frontend, fetching product data from the App Server.
**App Server:** Handles backend logic and interacts with the RDS database.
**RDS:** Stores product information.
**Load Balancer:** Balancing the traffic to the Web server across multiple AZs.

--------------------------------------------------------------------------------
## Conclusion <a name="conclusion"></a>

Congratulations! You've now gone through a comprehensive guide on setting up a 3-tier VPC architecture in AWS. Let's recap what we've covered:

1. We started with the basics of creating a VPC, setting up Internet and NAT Gateways, and configuring subnets and route tables.
2. We then moved on to creating security groups and launching EC2 instances in each tier.
3. We explored optional components like adding an Application Load Balancer, setting up an Amazon RDS instance, and configuring Auto Scaling.
4. We delved into advanced configurations and best practices to enhance your VPC setup.
5. We provided extra suggestions to further optimize and secure your architecture.
6. Finally, we discussed important cost considerations to help you manage and optimize your AWS spending.

This 3-tier VPC architecture provides a solid foundation for hosting scalable, secure, and highly available applications on AWS. However, remember that this is a starting point. As your application grows and your requirements evolve, you may need to adapt and expand this architecture.

Key takeaways:
- Always prioritize security in your design decisions.
- Regularly review and optimize your setup for performance and cost-efficiency.
- Stay updated with AWS best practices and new service offerings that could benefit your architecture.
- Consider using Infrastructure as Code for managing your VPC setup, especially for production environments.
- Implement proper monitoring and alerting to ensure the health and performance of your infrastructure.

Remember, building a robust cloud infrastructure is an iterative process. Continually assess your architecture against your business needs, security requirements, and AWS's latest offerings.

I hope this guide has provided you with a comprehensive understanding of setting up a 3-tier VPC in AWS. As you implement this architecture, don't hesitate to refer back to specific sections as needed. Good luck with your AWS journey!

--------------------------------------------------------------------------------
