import folium
from folium.plugins import MarkerCluster

def initMap(bboxCenter):
    map = folium.Map(location = bboxCenter, zoom_start = 13)

