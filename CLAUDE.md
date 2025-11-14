# CLAUDE.md - AI Assistant Guide for awesome-flutter

**Last Updated**: 2025-11-14
**Repository**: awesome-flutter
**Type**: Curated Resource List (Awesome List)
**License**: CC0 1.0 Universal (Public Domain)

---

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Codebase Structure](#codebase-structure)
3. [Critical File Management Rules](#critical-file-management-rules)
4. [Content Organization](#content-organization)
5. [Development Workflows](#development-workflows)
6. [Formatting Conventions](#formatting-conventions)
7. [Contribution Guidelines](#contribution-guidelines)
8. [Quality Control Standards](#quality-control-standards)
9. [AI Assistant Best Practices](#ai-assistant-best-practices)

---

## Repository Overview

### Purpose
This is a **curated list of Flutter resources** following the "Awesome List" standard. It aggregates:
- Articles (tutorials, how-tos, advanced topics)
- Videos and educational content
- UI components and widgets
- Plugins and packages
- Frameworks and architectural patterns
- Open-source applications
- Development tools and utilities
- Community resources

### Key Characteristics
- **Community-Driven**: Accepts contributions from Flutter developers worldwide
- **Quality-Focused**: Enforces strict formatting and content standards
- **Dynamic Metrics**: Tracks GitHub stars, Medium claps, and YouTube engagement
- **Template-Based**: Uses a two-file system for content management

### Maintainer
- **Primary**: Robert Felker ([LinkedIn](https://www.linkedin.com/in/robert-felker/))
- **Current Fork**: ParkChongsam/awesome-flutter

---

## Codebase Structure

```
/home/user/awesome-flutter/
├── .git/                           # Git repository data
├── .github/
│   └── pull_request_template.md   # PR template for contributors
├── .gitattributes                  # Git language detection configuration
├── README.md                       # ⚠️ AUTO-GENERATED - DO NOT EDIT
├── contributing.md                 # Contribution guidelines
└── source.md                       # ✅ SOURCE OF TRUTH - EDIT THIS FILE
```

### File Purposes

| File | Purpose | Editable |
|------|---------|----------|
| **source.md** | Template file with placeholders for dynamic metrics | ✅ YES - Edit this file |
| **README.md** | Public-facing file with populated metrics | ❌ NO - Auto-generated |
| **contributing.md** | Guidelines for contributors | ⚠️ Rarely modified |
| **.gitattributes** | Marks README.md as generated, sets language to Dart | ⚠️ Configuration file |
| **.github/pull_request_template.md** | PR template reminder | ⚠️ Rarely modified |

---

## Critical File Management Rules

### ⚠️ MOST IMPORTANT RULES FOR AI ASSISTANTS

1. **NEVER EDIT README.md DIRECTLY**
   - README.md is AUTO-GENERATED from source.md
   - All changes MUST be made to source.md
   - Editing README.md will be overwritten and PRs will be rejected

2. **ALWAYS USE source.md FOR CONTENT CHANGES**
   - Add new resources to source.md
   - Update descriptions in source.md
   - Modify categories in source.md
   - Use placeholders for dynamic metrics (see below)

3. **UNDERSTAND THE PLACEHOLDER SYSTEM**

   Source.md uses special markers that get replaced during generation:

   ```markdown
   <!-- In source.md -->
   [Repository Name](link) <!--stargazers:owner/repo--> - Description

   <!-- Becomes in README.md -->
   [Repository Name](link) [1651⭐] - Description
   ```

   **Placeholder Types**:
   - `<!--stargazers:owner/repo-->` → GitHub star count `[1651⭐]`
   - `<!--claps:article-path-->` → Medium claps `[1.1K claps👏]`
   - `<!--youtube:video/id-->` → YouTube stats `[72🎬]` or `[430👍]`
   - `@stackoverflow@` → StackOverflow badge count
   - `@repositories@` → Total GitHub repositories count
   - `@items@` → Total items in list count

### When to Use Placeholders

```markdown
✅ CORRECT (source.md):
- [Flutter Examples](https://github.com/nisrulz/flutter-examples) <!--stargazers:nisrulz/flutter-examples--> - Simple basic isolated apps

❌ WRONG (source.md):
- [Flutter Examples](https://github.com/nisrulz/flutter-examples) [1651⭐] - Simple basic isolated apps

✅ CORRECT (source.md):
- [Google IO 2018](link) <!--claps:flutter-io/building-beautiful-flexible-user-interfaces--> - Building beautiful UIs

❌ WRONG (source.md):
- [Google IO 2018](link) [1.1K claps👏] - Building beautiful UIs
```

---

## Content Organization

### Category Hierarchy

The repository is organized into these main sections:

1. **Articles**
   - Begin with (introductory content)
   - Tutorial
   - Howtos
   - Websites / Blogs
   - Advanced

2. **Videos**
   - Educational series
   - Tutorial channels
   - Live coding sessions

3. **Components**
   - Demonstrations
   - UI (Sticky Headers, Radial Menus, Tinder Cards, etc.)
   - Input widgets
   - Material Design components
   - Effects (animations, transitions)
   - Lists (grid views, drag & drop)
   - Calendars
   - Images
   - Maps
   - Charts

4. **Navigation**
   - Routers
   - Page indicators
   - Swipers

5. **Auth**
   - Local authentication
   - OAuth providers
   - Social logins

6. **Text & Rich Content**
   - Markdown renderers
   - Rich text editors
   - Masked inputs

7. **Analytics**
   - Google Analytics
   - Firebase Analytics
   - Third-party analytics

8. **Build Automation**
   - CI/CD configurations
   - Testing frameworks

9. **Styling**
   - Theme explorers
   - Color utilities

10. **Media**
    - Audio (players, recorders)
    - Video (WebRTC, players)
    - Voice (speech recognition)

11. **Storage**
    - Firebase Storage
    - Secure storage
    - Databases

12. **Monetization**
    - AdMob
    - In-app purchases
    - Payment integrations

13. **Templates**
    - UI kits
    - Complete app templates
    - Design patterns

14. **Machine Learning**
    - ML Kit integrations
    - IBM Watson

15. **Plugins**
    - Device (WebView, Location, Notifications)
    - Scanner (QR codes)
    - Bluetooth / NFC / Beacon
    - Storage (SQLite, MMKV)
    - Services (Dialogflow, OneSignal, Intercom)

16. **Frameworks**
    - Bloc
    - Redux / ELM / Dependency Injection
    - Data management
    - Animation frameworks
    - Game engines

17. **Open Source Apps**
    - Example applications
    - Games
    - Production apps

18. **Utilities**
    - Development tools
    - Desktop embedding

19. **Community**
    - Forums
    - Chat groups
    - GitHub organizations

20. **Books**
    - Published Flutter books

21. **Bonus**
    - Miscellaneous resources
    - Fun content

---

## Development Workflows

### Adding a New Resource

1. **Identify the Correct Category**
   - Find the most appropriate section in source.md
   - If no category fits, suggest a new one

2. **Format the Entry Correctly**
   ```markdown
   - [Resource Name](https://link-to-resource) <!--stargazers:owner/repo--> - Brief description by [Author Name](https://author-link)
   ```

3. **Add to Bottom of Category**
   - New entries go at the END of their category
   - Maintain alphabetical order within subcategories if applicable

4. **Include Visual Documentation**
   - For UI components: Include screenshots or GIFs
   - Link to visual demos when available

5. **Use Placeholders for Metrics**
   - GitHub repos: `<!--stargazers:owner/repo-->`
   - Medium articles: `<!--claps:author/article-slug-->`
   - YouTube videos: `<!--youtube:video/video-id-->`

### Example Addition

```markdown
### UI

<!-- Existing entries... -->

- [Your Widget Name](https://github.com/username/repo) <!--stargazers:username/repo--> - Short description of what it does by [Author Name](https://github.com/username)
```

### Paid Solutions Policy

Paid solutions are accepted ONLY if they offer:
- Free tier for open source projects, OR
- Limited features for personal developers (not time-limited)

**Rationale**: "Fair is fair" - resources should be accessible to the Flutter community

---

## Formatting Conventions

### Standard Format

```markdown
- [Title](URL) <!--placeholder--> - Description by [Author](author-url)
```

### Rules

1. **Title Casing**: Use AP style title case
   ```markdown
   ✅ "Building Beautiful User Interfaces"
   ❌ "Building beautiful user interfaces"
   ❌ "Building Beautiful User Interfaces With Flutter"
   ```

2. **Descriptions**:
   - Start with a capital letter
   - Keep it short and descriptive (1-2 lines max)
   - Don't mention "Flutter" in every description (it's implied)
   - Focus on what makes the resource unique

3. **Author Attribution**:
   ```markdown
   by [Full Name](link-to-profile)
   ```
   - Always include author when known
   - Link to GitHub, Twitter, or personal site

4. **URLs**:
   - Use HTTPS when available
   - GitHub links should point to main repo page
   - Article links should be direct URLs

5. **No Trailing Whitespace**:
   - Configure your editor to remove trailing spaces

### Metric Display (README.md only)

After generation, metrics appear as:
- GitHub: `[1651⭐]`
- Medium: `[1.1K claps👏]`
- YouTube views: `[430👍]`
- YouTube videos: `[72🎬]`

---

## Contribution Guidelines

### Commit Messages

✅ **Good Commit Messages**:
```
Add Flutter Hooks package to Components/State Management
Update Firebase Auth documentation link
Fix typo in Animation section
Add new ML Kit integration example
```

❌ **Bad Commit Messages** (Will be rejected):
```
Update
Fix
Changes
asdf
.
```

### Pull Request Requirements

1. **Meaningful Title**: Describe what you're adding/changing
2. **Individual PRs**: One resource per pull request
3. **Search First**: Check for duplicates before submitting
4. **Test Your Links**: Ensure all URLs work
5. **Documentation**: Package should be documented
6. **Quality**: Resource should be tested and functional

### Pull Request Template

When creating a PR, you'll see:
```markdown
You've read How to contribute right?

So tell me more about your awesome contribution and add the badge
to your repo after it's accepted :D

[Awesome Flutter Badge Code]
```

---

## Quality Control Standards

### Content Quality Checklist

- [ ] Resource is relevant to Flutter development
- [ ] Links are functional and point to correct destinations
- [ ] Description is clear and concise
- [ ] Author attribution is included (when applicable)
- [ ] Format follows the style guide
- [ ] No spelling or grammar errors
- [ ] Added to correct category
- [ ] Placed at bottom of category
- [ ] Uses appropriate placeholder for metrics
- [ ] Screenshots/GIFs included for UI components

### What Gets Rejected

❌ **Rejected Submissions**:
- Editing README.md instead of source.md
- Non-meaningful commit messages
- Duplicate entries
- Broken links
- Paid-only solutions without free tier
- Poorly documented resources
- Off-topic content
- Spam or self-promotion without value

✅ **Accepted Submissions**:
- Well-documented packages
- Quality tutorials and articles
- Useful tools and utilities
- Open-source applications
- Properly formatted entries
- Unique, valuable resources

---

## AI Assistant Best Practices

### When Helping Users

1. **Always Check Which File to Edit**
   ```
   User: "Add this package to the list"
   AI: *Edits source.md, NOT README.md*
   ```

2. **Use Correct Placeholders**
   ```markdown
   <!-- For GitHub repos -->
   <!--stargazers:owner/repo-->

   <!-- For Medium articles -->
   <!--claps:@author/article-slug-->

   <!-- For YouTube -->
   <!--youtube:video/VIDEO_ID-->
   ```

3. **Verify Category Placement**
   - Read the existing content to understand category purpose
   - Place in most specific applicable category
   - Suggest new category if nothing fits

4. **Format Consistently**
   - Match existing formatting exactly
   - Pay attention to spacing, capitalization, punctuation
   - Use same structure as surrounding entries

5. **Quality Over Quantity**
   - One well-formatted entry is better than multiple rushed ones
   - Verify links before adding
   - Write meaningful descriptions

### Example Interaction

```
User: "Add the flutter_hooks package to the list"

AI Response:
I'll add flutter_hooks to source.md in the appropriate category.

[Searches source.md for best category]
[Finds "Frameworks" or creates "State Management" section]
[Formats entry with placeholder]
[Adds to bottom of category]
[Verifies formatting matches existing entries]

Added to source.md at line XXX:
- [Flutter Hooks](https://github.com/rrousselGit/flutter_hooks)
  <!--stargazers:rrousselGit/flutter_hooks--> - React hooks
  implementation for Flutter by [Remi Rousselet](https://github.com/rrousselGit)
```

### Common Mistakes to Avoid

❌ **Don't**:
- Edit README.md
- Add hard-coded star counts
- Skip author attribution
- Use incorrect title casing
- Add to top of category
- Include "Flutter" redundantly in descriptions
- Create vague descriptions
- Forget placeholders for GitHub repos

✅ **Do**:
- Edit source.md
- Use placeholder comments
- Include author with link
- Use AP style title case
- Add to bottom of category
- Write concise, specific descriptions
- Include appropriate placeholders
- Verify formatting matches repository style

### Testing Changes

Before committing:
1. **Verify file**: Changed source.md, not README.md
2. **Check placeholders**: Correct format for metric type
3. **Validate links**: All URLs accessible
4. **Review formatting**: Matches existing entries
5. **Read description**: Clear, concise, capital first letter
6. **Check author**: Name and link included
7. **Confirm category**: Most appropriate section
8. **Position**: Added to bottom of category

---

## Git Workflow for AI Assistants

### Current Branch
```bash
claude/claude-md-mhzhxaqj4gn62ecb-01HJsTCMiSp5xTMW16Gjnq5i
```

### Commit Pattern

```bash
# Good commit workflow
git add source.md
git commit -m "Add Flutter Hooks to Frameworks section"
git push -u origin claude/claude-md-mhzhxaqj4gn62ecb-01HJsTCMiSp5xTMW16Gjnq5i
```

### What Not to Commit

- ❌ README.md (unless explicitly generating)
- ❌ Temporary files
- ❌ Editor configurations
- ❌ Personal notes

### What to Commit

- ✅ source.md modifications
- ✅ contributing.md updates (rare)
- ✅ New documentation (if adding)

---

## Metadata Reference

### Badge Placeholders in source.md

```markdown
<img alt="StackOverflow" src="https://img.shields.io/badge/StackOverflow-@stackoverflow@-orange.svg" />
<img alt="Repos" src="https://img.shields.io/badge/Repos-@repositories@-brightgreen.svg" />
<img alt="Entries" src="https://img.shields.io/badge/Items-@items@-lightgrey.svg" />
```

These get replaced with actual counts during generation.

### Repository Statistics (as of last update)

- **Total Markdown Files**: 3 (source.md, README.md, contributing.md)
- **Total Lines**: ~955 across all markdown files
- **Total Entries**: 234+ Flutter resources
- **Categories**: 20+ main categories
- **Dynamic Metrics Tracked**: 188+ placeholders

---

## Quick Reference Card

### File to Edit
| Task | File |
|------|------|
| Add resource | `source.md` |
| Update description | `source.md` |
| Fix typo | `source.md` |
| Change category | `source.md` |
| Update guidelines | `contributing.md` |
| **Never edit** | ~~README.md~~ |

### Placeholder Syntax
| Platform | Syntax |
|----------|--------|
| GitHub | `<!--stargazers:owner/repo-->` |
| Medium | `<!--claps:@author/article-slug-->` |
| YouTube | `<!--youtube:video/VIDEO_ID-->` |
| StackOverflow Badge | `@stackoverflow@` |
| Repositories Badge | `@repositories@` |
| Items Badge | `@items@` |

### Entry Format
```markdown
- [Title](URL) <!--placeholder--> - Description by [Author](author-url)
```

### Where to Add
- **Position**: Bottom of category
- **File**: source.md
- **Format**: Match existing entries
- **Test**: Verify all links work

---

## Troubleshooting

### Issue: PR Rejected with "Don't edit README"
**Solution**: You edited README.md instead of source.md. Redo changes in source.md.

### Issue: Metrics not showing
**Solution**: Ensure you used placeholder comments, not hard-coded values.

### Issue: Formatting looks different
**Solution**: Check spacing, capitalization, and compare with nearby entries.

### Issue: Not sure which category
**Solution**: Search source.md for similar resources and add to same category.

### Issue: Commit message rejected
**Solution**: Use descriptive message explaining what you added/changed.

---

## Additional Resources

- **Contribution Guidelines**: `/home/user/awesome-flutter/contributing.md`
- **PR Template**: `/home/user/awesome-flutter/.github/pull_request_template.md`
- **Source File**: `/home/user/awesome-flutter/source.md`
- **Code of Conduct**: [Spring Framework CoC](https://github.com/spring-projects/spring-framework/blob/master/CODE_OF_CONDUCT.adoc)

---

## Summary for AI Assistants

**Remember These Critical Points**:

1. ✅ **EDIT source.md** - Never README.md
2. 📝 **USE PLACEHOLDERS** - For stars, claps, views
3. 📍 **ADD TO BOTTOM** - Of relevant category
4. 🎨 **MATCH FORMAT** - Exactly like existing entries
5. 💬 **MEANINGFUL COMMITS** - Describe what you're adding
6. 🔗 **TEST LINKS** - Before committing
7. 👤 **ATTRIBUTE AUTHORS** - Include name and link
8. 📖 **TITLE CASE** - AP style for titles
9. 🎯 **RIGHT CATEGORY** - Most specific applicable section
10. ✨ **QUALITY FIRST** - Well-formatted > rushed

---

**End of CLAUDE.md** | Generated: 2025-11-14 | Repository: awesome-flutter
