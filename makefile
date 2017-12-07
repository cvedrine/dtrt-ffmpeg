SHELL=zsh

encoder_tools= \
	dtrt-ffmpeg-thumbnails \
	dtrt-ffmpeg-guess-config \
	dtrt-ffmpeg-overview \
	dtrt-ffmpeg.zsh \
	pod-ssh.zsh \
	process \
	ffmpod-rest \
	dtrt-ffmpeg-downscale \
	ffmpod

pod_tools=( bin/navigator-wrapper )

pod:
	install -d ${BINDIR}
	install ${pod_tools} ${BINDIR}

# don't forget to edit and copy podrc.sample
# to ~/.podrc
encoder:
	install -d ${BINDIR}
	install ${encoder_tools} ${BINDIR}

