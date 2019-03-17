from Location import Location

gloucester = Location()
cumberland = Location()
russell = Location()
carlington = Location()
kanata = Location()
goulborun = Location()
manotick = Location()
westboro = Location()
ficko = Location()
greenbelt = Location()
dt = Location()
orleans = Location()
vanier = Location()
overbrook = Location()
altavista = Location()
kinburn = Location()
bayshore = Location()
glebe = Location()

neighborhoods = []


def generate_neighborhood_lookup_table():
    gloucester.neighborhood = "Gloucester"
    gloucester.longitude = -75.594271
    gloucester.latitude = 45.447405
    neighborhoods.append(gloucester)

    cumberland.neighborhood = "Cumberland"
    cumberland.longitude = -75.406015
    cumberland.latitude = 45.517417
    neighborhoods.append(cumberland)

    russell.neighborhood = "Russell"
    russell.longitude = -75.359435
    russell.latitude = 45.259366
    neighborhoods.append(russell)

    carlington.neighborhood = "Carlington"
    carlington.longitude = -75.733264
    carlington.latitude = 45.377204
    neighborhoods.append(carlington)

    kanata.neighborhood = "Kanata"
    kanata.longitude = -75.898708
    kanata.latitude = 45.308871
    neighborhoods.append(kanata)

    goulborun.neighborhood = "Goulborun"
    goulborun.longitude = -75.906236
    goulborun.latitude = 45.235056
    neighborhoods.append(goulborun)

    manotick.neighborhood = "Manotick"
    manotick.longitude = -75.719692
    manotick.latitude = 45.225094
    neighborhoods.append(manotick)

    westboro.neighborhood = "Westboro"
    westboro.longitude = -75.755440
    westboro.latitude = 45.394790
    neighborhoods.append(westboro)

    ficko.neighborhood = "Ficko"
    ficko.longitude = -75.628624
    ficko.latitude = 45.280560
    neighborhoods.append(ficko)

    greenbelt.neighborhood = "Greenbelt"
    greenbelt.longitude = -75.555951
    greenbelt.latitude = 45.349700
    neighborhoods.append(greenbelt)

    dt.neighborhood = "Downtown"
    dt.longitude = -75.700259
    dt.latitude = 45.419999
    neighborhoods.append(dt)

    orleans.neighborhood = "Orleans"
    orleans.longitude = -75.504788
    orleans.latitude = 45.45569
    neighborhoods.append(orleans)

    vanier.neighborhood = "Vanier"
    vanier.longitude = -75.659041
    vanier.latitude = 45.437095
    neighborhoods.append(vanier)

    overbrook.neighborhood = "Overbrook"
    overbrook.longitude = -75.653198
    overbrook.latitude = 45.424019
    neighborhoods.append(overbrook)

    altavista.neighborhood = "Alta Vista"
    altavista.longitude = -75.657221
    altavista.latitude = 45.386999
    neighborhoods.append(altavista)

    kinburn.neighborhood = "Kinburn"
    kinburn.longitude = -76.188478
    carlington.latitude = 45.391817
    neighborhoods.append(kinburn)

    bayshore.neighborhood = "Bayshore"
    bayshore.longitude = -75.807744
    bayshore.latitude = 45.348293
    neighborhoods.append(bayshore)

    glebe.neighborhood = "Glebe"
    glebe.longitude = -75.688772
    glebe.latitude = 45.403690
    neighborhoods.append(glebe)

    return neighborhoods
