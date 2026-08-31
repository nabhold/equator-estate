# Equator & Estate Co. Digital Estate

`nabhold/equator-estate` is an independently deployable B2C property digital
estate in the Nabhold ecosystem. The current application is a legacy Django
baseline, so Codespaces uses the `baobab-dev` v1.2.6 full profile until the
planned frontend architecture is agreed.

## Foundation 4

The repository declares its development environment in
`.nabhold/environment.yaml`, uses SHA-pinned GitHub Actions, assigns ownership
through `.github/CODEOWNERS`, and consumes the canonical Foundation 4 gate from
`nabhold/shared`. The gate validates contract compatibility and reproducibility
and scans dependencies, source, secrets, configuration, and the built image.

Copy `.env.example` to `.env` for local development and replace placeholder
values. Never commit `.env` or production credentials.

Branch protection is a repository setting: protect `main`, require pull
requests and CODEOWNER review, and require `foundation` plus application CI.
