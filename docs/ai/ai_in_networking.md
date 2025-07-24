# AI in Networking: From Insight to Action

Artificial Intelligence (AI) is rapidly transforming the networking world. What once required teams of engineers sifting through logs, running scripts, and checking configurations can now be accelerated, enhanced, and even autonomously handled by AI agents.

In this blog post, we’ll explore the role of AI in networking, how it can interact with modern systems like [Nautobot](https://nautobot.com/) (as a CMDB and automation platform), and what it takes to build AI agents that can query network data and interact with real devices.

---

## 🤖 What Can AI Do in Networking?

At a high level, AI in networking can be applied to the following areas:

- **Observability & Monitoring**: AI can detect anomalies in traffic, predict failures, and surface insights from logs and metrics.
- **Intent Verification**: AI can continuously validate that the network is behaving as intended based on policy.
- **Natural Language Querying**: Users can ask questions like _"Which switches in Site A are running outdated firmware?"_
- **Automated Troubleshooting**: AI agents can run diagnostic commands and summarize results.
- **Autonomous Configuration**: Based on input or learned behavior, AI can generate and apply configurations safely.

---

## 🔗 Interacting with Nautobot (CMDB)

[Nautobot](https://github.com/nautobot/nautobot) is a powerful source of truth for network infrastructure. With its robust API and plugin architecture, it becomes an ideal partner for AI-driven systems.

### Use Case: AI Agent to Query Nautobot

Imagine a conversational AI agent that can answer questions like:

- "List all devices at the **Berlin** site."
- "Which devices haven’t been backed up in the last 24 hours?"
- "Are there any devices with a lifecycle end-of-support date within the next 6 months?"

#### How It Works

1. **Natural Language Parsing**: The AI model parses user input and identifies intent and entities (e.g., site name, device type).
2. **Nautobot API Interaction**: The agent translates this into a Nautobot GraphQL or REST API query.
3. **Response Generation**: The AI formats and returns the response in a human-readable way, optionally with links to Nautobot UI.

> Bonus: With plugins like **Nautobot ChatOps**, AI can even interact via Slack or MS Teams!

---

## ⚙️ Interacting with Network Devices

While Nautobot tells us **what should be**, interacting with devices reveals **what is**.

AI can connect to devices using SSH, NETCONF, or REST APIs to:

- Check software versions
- Verify interface statuses
- Review BGP neighbors
- Collect configuration snippets

### Use Case: AI Agent for Device Inspection

You could create an AI agent with the ability to:

- Connect to a switch via SSH
- Run commands like `show version` or `show interface status`
- Compare the output against Nautobot’s intended state
- Flag mismatches or recommend actions

### Tooling Options

- **NAPALM**: Multi-vendor abstraction for reading from devices
- **Scrapli**: Flexible Python library for interacting with CLI devices
- **Netmiko / Paramiko**: Lower-level SSH options

> Pro Tip: Create reusable prompt templates to tell your AI agent what commands to run based on device type or vendor.

---

## 🧠 Building AI Agents for Networking

### Architecture Overview

1. **Frontend Interface** (optional): A chatbot or web UI for input/output
2. **LLM Core**: A language model like GPT-4, Claude, or open-source LLM
3. **Toolset Plugins**: Custom functions that allow the LLM to call APIs or connect to devices
4. **Memory Store** (optional): Save past interactions, common queries, device state snapshots

### Popular Frameworks

- **LangChain / LlamaIndex**: For building tool-using agents with memory
- **Semantic Kernel**: For .NET/C# ecosystems
- **AutoGen**: Agent-to-agent collaboration framework from Microsoft

---

## 🛠 Example Prompts for Your AI Agent

```text
> What devices are in site "NYC-Core"?
→ [AI agent calls Nautobot GraphQL API]

> Login to router R1 and check if interface Gi0/1 is up.
→ [AI agent calls a function that uses Scrapli to connect and parse output]

> Create a summary of all devices with CVEs in the last 90 days.
→ [Agent queries Nautobot Software Inventory + CVE plugins]

```
See [Youtube channel of John Capobianco](https://www.youtube.com/@johncapobianco2527) for examples of AI agents interacting with network devices


---

## 🔒 Security Considerations

While AI adds power and flexibility, it also introduces risk:

- Never give unrestricted shell access to an LLM
- Use strict function calling with clearly scoped permissions
- Validate all input/output when interacting with devices

---

## 🧩 Final Thoughts

AI in networking isn’t about replacing engineers — it’s about **amplifying their abilities**. By combining natural language understanding, structured APIs like Nautobot’s, and secure device communication, we can build intelligent agents that answer questions, identify issues, and even take action.

The future is already here. It's time to start experimenting.

---

## 📚 Further Reading
- [John Capobianco YouTube channel](https://www.youtube.com/@johncapobianco2527)
- [Nautobot Docs](https://docs.nautobot.com/)
- [LangChain for Python](https://python.langchain.com/)
- [NAPALM Project](https://github.com/napalm-automation/napalm)
- [Scrapli](https://github.com/carlmontanari/scrapli)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)