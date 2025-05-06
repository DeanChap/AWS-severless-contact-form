# AWS-severless-contact-form

Serverless Contact Form with AWS & Terraform

Table of Contents
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Deployment](#deployment)
- [Testing](#testing)
- [Cleanup](#cleanup)
- [Troubleshooting](#troubleshooting)


#Project Overview

Goal: Build a contact form backend using:
* API Gateway (for HTTP access)
* AWS Lambda (to run code)
* Amazon SES (to send emails)
* CloudWatch (to monitor application performance)

This project automates the deployment of a contact form on AWS. The contact form allows users to submit their information, which is processed by a Lambda function. The Lambda function sends the data via email using AWS SES (Simple Email Service). The API Gateway exposes the contact form to the public.  The deployment is managed with GitHub Actions CI/CD and Cloud Watch is used separately for monitoring performance.

#Prerequisites

Before deploying the contact form, make sure you have the following:
- [AWS Account](https://aws.amazon.com)
- AWS CLI configured (`aws configure`)
- [Terraform](https://www.terraform.io/downloads.html)
- [GitHub Account](https://github.com/)
- Access to GitHub Secrets for storing AWS credentials
- SES verified email addresses (for sending and receiving emails)

#Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/DeanChap/AWS-severless-contact-form.git
    cd AWS-severless-contact-form
    ```

2. Create and configure your **AWS credentials** in GitHub Secrets (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`).

3. Set up the email variables in `emails.tfvars`:
   
    ```hcl
    email_from = "your-email@example.com"
    email_to   = "recipient-email@example.com"
    ```

4. Install required dependencies (if applicable for local testing):
   
    ```bash
    terraform init
    ```

#Deployment

Using GitHub Actions (CI/CD):

1. Push to the `main` branch to trigger the GitHub Actions workflow. This will automatically:
   - Zip the Lambda function.
   - Initialize Terraform.
   - Apply Terraform configuration to create resources on AWS.

2. The workflow will deploy:
   - AWS Lambda function (`contact_form_lambda`).
   - API Gateway for HTTP endpoints.
   - IAM roles and policies.
   - SES permissions for sending emails.

#Manual Deployment:

1. Import resources (if you are managing pre-existing resources) with Terraform:

    ```bash
    terraform import aws_lambda_function.contact_form contact_form_lambda
    terraform import aws_iam_role.lambda_exec lambda_exec_role
    ```

2. Apply the Terraform plan:

    ```bash
    terraform apply -var-file="emails.tfvars"
    ```

#Testing

Once deployed, you can test the API by sending a POST request to the API Gateway endpoint:

- Use tools like Postman or CURL to send a test request:

    ```bash
    curl -X POST https://<api-endpoint>/contact \
    -d '{"name":"Test User", "email":"test@example.com", "message":"Hello"}'
    ```

- Check if an email is received at the address configured in `email_to`.

#Cleanup

To remove the infrastructure when you're done:

1. Run the following command to destroy all resources:

    ```bash
    terraform destroy -var-file="emails.tfvars"
    ```

2. This will remove the Lambda function, API Gateway, IAM roles, and other resources created during deployment.

#Troubleshooting

Error: "Resource already exists" during Terraform apply
1. **Re-import the existing Lambda** and IAM role into the Terraform state:

    ```bash
    terraform state rm aws_lambda_function.contact_form
    terraform import aws_lambda_function.contact_form contact_form_lambda
    ```

2. Run `terraform plan` again to check the status:

    ```bash
    terraform plan -var-file="emails.tfvars"
    ```

3. If the issue persists, check if the Lambda function or IAM role was created manually. In that case, you may need to remove the existing resources before continuing.

Lambda Function Timeout

If the Lambda function is taking too long to create, ensure that the function's code is correctly packaged as `lambda.zip` and that all resources (IAM roles, permissions) are properly set.

---

#Contributing

Feel free to fork this project, contribute to it, or open an issue for any bugs or improvements. Any issues or questions please email deanchaps@gmail.com

---
