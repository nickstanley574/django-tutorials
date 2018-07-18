from django import forms 

class CommentForm(forms.Form):
    
    name = forms.CharField(max_length=20, 
        widget=forms.TextInput(attrs={'class' : 'from-control', 'placeholder' : 'Name'})) 
    comment = forms.CharField(widget=forms.Textarea(attrs={'class' : 'from-control', 'placeholder' : 'Comment'})) 