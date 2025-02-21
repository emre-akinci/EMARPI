# gui/parts_window_gtk3.py

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from database import SessionLocal
from database.models import Part

class AddPartDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Add New Part", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(400, 300)
        
        box = self.get_content_area()
        grid = Gtk.Grid()
        grid.set_column_spacing(8)
        grid.set_row_spacing(8)
        grid.set_border_width(12)
        box.add(grid)

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
            label = Gtk.Label(label=label_text)
            label.set_halign(Gtk.Align.END)
            entry = Gtk.Entry()
            self.entries[key] = entry

            grid.attach(label, 0, row, 1, 1)
            grid.attach(entry, 1, row, 1, 1)
            row += 1

        self.manufactured_here_check = Gtk.CheckButton("Manufactured Here?")
        self.rohs_check = Gtk.CheckButton("RoHS Compliant?")
        grid.attach(self.manufactured_here_check, 0, row, 2, 1)
        row += 1
        grid.attach(self.rohs_check, 0, row, 2, 1)
        row += 1

        label = Gtk.Label(label="Comment")
        label.set_halign(Gtk.Align.END)
        self.comment_view = Gtk.TextView()
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.comment_view)
        scrolled.set_min_content_height(60)

        grid.attach(label, 0, row, 1, 1)
        grid.attach(scrolled, 1, row, 1, 1)
        row += 1

        self.show_all()

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
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_border_width(6)

        # Top button bar
        button_box = Gtk.Box(spacing=6)
        self.pack_start(button_box, False, False, 0)

        add_button = Gtk.Button("Add Part")
        add_button.connect("clicked", self.on_add_part_clicked)
        button_box.pack_start(add_button, False, False, 0)

        refresh_button = Gtk.Button("Refresh")
        refresh_button.connect("clicked", self.on_refresh_clicked)
        button_box.pack_start(refresh_button, False, False, 0)

        # TreeView to list parts
        self.store = Gtk.ListStore(int, str, str, str)
        self.treeview = Gtk.TreeView(self.store)

        for i, col_title in enumerate(["ID", "Part Number", "Manufacturer", "Description"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            self.treeview.append_column(column)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.treeview)
        self.pack_start(scrolled, True, True, 0)

        self.load_parts()

    def load_parts(self):
        self.store.clear()
        session = SessionLocal()
        parts = session.query(Part).order_by(Part.id.desc()).all()
        for p in parts:
            self.store.append([p.id, p.part_number, p.manufacturer or "", p.description or ""])
        session.close()

    def on_add_part_clicked(self, widget):
        dialog = AddPartDialog(self.get_toplevel())
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            data = dialog.get_part_data()
            session = SessionLocal()
            new_part = Part(**data)
            session.add(new_part)
            session.commit()
            session.close()
            self.load_parts()

        dialog.destroy()

    def on_refresh_clicked(self, widget):
        self.load_parts()
