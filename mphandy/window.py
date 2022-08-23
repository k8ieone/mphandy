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
        # Defining stack and stackswitcher
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(1000)
        self.stackswitcher = Gtk.StackSwitcher(stack=self.stack)

        # Create and set a headerbar for the window
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        # Box for the stack switcher
        self.swboxh = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.swboxh.append(self.stackswitcher)

        # Set the stack switcher box as the title widget
        self.header.set_title_widget(self.swboxh)

        # Box for all the boxes
        self.rootbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # root box to window
        self.set_child(self.rootbox)

        # Add the stack to the root box
        self.rootbox.append(self.stack)

        # Box with all the buttons
        self.buttonbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.buttonbox.set_margin_top(20)
        self.buttonbox.set_margin_bottom(20)
        self.buttonbox.set_margin_start(20)
        self.buttonbox.set_margin_end(20)
        self.buttonbox.set_spacing(100)
        self.buttonbox.set_homogeneous(True)
        self.button = Gtk.Button(label="Hello there!")
        self.button.connect('clicked', self.hello)
        self.button2 = Gtk.Button(label="MPD")
        self.button2.connect('clicked', self.list_mpd_root)
        self.buttonbox.append(self.button) # Put button in the first of the two vertial boxes
        self.buttonbox.append(self.button2) # Put button in the first of the two vertial boxes

        self.check = Gtk.CheckButton(label="And goodbye?")

        # Add the button box to the stack page
        self.stack.add_titled(self.buttonbox, "1", "Now playing")
        self.stack.add_titled(self.check, "2", "Browse")

    def hello(self, button):
        print("General Kenobi...")

    def list_mpd_root(self, button):
        self.dialog = Gtk.MessageDialog(text="Server's response", secondary_text=client.client_test())
        self.dialog.present()
        print(client.client_test())

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.window = MainWindow(application=app)
        self.window.present()

if __name__ == "__main__":
    app = MyApp(application_id="com.example.GtkApplication")
    app.run(sys.argv)
