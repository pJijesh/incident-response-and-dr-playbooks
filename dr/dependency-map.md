# Dependency map

A dependency map shows what must be working for each service to work. It answers the question the [BIA](bia-template.md) cannot: "if X fails, what else goes down with it?". Use it to check tier assignments (a service cannot be recovered faster than the things it depends on) and to decide the recovery order in the [DR plan](dr-plan-template.md).

The diagram is for a fictional mid-size company with Microsoft 365 and hybrid Active Directory, matching the [BIA worked example](bia-worked-example.md). Replace the boxes with your own services.

![Dependency map for a fictional company](../docs/dependency-map.png)

Reading it: an arrow from A to B means "B depends on A" (if A fails, B is affected). Colours show the recovery tier from the [tier table](rto-rpo-tiers.md): red is Tier 0 (foundation), orange is Tier 1, yellow is Tier 2, blue is Tier 3, and dashed grey boxes are third parties you do not control. Dotted arrows show the managed service provider's access or support role.

## Source

The diagram source is [dependency-map.mmd](dependency-map.mmd). GitHub renders the Mermaid block below directly. The PNG in `docs/` is produced from the same source with the Mermaid command line tool:

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i dr/dependency-map.mmd -o docs/dependency-map.png -w 1800 -b white
```

```mermaid
flowchart TB
  classDef t0 fill:#fde2e2,stroke:#b42318,color:#111
  classDef t1 fill:#ffedd5,stroke:#c2410c,color:#111
  classDef t2 fill:#fef9c3,stroke:#a16207,color:#111
  classDef t3 fill:#e0f2fe,stroke:#0369a1,color:#111
  classDef ext fill:#f3f4f6,stroke:#4b5563,stroke-dasharray: 5 3,color:#111

  subgraph FOUND["Foundation services (Tier 0)"]
    ISP["Internet connectivity<br/>(primary + secondary ISP)"]:::t0
    DNS["DNS and domain registrar"]:::t0
    FW["Firewalls and VPN"]:::t0
    AD["On-premises Active Directory"]:::t0
    ENTRA["Microsoft Entra ID<br/>(sync, MFA, Conditional Access)"]:::t0
    PWR["Power and comms room"]:::t0
  end

  subgraph PLAT["Platform services (Tier 1)"]
    M365["Microsoft 365<br/>Exchange Online, Teams, SharePoint"]:::t1
    INTUNE["Intune and endpoint protection"]:::t1
    BKP["Backup platform<br/>(immutable copy + offline copy)"]:::t1
    FS["File servers"]:::t1
    TEL["Telephony"]:::t1
  end

  subgraph BUS["Business applications"]
    FMS["Freight management system<br/>(SaaS)"]:::t1
    CUS["Customs declaration service<br/>(supplier hosted)"]:::t1
    WMS["Warehouse scanning and stock"]:::t1
    FIN["Finance and payments"]:::t2
    PAY["Card payment gateway<br/>(PCI scope)"]:::t2
    CRM["CRM and quoting"]:::t3
    HR["HR and payroll"]:::t2
  end

  subgraph EXT["Third parties"]
    MSP["Managed service provider"]:::ext
    BANK["Bank and payment partners"]:::ext
    CARR["Carrier and agent portals"]:::ext
    AUTH["Customs and regulator portals"]:::ext
  end

  PWR --> FW
  PWR --> AD
  ISP --> FW
  ISP --> DNS
  FW --> AD
  AD --> ENTRA
  ENTRA --> M365
  ENTRA --> INTUNE
  ENTRA --> FMS
  ENTRA --> CRM
  ENTRA --> HR
  AD --> FS
  AD --> WMS
  DNS --> M365
  DNS --> FMS
  FS --> BKP
  M365 --> BKP
  M365 --> TEL
  FMS --> CUS
  AUTH --> CUS
  CARR --> FMS
  FMS --> FIN
  FMS --> WMS
  BANK --> FIN
  BANK --> PAY
  MSP -.-> FW
  MSP -.-> BKP
  MSP -.-> INTUNE
```

## How to build your own in an hour

1. List your business processes from the BIA and the systems each one uses.
2. For each system, ask: what does it need to run? Typical answers are identity, network, DNS, power, a database, a supplier, a licence, a person with specific knowledge.
3. Add arrows from the dependency to the dependent service.
4. Colour by tier. Any arrow that goes from a lower tier (slower recovery) into a higher tier (faster recovery) is a problem to fix, either by raising the dependency's tier or by accepting and recording the risk.
5. Mark single points of failure: one firewall, one ISP, one person, one supplier.
6. Review after every major change, and after every incident or test.

## What to look for

| Finding | Example response |
|---|---|
| A T1 service depends on something with no recovery plan | Add it to the DR plan and the test schedule |
| One identity platform feeds everything | Treat identity as T0, keep break-glass accounts and a tested rebuild |
| One supplier appears under many services | Review the contract, incident contacts and service levels against the strictest RTO |
| A dependency is a person | Document the procedure and train a deputy |
| Backups depend on the same identity as production | Separate the backup administration credentials |
