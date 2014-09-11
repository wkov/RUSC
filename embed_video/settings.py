from django.conf import settings


EMBED_VIDEO_BACKENDS = getattr(settings, 'EMBED_VIDEO_BACKENDS', (
    'embed_video.backends.YoutubeBackend',
    'embed_video.backends.VimeoBackend',
    'embed_video.backends.SoundCloudBackend',
))

EMBED_VIDEO_TIMEOUT = getattr(settings, 'EMBED_VIDEO_TIMEOUT', 10)

EMBED_VIDEO_YOUTUBE_DEFAULT_QUERY = \
    getattr(settings, 'EMBED_VIDEO_YOUTUBE_DEFAULT_QUERY', 'wmode=opaque')
