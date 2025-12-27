from django.forms import ModelForm
from django import forms
from store.models import Contact, Product, Category, BillingAddress



INPUT_CLASSES = 'form-control border-0 py-4'



class AddContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = ['name','email','subject','message']

        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Email'}),
            'subject': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': INPUT_CLASSES, 'placeholder': 'Your Message'}),
        }


class AddProductForm(ModelForm):
    
    class Meta:
        model = Product
        fields = ['category','name','slug','price','stock','description','sizes','colors','thumbnail'] 

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control border-0 px-2'}),
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Name'}),
            'slug': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Slug'}),
            'price': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Price'}),
            'stock': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Stock'}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES, 'placeholder': 'Description'}),
            'sizes': forms.CheckboxSelectMultiple(),
            'colors': forms.CheckboxSelectMultiple(),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control border-0 px-2'}),
        }

class EditProductForm(ModelForm):
    
    class Meta:
        model = Product
        fields = ['name','slug','price','stock','description','sizes','colors','thumbnail','out_of_stock'] 

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control border-0 px-2'}),
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Name'}),
            'slug': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Slug'}),
            'price': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Price'}),
            'stock': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Stock'}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES, 'placeholder': 'Description'}),
            'sizes': forms.CheckboxSelectMultiple(),
            'colors': forms.CheckboxSelectMultiple(),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control border-0 px-2'}),
            'out_of_stock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AddCategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'thumbnail']

        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Name'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control border-0 px-2'}),
        }
        

class BillingAddressForm(ModelForm):

    REGION_CHOICES = [
        ('Adrar', 'Adrar'),
        ('Chlef', 'Chlef'),
        ('Laghouat', 'Laghouat'),
        ('Oum El Bouaghi', 'Oum El Bouaghi'),
        ('Batna', 'Batna'),
        ('Bejaia', 'Bejaia'),
        ('Biskra', 'Biskra'),
        ('Bechar', 'Bechar'),
        ('Blida', 'Blida'),
        ('Bouira', 'Bouira'),
        ('Tamanrasset', 'Tamanrasset'),
        ('Tebessa', 'Tebessa'),
        ('Tlemcen', 'Tlemcen'),
        ('Tiaret', 'Tiaret'),
        ('Tizi Ouzou', 'Tizi Ouzou'),
        ('Algiers', 'Algiers'),
        ('Djelfa', 'Djelfa'),
        ('Jijel', 'Jijel'),
        ('Setif', 'Setif'),
        ('Saïda', 'Saïda'),
        ('Skikda', 'Skikda'),
        ('Sidi Bel Abbes', 'Sidi Bel Abbes'),
        ('Annaba', 'Annaba'),
        ('Guelma', 'Guelma'),
        ('Constantine', 'Constantine'),
        ('Medea', 'Medea'),
        ('Mostaganem', 'Mostaganem'),
        ('Msila', 'Msila'),
        ('Mascara', 'Mascara'),
        ('Ouargla', 'Ouargla'),
        ('Oran', 'Oran'),
        ('El Bayadh', 'El Bayadh'),
        ('Illizi', 'Illizi'),
        ('Bordj Bou Arreridj', 'Bordj Bou Arreridj'),
        ('Boumerdes', 'Boumerdes'),
        ('El Tarf', 'El Tarf'),
        ('Tindouf', 'Tindouf'),
        ('Tissemsilt', 'Tissemsilt'),
        ('El Oued', 'El Oued'),
        ('Khenchela', 'Khenchela'),
        ('Souk Ahras', 'Souk Ahras'),
        ('Tipaza', 'Tipaza'),
        ('Mila', 'Mila'),
        ('Aïn Defla', 'Aïn Defla'),
        ('Naama', 'Naama'),
        ('Aïn Temouchent', 'Aïn Temouchent'),
        ('Ghardaia', 'Ghardaia'),
        ('Relizane', 'Relizane'),
        ('Timimoun', 'Timimoun'),
        ('Bordj Badji Mokhtar', 'Bordj Badji Mokhtar'),
        ('Ouled Djellal', 'Ouled Djellal'),
        ('Béni Abbès', 'Béni Abbès'),
        ('In Salah', 'In Salah'),
        ('In Guezzam', 'In Guezzam'),
        ('Touggourt', 'Touggourt'),
        ('Djanet', 'Djanet'),
        ('El M’Ghaier', 'El M’Ghaier'),
        ('El Meniaa', 'El Meniaa'),
    ]

    # Instead of including region in widgets, we define it as a ChoiceField directly within the form class. This is because ChoiceField requires choices (REGION_CHOICES in this case) to be specified explicitly within the form class.
    region = forms.ChoiceField(choices=REGION_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Region / Wilaya'}))

    # Defines the form's metadata, including the model (BillingAddress) and which fields from the model should be included in the form.
    class Meta:
        model = BillingAddress
        fields = ['first_name', 'last_name', 'email', 'mobile_no','region','municipality','street','postal_code']

        # Customizes the HTML attributes of the input elements
        widgets = {
            'first_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'}),
            'mobile_no' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Mobile No'}),
            'municipality' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Municipality'}),
            'street' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
            'postal_code' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Code postal'})
        }




