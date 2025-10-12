Secrets and Access (local development)

This project uses Streamlit secrets to store your OpenAI API key and a small email whitelist for access control.

Local setup (development):
1. Open `.streamlit/secrets.toml` and replace the placeholder `OPENAI_API_KEY` with your real key.
2. Add emails to the `[whitelist].emails` list for people allowed to use the app.
3. `.streamlit/secrets.toml` is included in `.gitignore` to avoid accidental commits.

On Streamlit Cloud:
- Go to your app's Settings → Secrets and paste the same keys there instead of committing the file.
- Example keys:
  OPENAI_API_KEY: sk-...
  whitelist:
    emails:
      - your.email@example.com
      - friend@example.com

Security note:
- Never commit your real API keys to Git. Use Streamlit secrets for hosted apps or environment variables for CI/CD and servers.
