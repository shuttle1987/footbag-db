import factory
from django.test import TestCase
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from apps.footbagmoves.models import Component
from apps.footbagmoves.constants import YOUTUBE_VIDEO_TYPE

class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = 'test@example.com'
    username = 'tester'
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')

    is_superuser = True
    is_staff = False
    is_active = True

def management_form_helper(total_forms, initial_forms, max_forms, min_forms):
    return {
        "TOTAL_FORMS": total_forms,
        "INITIAL_FORMS": initial_forms,
        "MIN_NUM_FORMS": min_forms,
        "MAX_NUM_FORMS": max_forms,
    }


def generate_video_formset(prefix, videos, component_id=""):
    """
    Generate the formset for a Video type
    :prefix: formset_prefix
    :videos: list of dictionaries containing video info
    """
    number_videos = len(videos)
    management_form_data = management_form_helper(
        total_forms=number_videos,
        initial_forms=0,
        max_forms=20,
        min_forms=0
    )
    data_dict = {}
    data_dict.update(management_form_data)
    for number, video in enumerate(videos):
        vid_form_data = {
           "%d-video_type"%number : video["video_type"],
           "%d-URL"%number : video["URL"],
           "%d-start_time"%number : video["start_time"],
           "%d-end_time"%number : video["end_time"],
           "%d-component"%number : component_id,
        }
        data_dict.update(vid_form_data)
    return {prefix + "-" + key: value for key, value in data_dict.items()}

class FootbagComponentViews(TestCase):
    """Test views for footbag component creation"""
    def setUp(self):
        self.user = UserFactory.create()

    def new_component_post_data(self, name):
        """Data to post to the page"""
        data = {
            "name": name,
            "tips": "test move",
        }
        component_demonstration_videos_form_data = generate_video_formset(
            prefix="componentdemonstrationvideo_set",
            videos=[{
                "video_type": YOUTUBE_VIDEO_TYPE,
                "URL": "",
                "start_time": "0",
                "end_time": "0",
                "component": "",
            }]
        ) 
        data.update(component_demonstration_videos_form_data)
        component_tutorial_videos_form_data = generate_video_formset(
            prefix="componenttutorialvideo_set",
            videos=[{
                "video_type": YOUTUBE_VIDEO_TYPE,
                "URL": "",
                "start_time": "0",
                "end_time": "0",
                "component": "",
            }]
        ) 
        data.update(component_tutorial_videos_form_data)
        return self.client.post(reverse('component-new'), data, follow=True)

    def test_component_gettable(self):
        """Test that the GET request for an existing move works"""
        new_component = Component(name="NewlyAdded")
        new_component.save()
        component_url = reverse('component_detail', args=(new_component.slug,))
        resp = self.client.get(component_url)
        self.assertEqual(resp.status_code, 200)

    def test_valid_component_creation(self):
        """Test that sending the post data of a valid move gives 302 redirect"""
        self.client.login(username=self.user.username, password='adm1n')
        response = self.new_component_post_data("NewComponent")
        expected_url = reverse('component_detail', args=("NewComponent",))
        self.assertEqual(response.status_code, 200)
