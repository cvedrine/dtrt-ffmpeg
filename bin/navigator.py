from django.core.management.base import BaseCommand, CommandError
from pods.models import Pod
from filer.models.foldermodels import Folder
from filer.models.imagemodels  import Image
from django.core.files import File

class Navigator():

    def cdrel(self,name):
	self.pwd, _ = Folder.objects.get_or_create\
	    ( name=name
	    , owner=self.pwd.owner
	    , parent=self.pwd )
        return self.pwd

    def cdpk(self,pk): self.pwd, _ = Folder.objects.get(id=int(pk))

    def go_home(self,owner):
	self.pwd = Folder.objects.get\
	    ( name=owner
	    , owner=owner
	    , level=0 )

    def go_video_slug(self,video):
	self.go_home(video.owner)
        return self.cdrel(video.slug)

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

def V(v):
    if isinstance(v,Pod): return v
    if isinstance(v,str): return Pod.objects.get(id=v)
    return None

class Command(BaseCommand):
    args = '<video t t ...>'
    help = 'Encodes the specified content.'

    def get_slug(self,video):
        video = V(video)
        n = Navigator()
        n.go_video_slug(V(video))
        p = n.pwd
        for i in [ p.name, p.pk ]: print(i)

    def set_thumbnails(self,video,*ts):
	video = V(video)
	store = Navigator()
	store.go_video_slug(video)
	thumbnails =\
	    [ store.store( Image, t, "%d_%s.png" % (video.id, i) )
		for i,t in enumerate(ts) ]
	for t in thumbnails: t.save()
	video.thumbnail = thumbnails[1]
	video.save()




    def handle(self, *args, **options): getattr(self,args[0])(*args[1:])




