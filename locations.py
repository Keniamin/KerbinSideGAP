from classes import Location, LocationAltitude as Alt


LOCATIONS = [
    Location(
        "Arakebo", "Arakebo, a small island with radio telescope observatory and post-flight rehabilitation clinic for kerbonauts.",
        helipad=(8.391118, 179.643722, Alt(60, 1711.71)),
        staff_spawn=(8.391172, 179.64704, Alt(37, 1733.78)),
        vip_spawn=(8.360934, 179.770392, Alt(6, 1529.22)),
        kk_base_name="Arakebo Observatory",
    ),
    Location(
        "Ben Bay", "KashCorp headquarter in the Ben Bay, not far from the KSC.",
        helipad=(13.2242, -64.1848, Alt(1, 40.84)),
        staff_spawn=(13.226728, -64.184141, Alt(2, 41.1)),
        launch_refund=25,
    ),
    Location(
        "Black Krags", "Small air base beside the Black Krags mountain range, primarily used for basic flight training.",
        aircraft_launch=(11.32069, -87.6877, Alt(4, 321.2)),
        staff_spawn=(11.319044, -87.681677, Alt(1, 322.91)),
        launch_refund=10,
        recovery_factor=75,
        runways=[
            ((11.32039, 272.312225, 326, 0), (11.258509, 272.304277, 326, 0)),
        ],
    ),
    Location(
        "Coaler Crater", "Small airfield located in beautiful region of lakes and shores called Coaler Crater.",
        aircraft_launch=(35.4291, -98.9055, Alt(1, 67.83)),
        staff_spawn=(35.428764, -98.915376, Alt(1, 69.07)),
        launch_refund=5,
        recovery_factor=60,
        runways=[
            ((35.429, 261.095, 70, 5), (35.3875, 261.0318, 70, 7.5)),
        ],
    ),
    Location(
        "Deadkerbal Pit", "Deadkerbal Pit, a small base located in the mountains on the edge of desert, the site of designing and testing of new rockets.",
        helipad=(14.80408, -127.5957, Alt(1, 1741.04)),
        staff_spawn=(14.799917, -127.593289, Alt(1, 1741.1)),
        launch_refund=10,
        recovery_factor=80,
    ),
    Location(
        "Donby Hole", "Centre of geological study inside the strange natural formation known as the Donby Hole.",
        helipad=(13.72265, 70.40235, Alt(4, 2744.83)),
        staff_spawn=(13.724773, 70.401604, Alt(8, 2742.88)),
        launch_refund=10,
        recovery_factor=60,
    ),
    Location(
        "Dull Spot", "Dull Spot, launch site deep in the Northern hemisphere.",
        aircraft_launch=(63.88354, -172.4476, Alt(6, 420.59)),
        aircraft_parking=(63.876731, -172.458955, Alt(0, 418.42)),
        staff_spawn=(63.877764, -172.452818, Alt(1, 418.88)),
        launch_refund=10,
        recovery_factor=75,
        runways=[
            ((63.8877, 187.55933, 427, 5), (63.9802, 187.713, 428, 0)),
        ],
    ),
    Location(
        "Dundard's Edge", "Dundard's Edge, a big base which is used as a control centre and a training facility for kerbonauts. At the base they can master climbing, rafting and advanced flight operations along the canyons.",
        helipad=(44.259663, -132.040896, Alt(4, 528.06)),
        aircraft_launch=(44.274531, -132.002871, Alt(6, 522.58)),
        aircraft_parking=(44.265227, -132.008366, Alt(7, 522.49)),
        staff_spawn=(44.270053, -132.006111, Alt(8, 522.0)),
        vip_spawn=(44.250294, -132.069326, Alt(4, 530.63)),
        recovery_factor=60,
        kk_base_name="Dundard's Edge Runway",
        runways=[
            ((44.274, 227.99725, 528, 0), (44.11, 227.9865, 531, 0)),
        ],
    ),
    Location(
        "Everkrest", "Small building on the slope of the Everkrest, one of the highest mountains on the Kerbin.",
        helipad=(-14.12746, 71.6633, Alt(11, 5229.25)),
        launch_refund=10,
        recovery_factor=70,
    ),
    Location(
        "Goldpool", "Harbour and launch site in the tropics called Goldpool.",
        aircraft_launch=(-1.109713, 17.36675, Alt(13, 0.0)),
        aircraft_parking=(-1.118301, 17.366416, Alt(0, 5.75)),
        launch_refund=10,
        recovery_factor=75,
        runways=[
            ((-1.10461, 17.36696, 13, 7.5), (-0.99065, 17.37167, 14, 0)),
        ],
    ),
    Location(
        "Green Coast", "Big civil airport and cargo terminal at the Green Coast, most popular recreation region of the Kerbin with lakes, mountains and shores.",
        helipad=(-3.46855, 179.164239, Alt(18, 207.2)),
        aircraft_launch=(-3.492128, 179.092387, Alt(10, 212.48)),
        aircraft_parking=(-3.460863, 179.157881, Alt(20, 204.24)),
        staff_spawn=(-3.461791, 179.152745, Alt(17, 206.53)),
        launch_refund=20,
        recovery_factor=70,
        runways=[
            ((-3.493906, 179.0893, 223, 5), (-3.4185, 179.2175, 224, 5)),
        ],
    ),
    Location(
        "Green Peaks", "Research centre in the hills known as Green Peaks dedicated to botanical and medical studies.",
        helipad=(-0.737478, 74.954638, Alt(4, 1240.85)),
        staff_spawn=(-0.739691, 74.955241, Alt(7, 1239.6)),
    ),
    Location(
        "Guardian's Basin", "Tourist base with a helipad in a beautiful natural region known as Guardian's Basin.",
        helipad=(42.648578, -50.90711, Alt(2, 726.27)),
        vip_spawn=(42.643985, -50.898159, Alt(1, 722.4)),
        launch_refund=10,
        recovery_factor=70,
    ),
    Location(
        "Hanbert Cape", "Base at the South edge of the continent called Hanbert Cape in the honour of a great explorer Hanbert Kerman.",
        helipad=(-22.639811, -140.243583, Alt(16, 14.2)),
        aircraft_launch=(-22.61177, -140.2546, Alt(4, 0.0)),
        aircraft_parking=(-22.617221, -140.255614, Alt(0, 2.14)),
        staff_spawn=(-22.615803, -140.253584, Alt(2, 0.51)),
        launch_refund=10,
        recovery_factor=75,
        runways=[
            ((-22.6067, 219.74633, 6, None), (-22.493, 219.76747, 6, 0)),
        ],
    ),
    Location(
        "Jeb's Island Resort", "Beautifull island in the neighborhood of KSC where Jebediah Kerman founded a small resort area.",
        helipad=(6.840006, -62.314309, Alt(4, 53.78)),
        vip_spawn=(6.886829, -62.27082, Alt(4, 0.8)),
        launch_refund=25,
        recovery_factor=90,
    ),
    Location(
        "Kerbal Space Centre", "KSC, the largest launch base and main rocket science research centre of the Kerbin.",
        helipad=(-0.096749, -74.6199, Alt(111, 64.78)),
        aircraft_launch=(-0.048742, -74.717311, Alt(5, 64.78)),
        aircraft_parking=(-0.056808, -74.620188, Alt(4, 64.78)),
        staff_spawn=(-0.060086, -74.64866, Alt(7, 64.78)),
        vip_spawn=(-0.161098, -74.7062, Alt(3, 64.78)),
        recovery_factor=95,
        kk_base_name=False, # no base existence check needed
        runways=[
            ((-0.048777, 285.299735, 70, 0), (-0.050059, 285.482482, 70, 0)),
        ],
        aircraft_launch_allowed_distance=100,
    ),
    Location(
        "Kerbin's Bottom", "Small research centre with a radio telescope on the cold island called Kerbin's Bottom.",
        aircraft_launch=(-50.49029, 170.5781, Alt(4, 102.8)),
        staff_spawn=(-50.493479, 170.5815, Alt(1, 104.92)),
        launch_refund=5,
        recovery_factor=50,
        runways=[
            ((-50.49, 170.5786, 107, 6), (-50.4747, 170.675, 107, 0)),
        ],
    ),
    Location(
        "Kerbin's Heart Science Centre", "Large geological research center at the origins of the river in the mountains which some call Kerbin's Heart.",
        helipad=(-6.726014, 28.59504, Alt(15, 219.11)),
        staff_spawn=(-6.724881, 28.593858, Alt(18, 220.0)),
        launch_refund=20,
    ),
    Location(
        "Kerman Lake", "Big privately owned airport on the Kerman Lake in arguably the most densely populated area of the Kerbin.",
        aircraft_launch=(11.27818, -63.5258, Alt(7, 31.7)),
        aircraft_parking=(11.264833, -63.510984, Alt(14, 25.78)),
        staff_spawn=(11.273144, -63.524966, Alt(10, 29.74)),
        vip_spawn=(11.106889, -63.426807, Alt(3, 0.0)),
        launch_refund=25,
        runways=[
            ((11.2799, 296.4731, 39, 8), (11.136, 296.5719, 42, 7.5)),
        ],
    ),
    Location(
        "KKVLA", "Karl Kerbansky's Very Large Array, the largest radio-telescope on the Kerbin and big research centre in the middle of Kerbin's Greater Desert.",
        helipad=(10.60579, -132.2675, Alt(17, 343.87)),
        aircraft_launch=(10.64686, -132.0973, Alt(49, 283.29)),
        aircraft_parking=(10.614288, -132.104367, Alt(34, 294.28)),
        staff_spawn=(10.605065, -132.268975, Alt(18, 344.29)),
        launch_refund=10,
        recovery_factor=50,
        kk_base_name="Area 110011",
        runways=[
            ((10.634098, 227.893294, 333, 0), (10.317334, 227.661287, 349, 0)),
        ],
    ),
    Location(
        "Lake Dermal", "Cargo base and civil regional airport near the Lake Dermal.",
        aircraft_launch=(22.70452, -120.9398, Alt(12, 550.36)),
        aircraft_parking=(22.720178, -120.952478, Alt(10, 552.72)),
        staff_spawn=(22.715601, -120.945915, Alt(9, 553.15)),
        recovery_factor=75,
        runways=[
            ((22.70469, 239.0598, 562, 0), (22.8284, 238.9345, 565, 0)),
        ],
    ),
    Location(
        "Lodnie Isles", "Civil airport serving the archipelago of the Lodnie Isles.",
        helipad=(29.714922, 14.253427, Alt(18, 422.96)),
        aircraft_launch=(29.73803, 14.19844, Alt(8, 432.21)),
        aircraft_parking=(29.67851, 14.274045, Alt(27, 413.76)),
        launch_refund=5,
        recovery_factor=60,
        runways=[
            ((29.7373, 14.1991, 441, 0), (29.5955, 14.3026, 441, 0)),
        ],
    ),
    Location(
        "Lushlands", "National airport of the Lushlands, agricultural country at the largest continent of the Kerbin.",
        aircraft_launch=(2.156698, 26.61129, Alt(11, 763.12)),
        aircraft_parking=(2.168899, 26.608008, Alt(16, 758.68)),
        staff_spawn=(2.159583, 26.607936, Alt(13, 761.11)),
        recovery_factor=50,
        runways=[
            ((2.157, 26.61125, 774, 0), (2.323, 26.64606, 777, 0)),
        ],
    ),
    Location(
        "Mount Snowey", "Launch complex atop the Mount Snowey, one of the highest peaks of Blizzard Mountain Range.",
        helipad=(20.41318, -78.1654, Alt(3, 3484.37)),
        staff_spawn=(20.414039, -78.168755, Alt(2, 3486.52)),
        recovery_factor=75,
    ),
    Location(
        "Old KSC", "The former main launch base and nowadays a big centre of space industry known as the Old KSC.",
        aircraft_launch=(20.650399, -146.439907, Alt(2, 427.84)),
        aircraft_parking=(20.606134, -146.484644, Alt(6, 423.53)),
        staff_spawn=(20.645796, -146.451644, Alt(9, 421.23)),
        launch_refund=20,
        recovery_factor=80,
        kk_base_name="KSC 2 Spaceplane Base",
        runways=[
            ((20.648, 213.5595, 429, 10), (20.5115, 213.5175, 430, 0)),
            ((20.68, 213.413, 432, None), (20.507, 213.4317, 432, 7.5)),
        ],
    ),
    Location(
        "Polar Research Centre", "Research centre located not far from Kerbin's North Pole.",
        aircraft_launch=(79.57256, -77.4097, Alt(4, 30.0)),
        aircraft_parking=(79.571123, -77.384329, Alt(4, 30.0)),
        staff_spawn=(79.570798, -77.374996, Alt(6, 30.0)),
        vip_spawn=(79.25517, -78.4412, Alt(6, 30.0)),
        recovery_factor=80,
        runways=[
            ((79.57256, 282.5903, 34, 0), (79.45485, 282.4466, 34, 0)),
        ],
    ),
    Location(
        "Round Range", "Big airport serving the mountain areas at the East of the largest continent of the Kerbin, located in the mountain valley known as Round Range.",
        helipad=(-6.018824, 99.5179, Alt(3, 1243.15)),
        aircraft_launch=(-6.012046, 99.388914, Alt(19, 1229.56)),
        aircraft_parking=(-5.998266, 99.431881, Alt(15, 1235.42)),
        launch_refund=10,
        recovery_factor=80,
        kk_base_name="Round Range Runway",
        runways=[
            ((-6.0122, 99.39, 1250, None), (-6.0313, 99.53915, 1249, 6)),
        ],
    ),
    Location(
        "Sanctuary Mouth", "Base on the mouth of the Sanctuary River, which was originally used as a launch site and cargo terminal, but was further supplemented with the passenger terminal to serve as a civil airport for nearby cities.",
        aircraft_launch=(23.68121, -39.9442, Alt(13, 0.0)),
        aircraft_parking=(23.674524, -39.917175, Alt(1, 19.09)),
        launch_refund=10,
        recovery_factor=75,
        runways=[
            ((23.68088, 320.0516, 14, 0), (23.67076, 319.9245, 15, 0)),
        ],
    ),
    Location(
        "Sandy Island", "Small remote transit base on the sandy island near the equator.",
        helipad=(-3.233412, -7.0048, Alt(1, 41.36)),
        staff_spawn=(-3.233296, -7.002907, Alt(1, 41.26)),
        launch_refund=20,
        recovery_factor=80,
    ),
    Location(
        "Sea's End", "Experimental multi-purpose base on the coast of internal sea.",
        aircraft_launch=(-34.11739, 79.79356, Alt(7, 0.0)),
        aircraft_parking=(-34.117719, 79.77547, Alt(3, 2.95)),
        staff_spawn=(-34.119365, 79.776039, Alt(2, 3.84)),
        recovery_factor=75,
        runways=[
            ((-34.118315, 79.8, 8, None), (-34.13773, 79.9365, 8, 0)),
        ],
    ),
    Location(
        "South Hope", "Big airport on the South Hope Islands, which is poorly maintained but is now the only airport serving Southern part of the continent, so having significant passenger flow and relatively intensive air traffic.",
        aircraft_launch=(-49.796341, 16.994601, Alt(18, 240.97)),
        aircraft_parking=(-49.801531, 17.051201, Alt(23, 238.1)),
        launch_refund=20,
        recovery_factor=75,
        runways=[
            ((-49.794, 16.99422, 260, 0), (-49.555, 16.9545, 260, 0)),
        ],
    ),
    Location(
        "South Point", "Small airfield to the South of the Green Coast serving some charter flights.",
        aircraft_launch=(-17.82059, 166.4277, Alt(2, 233.53)),
        staff_spawn=(-17.827524, 166.428829, Alt(1, 235.08)),
        launch_refund=10,
        runways=[
            ((-17.821, 166.4276, 236, 0), (-17.8689, 166.381, 237, 5)),
        ],
    ),
    Location(
        "South Pole Station", "Station in the arctic very close to South Pole used for snow properties research, which provides facility for training kerbonauts to survive in extreme environment.",
        helipad=(-84.73068, 142.6664, Alt(1, 30.0)),
        aircraft_launch=(-84.73943, 142.7313, Alt(1, 30.0)),
        staff_spawn=(-84.738, 142.692, Alt(1, 30.0)),
        recovery_factor=80,
        runways=[
            ((-84.73815, 142.75, 32, 0), (-84.653, 143.93, 33, 0)),
        ],
    ),
    Location(
        "The Shelf", "Small air base between two large bays on the small island far to the South, mainly used as a transit point for cargo for South Pole Station.",
        aircraft_launch=(-53.81633, -162.0954, Alt(8, 307.52)),
        staff_spawn=(-53.8197, -162.0991, Alt(7, 307.15)),
        launch_refund=10,
        recovery_factor=50,
        runways=[
            ((-53.8167, 197.906, 316, 0), (-53.855, 197.9901, 316, 0)),
        ],
    ),
    Location(
        "Valentina's Landing", "Big civil and cargo airport located close to Valentina's hometown.",
        aircraft_launch=(-49.594207, 127.7067, Alt(7, 114.02)),
        aircraft_parking=(-49.593077, 127.74, Alt(20, 99.62)),
        staff_spawn=(-49.58033, 127.722347, Alt(10, 112.55)),
        recovery_factor=50,
        runways=[
            ((-49.5955, 127.7074, 121, 7.5), (-49.359, 127.56575, 126, 0)),
        ],
    ),
]
