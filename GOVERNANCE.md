OpenWDL Governance and Process
==============================

Table of Contents
-----------------
[Table of Contents]: #table-of-contents
  - [Governance](#governance)
  - [RFC Process](#rfc-process)
  
Governance
----------

WDL has a community-driven development process where most decisions are made through consensus, under the stewardship of a 'core team'. The core team is responsible for steering the design and development process, overseeing the introduction of new features, setting priorities and release schedule, and ultimately making decisions for the rare instances where there is no community consensus. 

Current core team members are:

| Name               | Organization            | github                  |
|:-------------------|:-------------|:------------------
| Brad Chapman       | Harvard School of Public Health | [chapmanb](https://github.com/chapmanb) |
| Jeff Gentry        | Broad Institute                 | [geoffjentry](https://github.com/geoffjentry) |
| Mike Lin           | DNAnexus                        | [mlin](https://github.com/mlin) |
| Patrick Magee      | DNAstack                        | [patmagee](https://github.com/patmagee) |
| Brian O'Connor     | University of California, Santa Cruz | [briandoconnor](https://github.com/briandoconnor) |
| Abirami Prabhakaran| Intel | [aprabhak2](https://github.com/aprabhak2) |
| Geraldine Van der Auwera | Broad Institute | [vdauwera](https://github.com/vdauwera) |


At the core group's discretion a new member may be added by a majority vote. This addition will be done to recognize **significant** contributions to the community. *Contributions* include such things as:

 - Active participation in discussions, mailing list, forums
 - Community building efforts
 - Helping with documentation, standards documents, etc
 - Building supporting software and tooling

Generally members are only removed at their own request are due to very long term inactivity. In extreme circumstances the core group can vote to remove a member.

RFC Process
-----------

Most technical decisions are decided through the "RFC" ([Request for Comments](https://en.wikipedia.org/wiki/Request_for_Comments)) process. Small changes, such as minor grammatical edits to the specification, do not need to need to follow the RFC process. However, if one intends to make a substantive change to the WDL specification , the following process should be adhered to:

 1. Ideally have an informal discussion of the topic on the [mailing list](https://groups.google.com/forum/#!forum/openwdl) and/or the [gitter channel](https://gitter.im/openwdl/wdl) in order to gauge basic viability. As a rule of thumb, receiving encouraging feedback from long-standing community members is a good indication that the RFC is worth pursuing.
 2. Write up a formal proposal, including requested changes to the current specification, as a pull request on GitHub
 3. A core team member will be assigned as the *shepherd* of this RFC. The shepherd shall be responsible for keeping the discussion moving and ensuring all concerns are responded to.
 4. Work to build broad support from the community. Encouraging people to comment, show support, show dissent, etc. Ultimately the level of community support for a change will decide its fate. 
 5. RFCs rarely go through this process unchanged, especially as alternatives and drawbacks are discovered. You can make edits to the RFC to clarify or change the design, but make changes as new commits to the pull request, and leave a comment on the pull request explaining your changes. Specifically, do not squash or rebase commits after they are visible on the pull request.
 6. When it appears that a discussion is no longer progressing in a constructive way, or a general consensus has been reached, the shepherd will make an official summary on where the consensus has wound up.
 7. The shepherd will put out an official call for votes. This call shall be advertised broadly and will last ten calendar days. Any interested member may vote via +1/-1.
 8. After the voting process is complete the core group shall decide to officially approve this RFC. It is expected that barring extreme circumstances this is a rubber stamp of the voting process. An example of an exceptional case would be if representatives for every WDL implementation vote against the feature for feasibility reasons.

When an RFC is approved it will become part of the current draft version of the specification. This will allow time for implementers to verify feasibility and cutting edge users  to get used to the new syntax. In order to prevent untested features from entering into an official specification version at least one WDL implementation must support a feature before it’s allowed to be merged into the current draft version.
