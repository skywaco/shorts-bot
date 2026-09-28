🤖 Shorts Bot

An end-to-end AI-powered short-form video automation pipeline for generating, editing, and publishing YouTube Shorts and Instagram Reels.

Shorts Bot automates the repetitive parts of short-form content production. Instead of manually writing a script, finding footage, generating a voiceover, adding captions, editing the video, adding music, and uploading it, the bot connects these stages into one configurable workflow.

✨ What It Does

At a high level, Shorts Bot takes a content topic and turns it into a finished vertical short-form video.

Topic / Input
     ↓
AI Script Generation
     ↓
Sentence / Scene Breakdown
     ↓
 ┌───────────────┬────────────────┐
 ↓               ↓                ↓
Pexels        ElevenLabs      Scene Data
Footage       Voiceover           │
 └───────────────┴────────────────┘
                 ↓
          Video Composition
                 ↓
      ┌──────────┼──────────┐
      ↓          ↓          ↓
   Captions    Music     Formatting
      └──────────┼──────────┘
                 ↓
          Final Vertical Video
                 ↓
        ┌────────┴────────┐
        ↓                 ↓
     YouTube           Instagram
      Shorts             Reels
        └────────┬────────┘
                 ↓
          Excel Tracking

🚀 Features

🧠 AI Script Generation

Uses Groq with Llama to generate short-form scripts from the configured topic/content workflow.

The generation stage is designed around short-form content, with scripts that can be broken into individual scenes and matched with visual footage.

The AI provider is kept separate from the rest of the pipeline so it can be replaced or extended later.

🎙️ AI Voiceover Generation

Uses ElevenLabs to convert generated scripts into AI voiceovers.

The voiceover acts as an important timing reference for the rest of the video pipeline.

🎥 Automated Stock Footage Search

Uses the Pexels API to search for stock footage relevant to the generated scenes.

The workflow can:

Break the script into visual segments.

Generate/search for relevant visual terms.

Query Pexels.

Select usable footage.

Download clips.

Pass them into the rendering pipeline.

This removes a major manual step from short-form editing.

✂️ Automated Video Assembly

Uses FFmpeg and Python to combine the different media components.

The rendering pipeline can combine:

Stock footage

AI voiceover

Captions

Background music

Scene timing

Vertical formatting

Final encoding

The goal is to produce a ready-to-publish short without requiring manual editing software.

📝 Automatic Captions

The generated short includes synchronized captions based on the narration/timing information.

Captions make the content easier to follow when viewers watch without sound.

🎵 Background Music

The pipeline supports background music as an additional audio layer underneath the voiceover.

Music should remain a supporting element so that narration remains understandable.

📱 Vertical Short-Form Output

The project is designed for vertical short-form content, primarily targeting:

YouTube Shorts

Instagram Reels

📤 YouTube Upload Automation

Completed videos can be passed through the YouTube publishing workflow.

This reduces the need to manually upload every generated video.

📸 Instagram Publishing

The project also contains an Instagram publishing workflow.

The exact publishing requirements depend on the current Meta/Instagram API configuration, account permissions, and credentials.

📊 Content Tracking

The project uses Excel-based tracking to record information about generated/published content and automation runs.

This provides a simple way to keep track of the content pipeline without requiring a separate database.

🔄 Batch Processing

The automation is designed to process multiple pieces of content rather than requiring every video to be created manually.

This makes the project suitable for repeatable content-production workflows.

🛡️ Error Handling

Because the project depends on multiple external services, failures can happen at individual stages.

The workflow is structured so that failures can be identified and handled without unnecessarily rebuilding the entire pipeline.

Typical failure sources include:

API rate limits

Invalid credentials

Network errors

Missing stock footage

Voice generation failures

Video rendering errors

Platform publishing errors

🧩 Technology Stack

Component

Technology

Language

Python

AI / Script Generation

Groq + Llama

Text-to-Speech

ElevenLabs

Stock Footage

Pexels API

Video Processing

FFmpeg

Automation

Python

YouTube Publishing

YouTube API / OAuth

Instagram Publishing

Instagram / Meta API workflow

Tracking

Excel / .xlsx

Configuration

Environment variables

