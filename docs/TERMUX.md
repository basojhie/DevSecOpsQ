# Termux controller

Termux is a lightweight remote control/status client. The security tools run in GitHub-hosted runners, not on the phone.

## Requirements

- Termux from a trusted distribution source
- GitHub token with **Actions: read/write** and **Contents: read** for this repository only
- A private Telegram bot token/chat ID only if Telegram notifications are enabled

## Configure

```sh
pkg update -y
pkg install -y curl jq
mkdir -p ~/.config/devsecopsq
cat > ~/.config/devsecopsq/config <<'EOF'
OWNER=basojhie
REPO=DevSecOpsQ
WORKFLOW=asm.yml
BRANCH=main
EOF
chmod 700 ~/.config/devsecopsq
```

Save a fine-grained token in a private file; do not paste it into chats or command history:

```sh
umask 077
printf 'GITHUB_TOKEN=' > ~/.config/devsecopsq/secret
read -r -s TOKEN
printf '%s\n' "$TOKEN" >> ~/.config/devsecopsq/secret
unset TOKEN
chmod 600 ~/.config/devsecopsq/secret
```

## Trigger passive scan

```sh
source ~/.config/devsecopsq/config
source ~/.config/devsecopsq/secret
curl -fsS -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/$OWNER/$REPO/actions/workflows/$WORKFLOW/dispatches" \
  -d "{\"ref\":\"$BRANCH\",\"inputs\":{\"profile\":\"passive\"}}"
unset GITHUB_TOKEN
```

GitHub returns HTTP 204 on accepted dispatch. Check workflow status in the GitHub Actions UI. Do not enable staging assessment until the target registry contains explicit written approval and staging environment metadata.

## Token rotation

Rotate the fine-grained token periodically, revoke it immediately if exposed, and keep repository access restricted. The controller intentionally does not accept arbitrary hostnames.
