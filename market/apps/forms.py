from parsley.decorators import parsleyfy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms

from market.apps.models import App, Review

class AppForm(forms.ModelForm):
    class Meta:
        model = App

@parsleyfy
class SubmitAppForm(forms.Form):
    xml = forms.URLField(
        label = "Install URL",
        required = True,
    )

    def __init__(self, *args, **kwargs):
        super(SubmitAppForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-form-submit-app'
        self.helper.form_class = 'form-submit-app'
        self.helper.form_method = 'post'
        self.helper.form_action = 'apps_submit'

        self.helper.add_input(Submit('submit', 'Submit'))

@parsleyfy
class ReviewForm(forms.Form):
    rating = forms.TypedChoiceField(
        label = "Rating",
        choices = Review.RATING_OPTIONS,
        coerce = lambda x: int(x),
        widget = forms.RadioSelect,
        initial = '3',
        required = True,
    )

    text = forms.CharField(
        label = "Review",
        max_length = 500,
        widget = forms.Textarea,
        required = False,
    )

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-form-review'
        self.helper.form_class = 'form-review'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('rating', css_class="star"),
            Field('text'),
            #ButtonHolder(
            #    Submit('submit', 'Submit')
            #)
        )

        self.helper.add_input(Submit('submit', 'Submit'))