Version Control

Git + GitHub

🏗️ Architecture

The project follows a pipeline-based architecture:

                ┌─────────────────┐
                │  Topic / Input  │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ Script Generator│
                │   Groq / Llama  │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ Scene Breakdown │
                └───────┬─┬───────┘
                        │ │
              ┌─────────┘ └─────────┐
              ↓                     ↓
      ┌───────────────┐     ┌───────────────┐
      │ Pexels Search │     │  ElevenLabs   │
      │    Footage    │     │   Voiceover   │
      └───────┬───────┘     └───────┬───────┘
              │                     │
              └──────────┬──────────┘
                         ↓
                ┌─────────────────┐
                │ Video Rendering │
                │     FFmpeg      │
                └────────┬────────┘
                         ↓
             ┌───────────┼───────────┐
             ↓           ↓           ↓
          Captions     Music      Formatting
             └───────────┼───────────┘
                         ↓
                ┌─────────────────┐
                │  Final Video   │
                └────────┬────────┘
                         ↓
              ┌──────────┴──────────┐
              ↓                     ↓
        ┌────────────┐       ┌────────────┐
        │  YouTube   │       │ Instagram  │
        │   Shorts   │       │   Reels    │
        └────────────┘       └────────────┘
                         ↓
                ┌─────────────────┐
                │ Excel Tracking  │
                └─────────────────┘

The major advantage of this structure is modularity. Individual services can be replaced without rebuilding the entire application.

For example:

Groq
  ↓
Another LLM provider

ElevenLabs
  ↓
Another TTS provider

Pexels
  ↓
Another stock-media provider

Excel
  ↓
SQLite / PostgreSQL / Supabase

📁 Project Structure

A typical repository structure looks like:

shorts-bot/
│
├── main.py
├── config.py
├── requirements.txt
├── setup.bat
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
│
├── assets/
│   ├── music/
│   └── ...
│
├── output/
│   └── ...
│
├── logs/
│   └── ...
│
└── ...

The exact structure may evolve as the project develops.

The important architectural separation is between:

Configuration
Generation
Media
Rendering
Publishing
Tracking

⚙️ Requirements

Before running Shorts Bot, install:

Python 3.x

FFmpeg

Git

Internet access

Required API credentials

A Google/YouTube account if YouTube publishing is enabled

An appropriately configured Instagram/Meta account if Instagram publishing is enabled

🔑 API Services

Groq

Used for AI-powered script generation.

You need:

Groq API key

Access to the configured Llama model

ElevenLabs

Used for AI voice generation.

You need:

ElevenLabs API key

A configured voice

Appropriate API/account access

Pexels

Used to search for stock footage.

You need:

Pexels API key

YouTube

YouTube publishing requires the appropriate Google/YouTube API and OAuth configuration.

You will generally need the required Google Cloud project/API configuration and OAuth credentials for the publishing workflow.

Instagram

Instagram publishing requires the appropriate Meta/Instagram API setup and account permissions supported by the implementation.

Platform requirements can change, so verify the current Meta documentation before deploying the publishing component.

🔐 Environment Configuration

Never commit real credentials to GitHub.

Create a local .env file based on .env.example.

Example:

GROQ_API_KEY=your_groq_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
PEXELS_API_KEY=your_pexels_key_here

# Add platform-specific credentials required by your setup.

Your repository should contain:

.env.example

but should not contain:

.env

🚨 Security

This project interacts with several APIs and authentication systems.

Never commit:

API keys

Access tokens

Refresh tokens

OAuth client secrets

Google credentials

Instagram credentials

.env

Private certificates

Personal account information

Token/cache files

If a credential is accidentally pushed to GitHub, deleting the file is not enough. Treat the credential as compromised and rotate/revoke it through the relevant provider.

🛠️ Installation

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/shorts-bot.git
cd shorts-bot

Replace YOUR_USERNAME with your GitHub username.

2. Create a virtual environment

Windows

python -m venv venv
venv\Scripts\activate

macOS / Linux

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Install FFmpeg

Verify that FFmpeg is available:

ffmpeg -version

If the command is not recognized, install FFmpeg and add it to your system PATH.

5. Configure environment variables

Copy:

