<sub>[← all labs](../../README.md)</sub>

# Terraform for a hybrid-cloud SaaS platform

> Modules for what's shared, environments for what differs, and CI that proves both before anyone runs apply.

`Terraform` · `Azure` · `AWS`

**Companion to:**
- [Hybrid-Cloud SaaS Platform with Terraform](https://www.linkedin.com/pulse/hybrid-cloud-saas-platform-terraform-tony-honesto-adfac/)

## What it shows

- Reusable modules: an AWS network (VPC, subnets across AZs) and an Azure app (resource group, plan, Linux web app).
- Per-environment stacks (`envs/dev`, `envs/prod`) that call the same modules with different sizes.
- CI runs `terraform init -backend=false` and `terraform validate` per environment with no cloud credentials.
- Policy-as-code tests: pinned providers, required tags, HTTPS + TLS 1.2, multi-AZ prod and no Basic SKU in prod.

## Run it

```bash
bash labs/terraform-hybrid-cloud/ci.sh   # validate every env, then policy tests
# against real accounts:
cd envs/dev && terraform init && terraform plan
```

Real output (from this lab's CI run):

```text
== envs/dev/
Success! The configuration is valid.

== envs/prod/
Success! The configuration is valid.

test_every_environment_tags_its_resources (test_policy.PolicyTests.test_every_environment_tags_its_resources) ... ok
test_every_provider_is_version_pinned (test_policy.PolicyTests.test_every_provider_is_version_pinned) ... ok
test_prod_is_multi_az_and_not_on_basic_sku (test_policy.PolicyTests.test_prod_is_multi_az_and_not_on_basic_sku) ... ok
test_web_app_enforces_https_and_tls12 (test_policy.PolicyTests.test_web_app_enforces_https_and_tls12) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
```

## What's in here

| File | Purpose |
|---|---|
| `modules/aws-network/` | VPC and subnets across availability zones |
| `modules/azure-app/` | Resource group, service plan and web app |
| `envs/dev, envs/prod` | Environment stacks |
| `ci.sh` | Validate without credentials, then policy tests |
| `tests/` | Policy-as-code checks |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| `-backend=false` | Remote state in S3 + DynamoDB lock or Azure Storage |
| Python policy tests | OPA / Sentinel / Checkov in the pipeline |
| validate only | plan on PR, apply on merge with approvals |
