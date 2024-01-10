# Deploying Azure Function App with Selenium Web Parsing using Docker, ACRs & Azure Pipelines

Deploying an Azure Function App built with the Python V2 programming model. The focus is on automating web parsing through Selenium, and the deployment utilizes Docker, Azure Container Registries (ACRs), and Azure Pipelines.
The deployment involves building a Docker image from the base Azure Function image, pre-packaging it with our code, the Google Chrome executable, and the Selenium Web Driver.

## Prerequisites

Before you proceed, make sure you have the following:

- An Azure subscription
- Docker installed on your local machine
- Access to Azure Container Registries (ACRs)
- An Azure DevOps account for Azure Pipelines

## Deployment Steps

Follow these steps for a successful deployment:

1. **Azure Function App Setup:**
   - Create a new Azure Function App using the Azure Portal.
   - Choose Python as the runtime stack and select the appropriate version.

2. **Write Function Code:**
   - Write the Python function code in `function_app.py` for web parsing using Selenium.
   - Include any required dependencies in `requirements.txt`.

3. **Docker Image Build:**
   - Create a `Dockerfile` to package your Python function into a Docker image.
   - Pre-package the image with the code, Google Chrome executable, and Selenium Web Driver.

4. **Azure Container Registry (ACR) Setup:**
   - Set up an Azure Container Registry (ACR) in Azure to store Docker images.

5. **Azure Pipelines Configuration:**
   - Create a new Azure Pipeline in Azure DevOps.
   - Configure the build pipeline YAML (`azure-pipelines.yml`) for Docker image builds.
6. **Run the docker image locally**
   - Login to your Azure Conatiner Registry using `docker login` or `az acr login`
   - Pull the image created from your repository `docker pull <your_image>:tag`
   - Run it in a container `docker run -d -p <port>:80 <your_image>`
   - Access your Azure function App `http://localhost:<port>/api/SearchAmazonProducts?search=laptop&pages=1`

6. **Run Azure Pipelines:**
   - Trigger the pipeline manually or set up triggers for automatic builds.
   - Monitor the pipeline run for any errors.

7. **Verify Function App Deployment:**
   - Once the pipeline is successful, verify the Azure Function App deployment in the Azure Portal.

## Notes

- The `Dockerfile` is configured to include the Python function code, Google Chrome, and the Selenium Web Driver.
- The `azure-pipelines.yml` file defines the build pipeline in Azure Pipelines.

Feel free to customize this deployment based on your specific project requirements. Happy deploying!
