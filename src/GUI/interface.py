import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
import sys
import os

# Agrega la ruta al sistema
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logic.logica import calculate_item_total, calculate_total_purchase 

# Constantes
FIXED_TAX_PER_PLASTIC_BAG = 66

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Título
        self.add_widget(Label(text="--- Menú de Cálculo de Impuestos ---", font_size=24))
        
        # Botones
        self.item_button = Button(text="1. Calcular Total Item", size_hint=(1, 0.2))
        self.item_button.bind(on_press=self.open_item_popup)
        self.add_widget(self.item_button)

        self.purchase_button = Button(text="2. Calcular Total Compra", size_hint=(1, 0.2))
        self.purchase_button.bind(on_press=self.open_purchase_popup)
        self.add_widget(self.purchase_button)

        self.exit_button = Button(text="3. Salir", size_hint=(1, 0.2))
        self.exit_button.bind(on_press=self.exit_app)
        self.add_widget(self.exit_button)

    def open_item_popup(self, instance):
        self.item_popup = ItemPopup()
        self.item_popup.open()

    def open_purchase_popup(self, instance):
        self.purchase_popup = PurchasePopup()
        self.purchase_popup.open()

    def exit_app(self, instance):
        App.get_running_app().stop()

class ItemPopup(Popup):
    def __init__(self, **kwargs):
        super(ItemPopup, self).__init__(**kwargs)
        self.title = "Calcular Total Item"
        self.size_hint = (0.8, 0.8)

        layout = BoxLayout(orientation='vertical')
        
        # Campos de entrada
        self.price_input = TextInput(hint_text="Precio unitario del artículo", multiline=False)
        self.quantity_input = TextInput(hint_text="Cantidad del artículo", multiline=False)

        # Dropdown para selección de impuestos
        self.tax_spinner = Spinner(
            text='Seleccione Impuesto',
            values=( 
                'IVA 19%', 'IVA 5%', 'Exento', 'Bolsas Plásticas (66 COP)',
                'Vehículo mayor a 200cc (8%)', 
                'Licores < 35% (25%)', 
                'Licores > 35% (40%)', 
                'Vinos < 14% (20%)', 
                'Vinos > 14% (20%)'
            ),
            size_hint=(1, None),
            height=40
        )

        layout.add_widget(Label(text="Ingrese el precio y la cantidad del artículo:"))
        layout.add_widget(self.price_input)
        layout.add_widget(self.quantity_input)
        layout.add_widget(self.tax_spinner)
        
        # Botón para calcular total
        self.calc_button = Button(text="Calcular", size_hint=(1, 0.2))
        self.calc_button.bind(on_press=self.calculate_item)
        layout.add_widget(self.calc_button)

        # Etiqueta para mostrar el total de impuestos y precio
        self.result_label = Label(text="")
        layout.add_widget(self.result_label)

        self.content = layout

    def calculate_item(self, instance):
        try:
            unit_price = float(self.price_input.text)
            quantity = int(self.quantity_input.text)
            selected_tax = self.tax_spinner.text

            # Determinar el tipo de impuesto según la selección
            if selected_tax == 'IVA 19%':
                tax_type = 19
            elif selected_tax == 'IVA 5%':
                tax_type = 5
            elif selected_tax == 'Exento':
                tax_type = 0
            elif selected_tax == 'Bolsas Plásticas (66 COP)':
                tax_type = FIXED_TAX_PER_PLASTIC_BAG  # Usar valor positivo
            elif selected_tax == 'Vehículo mayor a 200cc (8%)':
                tax_type = 8
            elif selected_tax == 'Licores < 35% (25%)':
                tax_type = 25
            elif selected_tax == 'Licores > 35% (40%)':
                tax_type = 40
            elif selected_tax == 'Vinos < 14% (20%)':
                tax_type = 20
            elif selected_tax == 'Vinos > 14% (20%)':
                tax_type = 20
            
            # Calcular el total de impuestos y el total del artículo
            if selected_tax == 'Bolsas Plásticas (66 COP)':
                total_tax = tax_type * quantity  # Total de impuestos para bolsas plásticas
            else:
                total_tax = (unit_price * tax_type / 100) * quantity  # Cálculo estándar de impuestos
            
            total_item = (unit_price * quantity) + total_tax
            self.result_label.text = f"Total Impuesto: {total_tax:.2f}\nTotal Ítem: {total_item:.2f}"
        except Exception as e:
            self.result_label.text = f"Error: {e}"

