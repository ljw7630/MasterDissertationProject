from django.forms import ModelForm
from models import Triple


class TripleForm(ModelForm):
	class Meta:
		model = Triple
		exclude = ('answer')

	def __init__(self, *args, **kwargs):
		super(TripleForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)

		if instance and instance.pk:
			self.fields['predicate'].widget.attrs['readonly'] = True

	def clean_predicate(self):
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			return instance.predicate
		else:
			return self.cleaned_data['predicate']