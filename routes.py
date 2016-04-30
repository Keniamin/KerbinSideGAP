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
    ("Deadkerbal Pit", "Hanbert Cape"): ServiceFlightContract(
        objective="Our engineers have successfully launched the rocket at the Deadkerbal Pit. Next launch in their schedule would be at the Hanbert Cape. Please, transport them there.",
        staff_type="Engineer",
    ),
    ("Dull Spot", "Old KSC"): ServiceFlightContract(
        objective="Transport our engineers, whose watch at the Dull Spot base is over, back to our headquarter at The Old KSC.",
        staff_type="Engineer",
    ),
    ("Hanbert Cape", "The Shelf"): ServiceFlightContract(
        staff_type="Engineer",
    ),
    ("KKVLA", "Arakebo"): ServiceFlightContract(
        objective="Scientific group in the Arakebo Observatory has some technical problems with the telescope. They asked for help since our company has some qualified engineers at the KKVLA. Transport our engineers to the Arakebo.",
        staff_type="Engineer",
    ),
    ("Mount Snowey", "Deadkerbal Pit"): ServiceFlightContract(
        objective="Our engineers from the Mount Snowey have great experience of mountain launches. Transport our specialists to the Deadkerbal Pit to help the team of that launch site prepare a difficult launch.",
        staff_type="Engineer",
    ),
    ("Sandy Island", "Kerbin's Heart Science Centre"): ServiceFlightContract(
        objective="Our engineers at the Sandy Island transit base are waiting for the transport that will take them to the Kerbin's Heart Science Centre.",
        staff_type="Engineer",
    ),
    ("South Point", "Kerbin's Bottom"): ServiceFlightContract(
        objective="Our engineers are going to the Kerbin's Bottom base to work with the radio telescope. At the moment they are stuck at the South Point airport. We need a plane to help them.",
        staff_type="Engineer",
    ),
    ("The Shelf", "South Pole Station"): ServiceFlightContract(
        staff_type="Engineer",
    ),
    ("Donby Hole", "Kerbin's Heart Science Centre"): ServiceFlightContract(
        objective="Our scientists from Donby Hole research centre were invited to the geological conference at the Kerbin's Heart Science Centre. Help them get there.",
        staff_type="Scientist",
    ),
    ("Dundard's Edge", "Polar Research Centre"): ServiceFlightContract(
        objective="We want to organize a scientific expedition to study polar mountains. Transport scientists from Dundard's Edge, where they were trained, to the starting point of expedition - Polar Research Centre.",
        staff_type="Scientist",
    ),
    ("Green Peaks", "Round Range"): ServiceFlightContract(
        objective="Our medical scientists investigated rare herbs at the Green Peaks. Their research is nearing completion, so they want to return home. Transport them to the Round Range airport.",
        staff_type="Scientist",
    ),
    ("Kerbin's Bottom", "The Shelf"): ServiceFlightContract(
        objective="Loaders at The Shelf station have damaged the container with our scientific equipment prepared for shipment to the Pole. Bring there our scientists from nearby Kerbin's Bottom base to assess the damage and decide whether the equipment is suitable for further use.",
        staff_type="Scientist",
    ),
    ("Kerbin's Heart Science Centre", "Lodnie Isles"): ServiceFlightContract(
        objective="Transport scientists who are on vacation from mountain Kerbin's Heart Science Centre to the airport of Lodnie Isles.",
        staff_type="Scientist",
    ),
    ("Polar Research Centre", "Sanctuary Mouth"): ServiceFlightContract(
        objective="Transport our scientists whose working shift at the Polar Research Centre is over to the Sanctuary Mouth.",
        staff_type="Scientist",
    ),
    ("South Pole Station", "Sea's End"): ServiceFlightContract(
        objective="Our kerbonauts were at pre-flight training at the South Pole Station. Transport them to the Sea's End base, where their mission will start.",
        staff_type="Scientist",
    ),
    ("Coaler Crater", "Black Krags"): ServiceFlightContract(
        objective="All pilots who perform our charter flights must regularly pass an exam to confirm their qualification. Transport pilots from our office at the Coaler Crater to the Black Krags base where their exam will take place.",
        staff_type="Pilot",
    ),
    ("Kerbal Space Centre", "Dundard's Edge"): ServiceFlightContract(
        objective="Our company arranged for our pilots to be trained at the Dundard's Edge base to improve their skills. Transport pilots to the base so they can start training.",
        staff_type="Pilot",
    ),
    ("Sea's End", "Goldpool"): ServiceFlightContract(
        objective="We have a valuable cargo at the Goldpool base the delivery of which we can entrust only to our employees. Transport our pilots from the Sea's End base to the Goldpool.",
        staff_type="Pilot",
    ),

    # Business flight contracts
    ("Arakebo", "Green Coast"): BusinessFlightContract(
        objective="@/VIK, the head doctor of the Green Coast's city hospital, was on a business trip in Aracebo Island clinic. Now @/VIKwho needs to go home. Meet @/VIKwhom near the clinic and transport to Green Coast.",
        staff_type="Scientist",
        reward=5500,
    ),
    ("Dundard's Edge", "South Hope"): BusinessFlightContract(
        objective="Due to growing air traffic South Hope airport needs qualified air traffic controller. @/VIK is a great one. Meet @/VIKwhom near the Dundard's Edge control tower and transport to South Hope.",
        staff_type="Pilot",
        reward=33000,
    ),
    ("Guardian's Basin", "Jeb's island resort"): BusinessFlightContract(
        objective="Kerbin Aerotech held a draw among it's employees. The winner, @/VIK, got the tour including the best recreation facilities of Kerbin. Today @/VIKwho is leaving the Guardian's Basin tourist base and moving to the next point of the tour. Transport @/VIKwhom to Jeb's island resort.",
        staff_type="Pilot",
        reward=7000,
    ),
    ("Jeb's island resort", "Ben Bay"): BusinessFlightContract(
        objective="The key employee of the KashCorp, @/VIK, is resting at the Jeb's island resort, but is urgently needed in the headquarter of the company. Meet @/VIKwhom near the cottage which @/VIKwho rents and transport to the Ben Bay.",
        staff_type="Engineer",
        reward=4000,
    ),
    ("Kerbal Space Centre", "Old KSC"): BusinessFlightContract(
        objective="One of the space corporations located in the KSC tends to enter into a contract for the supply of parts for the spacecrafts with SpaceTech Industrial. Organize a transfer from the office to the airport for the CEO of company, @/VIK, and transport @/VIKwhom to the headquarters of the SpaceTech Industrial at the Old KSC for the negotiation of the contract.",
        staff_type="Engineer",
        reward=15000,
    ),
    ("Kerman Lake", "Sea's End"): BusinessFlightContract(
        objective="The scientists from Institute of Water Research located at Kerman Lake need to analize water samples from the inner sea. Meet their collegue @/VIK with a portative water analizator near the Institute and transport @/VIKwhom to the Sea's End base.",
        staff_type="Scientist",
        reward=22000,
    ),
    ("Polar Research Centre", "KKVLA"): BusinessFlightContract(
        objective="Engineers serving KKVLA suspect that an error crept in the settings of antennas synchronization system. They need a piece of advice from a famous scientist @/VIK, who will help them dispel the doubts. Unfortunately, @/VIKwho is now working in the distant observatory in the area of Polar Research Centre. Transport @/VIKwhom to Polar Research Centre airport and then bring to KKVLA.",
        special_notes="Observatory located quite far from airfield, but has it's own helipad. So the good way to transport @/VIK to the plane is to send helicopter for @/VIKwhom from Bio-Dome's helipad.",
        staff_type="Scientist",
        reward=13000,
    ),

    # Tourist groups contracts
    ("Round Range", "Everkrest"): TouristGroupFlightContract(
        objective="The group of mountain climbers wants to rent a helicopter which will transport them from their arrival airport, Round Range, to the base camp on Everkrest.",
        reward=9000,
    ),
    ("Kerbal Space Centre", "Jeb's island resort"): TouristGroupFlightContract(
        objective="KSC is looking for helicopter which can transport kerbonauts, who returned from a flight, to the Jeb's island resort for a deserved rest.",
        reward=5000,
    ),
    ("Ben Bay", "Guardian's Basin"): TouristGroupFlightContract(
        objective="One of the departments of the KashCorp organized an offsite corporate party at the Guardian's Basin. Transport participants from the headquarters of KashCorp at the Ben Bay to the tourist base.",
        reward=8000,
    ),

    # Charter flight contracts
    ("Coaler Crater", "Kerman Lake"): CharterFlightContract(),
    ("South Point", "Round Range"): CharterFlightContract(),
    ("Lake Dermal", "Coaler Crater"): CharterFlightContract(),
    ("Old KSC", "Green Coast"): CharterFlightContract(),
    ("Kerman Lake", "Sanctuary Mouth"): CharterFlightContract(),
    ("Lodnie Isles", "Lushlands"): CharterFlightContract(),
    ("Green Coast", "South Point"): CharterFlightContract(),

    # Commercial flight contracts
    ("Green Coast", "Lake Dermal"): CommercialFlightContract(),
    ("Green Coast", "Sanctuary Mouth"): CommercialFlightContract(),
    ("South Hope", "Round Range"): CommercialFlightContract(),
    ("Sanctuary Mouth", "Lodnie Isles"): CommercialFlightContract(),
    ("Lake Dermal", "Round Range"): CommercialFlightContract(),
    ("Lushlands", "Sanctuary Mouth"): CommercialFlightContract(),
    ("Lushlands", "South Hope"): CommercialFlightContract(),
    ("Round Range", "Green Coast"): CommercialFlightContract(),
    ("Lodnie Isles", "Round Range"): CommercialFlightContract(),
    ("Sanctuary Mouth", "Lake Dermal"): CommercialFlightContract(),
    ("Sanctuary Mouth", "South Hope"): CommercialFlightContract(),
    ("South Hope", "Lodnie Isles"): CommercialFlightContract(),
    ("Round Range", "Lushlands"): CommercialFlightContract(),
}
