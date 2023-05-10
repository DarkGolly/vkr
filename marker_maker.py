import folium

from Ship import Ship
from db import DataBase


class MarkersMaker:
    db = DataBase()
    cur_list = None
    ship = None

    def plotMarkers(self):
        self._plotQuery()
        map = folium.Map(
            location=[59.912605, 30.245085],
            tiles='Stamen Terrain',
            zoom_start=13
        )
        if self.cur_list:
            for i in self.cur_list:
                self.ship = Ship(i)
                folium.Marker(
                    location=[self.ship.lat, self.ship.lon],
                    popup=str(self.ship.mmsi),
                    tooltip="Подробнее"
                ).add_to(map)

        return map._repr_html_()

    def _plotQuery(self):
        self.cur_list = self.db.execute_query_all()
