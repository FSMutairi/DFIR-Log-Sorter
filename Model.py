#!/usr/bin/env python3
"""
AI Model Configuration for DFIR Log Sorter
Contains the prompt template for Ollama-based log analysis.

Author: Faris
Created: 2024
"""

import ollama

user_input = """
 Incident Investigation Request

I am currently investigating a cyberattack on my company. Below is a series of suspicious log entries I’ve extracted from our environment. I need your help to analyze this potential breach comprehensively.

Please perform a thorough investigation of the logs and provide insight into the following:

 What You Should Analyze and Report:
1. Attack Timeline & Description

    1-1. Construct a detailed timeline of the incident based on the log timestamps

    1-2. Clearly describe the attacker’s goals and tactics (Initial Access, Execution, Lateral Movement, etc.)

2. Compromised Elements

    2-1. List all compromised user accounts

    2-2. Identify affected hosts, services, and sensitive data assets

3. IOCs (Indicators of Compromise)
Extract any relevant:

    3-1. Malicious IPs

    3-2. File hashes / names

    3-3. Domains (e.g. C2 servers)

    3-4. Suspicious processes or commands

    3-5. Ports used (e.g., 8080, 9001, SSH)

4. Containment & Remediation Recommendations

    4-1. Give prioritized steps to contain the incident (e.g., isolate hosts, disable accounts)

    4-2. Suggest remediation actions (malware removal, password rotation, patching, etc.)

    4-3. Include command-line examples for Linux/Windows systems if applicable

    5. Immediate Actions for SOC/IR Team

    5-1. As an investigator, what actions should I take right now?

    5-2. Include advice on:

    5-2-1. Evidence preservation

    5-2-2. Log collection

    5-2-3. Internal and external communication

    5-2-4. Next phase of forensic investigation

6. (Optional) Executive Summary

    6-1. If possible, provide a short summary suitable for non-technical management

    6-2. Focus on impact, business risk, and high-level next steps

These are the logs:



Please prioritize accuracy, clarity, and real-world best practices. If something is unclear from the logs, feel free to note assumptions or ask for more data.
"""

response = ollama.chat(model="qwen2.5:7b", messages=[{"role": "user", "content": user_input}])

print(response['message']['content'])