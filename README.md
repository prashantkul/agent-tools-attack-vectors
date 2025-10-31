# Agent Tools Attack Vectors Lab

This repository contains security labs for exploring agent tool attack vectors.

## 🤖 GitHub Actions Automation

This repository includes automated workflows to help with lab creation:

### Issue to Lab Workflow

When you create or edit an issue, the workflow automatically:

1. **Creates a lab branch** named `lab/issue-{number}`
2. **Saves issue content** to `.lab-issues/issue-{number}.md`
3. **Posts a comment** with instructions for working on the lab

### How to Use

1. **Create a GitHub Issue** with your lab requirements
2. **Wait for the automation** to create a branch and save the issue content
3. **Work with Claude** by:
   ```bash
   # Check out the lab branch
   git checkout lab/issue-{number}

   # Read the issue file
   cat .lab-issues/issue-{number}.md
   ```
4. **Ask Claude** to implement the lab based on the issue requirements

### Manual Access to Issue Content

If you need to access an existing issue (like issue #1):

```bash
# The automation will have created:
# - Branch: lab/issue-1
# - File: .lab-issues/issue-1.md
git checkout lab/issue-1
cat .lab-issues/issue-1.md
```

Then share the content with Claude to start building the lab!

## Repository Structure

```
agent-tools-attack-vectors/
├── .github/
│   └── workflows/
│       └── issue-to-lab.yml    # Automation workflow
├── .lab-issues/                # Issue content files
│   └── issue-{number}.md       # Individual issue details
└── README.md                   # This file
```

## Getting Started

1. Create an issue describing your lab requirements
2. The automation will set up a branch and save the issue content
3. Use Claude to implement the lab based on the requirements

## License

This is a security research and educational repository.
