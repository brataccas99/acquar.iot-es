# AquaR.IoT ES: A Serverless Enhanced Aquarium with IoT ESP32 Board, AWS Services, and Telegram Integration

# Abstract:
AquaR.IoT ES (Enhanced Serverless) is a captivating project that showcases the fusion of IoT, serverless programming, and cloud integration to create a cutting-edge aquarium experience. This project, in his standard version (here's the repo: <url>https://github.com/brataccas99/acquar.iot</url>), features a fully functional aquarium populated with mesmerizing red fishes, equipped with an IoT ESP32 board, an array of sensors, motors, clocks, bridges, and other IoT components. By leveraging the power of the Zerynth platform, Python, and Zerynth Cloud, users can remotely interact with the aquarium, issuing commands such as feeding the fishes, oxygen regeneration, and water cleaning while effortlessly gathering valuable statistical data through Ubidots.

In this enhanced version, AquaR.IoT ES embraces the advancements in technology by migrating from Zerynth to AWS services for serverless programming. Leveraging AWS Lambda and DynamoDB, the project achieves a more scalable, efficient, and streamlined architecture. Additionally, a Telegram bot replaces the previous Zerynth Cloud functionality, enabling users to effortlessly send commands to the aquarium via AWS Lambda's seamless integration with the popular messaging platform.

AquaR.IoT ES represents a remarkable integration of cutting-edge technologies, enabling a fascinating and interactive aquarium experience that exemplifies the potential of IoT, serverless programming, and cloud integration.

## Architecture

![arch](./images/arch.png)

There are some devices (simulated) that send datas to SQS queues and a lambda function that colud be triggered manually. This lambda does an average and saves datas on DynamoDB. All the datas are accessed by a Telegram bot. This bot can trigger IoT sensors and the lambda for store datas. It can also switch on or off sensors. It also offers a way to send recap emails to the user.

## Prerequisite
- docker
- Node.js
- A telegram bot token

## How to run this project

- clone this repo: <code>https://</code>
- run <code>docker run -d --rm -p 4566:4566 --name aws localstack/localstack:1.4</code>
- run <code>npm install</code>
- go into <code>deploy</code> and re-run the command above
- in the root directory run <code>npm run build</code>
- run <code>npm run start</code>
- run <code>npm run setup</code>
- run <code>.\copy.bat</code>
- verify your email with: <code>aws ses verify-email-identity --email-address <your-email> --endpoint-url="http://localhost:4566"</code>

After this, setup all the lamba functions:

- <code>aws iam create-role --role-name lambdarole --assume-role-policy-document file://role_policy.json --query 'Role.Arn' --endpoint-url=http://localhost:4566</code>
- <code> aws iam put-role-policy --role-name lambdarole --policy-name lambdapolicy --policy-document file://policy.json --endpoint-url=http://localhost:4566</code> 

And then create the functions:

- <code>aws lambda create-function --function-name offsensors --zip-file fileb://functions.zip --handler deploy/offSensors.lambdaHandler --runtime nodejs18.x --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566</code>

- <code>aws lambda create-function --function-name onsensors --zip-file fileb://functions.zip --handler deploy/onSensors.lambdaHandler --runtime nodejs18.x --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566</code>
  
- <code>aws lambda create-function --function-name offSensorAcquarium --zip-file fileb://functions.zip --handler deploy/offSensorAcquarium.lambdaHandler --runtime nodejs18.x --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566</code>

- <code>aws lambda create-function --function-name onSensorAcquarium --zip-file fileb://functions.zip --handler deploy/onSensorAcquarium.lambdaHandler --runtime nodejs18.x --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566</code>

- <code>aws lambda create-function --function-name generateO2 --zip-file fileb://functions.zip --handler deploy/generateO2.lambdaHandler --runtime nodejs18.x --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566</code>

- <code>aws lambda create-function --function-name giveFoodAcquarium --zip-file fileb://functions.zip --handler deploy/giveFoodAcquarium.lambdaHandler --runtime nodejs18.x --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566</code>

- <code>aws lambda create-function --function-name waterClean --zip-file fileb://functions.zip --handler deploy/waterClean.lambdaHandler --runtime nodejs18.x --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566</code>

- start the bot by typing: <code>python bot/bot.py</code>
