from classes import (
    ServiceFlightContract, BusinessFlightContract,
    TouristGroupFlightContract, CharterFlightContract,
    CommercialFlightContract,
)


ROUTES = {
    # Service flight contracts
    ("Black Krags", "Kerbal Space Centre"): ServiceFlightContract(
        objective="Our engineers provided technical support for our company's pilots during their training at the Black Krags base. Now the training is over. Return the engineers back to the KSC.",
        staff_type="Engineer",
    ),
    ("Coaler Crater", "Black Krags"): ServiceFlightContract(
        objective="All pilots who perform our charter flights must regularly pass an exam to confirm their qualification. Transport pilots from our office at the Coaler Crater to the Black Krags base where their exam will take place.",
        staff_type="Pilot",
    ),
    ("Deadkerbal Pit", "Hanbert Cape"): ServiceFlightContract(
        objective="Our engineers have successfully launched the rocket at the Deadkerbal Pit. Next launch in their schedule would be at the Hanbert Cape. Please, transport them there.",
        staff_type="Engineer",
    ),
    ("Donby Hole", "Kerbin's Heart Science Centre"): ServiceFlightContract(
        objective="Our scientists from Donby Hole research centre were invited to the geological conference at the Kerbin's Heart Science Centre. Help them get there.",
        staff_type="Scientist",
    ),
    ("Dull Spot", "Old KSC"): ServiceFlightContract(
        objective="Transport our engineers, whose watch at the Dull Spot base is over, back to our headquarter at The Old KSC.",
        staff_type="Engineer",
        beacons=['DUNDARDS-EDGE-NDB', 'OLD-KSC-NORTH-IAF'],
    ),
    ("Dundard's Edge", "Polar Research Centre"): ServiceFlightContract(
        objective="We want to organize a scientific expedition to study polar mountains. Transport scientists from Dundard's Edge, where they were trained, to the starting point of expedition - Polar Research Centre.",
        staff_type="Scientist",
    ),
    ("Green Peaks", "Round Range"): ServiceFlightContract(
        objective="Our medical scientists investigated rare herbs at the Green Peaks. Their research is nearing completion, so they want to return home. Transport them to the Round Range airport.",
        staff_type="Scientist",
    ),
    ("Hanbert Cape", "The Shelf"): ServiceFlightContract(
        staff_type="Engineer",
    ),
    ("Kerbal Space Centre", "Dundard's Edge"): ServiceFlightContract(
        objective="Our company arranged for our pilots to be trained at the Dundard's Edge base to improve their skills. Transport pilots to the base so they can start training.",
        staff_type="Pilot",
        beacons=['BLACK-KRAGS-NDB', 'COALER-CRATER-NDB'],
    ),
    ("Kerbin's Bottom", "The Shelf"): ServiceFlightContract(
        objective="Loaders at The Shelf station have damaged the container with our scientific equipment prepared for shipment to the Pole. Bring there our scientists from nearby Kerbin's Bottom base to assess the damage and decide whether the equipment is suitable for further use.",
        staff_type="Scientist",
    ),
    ("Kerbin's Bottom", "Valentina's Landing"): ServiceFlightContract(
        objective="We had a problem with Kerbin's Bottom telescope so we sent our engineers to fix it. Now their work is done. Transport them to the nearest civil airport, Valentina's Landing.",
        staff_type="Engineer",
    ),
    ("Kerbin's Heart Science Centre", "Lodnie Isles"): ServiceFlightContract(
        objective="Transport scientists who are on vacation from mountain Kerbin's Heart Science Centre to the airport of Lodnie Isles.",
        staff_type="Scientist",
    ),
    ("KKVLA", "Arakebo"): ServiceFlightContract(
        objective="Scientific group in the Arakebo Observatory has some technical problems with the telescope. They asked for help since our company has some qualified engineers at the KKVLA. Transport our engineers to the Arakebo.",
        staff_type="Engineer",
    ),
    ("Mount Snowey", "Deadkerbal Pit"): ServiceFlightContract(
        objective="Our engineers from the Mount Snowey have great experience of mountain launches. Transport our specialists to the Deadkerbal Pit to help the team of that launch site prepare a difficult launch.",
        staff_type="Engineer",
    ),
    ("Polar Research Centre", "Sanctuary Mouth"): ServiceFlightContract(
        objective="Transport our scientists whose working shift at the Polar Research Centre is over to the Sanctuary Mouth.",
        staff_type="Scientist",
        beacons=['GUARDIANS-BASIN-HIGH-NDB', 'SANCTUARY-PASS-NDB'],
    ),
    ("Sandy Island", "Kerbin's Heart Science Centre"): ServiceFlightContract(
        objective="Our engineers at the Sandy Island transit base are waiting for the transport that will take them to the Kerbin's Heart Science Centre.",
        staff_type="Engineer",
    ),
    ("Sea's End", "Goldpool"): ServiceFlightContract(
        objective="We have a valuable cargo at the Goldpool base the delivery of which we can entrust only to our employees. Transport our pilots from the Sea's End base to the Goldpool.",
        staff_type="Pilot",
        beacons=['LONELY-MOUNTAIN-NDB', 'TERMINAL-BAY-NDB'],
    ),
    ("South Point", "Kerbin's Bottom"): ServiceFlightContract(
        objective="Our engineers are going to the Kerbin's Bottom base to work with the radio telescope. At the moment they are stuck at the South Point airport. We need a plane to help them.",
        staff_type="Engineer",
    ),
    ("South Pole Station", "Sea's End"): ServiceFlightContract(
        objective="Our kerbonauts were at pre-flight training at the South Pole Station. Transport them to the Sea's End base, where their mission will start.",
        staff_type="Scientist",
        beacons=['AURORA-EDGE-NDB'],
    ),
    ("The Shelf", "South Pole Station"): ServiceFlightContract(
        staff_type="Engineer",
    ),
    ("Valentina's Landing", "Round Range"): ServiceFlightContract(
        objective="Our reserve pilot at the Round Range airport suddenly fell ill. We have to send there some more pilots to avoid the risk of flight cancellation. Transport our pilots from Valentina's Landing airport.",
        staff_type="Pilot",
        beacons=['SANDY-ISTHMUS-NDB', 'RR-ATC'],
    ),

    # Business flight contracts
    ("Arakebo", "Green Coast"): BusinessFlightContract(
        objective="@/VIK, the head doctor of the Green Coast's city hospital, was on a business trip in Arakebo Island clinic. Now @/VIKwho needs to go home. Meet @/VIKwhom near the clinic and transport to Green Coast.",
        staff_type="Scientist",
        reward=5500,
    ),
    ("Dundard's Edge", "South Hope"): BusinessFlightContract(
        objective="Due to growing air traffic South Hope airport needs qualified air traffic controller. @/VIK is a great one. Meet @/VIKwhom near the Dundard's Edge control tower and transport to South Hope.",
        staff_type="Pilot",
        reward=33000,
        beacons=['COALER-CRATER-NDB', 'BLACK-KRAGS-NDB', 'KSC-NDB', 'MIDISLAND-NDB', 'SCORPION-MOUNTAINS-NDB'],
    ),
    ("Guardian's Basin", "Jeb's Island Resort"): BusinessFlightContract(
        objective="Kerbin Aerotech held a draw among it's employees. The winner, @/VIK, got the tour including the best recreation facilities of Kerbin. Today @/VIKwho is leaving the Guardian's Basin tourist base and moving to the next point of the tour. Transport @/VIKwhom to Jeb's Island Resort.",
        staff_type="Pilot",
        reward=7000,
    ),
    ("Jeb's Island Resort", "Ben Bay"): BusinessFlightContract(
        objective="The key employee of the KashCorp, @/VIK, is resting at the Jeb's Island Resort, but is urgently needed in the headquarter of the company. Meet @/VIKwhom near the cottage which @/VIKwho rents and transport to the Ben Bay.",
        staff_type="Engineer",
        reward=4000,
    ),
    ("Kerbal Space Centre", "Old KSC"): BusinessFlightContract(
        objective="One of the space corporations located in the KSC tends to enter into a contract for the supply of parts for the spacecrafts with SpaceTech Industrial. Organize a transfer from the office to the airport for the CEO of company, @/VIK, and transport @/VIKwhom to the headquarters of the SpaceTech Industrial at the Old KSC for the negotiation of the contract.",
        staff_type="Engineer",
        reward=15000,
        beacons=['BLACK-KRAGS-NDB', 'LAKE-DERMAL-NDB', 'OLD-KSC-SOUTH-IAF'],
    ),
    ("Kerman Lake", "Sea's End"): BusinessFlightContract(
        objective="The scientists from Institute of Water Research located at Kerman Lake need to analize water samples from the inner sea. Meet their collegue @/VIK with a portative water analizator near the Institute and transport @/VIKwhom to the Sea's End base.",
        staff_type="Scientist",
        reward=22000,
        beacons=['MIDISLAND-NDB', 'SCORPION-MOUNTAINS-NDB', 'SOUTH-HOPE-NDB', 'LONELY-MOUNTAIN-NDB'],
    ),
    ("Polar Research Centre", "KKVLA"): BusinessFlightContract(
        objective="Engineers serving KKVLA suspect that an error crept in the settings of antennas synchronization system. They need a piece of advice from a famous scientist @/VIK, who will help them dispel the doubts. Unfortunately, @/VIKwho is now working in the distant observatory in the area of Polar Research Centre. Transport @/VIKwhom to Polar Research Centre airport and then bring to KKVLA.",
        special_notes="Observatory located quite far from airfield, but has it's own helipad. So the good way to transport @/VIK to the plane is to send helicopter for @/VIKwhom from Bio-Dome's helipad.",
        staff_type="Scientist",
        reward=13000,
        beacons=['DUNDARDS-EDGE-NDB'],
    ),

    # Tourist groups contracts
    ("Ben Bay", "Guardian's Basin"): TouristGroupFlightContract(
        objective="One of the departments of the KashCorp organized an offsite corporate party at the Guardian's Basin. Transport participants from the headquarters of KashCorp at the Ben Bay to the tourist base.",
        reward=8000,
    ),
    ("Kerbal Space Centre", "Jeb's Island Resort"): TouristGroupFlightContract(
        objective="KSC is looking for helicopter which can transport kerbonauts, who returned from a flight, to the Jeb's Island Resort for a deserved rest.",
        reward=5000,
    ),
    ("Round Range", "Everkrest"): TouristGroupFlightContract(
        objective="The group of mountain climbers wants to rent a helicopter which will transport them from their arrival airport, Round Range, to the base camp on Everkrest.",
        reward=9000,
    ),

    # Charter flight contracts
    ("Coaler Crater", "Kerman Lake"): CharterFlightContract(
        beacons=['MOUNT-SNOWEY-NDB'],
    ),
    ("Green Coast", "South Point"): CharterFlightContract(),
    ("Kerman Lake", "Sanctuary Mouth"): CharterFlightContract(),
    ("Lake Dermal", "Coaler Crater"): CharterFlightContract(),
    ("Lodnie Isles", "Lushlands"): CharterFlightContract(),
    ("Old KSC", "Green Coast"): CharterFlightContract(
        beacons=['TWIN-PEAKS-NDB'],
    ),
    ("South Point", "Round Range"): CharterFlightContract(
        beacons=['TROPIC-LAKES-NDB'],
    ),
    ("Valentina's Landing", "South Point"): CharterFlightContract(
        beacons=['SANDY-ISTHMUS-NDB'],
    ),

    # Commercial flight contracts
    ("Green Coast", "Lake Dermal"): CommercialFlightContract(
        beacons=['TWIN-PEAKS-NDB'],
    ),
    ("Green Coast", "Sanctuary Mouth"): CommercialFlightContract(
        beacons=['TWIN-PEAKS-NDB', 'LAKE-DERMAL-NDB', 'MOUNT-SNOWEY-NDB'],
    ),
    ("Lake Dermal", "Round Range"): CommercialFlightContract(
        beacons=['TWIN-PEAKS-NDB', 'GREEN-COAST-NDB', 'TROPIC-LAKES-NDB'],
    ),
    ("Lodnie Isles", "Round Range"): CommercialFlightContract(
        beacons=['SLEEPING-IDOL-NDB', 'GREEN-PEAKS-NDB', 'RR-ATC'],
    ),
    ("Lushlands", "Sanctuary Mouth"): CommercialFlightContract(
        beacons=['LODNIE-ISLES-NDB', 'PICTURESQUE-GULF-NDB'],
    ),
    ("Lushlands", "South Hope"): CommercialFlightContract(
        beacons=['TERMINAL-BAY-NDB'],
    ),
    ("Round Range", "Green Coast"): CommercialFlightContract(
        beacons=['TROPIC-LAKES-NDB'],
    ),
    ("Round Range", "Lushlands"): CommercialFlightContract(
        beacons=['GREEN-PEAKS-NDB', 'SLEEPING-IDOL-NDB'],
    ),
    ("Sanctuary Mouth", "Lake Dermal"): CommercialFlightContract(
        beacons=['MOUNT-SNOWEY-NDB'],
    ),
    ("Sanctuary Mouth", "Lodnie Isles"): CommercialFlightContract(
        beacons=['PICTURESQUE-GULF-NDB'],
    ),
    ("Sanctuary Mouth", "South Hope"): CommercialFlightContract(
        beacons=['MIDISLAND-NDB', 'SCORPION-MOUNTAINS-NDB'],
    ),
    ("South Hope", "Lodnie Isles"): CommercialFlightContract(
        beacons=['TERMINAL-BAY-NDB', 'LUSHLANDS-NDB'],
    ),
    ("South Hope", "Round Range"): CommercialFlightContract(
        beacons=['LONELY-MOUNTAIN-NDB', 'KRAKENS-BELLY-NDB', 'RR-ATC'],
    ),
    ("South Hope", "Valentina's Landing"): CommercialFlightContract(
        beacons=['LONELY-MOUNTAIN-NDB', 'AURORA-EDGE-NDB'],
    ),
    ("Valentina's Landing", "Green Coast"): CommercialFlightContract(
        beacons=['SANDY-ISTHMUS-NDB', 'SOUTH-POINT-NDB'],
    ),
}
