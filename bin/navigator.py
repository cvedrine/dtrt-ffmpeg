from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pods.models import Pod, EncodingPods
from filer.models.foldermodels import Folder
from filer.models.imagemodels  import Image
from django.core.files import File
from core.models import get_media_guard, EncodingType
import os

DEVNULL=None

import os

def root_for(base): return os.path.join( settings.MEDIA_ROOT, base )

class Navigator():

    def cdrel(self,name):
        """
            change the working directory relatively to the current one
        """
        self.wd, _ = Folder.objects.get_or_create\
            ( name=name
            , owner=self.wd.owner
            , parent=self.wd )
        return self.wd

    def cdpk(self,pk):
        """
            go to the directory ided by the pk
        """
        self.wd = Folder.objects.get(id=int(pk))

    def go_home(self,owner):
        """
            go to the home directory of a user (as django user)
        """
        self.wd = Folder.objects.get\
            ( name=owner
            , owner=owner
            , level=0 )

    def go_video_slug(self,video):
        """
            go to the slug of a video
        """

        V(video)
        self.go_home(video.owner)
        return self.cdrel(video.slug)

    def store(self,model,source,dest):

        file, DEVNULL = model.objects.get_or_create\
            ( folder = self.wd
            , name   = dest )

        file.file.save\
            ( dest
            , File(open(source))
            , save = True )
        file.owner = self.wd.owner
        return file

    def pwd(self):
        p = self.wd
        for i in [ p.name, p.pk, p.pretty_logical_path ]: print(i)

def V(v):
    if isinstance(v,Pod): return v
    if isinstance(v,str): return V(Pod.objects.get(id=v))
    raise Exception\
        ( "can't get a pod object from the %s %s"
        % (str(type(v)), v ))

def path_for_items_of_video(video):
    video = V(video)
    login = video.owner.username
    id    = video.id
    return os.path.join\
        ( getattr(settings,'VIDEOS_DIR','videos')
        , login
        , get_media_guard( login, id )
        , "%s" % id )

def ressources_root_for(video):
    video = V(video)
    login = video.owner.username
    id    = video.id
    return os.path.join\
        ( settings.MEDIA_ROOT
        , getattr(settings,'VIDEOS_DIR','video')
        , login
        , get_media_guard( login, id )
        , "%s" % id )

def get_video_scales():
    return [ e.output_height
        for e in EncodingType.objects.filter(mediatype='video') ]

class Command(BaseCommand):
    args = '<video t t ...>'
    help = 'Encodes the specified content.'

    def set_thumbnails_for(self,video,*ts):
        video = V(video)
        store = Navigator()
        store.go_video_slug(video)
        thumbnails =\
            [ store.store( Image, t, "%d_%s.png" % (video.id, i) )
                for i,t in enumerate(ts) ]
        for t in thumbnails: t.save()
        video.thumbnail = thumbnails[1]
        video.save()

    def ressources_root_for(self,video): print(root_for(path_for_items_of_video(V(video))))

    def get_video_scales(self):
        for e in get_video_scales(): print(e)

    def get_video_path(self,video): print(V(video).video.path)

    def add_overview_for(self,video,filename):
        place = os.path.join\
            ( path_for_items_of_video(video)
            , os.path.basename(filename) )
        video = V(video)
        video.overview = place
        video.save()
        print(root_for(place))

    def add_encoding_for(self,video,height,filename):

        video = V(video)

        place = os.path.join\
            ( path_for_items_of_video(video)
            , os.path.basename(filename) )

        etype = EncodingType.objects.filter\
            ( mediatype='video'
            , output_height=height )[0]

        epod, DEVNULL = EncodingPods.objects.get_or_create\
            ( video=video
            , encodingType=etype
            , encodingFormat="video/mp4")

        epod.encodingFile = place
        epod.save()
        video.save()

        print(root_for(place))

    def handle(self, *args, **options): getattr(self,args[0])(*args[1:])
