import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from . import client

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build_main_view(self)

    def build_main_view(self, *args, **kwargs):
        # Defining stack and stack switcher
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(1000)
        self.stackswitcher = Gtk.StackSwitcher(stack=self.stack)

        # Box for all the boxes
        self.rootbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Box for the stack switcher
        self.swboxh = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, )
        self.swboxh.append(self.stackswitcher)

        # root box to window
        self.set_child(self.rootbox)
        # Add the stack and the stack switcher box to the root box
        self.rootbox.append(self.swboxh)
        self.rootbox.append(self.stack)

        # Box with all the buttons
        self.buttonbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.button = Gtk.Button(label="Hello")
        self.button.connect('clicked', self.hello)
        self.button2 = Gtk.Button(label="Hello")
        self.button2.connect('clicked', self.list_mpd_root)
        self.buttonbox.append(self.button) # Put button in the first of the two vertial boxes
        self.buttonbox.append(self.button2) # Put button in the first of the two vertial boxes

        self.check = Gtk.CheckButton(label="And goodbye?")

        # Add the button box to the stack page
        self.stack.add_titled(self.buttonbox, "1", "Buttons")
        self.stack.add_titled(self.check, "2", "Check")

    def hello(self, button):
        print("Hello world")

    def list_mpd_root(self, button):
        self.dialog = Gtk.MessageDialog(text="Server's response", secondary_text=client.client_test())
        self.dialog.present()
        print(client.client_test())

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.headerbar = Gtk.HeaderBar()
        self.headerbar.show_close_button = False
        self.window = MainWindow(application=app, titlebar=self.headerbar)
        self.window.present()

if __name__ == "__main__":
    app = MyApp(application_id="com.example.GtkApplication")
    app.run(sys.argv)
