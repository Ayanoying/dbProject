from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QLineEdit,
    QLabel,
    QTextEdit,
)

from services.shopService import ShopService
from session import Session


class ShopView(QWidget):
    """Shop page to browse, buy, and activate cosmetic items."""

    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.service = ShopService()
        self.setWindowTitle("Boutique")
        self.setMinimumSize(800, 600)
        self.init_ui()
        self.refresh_items()
        self.refresh_inventory()

    def init_ui(self):
        layout = QVBoxLayout()

        self.items_label = QLabel("Objets disponibles")
        self.items_text = QTextEdit()
        self.items_text.setReadOnly(True)

        self.inventory_label = QLabel("Inventaire")
        self.inventory_text = QTextEdit()
        self.inventory_text.setReadOnly(True)

        self.item_id_input = QLineEdit()
        self.item_id_input.setPlaceholderText("ID de l'objet")

        self.btn_refresh = QPushButton("Rafraîchir")
        self.btn_buy = QPushButton("Acheter")
        self.btn_activate = QPushButton("Activer")
        self.btn_back = QPushButton("Retour")

        self.btn_refresh.clicked.connect(self.refresh_all)
        self.btn_buy.clicked.connect(self.buy_item)
        self.btn_activate.clicked.connect(self.activate_item)
        if self.main_window is not None:
            self.btn_back.clicked.connect(self.main_window.go_home)

        layout.addWidget(self.items_label)
        layout.addWidget(self.items_text)
        layout.addWidget(self.inventory_label)
        layout.addWidget(self.inventory_text)
        layout.addWidget(self.item_id_input)
        layout.addWidget(self.btn_refresh)
        layout.addWidget(self.btn_buy)
        layout.addWidget(self.btn_activate)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

    def refresh_all(self):
        self.refresh_items()
        self.refresh_inventory()

    def refresh_items(self):
        items = self.service.list_items()
        if not items:
            self.items_text.setPlainText("Aucun objet disponible.")
            return

        header = "ID | NOM | TYPE | DESCRIPTION | POINTS"
        rows = "\n".join(
            f"{item[0]} | {item[1]} | {item[2]} | {item[3]} | {item[4]}"
            for item in items
        )
        text = f"{header}\n{rows}"
        self.items_text.setPlainText(text)

    def refresh_inventory(self):
        if not Session.is_authenticated():
            self.inventory_text.setPlainText(
                "Connectez-vous pour voir votre inventaire."
            )
            return

        inventory = self.service.list_inventory()
        if not inventory:
            self.inventory_text.setPlainText("Inventaire vide.")
            return

        text = "\n".join(
            f"{item[0]} | {item[1]} | {item[2]} | {item[3]} | active={item[4]}"
            for item in inventory
        )
        self.inventory_text.setPlainText(text)

    def _selected_item_id(self):
        raw_value = self.item_id_input.text().strip()
        if not raw_value.isdigit():
            return None
        return int(raw_value)

    def buy_item(self):
        if not Session.is_authenticated():
            QMessageBox.warning(self, "Erreur", "Vous devez être connecté.")
            return

        item_id = self._selected_item_id()
        if item_id is None:
            QMessageBox.warning(self, "Erreur", "Entrez un ID d'objet valide.")
            return

        success = self.service.buy_item(item_id)
        if success:
            QMessageBox.information(self, "Boutique", "Objet acheté avec succès.")
            self.refresh_all()
        else:
            QMessageBox.warning(self, "Boutique", "Achat impossible.")

    def activate_item(self):
        if not Session.is_authenticated():
            QMessageBox.warning(self, "Erreur", "Vous devez être connecté.")
            return

        item_id = self._selected_item_id()
        if item_id is None:
            QMessageBox.warning(self, "Erreur", "Entrez un ID d'objet valide.")
            return

        success = self.service.activate_item(item_id)
        if success:
            QMessageBox.information(self, "Boutique", "Objet activé.")
            self.refresh_all()
        else:
            QMessageBox.warning(self, "Boutique", "Activation impossible.")
