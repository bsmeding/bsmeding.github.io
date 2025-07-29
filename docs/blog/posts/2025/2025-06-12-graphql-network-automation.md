---
authors: [bsmeding]
date: 2025-06-12
title: Supercharge Network Automation with GraphQL -> One Query to Rule Them All
tags: ["graphql", "network automation", "api", "jinja2", "opsmill", "nautobot"]
toc: true
layout: single
comments: true
---

# Supercharge Network Automation with GraphQL: One Query to Rule Them All

Network automation is evolving rapidly, and one of the most exciting developments is the adoption of **GraphQL** as a query language for APIs. Modern tools are embracing GraphQL, making it easier than ever to fetch exactly the data you need—no more chaining multiple REST API calls or wrestling with pagination. In this post, I'll show you how to leverage GraphQL for powerful, efficient [network automation](/index/#what-youll-find-here) workflows, with practical examples for platforms like [Nautobot](/blog/posts/tools/nautobot/), [OpsMill](/blog/posts/tools/opsmill/), and more.

<!-- more -->
---

## Why GraphQL for Network Automation?

Traditional [REST APIs](/blog/posts/tools/api/) are great, but they often require multiple calls to gather related data, and you may end up retrieving more (or less) than you actually need. **GraphQL** solves this by allowing you to:

- **Query exactly what you want**—no more, no less
- **Fetch deeply nested data in a single request**
- **Reduce network overhead and code complexity**
- **Easily introspect the API schema**

