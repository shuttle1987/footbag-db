from django import forms
from django.forms.models import BaseInlineFormSet

from apps.footbagmoves.models import MoveDemonstrationVideo
from apps.footbagmoves.models import URL_VIDEO_TYPE, YOUTUBE_VIDEO_TYPE, VIDEO_TYPES


class AtLeastOneRequiredInlineFormset(BaseInlineFormSet):
    """ A formset that requires you to enter at least one entry in order to validate """
    def clean(self):
        """Check that at least one has been entered"""
        super(AtLeastOneRequiredInlineFormset, self).clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
                for cleaned_data in self.cleaned_data):
            raise forms.ValidationError('At least one item is required.')

class VideoEntryForm(forms.ModelForm):
    """A form for entering in video details """
    class Meta:
        model = MoveDemonstrationVideo

    def clean(self):
        """ Validate that the end time is after the start time""" 
        start = self.cleaned_data.get("start_time")
        end = self.cleaned_data.get("end_time")
        if start and end and (start > end):
            raise forms.ValidationError("Error: Invalid timestamp, start time is after the end time")
            #TODO: need to remove invalid items by using del?
        return self.cleaned_data
