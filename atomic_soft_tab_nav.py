import sublime
import sublime_plugin


# Main Input Event Listener
class SoftTabNavListener(sublime_plugin.EventListener):
    view_settings = None
    plugin_settings = None


    def on_activated(self, view):
        self.view_settings = view.settings()
        self.plugin_settings = sublime.load_settings('Atomic Soft Tab Nav.sublime-settings')

    def on_text_command(self, view, command_name, args):
        if not self.view_settings.get('translate_tabs_to_spaces'):
            return None

        if (command_name != "move"):
            return None

        selection = view.sel()
        if len(view.sel()) != 1:
            return None

        has_active_selection = min([abs(x.b - x.a) for x in selection]) >= 1
        is_extending_selection = 'extend' in args and args['extend']
        if has_active_selection and not is_extending_selection:
            return None

        selection_start = selection[0].a
        selection_end = selection[0].b
        tab_size = self.view_settings.get('tab_size')

        if args.get('by') == 'characters':
            """
            Handles the case when the cursor will enter a soft tab.
             The author is unaware of how to cancel keyboard input
             commands so here we programatically move the cursor to the
             next edge of soft tab the cursor will enter and then move the
             cursor back/forward one character to "cancel" the original
             left/right key input.
            """
            beginning_of_cursor_line = view.line(selection_end).a
            selection_is_at_end_of_space_sequence = view.substr(sublime.Region(
                beginning_of_cursor_line,
                selection_end
            )) == " " * (selection_end - beginning_of_cursor_line)

            if not selection_is_at_end_of_space_sequence:
                return None

            position_in_block = (selection_end - beginning_of_cursor_line) % tab_size
            if args.get('forward') is True:
                remaining_text_in_current_tab_block = view.substr(sublime.Region(
                    selection_end,
                    selection_end + (tab_size - position_in_block)
                ))

                if remaining_text_in_current_tab_block == " " * (tab_size - position_in_block):
                    next_selection_end = selection_end + (tab_size - position_in_block) - 1
                else:
                    return None
            elif args.get('forward') is False:
                if selection_end == beginning_of_cursor_line:
                    return None
                if position_in_block == 0:
                    next_selection_end = selection_end - tab_size + 1
                else:
                    next_selection_end = selection_end - position_in_block + 1

            next_selection_start = (
                selection_start if is_extending_selection else next_selection_end
            )
            selection.clear()
            selection.add(sublime.Region(
                next_selection_start,
                next_selection_end
            ))
        elif args.get('by') == 'lines' and self.plugin_settings.get('enable_line_nav'):
            """
            Handles the case when the cursor moves onto a soft tab
             from a line above or below. In this case we programatically
             move the cursor to the next line and then replace the
             original keyboard input with left/right keydown depending on
             where the cursor is in the current soft tab block. This will
             trigger the previous if/else case and move the cursor onto
             the edge of the soft tab.
            """

            selection_line_start = view.line(selection_end).a
            selection_line_end = view.line(selection_end).b
            if args.get('forward') is True:
                next_line_start = selection_line_end + 1
                next_line_end = view.line(next_line_start).b
            elif args.get('forward') is False:
                next_line_end = selection_line_start - 1
                next_line_start = view.line(next_line_end).a
            position_in_block = (selection_end - selection_line_start) % tab_size

            # If next line length is smaller than position in current
            # line then the cursor can't hit a soft tab.
            if next_line_end - next_line_start < (tab_size - position_in_block) + selection_end - selection_line_start:
                return None

            next_selection_end = next_line_start + (selection_end - selection_line_start)
            next_selection_end_is_at_end_of_space_sequence = view.substr(sublime.Region(
                next_line_start,
                next_selection_end
            )) == " " * (selection_end - selection_line_start)
            if position_in_block != 0 and next_selection_end_is_at_end_of_space_sequence:
                remaining_text_in_next_tab_block = view.substr(sublime.Region(
                    next_selection_end,
                    next_selection_end + (tab_size - position_in_block)
                ))
                if remaining_text_in_next_tab_block == " " * (tab_size - position_in_block):
                    next_selection_start = (
                        selection_start if is_extending_selection else next_selection_end
                    )
                    selection.clear()
                    selection.add(sublime.Region(
                        next_selection_start, next_selection_end
                    ))
                    return ('move', {
                        'extend': is_extending_selection,
                        'forward': position_in_block >= tab_size // 2,
                        'by': 'characters'
                    })


# Window Commands of Preferences
class AtomicSoftTabNavEditSettingsCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command(
            'edit_settings',
            {
                "base_file": "${packages}/Atomic Soft Tab Nav/Atomic Soft Tab Nav.sublime-settings",
                "default":
                    "// See the left pane for the list of settings and valid values\n"
                    "{\n"
                    '    "enable_line_nav": false$0\n'
                    "}\n"
            }
        )


class AtomicSoftTabNavSetLineNavSettingsCommand(sublime_plugin.WindowCommand):
    def run(self, **args):
        if 'enable' in args:
            settings = sublime.load_settings('Atomic Soft Tab Nav.sublime-settings')
            settings.set('enable_line_nav', args['enable'])
            sublime.save_settings('Atomic Soft Tab Nav.sublime-settings')

