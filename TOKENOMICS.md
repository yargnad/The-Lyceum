# The Lyceum Tokenomics: A "Proof-of-Utility" Model

**Version:** 1.2 - October 21, 2025
**Status:** DRAFT - Critical Update: Layer 3 Architecture

## 1. Our Guiding Principle: "People Over Tokens"

This is the foundational, non-negotiable principle of The Lyceum's economy. The network is a public commons built for utility, not a speculative asset built for profit.

* **This is for the people, not for the tokens.**
* The token is **not** the product. The *utility* of the Pneuma AI, the Symbolon apps, and the sovereign communication network is the product.
* The token exists for only two reasons:
    1.  To **incentivize** participation and the contribution of real, useful hardware (compute, bandwidth, storage).
    2.  To **police** the network, providing an economic tool to disincentivize and punish bad-faith actors.

## 2. The "Anti-Blockchain" Architecture

The Lyceum is a "Proof-of-Utility" network, not a "Proof-of-Work" or "Proof-of-Stake" blockchain. We run a **Lightweight Encrypted Ledger** called the "Pneuma Vault," which is a simple, replicated database that tracks earned tokens.

## 3. The "Proof-of-Utility" Earning Model

Tokens are not "mined." They are **earned** as a direct receipt for providing verifiable, useful work to the commons. The resource cost of the token system itself is near-zero.

The workflow is as follows:

1.  **Job Submitted:** A user requests a Pneuma task.
2.  **Real Work Performed:** Pneuma routes the job to a Guardian node. That node's **NPU/GPU/CPU (the "Artillery")** performs the actual, valuable compute work.
3.  **Work Verified:** The job result is verified by the user's node or a nearby peer Guardian.
4.  **Ledger Updated:** Upon verification, the "Pneuma Vault" is notified and makes a simple database entry: `Node !a1b2c3d4 credited 0.1 tokens for Task #5879.`

## 4. Why We Don't Use the NPU for Tokenization

An NPU is a specialized piece of hardware, our "Artillery." We **never** waste our artillery on simple bookkeeping. The Pneuma Vault is a lightweight CPU task.

## 5. The Role and Lifecycle of a Token

### Earning (Incentive)

Users earn tokens by contributing verifiable resources. This is stratified by the value of the work.

* **Compute ("Reflex" Jobs):** Earning a standard rate of tokens for providing "autonomic" network services (running `SenseVoice`, `paroli`, or vetting Symbolons).
* **Compute ("Cortex" Jobs):** Earning a **premium rate** of tokens for contributing high-power hardware to the "fractured" federated LLM.
* **Relaying & Storage:** Earning tokens for providing verifiable, high-uptime **Layer 3 Backbone Relays** (via **900 MHz LoRa PTP** or **5 GHz Wi-Fi PTP**) or for hosting popular "Symbolon" apps for the Agora.

### Spending (Utility Access & Spam Prevention)

* Accessing high-value, network-wide "Cortex" compute resources (like the Pneuma LLM) will cost a tiny, fixed amount of tokens. This creates a functional, circular economy and prevents spam.
* This directly reinforces the "Homestead Principle": using your *own* nodes is always free.

### Staking (Policing & Trust)

* To offer a new "Symbolon" to the Agora, a developer with no reputation must "stake" a bond of tokens. If their app is found to be malicious by the Pneuma Guardians, their stake is "slashed" (burned or redistributed).
* This creates a powerful economic disincentive for bad actors and aligns developer incentives with the health of the commons.
