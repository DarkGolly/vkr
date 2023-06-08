import folium

from Meta import Meta
from Ship import Ship
from db import DataBase


class MarkersMaker:
    db = DataBase()
    cur_list = None
    ship = None
    meta = None

    def plotMarker(self, maram):
        self.cur_list = self.db.execute_query_one(maram)
        map = folium.Map(
            location=[59.912605, 30.245085],
            tiles='Stamen Terrain',
            zoom_start=12,
            width='100%',
            height='80%'
        )
        if len(self.cur_list)<1:
            return 0
        self.ship = Ship(self.cur_list[0])

        folium.Marker(
            location=[self.ship.lat, self.ship.lon],
            popup='Идентификатор: ' + str(self.ship.mmsi) + '\nКурс: ' + str(self.ship.course) +
                  f"\n <a href='http://127.0.0.1:5000/ship/{self.ship.mmsi}'>me.ru</a>",
            tooltip="Подробнее",
            # icon=folium.Icon(icon='arrow-up', color='blue', angle=int(self.ship.course)
            icon=folium.DivIcon(html=f"""<div style="color:#f00;content:url(static/marker.png);width:30px;
                            transform: rotate({str(self.ship.course)}deg);text-align:center;"></div>""")
            # icon=folium.Icon(icon='arrow-up', color='blue', angle=int(self.ship.course))
        ).add_to(map)

        map.save('templates/map.html')
        print("New map is save.")

    def plotMarkers(self, params, is_full):
        self._plotQuery(params, is_full)
        map = folium.Map(
            location=[59.912605, 30.245085],
            tiles='Stamen Terrain',
            zoom_start=12,
            width='100%',
            height='80%'
        )
        if self.cur_list and is_full == 'on':
            for i in self.cur_list:
                self.meta = Meta(i)
                map = self._Full(map)
        elif self.cur_list:
            for i in self.cur_list:
                self.ship = Ship(i)
                map = self._Base(map)

        map.save('templates/map.html')
        print("New map is save.")
        # return map._repr_html_()

    def _Base(self, map):
        folium.Marker(
            location=[self.ship.lat, self.ship.lon],
            popup='Идентификатор: ' + str(self.ship.mmsi) + '\nКурс: ' + str(self.ship.course) +
                  f'\n <a href="http://127.0.0.1:5000/ship/{self.ship.mmsi}">about</a>',
            tooltip="Подробнее",
            # icon=folium.Icon(icon='arrow-up', color='blue', angle=int(self.ship.course)
            icon=folium.DivIcon(html=f"""<div style="color:#f00;content:url(static/marker.png);width:30px;
                                    transform: rotate({str(self.ship.course)}deg);text-align:center;"></div>""")
            # icon=folium.Icon(icon='arrow-up', color='blue', angle=int(self.ship.course))
        ).add_to(map)
        return map

    def _Full(self, map):
        folium.Marker(
            location=[self.meta.lat, self.meta.lon],
            popup='Идентификатор: ' + str(self.meta.mmsi) + '\nКурс: ' + str(self.meta.course) +'\nНазвание: ' +
                  str(self.meta.shipname)+ '\nПозывной: ' + str(self.meta.callsign) +f'\n <a href="http://127.0.0.1:5000/ship/{self.meta.mmsi}">about</a>',
            tooltip="Подробнее",
            # icon=folium.Icon(icon='arrow-up', color='blue', angle=int(self.ship.course)
            icon=folium.DivIcon(html=f"""<div style="color:#f00;content:url(static/marker.png);width:30px;
                            transform: rotate({str(self.meta.course)}deg);text-align:center;"></div>""")
            # icon=folium.Icon(icon='arrow-up', color='blue', angle=int(self.ship.course))
        ).add_to(map)
        return map

    def _plotQuery(self, params, is_full):
        if is_full == 'on':
            self.cur_list = self.db.execute_query_twise(params)
        elif is_full == 'off' and params is not None:
            self.cur_list = self.db.execute_query_on(params)
        else:
            self.cur_list = self.db.execute_query_all()
