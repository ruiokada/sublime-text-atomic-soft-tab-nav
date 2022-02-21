# Sublime Text Soft Tab Nav

In Sublime Text, soft tabs (multiple spaces used as tabs) require as many arrow key presses as there are spaces to navigate. The purpose of this package is to make it so that soft tabs can be navigated just like tabs when using the arrow keys.

## Functions

The functionality of this package is simple. When the text cursor encounters a soft tab during arrow key input, this plugin will modify the arrow key input accordingly. The following are the arrow key input modification details:

* Soft tabs are assumed to appear only at the beginning of lines so multiple spaces that do not span to the beginning of the line are ignored.
* If the cursor is on the edge of a soft tab, then the arrow keys move the cursor as if the soft tabs were tabs.
* If the cursor is in the middle of a soft tab, then the arrow keys move the cursor as if the soft tab is multiple spaces until either end of the soft tab is reached.
* The above modifications are applied even in the case when the cursor is making a text selection.

If spaces as tabs is disabled in the current file view then this plugin will be disabled. The size of soft tabs depends on the tab size of the current file view.
