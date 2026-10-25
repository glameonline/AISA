// Demo content for the sample website themes. ?i=<key> picks the industry.
window.IND = {
  "aesthetic-clinic": {q:"skincare,spa", n:"Aesthetic Clinic", b:"Lumière Aesthetics", t:"Natural results. Expert hands.", s:["Anti-wrinkle","Dermal fillers","Skin boosters","Chemical peels"], c:["#f6e7e1","#b07a6a","#2b1f1c"], e:"✨", cta:"Book a consultation"},
  "plumber": {q:"plumber,pipes", n:"Plumber", b:"FlowRight Plumbing", t:"Leaks fixed fast. Same-day callouts.", s:["Emergency repairs","Boiler service","Bathroom fitting","Blocked drains"], c:["#e6f1fb","#1f6fb2","#0d2236"], e:"🔧", cta:"Call a plumber"},
  "driving-school": {q:"car,driving", n:"Driving School", b:"PassFirst Driving", t:"Pass first time with calm, patient instructors.", s:["Manual lessons","Automatic lessons","Intensive courses","Pass Plus"], c:["#fff6db","#e0a400","#2a2100"], e:"🚗", cta:"Book a lesson"},
  "electrician": {q:"electrician,wiring", n:"Electrician", b:"BrightSpark Electrical", t:"Safe, certified electrical work.", s:["Rewiring","EV charger install","Fuse boards","EICR certificates"], c:["#fff4e0","#f08a00","#26180a"], e:"⚡", cta:"Get a quote"},
  "construction": {q:"construction,building", n:"Construction Company", b:"Keystone Build", t:"Extensions, new builds and renovations done right.", s:["Extensions","Loft conversions","New builds","Groundworks"], c:["#eceae6","#c9541a","#1c1a17"], e:"🏗️", cta:"Start your project"},
  "it-company": {q:"technology,office", n:"IT Company", b:"Northgrid IT", t:"IT support that just works.", s:["Managed IT","Cyber security","Cloud & Microsoft 365","Helpdesk"], c:["#e8ecff","#4b5cff","#0e1130"], e:"💻", cta:"Book a free IT check"},
  "restaurant": {q:"restaurant,food", n:"Restaurant", b:"Ember & Oak", t:"Wood-fired food, made to share.", s:["Dinner menu","Sunday roast","Private dining","Takeaway"], c:["#f7ece2","#a8401f","#22130c"], e:"🍽️", cta:"Book a table"},
  "barber": {q:"barber,haircut", n:"Barber", b:"Sharp & Co Barbers", t:"Fresh fades. Clean shaves.", s:["Skin fades","Beard trims","Hot towel shave","Kids cuts"], c:["#ededed","#111111","#111111"], e:"💈", cta:"Book a cut"},
  "hair-salon": {q:"hairsalon,hair", n:"Hair & Beauty Salon", b:"Halo Hair Studio", t:"Colour, cuts and care you'll love.", s:["Balayage","Cut & finish","Keratin","Bridal hair"], c:["#f6eaf1","#b03a7a","#2a0f1e"], e:"💇", cta:"Book an appointment"},
  "dentist": {q:"dentist,smile", n:"Dentist", b:"Smile Studio Dental", t:"Gentle dentistry for the whole family.", s:["Check-ups","Teeth whitening","Invisalign","Implants"], c:["#e7f7f5","#0f9b8e","#06302c"], e:"🦷", cta:"Book a check-up"},
  "gym": {q:"gym,fitness", n:"Gym & Personal Trainer", b:"Forge Fitness", t:"Stronger every week.", s:["Personal training","Group classes","Nutrition plans","Online coaching"], c:["#eef0e6","#6b8e00","#151a05"], e:"🏋️", cta:"Start free trial"},
  "cleaning": {q:"cleaning,home", n:"Cleaning Company", b:"Sparkle Clean Co", t:"Spotless homes and offices.", s:["Home cleaning","Office cleaning","End of tenancy","Carpet cleaning"], c:["#e9f6ff","#1aa0e0","#05263a"], e:"🧽", cta:"Get a quote"},
  "accountant": {q:"office,finance", n:"Accountant", b:"Ledger & Lane", t:"Stress-free tax and accounts.", s:["Self assessment","Bookkeeping","VAT returns","Payroll"], c:["#eef1f6","#2b4a7e","#0d1729"], e:"📊", cta:"Book a free call"},
  "estate-agent": {q:"house,interior", n:"Estate Agent", b:"Hearth Homes", t:"Sell faster. Let smarter.", s:["Sales","Lettings","Free valuation","Property management"], c:["#f3efe8","#7a5c2e","#211a0e"], e:"🏡", cta:"Free valuation"},
  "roofer": {q:"roof,house", n:"Roofer", b:"TopLine Roofing", t:"Roofs repaired and replaced.", s:["Roof repairs","New roofs","Flat roofs","Gutters & fascias"], c:["#ecebf2","#4a3f8f","#14112a"], e:"🏠", cta:"Free roof check"},
  "solicitor": {q:"lawyer,office", n:"Solicitor", b:"Carter Lowe Solicitors", t:"Clear legal advice, fixed fees.", s:["Conveyancing","Wills & probate","Family law","Employment"], c:["#efece6","#5a1f2b","#1e0a0f"], e:"⚖️", cta:"Free first call"},
  "photographer": {q:"camera,photography", n:"Photographer", b:"Golden Hour Studio", t:"Photos you'll keep forever.", s:["Weddings","Portraits","Products","Events"], c:["#f5f0e6","#c08a2e","#21180a"], e:"📷", cta:"Check my dates"},
  "mechanic": {q:"mechanic,car", n:"Car Garage & Mechanic", b:"Gearhead Garage", t:"Honest repairs. Fair prices.", s:["MOT","Servicing","Diagnostics","Tyres & brakes"], c:["#ececec","#d32f2f","#1a0606"], e:"🔩", cta:"Book an MOT"},
  "care-home": {q:"elderly,care", n:"Care Home & Home Care", b:"Willow Care", t:"Kind care, close to home.", s:["Home care","Respite care","Dementia care","Live-in care"], c:["#edf5ec","#3f8a4a","#0f2412"], e:"🤝", cta:"Arrange a visit"},
  "landscaper": {q:"garden,landscape", n:"Gardener & Landscaper", b:"Greenleaf Gardens", t:"Gardens you'll love being in.", s:["Garden design","Patios","Fencing","Maintenance"], c:["#ecf4e6","#4c8a2b","#12240a"], e:"🌿", cta:"Get a quote"}
};
window.indKey = function(){var k=new URLSearchParams(location.search).get("i");return IND[k]?k:"plumber"};
window.CALL = "07535677302";
// Hand-picked Unsplash photos per industry (free licence), checked to load.
window.PICS = {
  "aesthetic-clinic":["1570172619644-dfd03ed5d881", "1512290923902-8a9f81dc236c", "1616394584738-fc6e612e71b9", "1596755389378-c31d21fd1273", "1487412947147-5cebf100ffc2", "1540555700478-4be289fbecef", "1515377905703-c4788e51af15", "1544161515-4ab6ce6db874"],
  "plumber":["1585704032915-c3400ca199e7", "1607472586893-edb57bdc0e39", "1621905252507-b35492cc74b4", "1584622650111-993a426fbf0a", "1552321554-5fefe8c9ef14", "1620626011761-996317b8d101", "1581244277943-fe4a9c777189", "1600566752355-35792bedcfea"],
  "driving-school":["1449965408869-eaa3f722e40d", "1503376780353-7e6692767b70", "1494976388531-d1058494cdd8", "1502877338535-766e1452684a", "1580273916550-e323be2ae537", "1511919884226-fd3cad34687c", "1469285994282-454ceb49e63c", "1533473359331-0135ef1b58bf"],
  "electrician":["1621905251918-48416bd8575a", "1555963966-b7ae5404b6ed", "1593941707882-a5bba14938c7", "1544724569-5f546fd6f2b5", "1473341304170-971dccb5ac1e"],
  "construction":["1504307651254-35680f356dfd", "1541888946425-d81bb19240f5", "1503387762-592deb58ef4e", "1531834685032-c34bf0d84c77", "1487958449943-2429e8be8625", "1517089596392-fb9a9033e05b"],
  "it-company":["1518770660439-4636190af475", "1497366216548-37526070297c", "1531297484001-80022131f5a1", "1550751827-4bd374c3f58b", "1504384308090-c894fdcc538d", "1519389950473-47ba0277781c", "1558494949-ef010cbdcc31", "1488590528505-98d2b5aba04b"],
  "restaurant":["1517248135467-4c7edcad34c4", "1414235077428-338989a2e8c0", "1555396273-367ea4eb4db5", "1504674900247-0877df9cc836", "1540189549336-e6e99c3679fe", "1565299624946-b28f40a0ae38", "1544025162-d76694265947", "1559339352-11d035aa65de"],
  "barber":["1503951914875-452162b0f3f1", "1585747860715-2ba37e788b70", "1621605815971-fbc98d665033", "1599351431202-1e0f0137899a", "1622286342621-4bd786c2447c", "1605497788044-5a32c7078486", "1512690459411-b9245aed614b", "1593702275687-f8b402bf1fb5"],
  "hair-salon":["1560066984-138dadb4c035", "1522337360788-8b13dee7a37e", "1562322140-8baeececf3df", "1580618672591-eb180b1a973f", "1595476108010-b4d1f102b1b1", "1519699047748-de8e457a634e", "1521590832167-7bcbfaa6381f", "1633681926022-84c23e8cb2d6"],
  "dentist":["1606811971618-4486d14f3f99", "1588776814546-1ffcf47267a5", "1629909613654-28e377c37b09", "1598256989800-fe5f95da9787", "1609840114035-3c981b782dfe", "1607613009820-a29f7bb81c04", "1588776814546-daab30f310ce", "1468493858157-0da44aaf1d13"],
  "gym":["1534438327276-14e5300c3a48", "1517836357463-d25dfeac3438", "1571019613454-1cb2f99b2d8b", "1540497077202-7c8a3999166f", "1583454110551-21f2fa2afe61", "1574680096145-d05b474e2155", "1581009146145-b5ef050c2e1e", "1549060279-7e168fcee0c2"],
  "cleaning":["1581578731548-c64695cc6952", "1527515637462-cff94eecc1ac", "1563453392212-326f5e854473", "1584820927498-cfe5211fd8bf", "1585421514738-01798e348b17", "1556911220-bff31c812dba", "1528740561666-dc2479dc08ab"],
  "accountant":["1554224155-6726b3ff858f", "1554224154-26032ffc0d07", "1460925895917-afdab827c52f", "1450101499163-c8848c66ca85", "1579621970563-ebec7560ff3e", "1586486855514-8c633cc6fd38", "1543286386-713bdd548da4"],
  "estate-agent":["1560518883-ce09059eeffa", "1564013799919-ab600027ffc6", "1600596542815-ffad4c1539a9", "1600585154340-be6161a56a0c", "1568605114967-8130f3a36994", "1502672260266-1c1ef2d93688", "1512917774080-9991f1c4c750", "1580587771525-78b9dba3b914"],
  "roofer":["1632759145351-1d592919f522", "1605276374104-dee2a0ed3cd6", "1570129477492-45c003edd2be", "1625602812206-5ec545ca1231", "1558036117-15d82a90b9b1", "1518780664697-55e3ad937233"],
  "solicitor":["1589829545856-d10d557cf95f", "1505664194779-8beaceb93744", "1521791055366-0d553872125f", "1479142506502-19b3a3b7ff33", "1507679799987-c73779587ccf", "1589391886645-d51941baf7fb", "1436450412740-6b988f486c6b"],
  "photographer":["1452587925148-ce544e77e70d", "1516035069371-29a1b244cc32", "1519741497674-611481863552", "1502920917128-1aa500764cbd", "1554048612-b6a482bc67e5", "1511285560929-80b456fea0bc", "1542038784456-1ea8e935640e", "1471341971476-ae15ff5dd4ea"],
  "mechanic":["1486262715619-67b85e0b08d3", "1487754180451-c456f719a1fc", "1530046339160-ce3e530c7d2f", "1625047509168-a7026f36de04", "1492144534655-ae79c964c9d7", "1619642751034-765dfdf7c58e"],
  "care-home":["1576765608535-5f04d1e3f289", "1559234938-b60fff04894d", "1447005497901-b3e9ee359928", "1573497019940-1c28c88b4f3e", "1544027993-37dbfe43562a"],
  "landscaper":["1558904541-efa843a96f01", "1585320806297-9794b3e4eeae", "1416879595882-3373a0480b5b", "1592150621744-aca64f48394a", "1523348837708-15d4a09cfac2", "1466692476868-aef1dfb1e735", "1598902108854-10e335adac99"]
};
// Photos are self-hosted copies of the PICS list (8 per industry) so they always load.
window.IMG=function(i){return"/img/themes/"+indKey()+"/"+(i%8)+".jpg"};
