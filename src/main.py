# src/main.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from gui.parts_window import PartsWindow
from database import engine
from database.models import Base

class EMARPIApp(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="EMARPI Aligni Clone - Parts (GTK3)")
        self.set_default_size(800, 600)
        self.add(PartsWindow())
        self.connect("destroy", Gtk.main_quit)
        self.show_all()

def main():
    # Ensure the database tables exist
    Base.metadata.create_all(bind=engine)

    app = EMARPIApp()
    Gtk.main()

if __name__ == "__main__":
    main()
