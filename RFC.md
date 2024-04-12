RFC Process
-----------

Most technical decisions are decided through the "RFC" ([Request for Comments](https://en.wikipedia.org/wiki/Request_for_Comments)) process. Small changes, such as minor grammatical edits to the specification, do not need to need to follow the RFC process. However, if one intends to make a substantive change to the WDL specification , the following process should be adhered to:

 1. Ideally have an informal discussion of the topic on [Slack](https://join.slack.com/t/openwdl/shared_invite/zt-ctmj4mhf-cFBNxIiZYs6SY9HgM9UAVw) and/or [GitHub discussions](https://github.com/openwdl/wdl/discussions) in order to gauge basic viability. As a rule of thumb, receiving encouraging feedback from long-standing community members is a good indication that the RFC is worth pursuing.
 2. Write up a formal proposal, including requested changes to the current specification, as a pull request on GitHub
 3. A core team member will be assigned as the *shepherd* of this RFC. The shepherd shall be responsible for keeping the discussion moving and ensuring all concerns are responded to.
 4. Work to build broad support from the community. Encouraging people to comment, show support, show dissent, etc. Ultimately the level of community support for a change will decide its fate. 
 5. RFCs rarely go through this process unchanged, especially as alternatives and drawbacks are discovered. You can make edits to the RFC to clarify or change the design, but make changes as new commits to the pull request, and leave a comment on the pull request explaining your changes. Specifically, do not squash or rebase commits after they are visible on the pull request.
 6. Every significant addition or change to the spec will require a test case to be accepted. See the [testing README](tests/README.md) for details on how to write tests.
 7. When it appears that a discussion is no longer progressing in a constructive way, or a general consensus has been reached, the shepherd will make an official summary on where the consensus has wound up.
 8. The shepherd will put out an official call for votes. This call shall be advertised broadly and will last ten calendar days. Any interested member may vote via +1/-1.
 9. After the voting process is complete the core group shall decide to officially approve this RFC. It is expected that barring extreme circumstances this is a rubber stamp of the voting process. An example of an exceptional case would be if representatives for every WDL implementation vote against the feature for feasibility reasons.

When an RFC is approved it will become part of the current draft version of the specification. This will allow time for implementers to verify feasibility and cutting edge users  to get used to the new syntax. In order to prevent untested features from entering into an official specification version at least one WDL implementation must support a feature before it’s allowed to be merged into the current draft version.
