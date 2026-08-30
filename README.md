Your personal AI tutor that generates questions from your syllabus PDF and asks them with natural voiceover. Perfect for exam preparation and active recall practice.

## Video tooling

This project uses [`claude-real-video`](https://github.com/HUANGCHIHHUNGLeo/claude-real-video) (`crv`) so AI agents can watch and transcribe video content (e.g. reviewing recorded lectures) as part of building the tutor.

```bash
pip install -r requirements.txt   # or: pip install "claude-real-video[whisper]"
```

The agent skill that documents how to use `crv` lives in `.agents/skills/claude-real-video-for-agents/` (symlinked for Claude Code under `.claude/skills/`).
