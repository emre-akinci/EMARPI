# gui/parts_window.py

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk

from database import SessionLocal
from database.models import Part

class AddPartDialog(Gtk.Dialog):
    """
    A simple dialog to add a new Part.
    """
    def __init__(self, parent):
        super().__init__(title="Add New Part", transient_for=parent, modal=True)

        self.set_default_size(400, 300)
        box = self.get_content_area()

        grid = Gtk.Grid(column_spacing=8, row_spacing=8, margin=12)
        box.append(grid)

        # Labels & Entries
        self.entries = {}

        row = 0
        for label_text, key in [
            ("Part Number", "part_number"),
            ("Part Type", "part_type"),
            ("Manufacturer", "manufacturer"),
            ("MFR Part #", "manufacturer_part_number"),
            ("Description", "description"),
            ("Value", "value"),
            ("Use-As Units", "use_as_units"),
        ]:
            label = Gtk.Label(label=label_text, halign=Gtk.Align.END)
            entry = Gtk.Entry()
            self.entries[key] = entry

            grid.attach(label, 0, row, 1, 1)
            grid.attach(entry, 1, row, 1, 1)
            row += 1

        # Checkboxes
        self.manufactured_here_check = Gtk.CheckButton(label="Manufactured Here?")
        self.rohs_check = Gtk.CheckButton(label="RoHS Compliant?")
        grid.attach(self.manufactured_here_check, 0, row, 2, 1)
        row += 1
        grid.attach(self.rohs_check, 0, row, 2, 1)
        row += 1

        # Comment (multi-line)
        label = Gtk.Label(label="Comment", halign=Gtk.Align.END)
        self.comment_view = Gtk.TextView()
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_child(self.comment_view)
        scrolled_window.set_min_content_height(60)

        grid.attach(label, 0, row, 1, 1)
        grid.attach(scrolled_window, 1, row, 1, 1)
        row += 1

        # Buttons
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Add Part", Gtk.ResponseType.OK)
        self.show()

    def get_part_data(self):
        buffer = self.comment_view.get_buffer()
        start_iter, end_iter = buffer.get_bounds()
        comment_text = buffer.get_text(start_iter, end_iter, False)

        return {
            "part_number": self.entries["part_number"].get_text().strip(),
            "part_type": self.entries["part_type"].get_text().strip(),
            "manufacturer": self.entries["manufacturer"].get_text().strip(),
            "manufacturer_part_number": self.entries["manufacturer_part_number"].get_text().strip(),
            "description": self.entries["description"].get_text().strip(),
            "value": self.entries["value"].get_text().strip(),
            "use_as_units": self.entries["use_as_units"].get_text().strip(),
            "manufactured_here": self.manufactured_here_check.get_active(),
            "rohs_compliant": self.rohs_check.get_active(),
            "comment": comment_text.strip()
        }


class PartsWindow(Gtk.Box):
    """
    Main widget to display a list of Parts and let you add new ones.
    """
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_margin_start(6)
        self.set_margin_end(6)
        self.set_margin_top(6)
        self.set_margin_bottom(6)

        # Top button bar
        button_box = Gtk.Box(spacing=6)
        self.append(button_box)

        add_button = Gtk.Button(label="Add Part")
        add_button.connect("clicked", self.on_add_part_clicked)
        button_box.append(add_button)

        refresh_button = Gtk.Button(label="Refresh")
        refresh_button.connect("clicked", self.on_refresh_clicked)
        button_box.append(refresh_button)

        # TreeView
        self.store = Gtk.ListStore(int, str, str, str) 
        # columns: ID, part_number, manufacturer, description

        self.treeview = Gtk.TreeView(model=self.store)

        for i, col_title in enumerate(["ID", "Part Number", "Manufacturer", "Description"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            self.treeview.append_column(column)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(self.treeview)
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        self.append(scrolled)

        # Load data initially
        self.load_parts()

    def load_parts(self):
        self.store.clear()
        session = SessionLocal()
        parts = session.query(Part).order_by(Part.id.desc()).all()
        for p in parts:
            self.store.append([p.id, p.part_number, p.manufacturer or "", p.description or ""])
        session.close()

    def on_add_part_clicked(self, button):
        dialog = AddPartDialog(self.get_root())
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            data = dialog.get_part_data()
            # Save to DB
            session = SessionLocal()
            new_part = Part(**data)
            session.add(new_part)
            session.commit()
            session.close()
            self.load_parts()

        dialog.destroy()

    def on_refresh_clicked(self, button):
        self.load_parts()
