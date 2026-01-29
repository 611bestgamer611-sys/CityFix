# CityFix Remote Git Hooks

Server-side Git hooks for the CityFix repository to enforce policies and automate workflows.

## Available Hooks

### pre-receive
Runs before accepting pushed commits:
- Prevents force pushes to protected branches (main/master)
- Validates commit message format (Conventional Commits)
- Checks for large files (>10MB)
- Validates branch naming conventions
- Optional: Enforces signed commits

### post-receive
Triggers after successful push:
- Triggers CI/CD pipelines via webhooks
- Sends Slack notifications
- Auto-deploys to staging (develop branch)
- Creates backups for production pushes
- Logs deployment events

### update
Validates branch operations:
- Prevents deletion of protected branches
- Enforces fast-forward only for protected branches
- Validates branch naming conventions
- Warns about large changesets
- Prevents force pushes to protected branches

## Installation on Git Server

### For Bare Repository

```bash
# Navigate to your bare repository
cd /path/to/cityfix.git/hooks/

# Copy hooks
cp /path/to/remote_hooks/* .

# Make executable
chmod +x pre-receive post-receive update

# Configure (see Configuration section)
```

### For GitHub/GitLab/Bitbucket

These platforms have their own webhook and branch protection mechanisms. The logic from these hooks can be adapted to:

- GitHub Actions workflows
- GitLab CI/CD pipelines
- Bitbucket Pipelines
- Pre-receive hooks (GitHub Enterprise, GitLab Premium)

## Configuration

### Environment Variables

Set these in your Git server environment or in the hook files:

```bash
# CI/CD Webhook
export CI_WEBHOOK_URL="https://ci.example.com/webhook"

# Slack Notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Backup Directory
export BACKUP_DIR="/var/backups/cityfix"
```

### Protected Branches

Edit the `update` hook to configure protected branches:

```bash
PROTECTED_BRANCHES=("main" "master" "production" "release/*")
```

### Branch Naming Conventions

The hooks enforce these patterns:
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical fixes
- `release/version` - Release branches
- `develop` - Development branch
- `main` / `master` - Production branch

## Webhook Integration

### CI/CD Webhook Payload

The post-receive hook sends this JSON payload:

```json
{
  "repository": "CityFix",
  "branch": "main",
  "commit": "a1b2c3d",
  "message": "feat: add new feature",
  "author": "John Doe <john@example.com>",
  "commits": 3
}
```

### Setting up Jenkins Webhook

```groovy
// Jenkinsfile webhook trigger
properties([
    pipelineTriggers([
        genericTrigger(
            genericVariables: [
                [key: 'BRANCH', value: '$.branch'],
                [key: 'COMMIT', value: '$.commit']
            ],
            causeString: 'Triggered by Git push',
            token: 'cityfix-webhook-token',
            printContributedVariables: true,
            printPostContent: true
        )
    ])
])
```

### Setting up Slack Webhook

1. Create a Slack App at https://api.slack.com/apps
2. Enable Incoming Webhooks
3. Add webhook to workspace
4. Copy webhook URL and set `SLACK_WEBHOOK_URL`

## Auto-Deployment

### Staging Deployment (develop branch)

Edit `post-receive` hook:

```bash
if [ "$BRANCH" = "develop" ]; then
    ssh user@staging-server << 'EOF'
        cd /opt/cityfix
        git pull origin develop
        docker-compose down
        docker-compose build
        docker-compose up -d
        docker-compose logs -f
EOF
fi
```

### Production Deployment (main branch)

**Warning:** Auto-deployment to production is risky. Use with caution!

```bash
if [ "$BRANCH" = "main" ]; then
    # Trigger production deployment via CI/CD
    curl -X POST "$CI_WEBHOOK_URL" \
        -H "X-Deploy-Environment: production" \
        -d '{"branch": "main"}'
fi
```

## Testing Hooks Locally

You can test remote hooks locally before deploying:

```bash
# Test pre-receive
cat <<EOF | bash remote_hooks/pre-receive
old-commit-hash new-commit-hash refs/heads/feature/test
EOF

# Test post-receive
cat <<EOF | bash remote_hooks/post-receive
old-commit-hash new-commit-hash refs/heads/develop
EOF

# Test update
bash remote_hooks/update refs/heads/feature/test old-hash new-hash
```

## Bypassing Hooks

Server-side hooks **cannot be bypassed** by clients, which is their purpose. However, administrators can:

```bash
# Disable hook temporarily
cd /path/to/repo.git/hooks/
mv pre-receive pre-receive.disabled

# Re-enable
mv pre-receive.disabled pre-receive
```

## Troubleshooting

### Hook Not Executing

Check permissions:
```bash
ls -la /path/to/repo.git/hooks/
chmod +x /path/to/repo.git/hooks/pre-receive
```

Check Git server logs:
```bash
tail -f /var/log/git/git-daemon.log
```

### Webhook Not Firing

Test manually:
```bash
curl -X POST "$CI_WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d '{"test": "true"}'
```

Check network connectivity from Git server.

### Hook Failing

Run hook manually with debug:
```bash
bash -x /path/to/repo.git/hooks/pre-receive
```

## Security Considerations

1. **Secrets Management**: Store webhook URLs and tokens securely
2. **Authentication**: Use tokens for webhook endpoints
3. **HTTPS**: Always use HTTPS for webhooks
4. **Validation**: Validate webhook signatures (GitHub, GitLab)
5. **Access Control**: Limit who can modify hooks on server
6. **Audit Logging**: Log all hook executions and outcomes

## Integration Examples

### GitHub Enterprise

```bash
# Set as global pre-receive hook
cp remote_hooks/pre-receive /opt/github/pre-receive.d/01-cityfix-validation
chmod +x /opt/github/pre-receive.d/01-cityfix-validation
```

### GitLab

Use GitLab's server hooks:
```bash
cp remote_hooks/* /opt/gitlab/embedded/service/gitlab-shell/hooks/
```

### Gitea/Gogs

```bash
cp remote_hooks/* /path/to/gitea/data/git/hooks/
```

## Maintenance

### Updating Hooks

1. Test changes locally
2. Backup existing hooks
3. Deploy to staging repository first
4. Monitor for issues
5. Deploy to production repository

### Monitoring

Monitor hook execution:
```bash
# Add to post-receive hook
echo "$(date) - Push to $BRANCH by $AUTHOR" >> /var/log/git-hooks.log
```

## Best Practices

1. **Test thoroughly** before deploying to production
2. **Document** all hook behaviors
3. **Version control** your hooks (this repository)
4. **Monitor** hook execution and failures
5. **Fail safely** - don't block pushes unnecessarily
6. **Communicate** hook policies to team
7. **Review** hook logs regularly

## Support

For issues with remote hooks:
- Check Git server documentation
- Review hook execution logs
- Test hooks in isolation
- Contact DevOps team

## Additional Resources

- [Git Hooks Documentation](https://git-scm.com/docs/githooks)
- [Pro Git - Git Hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [Conventional Commits](https://www.conventionalcommits.org/)
