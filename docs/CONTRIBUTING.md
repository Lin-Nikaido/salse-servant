# CONTRIBUTING

Thank you your joining to TRUST project!
If you not have developer permission for this project. [Let us know](https://teams.microsoft.com/l/team/19%3A0y18oOqTlX8-UJnHBcdSMHWqPrv4U1dCbOprt_2Tu701%40thread.tacv2/conversations?groupId=7457ac2e-39ed-4471-b635-7a58c30ef8e7&tenantId=d1c1335e-f582-42a9-b6fe-5e1a16eb9bc8), We can invite you.

# Get started

1. At first install `uv`. See also [here](https://docs.astral.sh/uv/getting-started/installation/)
2. Set up AWS Configure. See [AWS SSO configuration](#aws-sso-configuration).
3. Clone this repo
    ```commandline
    git clone https://github.com/YourIndependence/sales-servant\.git
    ```
4. Make venv
    ```commandline
    cd sales-servant
    uv venv --python "python3.12" ".venv"
    ```
5. Install dependency
    ```commandline
    uv sync --frozen --extra dev
    ```
6. Install dev tools.
   1. [archgate](https://github.com/archgate/cli) (ADR manager) is invoked via `npx` in git hooks - no explicit installation is required.
       **NOTICE**: archgate does not support `linux/arm64`. On that platform the hooks will automatically skip the check.

   2. And set up rulesync
       ```commandline
       .rulesync/rulesync.sh
       ```
   3. Install [gitleaks](https://github.com/gitleaks/gitleaks) (SAT for secrets).
    - Linux
        ```commandline
        apt install gitleaks
        ```
    - Mac
        ```commandline
        brew install gitleaks
        ```
    - Windows
        1. Download exe from [gitleaks](https://github.com/gitleaks/gitleaks/releases).
        2. Unpack and place exe into local. (e.g.: `C:\Users\{USER_NAME}\.gitleaks`)
        3. Set Path.

7. Run in local as trial.
    ```commandline
    uv run adk web
    ```

# Get started with devcontainer


# Start contributing

1. Set your development environment.
2. Select an issue you want to do.
   And assign the issue yourself.
   **NOTICE**
   If there are no issues you want to do. Create the issue first.
3. Change issue status: `In progress`
4. create workspace branch.
   See also [branch naming rule](CODING_RULES.md#branch-rules).
5. Implement or fix the issue you selected. and its test codes.
   See also [CODING_RULES](CODING_RULES.md).
   The place where unittests code implement: See also [ARCHITECTURE.md](ARCHITECTURE.md#directory-architecture)
6. Check the affected unit tests first. Unit tests must not require LocalStack, real AWS, Microsoft 365, Box, Azure, Google APIs, or repository secrets.
    ```commandline
    uv run pytest tests/unittests/<affected-path>/ -v
    ```
7. Check **whole** non-LibreOffice unit tests pass.
    ```commandline
    uv run pytest tests/unittests/
    ```
8. Format the code
    ```commandline
    uv run pre-commit run --all-files
    uv run ruff check --fix
    uv run ruff format
    npx archgate check
    ```
9. Push your branch.
10. Run integration tests when the change crosses service boundaries.
    ```commandline
    bash scripts/run-integration-tests.sh
    ```
    The LocalStack-backed profile uses LocalStack, MySQL, OpenSearch, and local Cognito. Tests that require real AWS must be marked `real_aws`; they are skipped automatically when `AWS_ENDPOINT_URL` points to LocalStack, without changing the pytest command.
11. Submit your PR.
    **Do not forget** write `close: #IssueNo` in PR description.

# Tips

## How to run test on bastion

1. Connect bastion env through SSH
   See also:[How to access EC2 from your local env](#how-to-access-ec2-from-your-local-machine)
2. Change directory and see the list of directories
    ```commandline
     cd /home/ec2-user/pythonProject
     ls
    ```
3. Select the directory that you want to run test code and move to that one.
   If you do not have a working copy yet, clone the repo and set it up first.
    ```commandline
    cd /home/ec2-user/pythonProject
    git clone https://github.com/tmc-ccoe/trust-core.git <your-work-dir>
    cd <your-work-dir>
    ```
    > **Note:** The repository is private. Authenticate on the bastion before
    > cloning (e.g. `gh auth login`, or a GitHub personal access token).
    > Then create the venv and install dependencies the same way as local setup.
    > See [Get started](#get-started) steps 4-5 (`uv venv` / `uv sync`).
    > Check out the branch you want to test and make it up to date.
    ```commandline
    git fetch && git switch <your-branch> && git pull
    ```
4. Run integration tests against real AWS resources.

    ```commandline
    uv run pytest -q tests/integration/
    ```

    To focus only on ECS task runner tests, use the `ecs` marker:

    ```commandline
    uv run pytest -q -m "real_aws and ecs" tests/integration/task_runner/
    ```

## How to access EC2 from your local machine.

There is a bastion EC2 instance in AWS. You can connect it with SSM.
To connect SSM, use web console or AWS CLI

```commandline
aws ssm start-session --target <INSTANCE ID>

# dev
aws ssm start-session --target i-0e7cec7ded0c78855

# staging
aws ssm start-session --target i-0cba4dfede69299d7

# main
aws ssm start-session --target i-01c6d7f6ea5730c55
```

If you cannot find some environment variables in EC2, run this code on EC2.

```commandline
source /etc/profile
```

## Auth bypass for local development (IMPERSONATE)

When running the server locally you sometimes need to call API endpoints without going through the full Cognito token flow - for example, to smoke-test a feature before the devcontainer Cognito mock is fully configured, or to run quick manual checks from `curl`.

**How it works**

Set `IMPERSONATE=true` in `LOCAL`, `LOCAL_CONTAINER`, or `CI`, then send requests **without** an `Authorization` header. The server skips JWT validation and synthesises a user from two optional request headers. Auth bypass is disabled for deployed environment names such as `dev`, `staging`, `main`, or unknown values even if `IMPERSONATE=true` is set.

| Header              | Default when omitted |
| ------------------- | -------------------- |
| `x-local-user-id`   | `local-user`         |
| `x-local-user-mail` | `local@example.com`  |

Example:
```bash
curl -H "x-local-user-id: my-id" \
     -H "x-local-user-mail: me@example.com" \
     http://localhost:8000/some/endpoint
```

## AWS SSO Configuration

To access AWS resources (Secrets Manager, DynamoDB, etc.) in your local environment, you need to configure AWS SSO.

### 1. Configure `~/.aws/config`

Add the following content to `~/.aws/config` (replace `<your_session_name>` with any name you prefer):

```ini
[profile TORODeveloperFullAccess-905418085415]
sso_session = <your_session_name>
sso_account_id = 905418085415
sso_role_name = TORODeveloperFullAccess
region = ap-northeast-1
output = json

[sso-session <your_session_name>]
sso_start_url = https://d-956703c220.awsapps.com/start/
sso_region = ap-northeast-1
sso_registration_scopes = sso:account:access
```

Alternatively, you can configure interactively:

```commandline
aws configure sso
```

### 2. Login to SSO

```commandline
aws sso login --profile TORODeveloperFullAccess-905418085415
```

A browser will open and prompt you for authentication. Complete the authentication process.

### 3. Verify Login

```commandline
AWS_PROFILE=TORODeveloperFullAccess-905418085415 aws sts get-caller-identity
```

If logged in successfully, your account information will be displayed.

### 4. Set Profile

**Option A: Set environment variable (current terminal session only)**

```commandline
export AWS_PROFILE=TORODeveloperFullAccess-905418085415
```

**Option B: Add to `.zshrc` (persistent)**

```commandline
echo 'export AWS_PROFILE=TORODeveloperFullAccess-905418085415' >> ~/.zshrc
source ~/.zshrc
```

## Develop with Claude Code

### Get started

Run with GitHub CodeSpaces. See also [/.devcontainer/Readme.md](/.devcontainer/Readme.md)

- Initialize `rulesync` (invoked via `npx` - no explicit installation required).
    ```commandline
    .rulesync/rulesync.sh
    ```
- Run claude Code
    ```commandline
    claude
    ```

### Claude Code Slash Commands & Skills

This project ships a set of Claude Code slash commands (skills) that automate common development workflows.
If you use [Claude Code](https://claude.ai/code), the following commands are available out of the box:

| Command                          | Description                                                                                                            |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `/build <issue>`                 | Implement a new feature from a GitHub Issue through a 6-phase workflow with user approval gate before any code changes |
| `/fix <issue>`                   | Fix a bug from a GitHub Issue through a 6-phase workflow with user approval gate before any code changes               |
| `/hotfix <issue>`                | Fix a critical production bug through a 7-phase workflow with dual-branch merge (main + dev)                           |
| `/record-architectural-decision` | Record or update an ADR in `docs/adrs/`                                                                                |
| `/draft-pr`                      | Generate a pull request title and body ready to copy-paste                                                             |

Skill definitions live in [.rulesync/](.rulesync/) and are loaded automatically by Claude Code.

## Working Agreement

- Communication Tools is MS Teams
    - [TRUST developer Team](https://teams.microsoft.com/l/team/19%3A0y18oOqTlX8-UJnHBcdSMHWqPrv4U1dCbOprt_2Tu701%40thread.tacv2/conversations?groupId=7457ac2e-39ed-4471-b635-7a58c30ef8e7&tenantId=d1c1335e-f582-42a9-b6fe-5e1a16eb9bc8)
