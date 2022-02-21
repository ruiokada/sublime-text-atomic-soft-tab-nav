import sublime
import sublime_plugin


class SoftTabNavListener(sublime_plugin.EventListener):
    view_settings = None

    def on_activated(self, view):
        self.view_settings = view.settings()

    def on_text_command(self, view, command_name, args):
        if not self.view_settings.get('translate_tabs_to_spaces'):
            return None

        if (command_name != "move" or (
                'by' in args and args['by'] != 'characters')):
            return None

        selection = view.sel()
        if len(view.sel()) != 1:
            return None

        has_active_selection = min([abs(x.b - x.a) for x in selection]) > 1
        is_extending_selection = 'extend' in args and args['extend']

        if has_active_selection and not is_extending_selection:
            return None

        selection_start = selection[0].a
        selection_end = selection[0].b
        tab_size = self.view_settings.get('tab_size')

        beginning_of_caret_line = view.line(selection_end).a

        selection_is_at_end_of_tab_sequence = (
            (selection_end - beginning_of_caret_line) % tab_size == 0 and
            view.substr(sublime.Region(
                beginning_of_caret_line,
                selection_end
            )) == " " * (selection_end - beginning_of_caret_line)
        )

        if selection_is_at_end_of_tab_sequence:
            move_direction = 1 if args['forward'] else -1
            next_block_of_characters = view.substr(sublime.Region(
                selection_end,
                selection_end + move_direction * tab_size
            ))
            caret_will_move_over_tab = (
                next_block_of_characters == " " * tab_size
            )

            if args['forward']:
                next_selection_overlaps_start = (
                    selection_end < selection_start and
                    selection_start < selection_end + tab_size
                )
            else:
                next_selection_overlaps_start = (
                    selection_start < selection_end and
                    selection_end - tab_size < selection_start
                )

            if caret_will_move_over_tab and not next_selection_overlaps_start:
                if is_extending_selection:
                    next_selection = (
                        selection_start,
                        selection_end + move_direction * (tab_size - 1)
                    )
                else:
                    next_selection = (
                        selection_end + move_direction * (tab_size - 1),
                        selection_end + move_direction * (tab_size - 1)
                    )
                selection.clear()
                selection.add(
                    sublime.Region(*next_selection)
                )
