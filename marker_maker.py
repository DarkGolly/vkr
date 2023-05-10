import folium

from Ship import Ship
from db import DataBase


class MarkersMaker:
    db = DataBase()
    cur_list = None
    ship = None

    def plotMarkers(self):
        self._plotQuery()
        if not self.cur_list:
            map = folium.Map(
                location=[59.912605, 30.245085],
                tiles='Stamen Terrain',
                zoom_start=13
            )
        else:
            map = folium.Map(
                location=[self.cur_list.pop()[8], self.cur_list.pop()[7]],
                tiles='Stamen Terrain',
                zoom_start=13
            )
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
