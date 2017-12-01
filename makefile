encoder_tools=(
	bin/dtrt-ffmpeg-thumbnails
	bin/dtrt-ffmpeg-guess-config
	bin/dtrt-ffmpeg-overview
	bin/dtrt-ffmpeg.zsh
	bin/pod-ssh.zsh
	bin/process
	bin/ffmpod-rest
	bin/dtrt-ffmpeg-downscale
	bin/ffmpod )

pod_tools=( bin/navigator-wrapper )

pod:
	cp $(pod_tools) $(BINDIR)


# don't forget to edit and copy podrc.sample
# to ~/.podrc
encoder:
	cp $(encoder_tools) $(BINDIR)