class PurchasePopup(Popup):
    def __init__(self, **kwargs):
        super(PurchasePopup, self).__init__(**kwargs)
        self.title = "Calcular Total Compra"
        self.size_hint = (0.8, 0.8)

        layout = BoxLayout(orientation='vertical')

        # Agregar una explicación
        layout.add_widget(Label(text="Ingrese los detalles de los artículos:"))

        # Lista de entradas de artículos
        self.item_data = []

        self.add_item_button = Button(text="Agregar Artículo", size_hint=(1, 0.2))
        self.add_item_button.bind(on_press=self.add_item)
        layout.add_widget(self.add_item_button)

        self.calc_button = Button(text="Calcular Total Compra", size_hint=(1, 0.2))
        self.calc_button.bind(on_press=self.calculate_purchase)
        layout.add_widget(self.calc_button)

        self.result_label = Label(text="")
        layout.add_widget(self.result_label)

        self.content = layout

    def add_item(self, instance):
        # Crear un nuevo conjunto de campos de entrada para un artículo
        item_layout = BoxLayout(orientation='horizontal')
        price_input = TextInput(hint_text="Precio", multiline=False)
        quantity_input = TextInput(hint_text="Cantidad", multiline=False)
        
        # Dropdown para selección de impuestos
        tax_spinner = Spinner(
            text='Seleccione Impuesto',
            values=(
                'IVA 19%', 'IVA 5%', 'Exento', 'Bolsas Plásticas (66 COP)',
                'Vehículo mayor a 200cc (8%)', 
                'Licores < 35% (25%)', 
                'Licores > 35% (40%)', 
                'Vinos < 14% (20%)', 
                'Vinos > 14% (20%)'
            ),
            size_hint=(1, None),
            height=40
        )
        
        self.item_data.append((price_input, quantity_input, tax_spinner))
        item_layout.add_widget(price_input)
        item_layout.add_widget(quantity_input)
        item_layout.add_widget(tax_spinner)

        self.content.add_widget(item_layout)

    def calculate_purchase(self, instance):
        items = []
        total_fixed_tax = 0  # Acumulador para el impuesto fijo de bolsas plásticas
        total_item_price = 0  # Acumulador para el precio total de los artículos
        try:
            for price_input, quantity_input, tax_spinner in self.item_data:
                selected_tax = tax_spinner.text
                
                # Si el impuesto es por bolsas plásticas
                if selected_tax == 'Bolsas Plásticas (66 COP)':
                    quantity = int(quantity_input.text)
                    total_fixed_tax += quantity * FIXED_TAX_PER_PLASTIC_BAG  # Solo sumar el total del impuesto fijo
                    total_item_price += float(price_input.text) * quantity  # Sumar el precio del artículo
                else:
                    unit_price = float(price_input.text)
                    quantity = int(quantity_input.text)
                    
                    # Determinar el tipo de impuesto según la selección
                    if selected_tax == 'IVA 19%':
                        tax_type = 19
                    elif selected_tax == 'IVA 5%':
                        tax_type = 5
                    elif selected_tax == 'Exento':
                        tax_type = 0
                    elif selected_tax == 'Vehículo mayor a 200cc (8%)':
                        tax_type = 8
                    elif selected_tax == 'Licores < 35% (25%)':
                        tax_type = 25
                    elif selected_tax == 'Licores > 35% (40%)':
                        tax_type = 40
                    elif selected_tax == 'Vinos < 14% (20%)':
                        tax_type = 20
                    elif selected_tax == 'Vinos > 14% (20%)':
                        tax_type = 20

                    # Agregar al total con precio unitario y el impuesto
                    items.append((unit_price, quantity, tax_type))
                    total_item_price += unit_price * quantity  # Sumar el precio del artículo

            total_tax, total_purchase = calculate_total_purchase(items)
            total_purchase += total_fixed_tax + total_item_price  # Sumar el impuesto fijo y el precio total de los artículos
            self.result_label.text = f"Total Impuesto: {total_tax + total_fixed_tax:.2f}\nTotal a Pagar: {total_purchase:.2f}"
        except Exception as e:
            self.result_label.text = f"Error: {e}"


class MyApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    MyApp().run()