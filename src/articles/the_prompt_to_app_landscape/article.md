---
description: What I think about when I think about building
publish_date: '2026-08-30'
title: The Prompt-to-App Landscape
---

# The Prompt-to-App Landscape

I've been building a piece of open source software called [Exhibit](https://github.com/momja/Exhibit). It's all about leveraging AI for making and using small apps that make your life better. It's become the first thing I reach for when I need to solve a problem, whether it be a one-off or evergreen task, Exhibit's artifacts can help me solve it.

As I try to understand how _others_ may find this useful, I've been taking a look at the landscape of prompt-to-app tools. Here are some notes on products in the space, and at the end I'll outline why I still think Exhibit is worth building.

### [Val Town](https://val.town)

> Val Town is how developers and operators instantly ship websites, automations, and [other tools](https://www.val.town/discover) to live URLs.

Val Town is very cool. They've done a lot of work to safely run AI-generated code in a sandboxed cloud environment. As of right now, Exhibit has no comparable server-side solution, as Artifacts are designed to be client-heavy, server-light. Exhibit's servers are primarily responsible for providing data synchronization across devices. This client-first approach means Exhibit cannot do all the fancy server stuff, like schedule actions or server-side integrations with other platforms. This constraint also buys Exhibit's artifacts immense flexibility. An artifact does not contain proprietary code. It's not complicated. It's a single .html file that you can copy and run anywhere. Also while Val Town is built for engineers, with technical language and tools, Exhibit aims to be for anyone.

### [v0](https://v0.app)

> v0 is an AI agent that helps anyone create real code and full-stack apps and agents.
> Ship features, refine designs, update copy, and create live prototypes, all with a prompt. Deploy to production immediately, or open a pull request for review.

v0 seems very capable at building full-fledged production applications and websites. It has all sorts of integrations and the expertise of Vercel behind it.

The site has an embedded VsCode editor, so you can manually view and edit the source. You can connect to a variety of databases, AI providers, sync with a github repo, and more. Of course, this is a Vercel product, so it's clearly focused on React and Next.js.

### [Lovable](https://lovable.com)

> Bring a new product, internal tool, or entire company to life.

Lovable is maybe the most separated from the world of engineering in terms of it's UX. I would say it leans heavily into vibe coding, with a focus on tools geared at helping people build businesses or commercial solutions.

### [Replit](https://replit.com)

> Turn ideas into apps in minutes — no coding needed

Replit has a full prompt-to-app pipeline, but you can also go deeper with their cloud IDE if you want to do more traditional engineering. From what I've read, Replit seems a bit more accessible in terms of source code about what's being built under the hood than, say, Lovable.

## More Prompt-to-app Software
- [Bolt.new](https://bolt.new)
- [Phoenix.new](https://phoenix.new)
- [Emergent](https://app.emergent.sh/)
- [Rork](https://rork.com)
- [Glide](https://glide.app)

## Why Build Exhibit?
Clearly there are a _lot_ of similar products in this space. That may at times feel discouraging. Lucky for me, right now I'm just building Exhibit for fun. So if no one else ever uses it, no harm done! Despite my freeing attitude, I do think Exhibit stands out for a couple reasons.

**Zero lock-in**: Exhibit is the most flexible of all these, because it's the simplest. There's no 'magic sauce' to an artifact, it's just HTML/CSS/JS, and as of right now, it's always a single file. That means you can download that file, run it locally, email it to your buddy, or take it to a different Exhibit instance. I think all these other platforms don't hide the source code for your project, but I believe they hope to keep you on their platform with their deployment infrastructure.

**No Servers Necessary**: If I just want to share a grocery shopping app with my family, why do I need to setup a database? That's actually where I first bounced off v0, because I couldn't get [Neon](https://neon.com/) to work out of the box and I gave up. Exhibit doesn't do that. It just uses [localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage), a standardized web API. If I really want to defend Exhibit's existence, I should tell you we do have a _little_ magic here, in that an artifact's localStorage is proxied to Exhibit's servers, so you get the same state in your artifacts, regardless of which device/browser you use. It's simple, but you can do a lot with it. If it's just an application for yourself, or a few other people, you probably don't _need_ a real database!

**Front-End Security:** Running untrusted code is a security risk. Exhibit runs Artifacts in a sandboxed iframe with a user-adjustible security policy. Say you have a really private Artifact, like a health tracker for your newborn. You _don't_ want that having any way of getting exposed to someone else on the internet. That's no problem with Exhibit. Just specify which websites you want to allow your Artifact to reach out to, and everything is blocked by default. This is a common risk with AI-generated code, as tricks like [prompt injection](https://owasp.org/www-community/attacks/PromptInjection) can spoil your agent into writing source code that may _try_ to leak your data. A sandbox helps prevent that worst-case scenario from happening.

**Self Host**: None of these other options are self-hostable. You can [deploy Exhibit yourself](https://github.com/momja/Exhibit/blob/main/docs/deployment.md) to truly own your software.

If you read this, let me know what you want to see from Exhibit! It's early days, I barely have a demo ready. If you _would_like to try it, you can [host it](https://github.com/momja/Exhibit/blob/main/docs/deployment.md) yourself, or send me an [email](mailto:me@maxomdal.com) for the hosted demo.