This is a game-changer for [network automation](/index/#what-youll-find-here), where you often need to build device configurations, inventory reports, or compliance checks from multiple data sources.

---

## Example: Fetching Device and Interface Data in One Query

Suppose you want to generate a configuration for a device, including all its interfaces and IP addresses. With REST, you'd need to:
- Get the device
- Get its interfaces (separate call)
- For each interface, get its IPs (more calls)

With GraphQL, it's just one query. Here’s an example using [Nautobot](/blog/posts/tools/nautobot/), but the pattern applies to any GraphQL-enabled platform:

```graphql
query {
  devices(name: "core-sw1") {
    name
    device_type { model }
    site { name }
    interfaces {
      name
      type
      enabled
      ip_addresses {
        address
      }
    }
  }
}
```

**Result:** You get a nested JSON structure with all the info you need, ready for [Jinja2 templating](/blog/posts/tools/jinja2/) or [Ansible automation](/blog/posts/tools/ansible/).

---

## Using GraphQL Data with Jinja2 for Config Generation

You can use the result of your GraphQL query directly in a [Jinja2](/blog/posts/tools/jinja2/) template to generate device configs. For example, in Python:

```python
import requests
from jinja2 import Template

# GraphQL endpoint and query
url = "https://your-platform.example.com/graphql/"
headers = {"Authorization": "Token <your_token>"}
query = '''
query {
  devices(name: "core-sw1") {
    name
    interfaces {
      name
      ip_addresses { address }
    }
  }
}
'''

response = requests.post(url, json={"query": query}, headers=headers)
data = response.json()["data"]["devices"][0]

# Jinja2 template
jinja_template = '''
hostname {{ name }}
{% for iface in interfaces %}
interface {{ iface.name }}
{% for ip in iface.ip_addresses %}  ip address {{ ip.address }}
{% endfor %}{% endfor %}
'''

print(Template(jinja_template).render(**data))
```

**Output:**
```
hostname core-sw1
interface GigabitEthernet0/1
  ip address 10.0.0.1/24
interface GigabitEthernet0/2
  ip address 10.0.1.1/24
```

For more on [Jinja2 templating in network automation](/tutorials/ansible_tutorial_1_concepts/), see our [Ansible tutorials](/tutorials/).

---

## More GraphQL Use Cases in Network Automation

- **Inventory Reports:** Fetch all devices, their roles, and statuses in one call.
- **Compliance Checks:** Query all interfaces with specific settings (e.g., shutdown, speed).
- **Topology Mapping:** Get all connections and build a live topology diagram.

### Example: Get All Devices in a Site (Generic GraphQL)
```graphql
query {
  devices(site: "ams-dc1") {
    name
    status
    device_type { model }
    primary_ip4 { address }
  }
}
```

For more inventory and compliance automation, check out our [network automation blog posts](/blog/index/) and [tutorials](/tutorials/).

---

## Beyond Nautobot: GraphQL in Other Network Automation Tools

[Nautobot](/blog/posts/tools/nautobot/) is just one example. Let’s look at how you can use GraphQL with other platforms.

### [OpsMill](/blog/posts/tools/opsmill/)
[OpsMill](/blog/posts/tools/opsmill/) is a modern network automation and orchestration platform that also exposes a GraphQL API. The approach is similar:

#### Example: Fetching Device Inventory from OpsMill
```graphql
query {
  devices(filter: { site: "ams-dc1" }) {
    name
    vendor
    model
    interfaces {
      name
      mac_address
    }
  }
}
```

#### Example: Python Script to Query OpsMill
```python
import requests

url = "https://opsmill.example.com/graphql/"
headers = {"Authorization": "Bearer <your_token>"}
query = '''
query {
  devices(filter: { site: "ams-dc1" }) {
    name
    vendor
    model
    interfaces { name mac_address }
  }
}
'''

resp = requests.post(url, json={"query": query}, headers=headers)
data = resp.json()["data"]["devices"]
print(data)
```

### Other Tools
- **[NetBox](/blog/posts/tools/netbox/) (with plugins):** Some NetBox plugins add GraphQL endpoints.
- **Custom APIs:** Many modern automation platforms are adding GraphQL support—check your tool’s docs!

---

## GraphQL vs. REST: Why It Matters

| Feature         | [REST API](/blog/posts/tools/api/)         | GraphQL API      |
|-----------------|------------------|------------------|
| Data granularity| Fixed endpoints  | Query exactly what you want |
| Nested data     | Multiple calls   | Single call      |
| Schema introspect| Limited         | Built-in         |
| Overfetch/Underfetch | Common      | Rare             |
| Tooling         | Mature           | Rapidly growing  |

**Bottom line:** GraphQL lets you build more efficient, maintainable, and powerful [automation workflows](/index/#what-youll-find-here).

---

## Tips for Using GraphQL in Network Automation

- **Explore the Schema:** Use tools like GraphiQL or Insomnia to browse available queries and fields.
- **Combine with Templating:** Use [Jinja2](/blog/posts/tools/jinja2/), [Nornir](/blog/posts/tools/nornir/), or [Ansible](/blog/posts/tools/ansible/) to turn GraphQL data into configs or reports.
- **Batch Operations:** Fetch all needed data in one go—great for large-scale automation.
- **Error Handling:** Check for errors in the GraphQL response (`response["errors"]`).
- **Authentication:** Use API tokens or OAuth as required by your platform.

---

## Conclusion

GraphQL is transforming how we interact with [network automation platforms](/index/#what-youll-find-here). Whether you’re using [Nautobot](/blog/posts/tools/nautobot/), [OpsMill](/blog/posts/tools/opsmill/), or another modern tool, GraphQL lets you:
- Fetch all the data you need in a single, efficient call
- Eliminate complex REST call chains
- Power up your automation with templating and reporting

**Ready to try it?** Start by exploring your tool’s GraphQL endpoint, build a query, and see how much easier your automation can be! For more inspiration, browse our [automation blog](/blog/index/) and [tutorials](/tutorials/).

---

## References & Further Reading
- [GraphQL Official Site](https://graphql.org/)
- [Nautobot GraphQL Docs](https://docs.nautobot.com/projects/core/en/stable/rest-api/graphql/)
- [OpsMill Documentation](https://opsmill.com/docs)
- [Jinja2 Templating](https://jinja.palletsprojects.com/)
- [Python requests Library](https://docs.python-requests.org/)
- [Network Automation Tutorials](/tutorials/)
- [Ansible Tool Overview](/blog/posts/tools/ansible/)
- [API Tool Overview](/blog/posts/tools/api/)

---

## Feedback

Have you used GraphQL in your network automation projects? Share your experiences or questions in the comments, or connect with me on [LinkedIn](https://www.linkedin.com/in/bartsmeding/). For more content, check out our [blog](/blog/index/) and [network automation resources](/index/#what-youll-find-here). 