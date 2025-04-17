from django import forms
from .models import DataSource, DataPack


class ContentSourceSelectionForm(forms.Form):
    sources = forms.ModelMultipleChoiceField(
        queryset=DataSource.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Get installed sources for this user
            installed_packs = DataPack.objects.filter(is_installed=True)
            self.fields['sources'].queryset = DataSource.objects.filter(
                id__in=installed_packs.values('source')
            )