.env.example

to:

.env

Then add your actual credentials.

Never commit .env.

▶️ Running the Bot

After installing dependencies and configuring the required services:

python main.py

The repository also includes a Windows-oriented setup script where applicable:

setup.bat

🔁 End-to-End Workflow

Step 1 — Topic

The workflow begins with a configured topic/content idea.

Example:

5 Facts About Black Holes

Step 2 — AI Script

The AI layer generates a short-form narration.

Conceptually:

Hook
↓
Fact 1
↓
Fact 2
↓
Fact 3
↓
Fact 4
↓
Fact 5
↓
Ending / CTA

Step 3 — Scene Breakdown

The generated script is divided into visual segments.

This allows narration to be connected to visual search terms.

Sentence 1 → Visual 1
Sentence 2 → Visual 2
Sentence 3 → Visual 3
...

Step 4 — Footage Search

The bot searches Pexels for footage matching the scene requirements.

The clips are downloaded and prepared for rendering.

Step 5 — Voice Generation

The script is sent to ElevenLabs.

The generated audio becomes the primary narration track.

Step 6 — Timing

Voiceover duration/timing is used to determine how the visual sequence and captions should be synchronized.

Step 7 — Captions

Caption information is generated from the narration and timing.

Step 8 — Rendering

The video pipeline combines:

Footage
+
Voiceover
+
Captions
+
Music
+
Formatting

into one final video.

Step 9 — Export

The finished vertical video is saved to the configured output location.

Step 10 — Publishing

If publishing is enabled and the necessary authentication is configured, the video can be sent to supported platforms.

Step 11 — Tracking

Relevant information about the run/content is recorded in the project's Excel tracking system.

🎬 Video Pipeline

The rendering stage can be visualized as:

             ┌───────────────┐
             │  Video Clips  │
             └───────┬───────┘
                     │
             ┌───────▼───────┐
             │    FFmpeg     │
             │ Video Engine  │
             └───────┬───────┘
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      ▼              ▼              ▼
 Voiceover       Captions         Music
      │              │              │
      └──────────────┼──────────────┘
                     ↓
              Final Short/Reel

🎛️ Configuration

Keep environment-specific values and credentials in configuration/environment variables rather than hard-coding them into the source.

Typical configuration areas include:

AI provider/model

Voice settings

Video dimensions

Output directories

Pexels search settings

Music settings

Publishing settings

Logging/tracking

Batch-processing behavior

🧪 Testing

Because the project communicates with multiple external services, test each stage independently when debugging.

Recommended order:

1. Script generation
        ↓
2. Voice generation
        ↓
3. Pexels search/download
        ↓
4. Video rendering
        ↓
5. Captions
        ↓
6. Final export
        ↓
7. YouTube publishing
        ↓
8. Instagram publishing

This makes it much easier to locate the source of an error.

🐛 Troubleshooting

FFmpeg not found

Run:

ffmpeg -version

If this fails, install FFmpeg and make sure it is included in PATH.

API authentication error

Check:

.env exists

Variable names match the code

API key is valid

Account/API access is active

Required permissions are enabled

The credential has not expired or been revoked

Pexels returns no usable footage

Possible causes:

Search term is too specific

No suitable footage exists

API limit reached

Temporary API/network failure

A future version can implement multiple fallback queries or alternative stock providers.

ElevenLabs voice generation fails

Check:

API key

Voice configuration

Account/API limits

Input text

Network connection

YouTube upload fails

Check:

Google OAuth setup

API access

Required scopes

Authentication state

Channel permissions

Video metadata

Current YouTube API restrictions

Instagram publishing fails

Check:

Meta/Instagram API configuration

Account permissions

Access token

Media requirements

Public media URL requirements

Current Meta platform restrictions

🧠 Design Philosophy

The main idea behind Shorts Bot is:

Automate repetitive content-production work while keeping every major stage modular and replaceable.

Rather than creating one giant script that does everything, the application treats content creation as a pipeline:

Generation
    ↓
Processing
    ↓
Media Retrieval
    ↓
Voice
    ↓
Rendering
    ↓
Publishing
    ↓
Tracking

This makes the system easier to debug, maintain, extend, and scale.

