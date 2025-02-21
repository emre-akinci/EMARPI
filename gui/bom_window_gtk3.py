# gui/bom_window_gtk3.py

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from database import SessionLocal
from database.models import BOMItem, Part

class BOMWindow(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_border_width(6)
        
        # Button bar: Add BOM Item, Refresh
        button_box = Gtk.Box(spacing=6)
        self.pack_start(button_box, False, False, 0)
        
        add_button = Gtk.Button("Add BOM Item")
        add_button.connect("clicked", self.on_add_bom_clicked)
        button_box.pack_start(add_button, False, False, 0)
        
        refresh_button = Gtk.Button("Refresh")
        refresh_button.connect("clicked", self.on_refresh_clicked)
        button_box.pack_start(refresh_button, False, False, 0)
        
        # TreeView to list BOM items
        self.store = Gtk.ListStore(int, str, str, float, str)
        self.treeview = Gtk.TreeView(self.store)
        for i, col_title in enumerate(["ID", "Parent Part", "Child Part", "Quantity", "Ref Designator"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            self.treeview.append_column(column)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.treeview)
        self.pack_start(scrolled, True, True, 0)
        
        self.load_bom_items()
    
    def load_bom_items(self):
        self.store.clear()
        session = SessionLocal()
        bom_items = session.query(BOMItem).order_by(BOMItem.id.desc()).all()
        for item in bom_items:
            # Retrieve parent and child part numbers for display
            parent = session.query(Part).get(item.parent_part_id)
            child = session.query(Part).get(item.child_part_id)
            parent_num = parent.part_number if parent else "N/A"
            child_num = child.part_number if child else "N/A"
            self.store.append([item.id, parent_num, child_num, item.quantity, item.reference_designator or ""])
        session.close()
    
    def on_add_bom_clicked(self, widget):
        dialog = AddBOMDialog(self.get_toplevel())
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            data = dialog.get_bom_data()
            session = SessionLocal()
            new_item = BOMItem(**data)
            session.add(new_item)
            session.commit()
            session.close()
            self.load_bom_items()
        dialog.destroy()
    
    def on_refresh_clicked(self, widget):
        self.load_bom_items()

class AddBOMDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Add BOM Item", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(400, 200)
        box = self.get_content_area()
        grid = Gtk.Grid()
        grid.set_column_spacing(8)
        grid.set_row_spacing(8)
        grid.set_border_width(12)
        box.add(grid)
        
        # Entries for Parent Part, Child Part, Quantity, Reference Designator
        self.entries = {}
        row = 0
        for label_text, key in [
            ("Parent Part ID", "parent_part_id"),
            ("Child Part ID", "child_part_id"),
            ("Quantity", "quantity"),
            ("Reference Designator", "reference_designator"),
        ]:
            label = Gtk.Label(label=label_text)
            label.set_halign(Gtk.Align.END)
            entry = Gtk.Entry()
            self.entries[key] = entry
            grid.attach(label, 0, row, 1, 1)
            grid.attach(entry, 1, row, 1, 1)
            row += 1
        
        self.show_all()
    
    def get_bom_data(self):
        try:
            parent_part_id = int(self.entries["parent_part_id"].get_text().strip())
        except ValueError:
            parent_part_id = 0
        try:
            child_part_id = int(self.entries["child_part_id"].get_text().strip())
        except ValueError:
            child_part_id = 0
        try:
            quantity = float(self.entries["quantity"].get_text().strip())
        except ValueError:
            quantity = 1.0
        
        reference_designator = self.entries["reference_designator"].get_text().strip()
        return {
            "parent_part_id": parent_part_id,
            "child_part_id": child_part_id,
            "quantity": quantity,
            "reference_designator": reference_designator
        }
