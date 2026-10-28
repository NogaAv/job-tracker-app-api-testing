# job-tracker-app-api-testing

Quick runner usage

All runner scripts now live in the `scripts/` directory.

- Bash / Linux / Git Bash:
  ./scripts/run_tests.sh --help
  ./scripts/run_tests.sh --tcid TC-001
  ./scripts/run_tests.sh -k login
  ./scripts/run_tests.sh tests/public/test_verify_public_status_endpoint.py

- Windows CMD:
  scripts\run_tests.bat --help
  scripts\run_tests.bat --tcid TC-001
  scripts\run_tests.bat tests/auth/test_verify_login.py

- PowerShell:
  ./scripts/run_tests.ps1 --help
  ./scripts/run_tests.ps1 -k "login and valid"
  ./scripts/run_tests.ps1 --tcid TC-005 --tcid TC-006

- Python entry point (best for CI/CD):
  python scripts/run_tests.py --help
  python scripts/run_tests.py --tcid TC-001
  python scripts/run_tests.py -k "login or summary"
  python scripts/run_tests.py tests/applications/test_verify_create_applications.py

The runner wraps pytest and supports custom tcid filtering, -k keyword matching, optional file targets, and timestamped JUnit/report output in reports/<timestamp>/.