Changelog
==========

<!--

Newest changes should be on top.

What should be mentioned (in order):
+ Optional: In **bold**. A backported notice.
+ A summary of the change.
+ A link to the PR for further reading.
+ Credit where credit is due by mentioning the github account.

Keep the changelog pleasant to read in the text editor:
+ Max 80 characters per line
+ Empty line between changes.
+ Newline between summary and link+credit.
+ Properly indent blocks.
-->

version 2.0.0
---------------------------
+ Added a required input and output format for workflow engines.
  [PR 357](https://github.com/openwdl/wdl/pull/357)

+ The input specification has been clarified.
  [PR 314](https://github.com/openwdl/wdl/pull/314) by @geoffjentry.

+ Added a list of keywords that can not be used as identifiers.
  [PR 307](https://github.com/openwdl/wdl/pull/307) by @mlin.

+ Empty call blocks have been clarified.
  [PR 302](https://github.com/openwdl/wdl/pull/302) by @aednichols.

+ Optional and non-empty type constraints have been clarified.
  [PR 290](https://github.com/openwdl/wdl/pull/290) by @mlin.

+ `object` has been removed from WDL. `struct` can be used to achieve the same
  type of functionality in a more explicit way.
  [PR 283](https://github.com/openwdl/wdl/pull/283) by @patmagee.

+ The way comments work has been clarified.
  [PR 277](https://github.com/openwdl/wdl/pull/277) by @patmagee.

+ Implement string escapes in the Hermes grammar.
  [PR 272](https://github.com/openwdl/wdl/pull/272) by @cjllanwarne.

+ Added `None` for explicitly stating that an optional variable is not defined.
  [PR 263](https://github.com/openwdl/wdl/pull/263) by @rhpvorderman.

+ **Backported to 1.0**: Fix a bug in the grammar regarding unescaped strings.
  [PR 253](https://github.com/openwdl/wdl/pull/253) and
  [PR 255](https://github.com/openwdl/wdl/pull/255) by @aednichols.

+ WDL Files should be encoded in UTF-8 now. String definitions have been
  clarfied.
  [PR 247](https://github.com/openwdl/wdl/pull/247) by @EvanTheB.

+ The version `statement` can now be the first *non-comment* statement. So it
  can be stated below a license header for example.
  [PR 245](https://github.com/openwdl/wdl/pull/245) by @ffinfo.

+ Added a `keys` function to get an array of keys from a map.
  [PR 244](https://github.com/openwdl/wdl/pull/244) by @ffinfo.

+ Added a new directory type to make it easier when working with inputs that
  consist of multiple files.
  [PR 241](https://github.com/openwdl/wdl/pull/241) by @cjllanwarne.

+ Several bugs in the grammar have been fixed.
  [PR 238](https://github.com/openwdl/wdl/pull/238) and
  [PR 240](https://github.com/openwdl/wdl/pull/240) by @cjllanwarne.

<!---
This is not implemented yet.
+ Type conversions and meanings have been clarified.
  [PR 235](https://github.com/openwdl/wdl/pull/235) by @EvanTheB.
-->

+ **Backported to 1.0**: Imports are now relative to their current location.
  [PR 220](https://github.com/openwdl/wdl/pull/220) by @geoffjentry.

+ Added conversion functions `as_pairs` and `as_map` to convert between
  `Array[Pair[X,Y]]` and `Map[X,Y]`.
  [PR 219](https://github.com/openwdl/wdl/pull/219) by @DavyCats.

+ Add an `after` keyword to run a task after other tasks.
  [PR 162](https://github.com/openwdl/wdl/pull/162) by @cjllanwarne.
