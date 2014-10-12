from django import forms

from constants import YOUTUBE_VIDEO_TYPE
from video_assets_models import VideoAsset
from video_api_helpers import is_youtube_video

class ComponentsInlineFormset(forms.models.BaseInlineFormSet):
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

    start_time = forms.IntegerField(required=False)
    end_time = forms.IntegerField(required=False)

    class Meta:
        model = VideoAsset
        fields = (
                'video_type',
                'URL',
                'start_time',
                'end_time',
        )

    def clean(self):
        """ Validates the video entry:
            checks the end time is after the start time.
            checks if a youtube video is entered in as a raw url."""
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")
        if start_time and end_time and (start_time >= end_time):
            raise forms.ValidationError("Error: Invalid timestamp, start time is not before the end time")
            #TODO: need to remove invalid items by using del?

        video_type = self.cleaned_data.get("video_type")
        url = self.cleaned_data.get("URL")
        if video_type != YOUTUBE_VIDEO_TYPE and is_youtube_video(url):
            raise forms.ValidationError("Error: a youtube link was entered in as a raw URL. Please use youtube video type instead.")
        return self.cleaned_data

#    def save(self):
#        """Save a video based on the verified data coming out of this form"""
#        pass

class VideosFormset(forms.models.BaseInlineFormSet):
    """A set of video entry forms """
    def is_valid(self):
        """Test that all individual videos are error free"""
        return (super(VideosFormset, self).is_valid() and
                not any(bool(e) for e in self.errors))

    def clean(self):
        """Test that all individual videos are valid"""
        super(VideosFormset, self).clean()
        for form in self.forms:
            form.is_valid()
