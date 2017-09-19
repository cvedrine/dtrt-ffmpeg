. rest-base.zsh

TOKEN=${POD_REST_TOKEN?please set POD_REST_TOKEN variable} \
URL=${POD_REST_URL?please set POD_REST_URL variable}       \
    set_rest_service pod

encoding_in_progress () {
    rest_client+=( -XPATCH -d '{ "encoding_in_progress" : '$1'  }' )
    shift
    "$@"
}

pod_encodingtypes        () { route $URL/coreencodingtype "$@" }
pod_encodings            () { route $URL/podsencodingpods "$@" }

info                     () { route $URL/podspod/${1?id of the video}.json ; shift ; "$@" }
infos                    () { print -u2 "DON'T DO THAT ($0) if you don't want to kill pod"  }
pod_thumbnail            () { route $URL/easythumbnailsthumbnail/$1.json ; shift; "$@" }
pod_thumbnails           () { route $URL/easythumbnailsthumbnail ; "$@" }
pod_thumbnail_source     () { route $URL/easythumbnailssource/$1.json ; shift; "$@" }
pod_thumbnail_sources    () { route $URL/easythumbnailssource    ; "$@" }
filer_image              () { route $URL/filerimage      ; "$@" }
filer_image_upload       () { route $URL/filerimage.json ; "$@" }
filer_file_upload        () { route $URL/filerfile.json  ; "$@" }
filer_file               () { route $URL/filerfile/$1.json ; shift; "$@" }
pod_folder               () { route $URL/filerfolder.json\?name=${1?slug of the filer folder} ; shift; "$@" }
filer_folder             () { route $URL/filerfolder.json ; "$@" }
django_content_type      () { route $URL/djangocontenttype.json\?app_label=${1?application label}\&model=${2?the model} ; shift 2; "$@" }
filer_folder_for_user    () { route $URL/filerfolder.json\?name=${1?owner name of the folder}\&owner=${2?owner id of the folder}\&level=0; shift 2; "$@" }


select_pod_encodingtypes () { jq " .results[] | select( ${1?selector} ) " }

as_height_id () {
        jq --raw-output ' .[]
        # | select( .output_height == 1080 )
        | @text "\(.output_height) \(.id)" '
}

overview_send () {
    scp $from $to
    pod PATCH "{ \"overview\": \"$to\" }" info $id }
