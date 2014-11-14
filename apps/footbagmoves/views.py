""" Views for the footbag moves and components """
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

import itertools

from apps.footbagmoves.models import Component, Move, MoveComponentSequence
from apps.footbagmoves.models import ComponentTutorialVideo, ComponentDemonstrationVideo
from apps.footbagmoves.models import MoveTutorialVideo, MoveDemonstrationVideo
from apps.footbagmoves.models import MoveNickname, ComponentNickname
from apps.footbagmoves.models import MoveTips, ComponentTips

from apps.footbagmoves.constants import YOUTUBE_VIDEO_TYPE, URL_VIDEO_TYPE

from apps.footbagmoves.video_api_helpers import extract_first_yt_url, extract_yt_id

from apps.footbagmoves.forms import ComponentEditForm, SearchForm


def get_last_3(queryset):
    """Get the last 3 objects that were added as determined by their id.
    :param queryset: the query set we are filtering on"""
    return queryset.order_by('id')[0:3]

def move_index(request):
    """ View for the moves index page """
    template = loader.get_template('footbagmoves/move_index.html')
    latest_moves = get_last_3(Move.objects.all())
    num_moves = Move.objects.count()
    context = RequestContext(request,{
        'number_of_moves': num_moves,
        'recent_moves': latest_moves,
    })
    return HttpResponse(template.render(context))

def move_detail(request, move_slug):
    """ View for the move details page"""
    try:
        #extract move information object
        current_move = Move.objects.get(slug=move_slug)
    except Move.DoesNotExist:
        template = loader.get_template('footbagmoves/move_not_found.html')
        context = RequestContext(request, {'move_slug' : move_slug})
        return HttpResponseNotFound(template.render(context))
    template = loader.get_template('footbagmoves/move_detail.html')
    #load move info from DB
    components_seq = MoveComponentSequence.objects.filter(move__exact=current_move)
    demo_video = MoveDemonstrationVideo.objects.filter(move__exact=current_move)
    tutorial_video = MoveTutorialVideo.objects.filter(move__exact=current_move)
    nicknames = MoveNickname.objects.filter(move__exact=current_move)
    move_tips = MoveTips.objects.filter(move__exact=current_move)
    #only load the youtube API if a youtube video is associated with the move
    load_youtube_api = (any(vid.video_type == YOUTUBE_VIDEO_TYPE for vid in demo_video) or
                        any(vid.video_type == YOUTUBE_VIDEO_TYPE for vid in tutorial_video))

    first_yt_video = next((vid for vid in itertools.chain(demo_video,tutorial_video) if
                           vid.video_type == YOUTUBE_VIDEO_TYPE), None)
    if load_youtube_api:
        first_yt_id = first_yt_video.video_id
    else:
        first_yt_id = ""

    #Used in the template to create class names for link elements so that we can extract the youtube videos from the DOM using javascript.
    video_types = {
        "URL": URL_VIDEO_TYPE,
        "Youtube": YOUTUBE_VIDEO_TYPE,
    }

    context = RequestContext(request, {
        'move' : current_move,
        'sequence': components_seq,
        'nicknames': nicknames,
        'video_demo': demo_video,
        'video_tutorial': tutorial_video,
        'load_youtube': load_youtube_api,
        'vid_types': video_types,
        'first_yt_id': first_yt_id,
        'first_yt_video': first_yt_video,
        'move_tips': move_tips[0],
    })
    return HttpResponse(template.render(context))

def component_index(request):
    """ View for the components index page """
    template = loader.get_template('footbagmoves/component_index.html')
    latest_components = get_last_3(Component.objects.all())
    num_components = Component.objects.count()
    context = RequestContext(request, {
        'number_of_components': num_components,
        'recent_components': latest_components,
    })
    return HttpResponse(template.render(context))

def component_detail(request, component_slug):
    """ View for the details of an individual component.
    If the component is found in the database the component_detail template is loaded
    and if not the component_not_found template is loaded."""
    try:
        current_component = Component.objects.get(slug=component_slug)
    except Component.DoesNotExist:
        template = loader.get_template('footbagmoves/component_not_found.html')
        context = RequestContext(request, {'component_slug' : component_slug})
        return HttpResponseNotFound(template.render(context))
    template = loader.get_template('footbagmoves/component_detail.html')
    #load component info from DB
    demo_video = ComponentDemonstrationVideo.objects.filter(component__exact=current_component)
    tutorial_video = ComponentTutorialVideo.objects.filter(component__exact=current_component)
    nicknames = ComponentNickname.objects.filter(component__exact=current_component)
    component_tips = ComponentTips.objects.filter(component__exact=current_component)

    #only load the youtube API if a youtube video is associated with the move
    load_youtube_api = (any(vid.video_type == YOUTUBE_VIDEO_TYPE for vid in demo_video) or
                        any(vid.video_type == YOUTUBE_VIDEO_TYPE for vid in tutorial_video))

    first_yt_video = next((vid for vid in itertools.chain(demo_video, tutorial_video) if
                           vid.video_type == YOUTUBE_VIDEO_TYPE), None)
    if load_youtube_api:
        first_yt_id = first_yt_video.video_id
    else:
        first_yt_id = ""

    #Used in the template to create class names for link elements so that we can extract the youtube videos from the DOM using javascript.
    video_types = {
        "URL": URL_VIDEO_TYPE,
        "Youtube": YOUTUBE_VIDEO_TYPE,
    }

    context = RequestContext(request, {
        'component' : current_component,
        'nicknames': nicknames,
        'video_demo': demo_video,
        'video_tutorial': tutorial_video,
        'load_youtube': load_youtube_api,
        'vid_types': video_types,
        'first_yt_id': first_yt_id,
        'first_yt_video': first_yt_video,
        'component_tips': component_tips[0],
    })
    return HttpResponse(template.render(context))

def search_page(request):
    """A search page for the footbag database"""
    template = loader.get_template('footbagmoves/search.html')
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_text = search_form.cleaned_data['search_text']
            nickname_objs = MoveNickname.objects.filter(nickname__exact=search_text)
            move_objs = [ nickname.move for nickname in nickname_objs]
            results_found = len(move_objs)
            if results_found > 0:
                results_info_text = "Found " + str(results_found) + " results for " + search_form.cleaned_data['search_text']
                show_results = True
            else:
                show_results = False
                results_info_text = "No results found for " + search_form.cleaned_data['search_text']
            #Note that this will hit the DB a lot(once per nickname found), some sort
            #of join method would be preferable as that potentially will scale better
            context = RequestContext(request, {
                'search_form': search_form,
                'show_results': show_results,
                'results_info': results_info_text,
                'results_list': move_objs,
            })
            return HttpResponse(template.render(context))
    else:
        search_form = SearchForm()
        show_results = False
    context = RequestContext(request, {
        'search_form': search_form,
    })
    return HttpResponse(template.render(context))

@login_required
def component_edit(request, component_id=None):
    """Edit a component or add a new one"""
    if component_id is None:
        edit_form = ComponentEditForm()
    else:
        current_component = Component.objects.get(pk=component_id)
        data = {
            'name': current_component.name,
        }
        edit_form = ComponentEditForm()
    context = RequestContext(request, {
        'edit_form': edit_form,
    })
    template = loader.get_template('footbagmoves/component_edit.html')
    return HttpResponse(template.render(context))

