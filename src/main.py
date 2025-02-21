# src/main.py

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from database import engine
from database.models import Base
from gui.parts_window_gtk3 import PartsWindow
from gui.bom_window_gtk3 import BOMWindow

class EMARPIApp(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="EMARPI Aligni Clone - Full Functionality (GTK3)")
        self.set_default_size(1000, 700)

        # Create a Notebook (tabs)
        notebook = Gtk.Notebook()
        self.add(notebook)

        # Parts Management Tab
        parts_tab = PartsWindow()
        notebook.append_page(parts_tab, Gtk.Label("Parts"))

        # BOM Management Tab
        bom_tab = BOMWindow()
        notebook.append_page(bom_tab, Gtk.Label("BOM"))

        # Future tabs: Inventory, MRP, etc. can be added here.

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

def main():
    # Initialize database tables
    Base.metadata.create_all(bind=engine)
    app = EMARPIApp()
    Gtk.main()

if __name__ == "__main__":
    main()