🔌 Extensibility

The architecture can be expanded with additional services.

AI

OpenAI

Anthropic

Google Gemini

Local LLMs

Additional Groq models

Voice

OpenAI TTS

Google Cloud TTS

Azure Speech

Other TTS providers

Local TTS

Media

Pixabay

Shutterstock

Storyblocks

Other stock-media providers

Publishing

TikTok

Facebook

LinkedIn

X

Additional YouTube channels

Storage

SQLite

PostgreSQL

Supabase

Firebase

Cloud object storage

📈 Roadmap

Possible future improvements:

Web dashboard

Content scheduling

Queue-based job processing

Database-backed tracking

Multiple AI providers

Automatic retries with exponential backoff

Better footage relevance scoring

Advanced caption styling

Automatic thumbnail generation

Analytics collection

Performance dashboard

Multi-channel publishing

Cloud deployment

Docker support

Background workers

Content approval workflow

Content deduplication

Structured logging

Automated content-quality checks

⚠️ Current Limitations

Shorts Bot depends on external APIs, so its behavior is affected by those services.

Possible limitations include:

API rate limits

API pricing

Service downtime

Authentication requirements

YouTube/Instagram API changes

Stock footage availability

AI generation quality

Voice-generation limits

Rendering time

Internet connectivity

Platform publishing restrictions

For public-facing content, generated videos should be reviewed when factual accuracy, copyright, licensing, brand safety, or platform compliance matters.

⚖️ Copyright & Platform Responsibility

Shorts Bot is an automation tool.

The operator is responsible for:

The topics and prompts used

Generated content

Media used in videos

Music licensing

Copyright compliance

API usage

Platform policies

Community guidelines

Account security

Any applicable disclosure requirements

Always verify that media, music, voices, and other assets are permitted for the intended use.

🔒 Privacy

Depending on configuration, information may be sent to third-party services including:

Groq

ElevenLabs

Pexels

Google/YouTube

Meta/Instagram

Do not provide sensitive or confidential information to third-party services unless you have verified that doing so is appropriate.

🧑‍💻 Development Guidelines

When extending the project, keep responsibilities separated.

A useful mental model is:

Generation
     ↓
Processing
     ↓
Media
     ↓
Rendering
     ↓
Publishing
     ↓
Tracking

Prefer:

Environment variables
        +
Configuration
        +
Modular functions
        +
Reusable components

over hard-coded secrets and environment-specific values.

🤝 Contributing

Contributions, improvements, bug reports, and ideas are welcome.

Typical workflow:

git clone https://github.com/YOUR_USERNAME/shorts-bot.git

cd shorts-bot

git checkout -b feature/my-feature

# Make changes

git add .

git commit -m "Add my feature"

git push origin feature/my-feature

Then open a pull request.

When contributing:

Keep changes focused

Never commit secrets

Update documentation when behavior changes

Test affected functionality

Explain significant architectural changes

Avoid unnecessary breaking changes

📄 License

This project is distributed under the license included in this repository.

See LICENSE for the complete terms.

🙌 Acknowledgements

This project uses several technologies and services:

Python — automation and orchestration

Groq — AI inference

Meta Llama — language model

ElevenLabs — AI voice generation

Pexels — stock media

FFmpeg — media processing

YouTube API — video publishing

Instagram / Meta APIs — social publishing

⭐ Project Vision

Shorts Bot was built around a simple idea:

What if the repetitive production process behind short-form content could be turned into a programmable pipeline?

Instead of treating content creation as disconnected manual tasks, the project connects:

Idea
 ↓
AI
 ↓
Script
 ↓
Voice
 ↓
Visuals
 ↓
Captions
 ↓
Editing
 ↓
Rendering
 ↓
Publishing
 ↓
Tracking

The long-term direction is to evolve this pipeline into a more intelligent content-automation system where generation, editing, scheduling, publishing, analytics, and optimization can operate as connected services.

⭐ If You Find This Useful

If the project helps you or gives you ideas for your own automation workflows, consider giving the repository a ⭐ on GitHub.

Issues, suggestions, and improvements are welcome.

Built with Python, AI, automation, FFmpeg, and a lot of experimentation.
