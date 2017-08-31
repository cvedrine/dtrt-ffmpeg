# exemples:
# show data about the encoding type of the video
# p pod_encodingtypes | select_pod_encodingtypes .id==$( p info $id | jq .type.id )
#

# p pod_encodingtypes |
#     select_pod_encodingtypes .id==5


# example: get encoding type by id
# rest pod pod_encodingtypes | select_pod_encodingtypes '.id == 2'
#
#

# pod pod_encodingtypes > types.json
# pod info 19005 > y.json
# pod PATCH '{"type": 5}' info 19005 > x.json > a.html
