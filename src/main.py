# src/main.py

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio

from database import engine
from database.models import Base
from gui.parts_window import PartsWindow

class EMARPIApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.emarpi.AligniClone",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        # Ensure DB tables exist (auto-migration)
        Base.metadata.create_all(bind=engine)

        window = Gtk.ApplicationWindow(application=self)
        window.set_title("EMARPI Aligni Clone - Parts")
        window.set_default_size(800, 600)

        parts_view = PartsWindow()
        window.set_child(parts_view)

        window.present()

def main():
    app = EMARPIApp()
    app.run()

if __name__ == "__main__":
    main()
