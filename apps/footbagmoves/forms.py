from django import forms

from apps.footbagmoves.models import MoveDemonstrationVideo
from apps.footbagmoves.models import URL_VIDEO_TYPE, YOUTUBE_VIDEO_TYPE, VIDEO_TYPES

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
        return cleaned_data
