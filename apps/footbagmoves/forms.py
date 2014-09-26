from django import forms
from django.forms.models import BaseInlineFormSet

from apps.footbagmoves.models import MoveDemonstrationVideo
from apps.footbagmoves.models import URL_VIDEO_TYPE, YOUTUBE_VIDEO_TYPE, VIDEO_TYPES


class ComponentsInlineFormset(BaseInlineFormSet):
    """ A formset that requires you to enter at least one entry in order to validate.
    This is used for entering in the components for the footbag moves."""
    def clean(self):
        """Check that at least one has been entered"""
        super(ComponentsInlineFormset, self).clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
                for cleaned_data in self.cleaned_data):
            raise forms.ValidationError('At least one item is required.')
        components_entered = set()
        for component in self.cleaned_data:
            seq_number = component.get('sequence_number', False)
            if seq_number and seq_number in components_entered:
                raise forms.ValidationError('A sequence number was repeated, sequence numbers must be unique')
            else:
                components_entered.add(seq_number)


class VideoEntryForm(forms.ModelForm):
    """A form for entering in video details """

    class Meta:
        model = MoveDemonstrationVideo
        fields = (
                'video_type',
                'URL',
                'use_start',
                'use_end',
                'start_time',
                'end_time',
        )

    def clean(self):
        """ Validate that the end time is after the start time""" 
        start = self.cleaned_data.get("use_start")
        end = self.cleaned_data.get("use_end")
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")
        if start and end and (start_time > end_time):
            raise forms.ValidationError("Error: Invalid timestamp, start time is after the end time")
            #TODO: need to remove invalid items by using del?
        return self.cleaned_data

class VideosFormset(BaseInlineFormSet):
    """A set of video entry forms """
    def is_valid(self):
        return (super(VideosFormset,self).is_valid() and
                not any(bool(e) for e in self.errors))

    def clean(self):
        super(VideosFormset, self).clean()
        for form in self.forms:
            form.is_valid()
