def rgb(r: int, g: int, b: int):
    """Функция для удобства хранения rgb"""
    return r, g, b


def curly_braces(line):
    """Функция помещает текст в фигурные скобки"""
    return "{" + line + "}"


class Style:
    def __init__(self, color_widget=None, color_background=None):
        self.color_widget_default = rgb(80, 111, 235)
        self.color_background_default = rgb(245, 245, 255)
        self.color_widget = color_widget
        self.color_background = color_background
        if color_widget is None:
            self.color_widget = self.color_widget_default
        if color_background is None:
            self.color_background = self.color_background_default

    def combo_box(self):
        """Стиль списка"""
        combo_box = f'''
            font: bold 16px;
            color: rgb{self.color_widget};
            border-radius: 5px;
            padding-left: 5px;
            padding-right: 5px;
            background-color: rgb{self.color_background}; 
            '''
        style_combo_box = "QComboBox" + curly_braces(combo_box)
        hover = f'''
            border: 2px solid rgb{self.color_widget};
            '''
        style_hover = "QComboBox:hover" + curly_braces(hover)
        focus = f'''
            border: 2px solid rgb{self.color_widget};
            '''
        style_focus = "QComboBox:focus" + curly_braces(focus)
        style_drop_down = '''
        QComboBox::drop-down 
        {
            width: 0px;
            height: 0px;
            border: 0px;
        }
        '''
        abstract_item_view = f'''
            font: bold 16px;
            color: rgb{self.color_widget};   
            background-color: rgb{self.color_background};
            padding: 10px;
            border: 2px solid rgb(212, 215, 255);
            border-radius: 10px;
            padding-left: 5px;
            padding-right: 5px;
            selection-background-color: rgb(140, 146, 255);
        '''
        style_abstract_item_view = "QComboBox QAbstractItemView" + curly_braces(abstract_item_view)
        style_list_view = '''
            QComboBox QListView
        {
            outline: 0px;
        }
        '''
        vertical = f'''
            background-color: rgb{self.color_background};
            width: 15px;
            margin: 15px 3px 15px 3px;
            border: 1px transparent rgb{self.color_background};
            border-radius: 4px;
            '''
        style_vertical = "QScrollBar:vertical" + curly_braces(vertical)
        handle_vertical = f''' 
            background-color: rgb{self.color_widget};         
            min-height: 5px;
            border-radius: 4px;
            '''
        style_handle_vertical = "QScrollBar::handle:vertical" + curly_braces(handle_vertical)
        style_arrow = '''
        QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical, QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical, QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
        {
            background: none;
        }
        '''

        return style_combo_box + style_hover + style_focus + style_drop_down + style_abstract_item_view + style_list_view + style_vertical + style_handle_vertical + style_arrow

    def check_box(self):
        """Стиль галочки"""
        style_check_box = f'''
            color: rgb{self.color_widget}; 
            font: bold 16px;
        '''
        return style_check_box


    def button(self):
        """Стиль кнопки"""
        button = f"""
            color: rgb(255, 255, 255);
            background-color: rgb{self.color_widget};
            border-style: outset;
            border-width: 2px;
            border-radius: 5px;
            border : 0px;
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
        """
        style_pressed = """
            QPushButton:pressed {
            background-color:  rgb(90, 120, 255)
            }
        """
        style_button = "QPushButton" + curly_braces(button)
        return style_button+style_pressed

    def line_edit(self):
        """Стиль поиска"""
        button = f"""
            color: rgb{self.color_widget};
            border-width: 2.5px;
            border-style: solid;
            background-color: rgb(255, 255, 255);
            border-color: rgb{self.color_widget};
        """
        style_line_edit = "QLineEdit" + curly_braces(button)
        return style_line_edit

    def line_edit1(self):
        """Стиль поиска"""
        button = f"""
            color: rgb{self.color_widget};
            border-width: 1.5px;
            border-style: solid;
            background-color: rgb(255, 255, 255);
            border-color: rgb{self.color_widget};
        """
        style_line_edit = "QLineEdit" + curly_braces(button)
        return style_line_edit

    def line_edit2(self):
        """Стиль поиска"""
        button = f"""
            color: rgb{self.color_widget};
            border-width: 0.5px;
            border-style: solid;
            background-color: rgb(255, 255, 255);
            border-color: rgb{self.color_widget};
        """
        style_line_edit = "QLineEdit" + curly_braces(button)
        return style_line_edit

    def label(self):
        """Стиль строчек"""
        style_label = f'''
            color: rgb{self.color_widget}; 
            font: bold 16px;
        '''
        return style_label


    def main_window(self):
        """Стиль окна"""
        style_main_window = f'''
            background-color: rgb{self.color_background};
        '''
        return style_main_window
