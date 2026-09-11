---
name: export-hermes-profile
description: "Export current Hermes to portable Office profile. Sync to GitHub."
---

# Export Hermes Profile Skill

**Use when user wants to export, sync, or update the Office Hermes profile with current configuration.**

Trigger phrases:
- "Export the current Hermes"
- "Sync Office Hermes"
- "Update Office Hermes profile"
- "Push Hermes configuration to office-hermes"

## Purpose

Automatically export the running Hermes environment to the portable Office Hermes profile on GitHub:

1. **Audit** current system for changes
2. **Detect** new/modified/deleted components
3. **Filter** secrets and personal data
4. **Update** profile repository
5. **Verify** security and portability
6. **Prepare** for Git commit/push

## How It Works

### Phase 1: Environment Audit

Scan current Hermes for:

- New skills (compare ~/.hermes/skills/ vs profiles/office-hermes/skills/categories/)
- Modified configuration (config.yaml diffs)
- New workflows (cron/jobs.json changes)
- Updated rules/protocols
- Memory schema changes
- MCP updates

### Phase 2: Filtering

For each discovered component:

1. **Secret scan** — Remove API keys, tokens, credentials
2. **Personal data scan** — Remove private memories, contacts
3. **Path normalization** — Convert absolute paths to relative
4. **Machine cleanup** — Remove environment-specific IDs

### Phase 3: Export

Export to ~/office-hermes-export/:

- Copy skill changes
- Update configuration
- Update workflows
- Regenerate MANIFEST.md
- Update skill inventory
- Update documentation

### Phase 4: Verification

Run comprehensive checks:

```bash
# Security audit
python3 scripts/verify/security-audit.py --strict
# Result: ✓ No secrets

# Portability check
python3 scripts/verify/portability-check.py
# Result: ✓ All components portable

# Git safety
git diff scripts/verify/git-safety-check.sh
# Result: ✓ Safe to commit

# Size check
du -sh profiles/office-hermes/
# Result: ~50MB (within limits)
```

### Phase 5: Prepare for Sync

Update Git metadata:

- Update MANIFEST.md with new timestamps
- Update EXPORT_SUMMARY.md with changes
- Generate export-log.txt
- Update .gitignore if needed
- Verify .env and credentials are ignored

### Phase 6: Commit & Push

If approved by user:

```bash
cd profiles/office-hermes
git add -A
git commit -m "chore: update office hermes profile [$(date +%Y-%m-%d)]"
git push origin office-hermes
```

## Safety Considerations

### Approval Required For:

- ✓ Any Git push (always ask)
- ✓ Deletion of files (show diff first)
- ✓ Force push (only if explicitly requested)
- ✓ Large changes (>100 files)

### Automatic Actions:

- ✓ Local auditing (read-only)
- ✓ Copying files locally
- ✓ Generating documentation
- ✓ Security scanning
- ✓ Creating commit messages

### Never Automatic:

- ✗ Git push without approval
- ✗ Git force push
- ✗ Deleting repository content
- ✗ Overwriting branches
- ✗ Modifying history

## Usage Examples

### Quick Export

```
Hermes: Export the current Hermes configuration
Skill: Audits, filters, exports, verifies, shows summary
User: Reviews summary and chooses to sync or save locally
Skill: If approved, commits and pushes to GitHub
```

### Sync with Review

```
Hermes: Sync Office Hermes
Skill: Exports changes and shows git diff
User: Reviews changes before proceeding
Skill: Creates commit and pushes
```

### Save Locally Only

```
Hermes: Export Hermes but don't push
Skill: Exports to ~/office-hermes-export/ without Git push
Result: Changes saved locally for manual review
```

### Force Sync (after approval)

```
Hermes: Force update office hermes, skip verification
Skill: Skips some checks (still security scans)
User: Must explicitly approve
Skill: Exports and pushes
```

## Output

After successful export/sync, shows:

```
✓ Export Summary
─────────────────────

Changes Detected:
  • 3 new skills (crm-analytics, export-hermes-profile, zendesk-integration)
  • 5 modified skills (updated documentation)
  • 2 new workflows (team-sync, client-update)
  • 1 new rule (multi-tenant-handling.md)
  • 0 deleted components

Security Check:
  ✓ No API keys found
  ✓ No tokens detected
  ✓ No credentials files
  ✓ No personal data leaked
  ✓ .gitignore complete

Portability:
  ✓ All paths normalized
  ✓ No machine-specific config
  ✓ All templates present
  ✓ Ready to clone

Repository:
  Branch: office-hermes
  Commit: feat: update office hermes profile [2026-09-11]
  Files Changed: 12
  Size: 50.2MB
  
Status: Ready to sync to GitHub

Waiting for approval to push...
```

## Configuration

### Required Environment

```bash
# GitHub credentials (for push)
export GITHUB_TOKEN=ghp_...  # GitHub Personal Access Token
# or:
export GIT_SSH_KEY=/path/to/ssh/key  # SSH key for Git

# Source control
HERMES_HOME=~/.hermes  # Current Hermes to export
EXPORT_DIR=~/office-hermes-export  # Export destination
REPO_DIR=~/Personal_Hermes_Agent  # Git repository path
```

### Optional Configuration

```yaml
# In config.yaml:
export_profile:
  auto_security_scan: true  # Always run security audit
  exclude_patterns:  # Never export
    - "*.key"
    - "*.pem"
    - "credentials.*"
    - ".env*"
  git_push_auto: false  # Always ask before pushing
  preserve_history: true  # Keep git history intact
```

## Limitations

- **Manual MCP credentials** — MCP auth must be configured separately
- **Large repositories** — May take time for 172+ skills
- **Network dependent** — Requires GitHub connectivity
- **Git history** — Does not rewrite or clean history
- **Secrets check** — Uses pattern matching (can miss edge cases)

## Troubleshooting

### "No changes detected"

```
Reason: Current Hermes matches office-hermes profile exactly
Action: This is normal after a recent sync
Solution: Make changes to Hermes and try again
```

### "Security warnings found"

```
Reason: Potential secrets or personal data detected
Action: Export halts, shows specific findings
Solution: Review the files and remove manually, or adjust patterns
```

### "Git push failed"

```
Reason: Network error or authentication issue
Action: Shows git error
Solution: 
  1. Verify GitHub credentials: export GITHUB_TOKEN=...
  2. Check network connectivity
  3. Try manual push: git push origin office-hermes
```

### "Portability check failed"

```
Reason: Absolute paths, machine-specific config, or environment vars detected
Action: Shows specific violations
Solution: Use path normalization tools or manual fixes
```

## Related Skills

- **omh-skill** — Manage local skills
- **omh-memory-sync** — Sync memory configuration
- **omh-code-review** — Review changes before commit
- **github-pr-workflow** — Create PR for changes

## See Also

- docs/export-hermes-profile.md — Detailed export documentation
- SECURITY.md — What can/cannot be exported
- MANIFEST.md — Component inventory
- scripts/export/ — Export scripts
- scripts/import/ — Import scripts

---

**Status**: READY FOR DEVELOPMENT  
**Priority**: HIGH (critical for profile sync)  
**Effort**: 2-3 days implementation  
**Dependencies**: Git CLI, Python 3.11+, security scanning tools
