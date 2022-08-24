import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib

from . import client

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build_main_view(self)
        GLib.set_application_name("mphandy")
        self.c = client.mpdclient()

    def build_stack_switcher(self):
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

    def build_root_box(self):
        # Box for all the boxes
        self.rootbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # root box to window
        self.set_child(self.rootbox)
        # Add the stack to the root box
        self.rootbox.append(self.stack)

    def build_player_box(self):
        # Create a vertical box to house the second box and the album art
        playerbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        playerbox.set_margin_top(50)
        playerbox.set_margin_bottom(10)
        playerbox.set_margin_start(20)
        playerbox.set_margin_end(20)
        playerbox.set_spacing(100)
        # Create album art
        albumart = Gtk.Image.new_from_file("img.png")
        albumart.set_pixel_size(300)
        playerbox.append(albumart)
        # Create another vertical box for all other elements
        elementbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        elementbox.set_spacing(10)
        elementbox.set_homogeneous(True)
        playerbox.append(elementbox)
        # Create the current song info section
        infobox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        infobox.set_spacing(1)
        infobox.set_homogeneous(True)
        artistname = Gtk.Label.new()
        albumname = Gtk.Label.new()
        songname = Gtk.Label.new()
        artistname.set_markup("<span font_weight=\"normal\">Album Artist</span>")
        albumname.set_markup("<span font_weight=\"light\">Album Name</span>")
        songname.set_markup("<span size=\"large\" font_weight=\"bold\">Song Name</span>")
        infobox.append(artistname)
        infobox.append(albumname)
        infobox.append(songname)
        elementbox.append(infobox)
        # Create the playback controls section
        controlsbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        controlsbox.set_homogeneous(True)
        controlsbox.set_spacing(5)
        playbutton = Gtk.Button()
        prevbutton = Gtk.Button()
        nextbutton = Gtk.Button()
        playbutton.set_icon_name("media-playback-start-symbolic")
        prevbutton.set_icon_name("media-skip-backward-symbolic")
        nextbutton.set_icon_name("media-skip-forward-symbolic")
        prevbutton.set_has_frame(False)
        nextbutton.set_has_frame(False)
        playbutton.connect('clicked', self.list_mpd_root)
        controlsbox.append(prevbutton)
        controlsbox.append(playbutton)
        controlsbox.append(nextbutton)
        elementbox.append(controlsbox)
        # Create the playback progress section
        progressbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        progressbox.set_homogeneous(True)
        controlsbox.set_spacing(2)
        curtime = Gtk.Label.new("00:00")
        songprogress = Gtk.Scale.new(Gtk.Orientation.HORIZONTAL, Gtk.Adjustment.new(25, 0, 100, 1, 1, 1))
        songlen = Gtk.Label.new("03:21")
        progressbox.append(curtime)
        progressbox.append(songprogress)
        progressbox.append(songlen)
        elementbox.append(progressbox)
        self.stack.add_titled(playerbox, "1", "Now playing")

    def build_browser_box(self):
        # Box with all the buttons
        browserbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        browserbox.set_margin_top(20)
        browserbox.set_margin_bottom(20)
        browserbox.set_margin_start(20)
        browserbox.set_margin_end(20)
        browserbox.set_spacing(100)
        browserbox.set_homogeneous(True)
        button = Gtk.Button(label="Hello there!")
        button.connect('clicked', self.hello)
        button2 = Gtk.Button(label="MPD")
        button2.connect('clicked', self.list_mpd_root)
        browserbox.append(button) # Put button in the first of the two vertial boxes
        browserbox.append(button2) # Put button in the first of the two vertial boxes
        self.stack.add_titled(browserbox, "2", "Browse")

    def build_hamburger_menu(self):
        # Create a new action
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.show_about)
        self.add_action(about_action)

        menu = Gio.Menu.new()
        menu.append("About", "win.about")

        popover = Gtk.PopoverMenu()
        popover.set_menu_model(menu)

        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(popover)
        self.hamburger.set_icon_name("open-menu-symbolic")
        self.header.pack_end(self.hamburger)

    def build_main_view(self, *args, **kwargs):
        # These functions build the contents of the main window
        self.build_stack_switcher()
        self.build_root_box()
        self.build_player_box()
        self.build_browser_box()
        self.build_hamburger_menu()

    def hello(self, button):
        print("General Kenobi...")

    def list_mpd_root(self, button):
        self.dialog = Gtk.MessageDialog(text="Server's response", secondary_text=self.c.get_song_info())
        self.dialog.add_button("Ok", 1)
        self.dialog.connect("response", self.close_dialog)
        self.dialog.set_transient_for(self)
        self.dialog.set_modal(self)
        self.dialog.present()

    def close_dialog(self, action, param):
        self.dialog.close()

    def show_about(self, action, param):
        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self)
        self.about.set_modal(self)
        self.about.set_authors(["k8ieone"])
        self.about.set_copyright("Copyright 2022 k8ieone")
        self.about.set_license_type(Gtk.License.MIT_X11)
        self.about.set_website("https://github.com/k8ieone/mphandy")
        self.about.set_website_label("GitHub repo")
        self.about.set_version("(version too early to tell)")
        self.about.set_logo_icon_name("org.example.example") # Location: /usr/share/icons/hicolor/scalable/apps/org.example.example.svg
        self.about.show()

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.window = MainWindow(application=app)
        self.window.present()

if __name__ == "__main__":
    app = MyApp(application_id="one.k8ie.mphandy")
    app.run(sys.argv)
