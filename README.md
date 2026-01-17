# LLMBox (ARCHIVED)

> **Status:** ARCHIVED - Patterns extracted to `@ankr/ai-router`

## Deprecation Notice

This repository has been **archived** as of January 2026. The Indic language routing and cost tracking patterns have been extracted and integrated into `@ankr/ai-router` v2.2.

### What was extracted:

| Component | Destination | Status |
|-----------|-------------|--------|
| Indic Language Detection | `@ankr/ai-router/indic.ts` | Integrated |
| Provider Fallback Chain | `@ankr/ai-router` | Already existed |
| Cost Tracking | `@ankr/ai-router/indic.ts` | Integrated |
| Caching Patterns | `@ankr/ai-router` | Already existed |

### Where to go now:

- **Main Monorepo:** [github.com/rocketlang/ankr-labs-nx](https://github.com/rocketlang/ankr-labs-nx)
- **AI Router Package:** `ankr-labs-nx/packages/ai-router`
- **Usage:**
  ```typescript
  import {
    detectLanguage,
    isIndicLanguage,
    prioritizeIndicProviders
  } from '@ankr/ai-router';
  ```

### Original Purpose

LLMBox was a Python library for "Bringing AI to the common man" with:

- Multi-provider routing (Groq, Ollama, DeepSeek, OpenRouter, LongCat)
- Indic language detection and preference
- Automatic fallback chain
- Cost tracking per request
- Response caching

### Why TypeScript?

The ANKR ecosystem is TypeScript-first. The Python patterns were ported to TypeScript for consistency with `@ankr/ai-router`.

---

*Archived by ANKR Labs | January 2026*
