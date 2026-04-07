# Scripts

Keep scripts config-driven and generic.

Rules:

- never hard-code personal absolute paths
- never embed secrets or provider keys
- keep login/session flows optional and documented, not bundled with private state
- treat captured data as local and private by default
- prefer mock JSON exports for public social-feed examples
- document private X browser/export workflows without committing sessions or profiles
