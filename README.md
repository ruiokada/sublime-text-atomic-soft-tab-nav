# Sublime Text Atomic Soft Tab Nav

In Sublime Text, soft tabs (multiple spaces used as tabs) require as many arrow key presses as there are spaces to navigate. The purpose of this package is to make it so that soft tabs can be navigated just like tabs when using the arrow keys.

![Standard Demo](https://raw.githubusercontent.com/ruiokada/sublime-text-atomic-soft-tab-nav/assets/demo.gif)

Set `enable_line_nav` to `true` in Atomic Soft Tab Nav plugin settings (access preferences via Command Palette or through the Preferences menu item) to enable atomic soft tabs when navigating by lines as shown below.

![With 'enable_line_nav' True Demo](https://raw.githubusercontent.com/ruiokada/sublime-text-atomic-soft-tab-nav/assets/demo-by-lines.gif)

## Install

Atomic Soft Tab Nav is available on Sublime Text's Package Control. To install use the command palette commands:

1. Package Control: Install Package
2. Install Atomic Soft Tab Nav

Otherwise, you can also manually install by cloning this repository into your user packages folder:

    git clone https://github.com/ruiokada/sublime-text-atomic-soft-tab-nav.git "Atomic Soft Tab Nav"

Sublime Text has a setting to visually distinguish tabs and soft tabs but it is not enabled by default. It is recommended to enable it by setting `draw_white_space` to `all` in your user settings file:

    {"draw_white_space": "all"}

## Functionality

The functionality of this package is simple. When the text cursor encounters a soft tab during arrow key input, this plugin will modify the arrow key input accordingly. The following are the arrow key input modification details:

* Soft tabs are assumed to appear only at the beginning of lines so multiple spaces that do not span to the beginning of the line are ignored.
* If the cursor is on the edge of a soft tab, then the left/right arrow keys move the cursor as if the soft tabs were tabs.
* If the cursor is in the middle of a soft tab, then the left/right arrow keys move the cursor to the end of the soft tab.
* If `enable_line_nav` is set to true in plugin settings then the up/down arrow keys will also treat soft tabs in a similar manner.
* The above modifications are applied even in the case when the cursor is making a text selection.
* The above modifications will not be applied if there are multiple active cursors.
* If the spaces as tabs function is disabled in the current file view then this plugin will be disabled.
* This package uses the soft tab size set by the current file view.
