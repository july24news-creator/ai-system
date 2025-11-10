# AI System Android Client (Simple)

This Android project is a minimal client that sends prompts to the AI server (FastAPI /predict endpoint) and shows the generated text.

Features
- Simple UI: prompt input + send button
- Async HTTP calls using OkHttp + Kotlin coroutines
- Builds a debug APK via GitHub Actions (.github/workflows/android-build.yml)

How to use
1. Configure server address:
   - In the app UI enter the server base URL (e.g. https://your-server.com)
   - Or set AI_SERVER_URL environment property in the build if needed.

2. Build locally:
   - Open `app-android` in Android Studio.
   - Let Gradle sync, then Run -> Build APK(s).

3. Build via GitHub Actions:
   - The workflow will produce a debug APK artifact. Download it from the Actions run.

Notes
- This client only calls a remote server. Running heavy models locally on Android is not recommended.
- For production, implement secure authentication (API keys, HTTPS, rate limits).