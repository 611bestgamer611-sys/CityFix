# CityFix Git Hooks

This directory contains Git hooks for the CityFix project to maintain code quality and consistency.

## Available Hooks

### pre-commit
Runs before creating a commit:
- Checks for console.log statements in frontend code
- Runs ESLint and Prettier on staged frontend files
- Runs Black formatter and Flake8 on Python files
- Checks for large files (>5MB)
- Scans for potential sensitive data (passwords, API keys, etc.)

### pre-push
Runs before pushing to remote:
- Warns when pushing to main/master branches
- Runs frontend build and TypeScript checks
- Runs backend tests for all services
- Optional Docker build verification
- Checks for uncommitted changes

### commit-msg
Validates commit messages:
- Enforces Conventional Commits format
- Checks message length (10-100 characters)
- Prevents WIP commits on main/master branches

### post-merge
Runs after a successful merge:
- Detects changes in package-lock.json and updates dependencies
- Detects changes in requirements.txt and updates dependencies
- Notifies about docker-compose.yml changes

## Installation

To install these hooks, run from the project root:

```bash
# Make hooks executable
chmod +x local_hooks/*

# Copy hooks to .git/hooks/
cp local_hooks/pre-commit .git/hooks/
cp local_hooks/pre-push .git/hooks/
cp local_hooks/commit-msg .git/hooks/
cp local_hooks/post-merge .git/hooks/
```

Or use this one-liner:

```bash
chmod +x local_hooks/* && cp local_hooks/pre-commit local_hooks/pre-push local_hooks/commit-msg local_hooks/post-merge .git/hooks/
```

## Uninstall

To remove hooks:

```bash
rm .git/hooks/pre-commit
rm .git/hooks/pre-push
rm .git/hooks/commit-msg
rm .git/hooks/post-merge
```

## Skipping Hooks

### Skip Pre-Commit Hook
```bash
git commit --no-verify -m "your message"
# or
git commit -n -m "your message"
```

### Skip Pre-Push Hook
```bash
git push --no-verify
# or
git push -n
```

**Note:** Use sparingly and only when necessary!

## Commit Message Format

Follow Conventional Commits specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes
- `build`: Build system changes

### Examples

```bash
# Good commit messages
git commit -m "feat: add user profile page"
git commit -m "fix(auth): resolve token expiration bug"
git commit -m "docs: update API documentation"
git commit -m "refactor(ticket): simplify ticket creation logic"
git commit -m "test: add unit tests for notification service"
git commit -m "chore: update dependencies"

# Bad commit messages (will be rejected)
git commit -m "update stuff"
git commit -m "fix bug"
git commit -m "WIP"
```

## Dependencies

### For Frontend Checks
- Node.js and npm
- ESLint (installed via npm)
- Prettier (installed via npm)

### For Backend Checks
- Python 3
- black (optional): `pip install black`
- flake8 (optional): `pip install flake8`
- pytest (optional): `pip install pytest`

### Install All Dependencies

```bash
# Frontend
cd src/CityFixUI
npm install

# Backend (example for one service)
cd src/AuthService
pip install -r requirements.txt
pip install black flake8 pytest
```

## Customization

You can customize the hooks by editing the files in the `local_hooks/` directory:

- Adjust linting rules
- Change file size limits
- Modify sensitive data patterns
- Add custom checks

After making changes, re-copy the hooks to `.git/hooks/`.

## Troubleshooting

### Hook Not Running
Make sure the hook is executable:
```bash
chmod +x .git/hooks/pre-commit
```

### Hook Failing Unexpectedly
Run the hook manually to see detailed output:
```bash
bash .git/hooks/pre-commit
```

### Disable a Specific Check
Edit the hook file and comment out the check you want to disable.

## CI/CD Integration

These hooks are meant for local development. The CI/CD pipeline has its own checks that may be stricter.

## Best Practices

1. **Install hooks immediately** after cloning the repository
2. **Don't skip hooks** unless absolutely necessary
3. **Fix issues** found by hooks rather than skipping them
4. **Update hooks** when best practices change
5. **Test hooks** after customization

## Support

For issues with hooks, refer to the main project documentation or contact the development team.
