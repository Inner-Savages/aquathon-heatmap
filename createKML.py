import simplekml as KML

kml = KML.Kml()
pol = kml.newpolygon(name='test')
pol.outerboundaryis = [(18.333868, -34.038274), (18.370618, -34.034421),
                       (18.350616, -34.051677), (18.333868, -34.038274)]
pol.style.polystyle.outline = 0
pol.style.polystyle.color = '990000ff'
kml.save('test.kml')