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
        self.wd, _ = Folder.objects.get_or_create\
            ( name=name
            , owner=self.wd.owner
            , parent=self.wd )
        return self.wd

    def cdpk(self,pk): self.wd = Folder.objects.get(id=int(pk))

    def go_home(self,owner):
        self.wd = Folder.objects.get\
            ( name=owner
            , owner=owner
            , level=0 )

    def go_video_slug(self,video):
        self.go_home(video.owner)
        return self.cdrel(video.slug)

    def store(self,model,source,dest):
        file, DEVNULL = model.objects.get_or_create\
            ( folder = self.wd
            , name   = dest
            , owner  = self.wd.owner )

        # sys_dest = os.path.join\
        #         ( settings.MEDIA_ROOT
        #         , getattr(settings,'VIDEOS_DIR','videos')
        #         , self.wd.pretty_logical_path, dest )

        # sys_dest =\
        #     settings.MEDIA_ROOT\
        #     + '/' + getattr(settings,'VIDEOS_DIR','videos')\
        #     + '/' + self.wd.pretty_logical_path\
        #     + '/' + dest

        # # os.rename( source, sys_dest)
        # print(" mv from %s -----------------> %s " % ( source, sys_dest))
        return file

    def pwd(self):
        p = self.wd
        for i in [ p.name, p.pk, p.pretty_logical_path ]: print(i)

def V(v):
    if isinstance(v,Pod): return v
    if isinstance(v,str): return Pod.objects.get(id=v)
    return None

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

        epod, DEVNULL  = EncodingPods.objects.get_or_create\
            ( video=video
            , encodingType=etype
            , encodingFile = place
            , encodingFormat="video/mp4")

        epod.save()
        video.save()

        print(root_for(place))

        # in perl:
        # say for grep /^[fp]/, keys %$epod
        #
        # now ... in python

        # import re
        # p = re.compile('^[fp]')

        # because the python syntax is weirdly inconsistent:

        # FUCK you python ... round 1
        # for d in dir(epod) if p.match(d): print(d)

        # FUCK you python ... round 2
        # for d in dir(epod): if p.match(d): print(d)


    def handle(self, *args, **options): getattr(self,args[0])(*args[1:])
