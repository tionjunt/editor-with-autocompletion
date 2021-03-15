from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

import os


class TextHelper(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    # This method is necessary because when insert_text is called,
    # selection_text property is empty even if some string was
    # selected. 
    def hold_selected(self):
        self.selected_text = self.selection_text

        if type(self.selection_from) == int:
            self.selected_from = self.selection_from
            self.selected_to = self.selection_to

            # i.e. if the string is selected from right to left
            if self.selected_from > self.selected_to:
                self.selected_from, self.selected_to = self.selected_to, self.selected_from
    

    def insert_text(self, ch, from_undo=False):
        if ch in ('{(["' + "'"):
            substring = self.get_paired_string(ch)
            return_value = super().insert_text(substring, from_undo=from_undo)
            self.do_cursor_movement('cursor_left')

            # To keep the string selected.
            self.select_text(self.selected_from+1, self.selected_to+1)
        else:
            return_value = super().insert_text(ch, from_undo=from_undo)
        return return_value
    

    def get_paired_string(self, ch):
        if ch == '{':
            return '{' + self.selected_text + '}'
        elif ch == '(':
            return '(' + self.selected_text + ')'
        elif ch == '[':
            return '[' + self.selected_text + ']'
        elif ch in ('"' + "'"):
            return ch + self.selected_text + ch


class FileDialog(Popup):
    save_file = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    

    def cancel(self, *args):
        self.dismiss()



class EditorWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    

    def key_action(self, *args):
        text_helper = self.ids['editor']
        text_helper.hold_selected()
    

    def save_file(self, file_path, file_name, *args):
        editor = self.ids['editor']
        full_path = os.path.join(file_path, file_name)
        with open(full_path, 'w') as f:
            f.write(editor.text)
        self.popup.dismiss()


    def ask_file_name(self, *args):
        self.popup = FileDialog(save_file=self.save_file)
        self.popup.open()



class EditorApp(App):
    def build(self):
        editor = EditorWidget()
        Window.bind(on_key_down=editor.key_action)
        return editor


if __name__ == "__main__":
    EditorApp().run()