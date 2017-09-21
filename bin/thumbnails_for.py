from django.core.management.base import BaseCommand, CommandError
from pods.models import Pod
from filer.models.foldermodels import Folder
from filer.models.imagemodels  import Image
from django.core.files import File

class Navigator():

    def relcd(self,name):
	self.pwd, _ = Folder.objects.get_or_create\
	    ( name=name
	    , owner=self.pwd.owner
	    , parent=self.pwd )

    def go_home(self,owner):
	self.pwd = Folder.objects.get\
	    ( name=owner
	    , owner=owner
	    , level=0 )

    def go_video_slug(self,video):
	self.go_home(video.owner)
	self.relcd(video.slug)

    def store(self,model,source,dest):
	file, _ = model.objects.get_or_create\
	    ( folder = self.pwd
	    , name   = dest )
        file.file.save\
	    ( dest
	    , File(open(source))
	    , save = True )
	file.owner = self.pwd.owner
	return file

class Command(BaseCommand):
    args = '<video t t ...>'
    help = 'Encodes the specified content.'

    def handle(self, *args, **options):
	vid = args[0]
	ts    = args[1:]
	video = Pod.objects.get(id=vid)
	store = Navigator()
	store.go_video_slug(video)
	thumbnails =\
	    [ store.store( Image, t, "%d_%s.png" % (video.id, i) )
		for i,t in enumerate(ts) ]
	for t in thumbnails: t.save()
	video.thumbnail = thumbnails[1]
	video.save()

