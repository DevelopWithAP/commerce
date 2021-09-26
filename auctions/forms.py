from auctions.models import Listing
from .models import Listing, Bid, Comment 
from django import forms

class CreateForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title", "description", "image",
            "category", "price"
        ]
        labels = {
            "title": "",
            "description": "",
            "image": "",
            "category": "",
            "price": "",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Product Title",
                    "class": "form-control mt-1"
                }),
            "description": forms.Textarea(attrs={
                "placeholder": "Product Description",
                "class": "form-control mt-1",
                "rows": 3
            }),
            "image": forms.URLInput(attrs={
                "class": "form-control mt-1",
                "placeholder": "Image URL",
            }),
            "price": forms.NumberInput(attrs={
                "placeholder": "Suggested Price (GBP)",
                "class": "form-control mt-1"
            }),
            "category": forms.Select(attrs={
                "placeholder": "Product Category",
                "class": "form-control mt-1"
            })
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        labels = {"amount": ""}
        widgets = {
            "amount" : forms.NumberInput(attrs = {
                "placeholder": "Your offer",
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"] 
        labels = {"text": ""}
        widgets = {
            "text": forms.Textarea(
                attrs= {
                    "placeholder" : "Comment",
                    "class": "form-control",
                    "rows" : 2
                }
            )
        }