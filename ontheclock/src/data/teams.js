// NFL Teams Data for "On The Clock" Draft Simulator
export const teams = [
  {
    id: 1,
    name: "Arizona Cardinals",
    abbreviation: "ARI",
    colors: {
      primary: "#97233F",
      secondary: "#000000"
    },
    ownership: "Michael Bidwill",
    generalManager: "Monti Ossenfort",
    headCoach: "Jonathan Gannon",
    needs: ["OL", "EDGE", "CB"],
    picks: [4, 27, 35, 71, 104, 138, 162, 186],
    salary_cap: {
      cap_space_2024: 13115113
    },
    trade_tendencies: "Aggressive in draft trades. Traded down from the 3rd overall pick to stockpile draft capital. Has shown willingness to trade picks for veteran talent.",
    recent_draft_history: "Selected OL Paris Johnson Jr. in 2023 (pick 6). Held two first-round picks in 2024, including one via trade from Houston (used on WR Marvin Harrison Jr.).",
    logo: "/assets/logos/ari.png"
  },
  {
    id: 2,
    name: "Atlanta Falcons",
    abbreviation: "ATL",
    colors: {
      primary: "#A71930",
      secondary: "#000000"
    },
    ownership: "Arthur Blank",
    generalManager: "Terry Fontenot",
    headCoach: "Arthur Smith",
    needs: ["EDGE", "TE", "CB"],
    picks: [8, 43, 74, 110, 146, 171, 209],
    salary_cap: {
      cap_space_2024: 31108021
    },
    trade_tendencies: "Historically more inclined to trade up for a target (e.g. 2011 moved up for WR Julio Jones in a blockbuster trade). Under current management, has mostly stayed put and used premium picks on offense. Rarely trades down in Round 1.",
    recent_draft_history: "Used top-8 picks on offensive skill players in four consecutive drafts (TE Kyle Pitts in 2021, WR Drake London in 2022, RB Bijan Robinson in 2023, plus traded up for QB Desmond Ridder in 2022 third round).",
    logo: "/assets/logos/atl.png"
  },
  {
    id: 3,
    name: "Baltimore Ravens",
    abbreviation: "BAL",
    colors: {
      primary: "#241773",
      secondary: "#000000"
    },
    ownership: "Steve Bisciotti",
    generalManager: "Eric DeCosta",
    headCoach: "John Harbaugh",
    needs: ["WR", "EDGE", "CB"],
    picks: [30, 62, 93, 130, 165, 200, 222],
    salary_cap: {
      cap_space_2024: 9604425
    },
    trade_tendencies: "Frequently trades down to stockpile picks under long-time GM Ozzie Newsome and successor DeCosta. Rarely trades up in Round 1. Notable exception: traded back into late 1st round in 2018 to draft QB Lamar Jackson.",
    recent_draft_history: "Selected WR Rashod Bateman in 2021 and WR Zay Flowers in 2023 in the first round, reflecting a push to get weapons for QB Lamar Jackson. Drafted S Kyle Hamilton in 2022 at pick 14, continuing a trend of defense-first picks.",
    logo: "/assets/logos/bal.png"
  },
  {
    id: 4,
    name: "Buffalo Bills",
    abbreviation: "BUF",
    colors: {
      primary: "#00338D",
      secondary: "#C60C30"
    },
    ownership: "Terry & Kim Pegula",
    generalManager: "Brandon Beane",
    headCoach: "Sean McDermott",
    needs: ["WR", "DL", "LB"],
    picks: [28, 60, 91, 129, 160, 198, 221],
    salary_cap: {
      cap_space_2024: 552172
    },
    trade_tendencies: "Generally builds through the draft; not shy to trade picks for proven talent (e.g. Diggs trade in 2020). Under GM Beane, has traded up on occasion (moved up in 2018 to draft Allen at 7th overall).",
    recent_draft_history: "Recent first rounds: 2021 DE Greg Rousseau, 2022 CB Kaiir Elam, 2023 TE Dalton Kincaid – addressing defense and adding weapons for Allen. Regular playoff contender with late-round picks.",
    logo: "/assets/logos/buf.png"
  },
  {
    id: 5,
    name: "Carolina Panthers",
    abbreviation: "CAR",
    colors: {
      primary: "#0085CA",
      secondary: "#101820"
    },
    ownership: "David Tepper",
    generalManager: "Scott Fitterer",
    headCoach: "Dave Canales",
    needs: ["QB", "OL", "WR"],
    picks: [1, 33, 65, 103, 142, 174, 185],
    salary_cap: {
      cap_space_2024: -862719
    },
    trade_tendencies: "Very aggressive under owner David Tepper. Traded a large haul (two 1st-rounders, two 2nd-rounders, plus WR D.J. Moore) to move up for the #1 pick in 2023. Willing to sacrifice future picks for a chance at a franchise quarterback.",
    recent_draft_history: "Held the 1st overall pick in 2023 after a blockbuster trade and selected QB Bryce Young. Drafted DT Derrick Brown (2020) and CB Jaycee Horn (2021) in the top-10, emphasizing defense.",
    logo: "/assets/logos/car.png"
  },
  {
    id: 6,
    name: "Chicago Bears",
    abbreviation: "CHI",
    colors: {
      primary: "#0B162A",
      secondary: "#C83803"
    },
    ownership: "Virginia Halas McCaskey (Halas family)",
    generalManager: "Ryan Poles",
    headCoach: "Matt Eberflus",
    needs: ["OL", "WR", "CB"],
    picks: [9, 40, 72, 109, 145, 180, 217],
    salary_cap: {
      cap_space_2024: 5419854
    },
    trade_tendencies: "In rebuild mode – traded veterans for picks (e.g. Roquan Smith in 2022). Poles showed a willingness to trade down: dealt the 2023 1st overall for multiple future picks. Previously, the Bears traded up for Fields in 2021.",
    recent_draft_history: "Selected QB Justin Fields 11th overall in 2021 after trading up with the Giants. New GM Ryan Poles traded the 2023 #1 pick for a haul including WR D.J. Moore and extra high picks, then drafted OT Darnell Wright at #10 in 2023.",
    logo: "/assets/logos/chi.png"
  },
  {
    id: 7,
    name: "Cincinnati Bengals",
    abbreviation: "CIN",
    colors: {
      primary: "#FB4F14",
      secondary: "#000000"
    },
    ownership: "Mike Brown (Brown family)",
    generalManager: "Duke Tobin (Dir. of Player Personnel, de facto GM)",
    headCoach: "Zac Taylor",
    needs: ["OL", "DL", "TE"],
    picks: [18, 49, 80, 115, 149, 183, 220],
    salary_cap: {
      cap_space_2024: 6093862
    },
    trade_tendencies: "Typically conservative in trading – rarely moves up or down in Round 1. The Bengals usually stick with their draft board; notable that they have never traded a future first-round pick.",
    recent_draft_history: "Hit on back-to-back top-5 picks with QB Joe Burrow (#1 in 2020) and WR Ja'Marr Chase (#5 in 2021), transforming the franchise. Drafted LT Jonah Williams in 2019 (1st round) and added defensive pieces like DB Dax Hill in 2022 (31st).",
    logo: "/assets/logos/cin.png"
  },
  {
    id: 8,
    name: "Cleveland Browns",
    abbreviation: "CLE",
    colors: {
      primary: "#FF3C00",
      secondary: "#311D00"
    },
    ownership: "Jimmy & Dee Haslam",
    generalManager: "Andrew Berry",
    headCoach: "Kevin Stefanski",
    needs: ["DL", "LB", "S"],
    picks: [26, 58, 89, 126, 157, 190, 228],
    salary_cap: {
      cap_space_2024: 1865990
    },
    trade_tendencies: "Aggressive under GM Andrew Berry and owner Haslam – traded multiple high picks for a franchise QB (Watson). Also traded a 2019 1st for WR Odell Beckham in 2019. Tends to trade picks for established players more than trading down for volume.",
    recent_draft_history: "Traded away three straight first-round picks (2022, 2023, 2024) in the Deshaun Watson deal, leaving the team without a Round 1 pick until 2025. Previously drafted QB Baker Mayfield #1 in 2018 and CB Denzel Ward #4 in 2018 (Ward is one of few first-round hits).",
    logo: "/assets/logos/cle.png"
  },
  {
    id: 9,
    name: "Dallas Cowboys",
    abbreviation: "DAL",
    colors: {
      primary: "#003594",
      secondary: "#041E42"
    },
    ownership: "Jerry Jones",
    generalManager: "Jerry Jones (Owner/GM)",
    headCoach: "Mike McCarthy",
    needs: ["OL", "DL", "CB"],
    picks: [24, 56, 87, 125, 155, 193, 216],
    salary_cap: {
      cap_space_2024: 20050038
    },
    trade_tendencies: "Rarely makes huge draft day trades in Round 1. The Jones regime usually stands pat in the first round – notable trade-up was in 2012 for CB Morris Claiborne. More often trades mid-round picks for veterans or trades down to add depth.",
    recent_draft_history: "Known for strong drafting: landed LB Micah Parsons in 2021 (Defensive Rookie of Year) and OT Tyron Smith (2011) & G Zack Martin (2014) in prior years. 2020 first-rounder CeeDee Lamb has become a star.",
    logo: "/assets/logos/dal.png"
  },
  {
    id: 10,
    name: "Denver Broncos",
    abbreviation: "DEN",
    colors: {
      primary: "#FB4F14",
      secondary: "#002244"
    },
    ownership: "Walton-Penner Family Ownership Group",
    generalManager: "George Paton",
    headCoach: "Sean Payton",
    needs: ["QB", "OL", "EDGE"],
    picks: [12, 44, 76, 112, 147, 189, 202],
    salary_cap: {
      cap_space_2024: 6100773
    },
    trade_tendencies: "Highly aggressive recently: traded two 1st-round and two 2nd-round picks (plus players) for Russell Wilson in 2022, and a 1st- and 2nd-round pick for coach Sean Payton (getting a 3rd in return).",
    recent_draft_history: "Traded away multiple high picks in 2022–2023 for QB Russell Wilson and coach Sean Payton. As a result, their last first-round pick was in 2021 (CB Patrick Surtain II, now All-Pro).",
    logo: "/assets/logos/den.png"
  },
  {
    id: 11,
    name: "Detroit Lions",
    abbreviation: "DET",
    colors: {
      primary: "#0076B6",
      secondary: "#B0B7BC"
    },
    ownership: "Sheila Ford Hamp (Ford family)",
    generalManager: "Brad Holmes",
    headCoach: "Dan Campbell",
    needs: ["CB", "DL", "LB"],
    picks: [27, 59, 90, 126, 159, 192, 230],
    salary_cap: {
      cap_space_2024: 23638725
    },
    trade_tendencies: "Under GM Brad Holmes, willing to trade within division: traded down with Vikings in 2022 (from #12 to #32) allowing MIN to draft Lewis Cine, while DET got Jameson Williams. Has also traded up (moved from 32 to 12 in 2022 for Williams).",
    recent_draft_history: "Capitalized on extra picks from the Matthew Stafford trade: drafted OT Penei Sewell (2021 1st round) and WR Jameson Williams (2022 1st round via trade up from 32 to 12). Selected DE Aidan Hutchinson #2 overall in 2022, who became Defensive Rookie of Year runner-up.",
    logo: "/assets/logos/det.png"
  },
  {
    id: 12,
    name: "Green Bay Packers",
    abbreviation: "GB",
    colors: {
      primary: "#203731",
      secondary: "#FFB612"
    },
    ownership: "Publicly owned (Green Bay Packers, Inc.) – President Mark Murphy",
    generalManager: "Brian Gutekunst",
    headCoach: "Matt LaFleur",
    needs: ["OL", "TE", "DL"],
    picks: [25, 57, 88, 122, 158, 191, 225],
    salary_cap: {
      cap_space_2024: 16128199
    },
    trade_tendencies: "Tends to avoid dramatic trades. Usually sticks with original picks – a conservative approach. Traded up occasionally (e.g., in 2020 for QB Jordan Love). In 2023, traded Aaron Rodgers to the Jets for a package including a pick swap in Round 1.",
    recent_draft_history: "Notoriously have not drafted a wide receiver in the 1st round since 2002. Instead, first-round picks have often been defense (CB Eric Stokes 2021, LB Quay Walker and DT Devonte Wyatt 2022) or quarterback (Jordan Love 2020 at pick 26 as Aaron Rodgers' eventual successor).",
    logo: "/assets/logos/gb.png"
  },
  {
    id: 13,
    name: "Houston Texans",
    abbreviation: "HOU",
    colors: {
      primary: "#03202F",
      secondary: "#A71930"
    },
    ownership: "Janice McNair (family of founder Bob McNair)",
    generalManager: "Nick Caserio",
    headCoach: "DeMeco Ryans",
    needs: ["OL", "WR", "DL"],
    picks: [3, 34, 67, 102, 139, 174, 185],
    salary_cap: {
      cap_space_2024: 5762155
    },
    trade_tendencies: "Dramatic moves recently: traded a haul to move up for Will Anderson Jr. in 2023 (sent 2023 2nd and 2024 1st to Arizona). Previously, traded superstar WR DeAndre Hopkins in 2020 (under prior coach/GM O'Brien) for relatively little return.",
    recent_draft_history: "In 2023, owned two top-3 picks: selected QB C.J. Stroud (#2) and traded up to #3 for DE Will Anderson Jr., using capital from the Watson trade. Traded franchise QB Deshaun Watson in 2022 for a package including three first-round picks.",
    logo: "/assets/logos/hou.png"
  },
  {
    id: 14,
    name: "Indianapolis Colts",
    abbreviation: "IND",
    colors: {
      primary: "#002C5F",
      secondary: "#A2AAAD"
    },
    ownership: "Jim Irsay",
    generalManager: "Chris Ballard",
    headCoach: "Shane Steichen",
    needs: ["QB", "OL", "CB"],
    picks: [15, 46, 79, 113, 149, 165, 206],
    salary_cap: {
      cap_space_2024: 10423917
    },
    trade_tendencies: "Ballard is known for trading down to accumulate picks and seldom trading future 1sts. Colts acquired Buckner in 2020 by giving up their 2020 1st. They generally stand pat or move down on draft day.",
    recent_draft_history: "Drafted QB Anthony Richardson at #4 overall in 2023 as the potential franchise QB. Previous first-rounders include DE Kwity Paye (2021) and WR Michael Pittman Jr. (2020 2nd-round, as no 2020 1st after trading down).",
    logo: "/assets/logos/ind.png"
  },
  {
    id: 15,
    name: "Jacksonville Jaguars",
    abbreviation: "JAX",
    colors: {
      primary: "#101820",
      secondary: "#D7A22A"
    },
    ownership: "Shahid Khan",
    generalManager: "Trent Baalke",
    headCoach: "Doug Pederson",
    needs: ["OL", "EDGE", "CB"],
    picks: [2, 34, 66, 106, 142, 172, 214],
    salary_cap: {
      cap_space_2024: 16954079
    },
    trade_tendencies: "Generally keeps high picks. Did trade Jalen Ramsey in 2019 for multiple 1sts (rebuilding move). Baalke has occasionally traded back – e.g., in 2022, traded out of the first round's later picks.",
    recent_draft_history: "Picked #1 overall in back-to-back drafts: QB Trevor Lawrence (2021) and DE Travon Walker (2022). Both are cornerstones of the rebuild. Also drafted RB Travis Etienne in 2021 (Round 1, #25). 2023 first-rounder was OT Anton Harrison.",
    logo: "/assets/logos/jax.png"
  },
  {
    id: 16,
    name: "Kansas City Chiefs",
    abbreviation: "KC",
    colors: {
      primary: "#E31837",
      secondary: "#FFB81C"
    },
    ownership: "Hunt Family (Clark Hunt, Chairman)",
    generalManager: "Brett Veach",
    headCoach: "Andy Reid",
    needs: ["WR", "OL", "DL"],
    picks: [32, 63, 95, 131, 166, 205, 233],
    salary_cap: {
      cap_space_2024: 217702
    },
    trade_tendencies: "Bold when needed: famously moved up to draft Mahomes. Also traded a 1st for DE Frank Clark in 2019, and traded away superstar WR Tyreek Hill in 2022 for a package of picks. Veach will trade up for a targeted player and trade veterans for cap reasons.",
    recent_draft_history: "Drafted QB Patrick Mahomes in 2017 after trading up from #27 to #10, a franchise-altering move that's yielded two Super Bowls. Recent first-rounders: RB Clyde Edwards-Helaire (2020), DE George Karlaftis (2022).",
    logo: "/assets/logos/kc.png"
  },
  {
    id: 17,
    name: "Las Vegas Raiders",
    abbreviation: "LV",
    colors: {
      primary: "#000000",
      secondary: "#A5ACAF"
    },
    ownership: "Mark Davis",
    generalManager: "Dave Ziegler",
    headCoach: "Antonio Pierce",
    needs: ["QB", "OL", "CB"],
    picks: [13, 45, 77, 114, 148, 181, 211],
    salary_cap: {
      cap_space_2024: 35455484
    },
    trade_tendencies: "The Raiders have been active in veteran trades (acquired Davante Adams in 2022 for a 1st and 2nd). On draft day, they haven't traded up in Round 1 recently, tending instead to use their picks.",
    recent_draft_history: "Recent first-round struggles: from 2019–2021, multiple 1st-round picks did not pan out (DE Clelin Ferrell #4 in 2019, WR Henry Ruggs III #12 in 2020, CB Damon Arnette #19 in 2020, OT Alex Leatherwood #17 in 2021 – all no longer with team).",
    logo: "/assets/logos/lv.png"
  },
  {
    id: 18,
    name: "Los Angeles Chargers",
    abbreviation: "LAC",
    colors: {
      primary: "#0080C6",
      secondary: "#FFC20E"
    },
    ownership: "Dean Spanos (Spanos family)",
    generalManager: "Tom Telesco",
    headCoach: "Brandon Staley",
    needs: ["OL", "WR", "DL"],
    picks: [5, 37, 69, 108, 141, 179, 207],
    salary_cap: {
      cap_space_2024: 3935186
    },
    trade_tendencies: "Telesco historically doesn't trade up much in the first round (the team has usually stayed at its slot). More likely to trade mid-round picks for immediate help. Generally conservative – values his picks and prefers to stand pat early.",
    recent_draft_history: "Drafted QB Justin Herbert at #6 in 2020, securing their franchise QB post-Philip Rivers. First-rounders have often been offense: OT Rashawn Slater (2021) became All-Pro, 2022 first-round pick Zion Johnson (Guard) and 2023 first WR Quentin Johnston.",
    logo: "/assets/logos/lac.png"
  },
  {
    id: 19,
    name: "Los Angeles Rams",
    abbreviation: "LAR",
    colors: {
      primary: "#003594",
      secondary: "#FFA300"
    },
    ownership: "Stan Kroenke",
    generalManager: "Les Snead",
    headCoach: "Sean McVay",
    needs: ["OL", "EDGE", "CB"],
    picks: [19, 52, 84, 116, 151, 184, 223],
    salary_cap: {
      cap_space_2024: 3097450
    },
    trade_tendencies: "Extremely aggressive trading first-round picks for established stars. Traded 2017 1st (Goff), 2018 1st (Brandin Cooks), 2019 1st (traded down), 2020 & 2021 1sts (Ramsey), 2022 & 2023 1sts (Stafford).",
    recent_draft_history: "Famously went seven straight years (2017–2023) without a first-round pick, trading them for veterans (QB Matthew Stafford, CB Jalen Ramsey, etc.). Relied on later rounds: e.g. 2022 drafted G Logan Bruss (3rd) as first selection, 2023 drafted G Steve Avila (2nd) first.",
    logo: "/assets/logos/lar.png"
  },
  {
    id: 20,
    name: "Miami Dolphins",
    abbreviation: "MIA",
    colors: {
      primary: "#008E97",
      secondary: "#FC4C02"
    },
    ownership: "Stephen M. Ross",
    generalManager: "Chris Grier",
    headCoach: "Mike McDaniel",
    needs: ["OL", "TE", "LB"],
    picks: [21, 53, 85, 120, 152, 186, 224],
    salary_cap: {
      cap_space_2024: 8131185
    },
    trade_tendencies: "Very aggressive in acquiring veteran talent recently: traded 2022 first-round pick (and more) for WR Tyreek Hill; traded 2023 first (via SF) for OLB Bradley Chubb. Will trade high picks if they feel they're close to contention.",
    recent_draft_history: "After a rebuild yielding three 1st-round picks in 2020 (including QB Tua Tagovailoa at #5), the Dolphins have since traded some picks for veterans. They forfeited their 2023 1st-rounder due to a league tampering penalty.",
    logo: "/assets/logos/mia.png"
  },
  {
    id: 21,
    name: "Minnesota Vikings",
    abbreviation: "MIN",
    colors: {
      primary: "#4F2683",
      secondary: "#FFC62F"
    },
    ownership: "Zygi Wilf (Wilf family)",
    generalManager: "Kwesi Adofo-Mensah",
    headCoach: "Kevin O'Connell",
    needs: ["QB", "DL", "CB"],
    picks: [11, 41, 73, 106, 154, 197, 210],
    salary_cap: {
      cap_space_2024: 10173975
    },
    trade_tendencies: "Analytics-driven front office is open to trades. Made multiple trades in 2022 draft (both down and up). Historically, Vikings trade down often to accumulate mid-round picks (Spielman earned nickname 'Trader Rick').",
    recent_draft_history: "New GM Adofo-Mensah's first draft (2022) included an unusual intradivision trade: traded down from #12 to #32 with Detroit, who picked WR Jameson Williams, while Vikings took S Lewis Cine at 32. 2023 first-rounder WR Jordan Addison has contributed immediately.",
    logo: "/assets/logos/min.png"
  },
  {
    id: 22,
    name: "New England Patriots",
    abbreviation: "NE",
    colors: {
      primary: "#002244",
      secondary: "#C60C30"
    },
    ownership: "Robert Kraft",
    generalManager: "Bill Belichick (de facto)",
    headCoach: "Bill Belichick",
    needs: ["QB", "OL", "WR"],
    picks: [7, 39, 70, 107, 143, 178, 215],
    salary_cap: {
      cap_space_2024: 36446038
    },
    trade_tendencies: "Known for trading down to acquire more picks. Belichick frequently moves out of the first round if value isn't there. They also trade picks for veterans. Rarely trade up in Round 1 (one exception: moved up for DE Chandler Jones in 2012).",
    recent_draft_history: "Drafting has been hit-or-miss post-Brady. 2021 1st-round QB Mac Jones made Pro Bowl as rookie. 2022 1st-round G Cole Strange was seen as a reach at #29. 2023 1st CB Christian Gonzalez looked promising (injured mid-season).",
    logo: "/assets/logos/ne.png"
  },
  {
    id: 23,
    name: "New Orleans Saints",
    abbreviation: "NO",
    colors: {
      primary: "#D3BC8D",
      secondary: "#101820"
    },
    ownership: "Gayle Benson",
    generalManager: "Mickey Loomis",
    headCoach: "Dennis Allen",
    needs: ["QB", "OL", "DL"],
    picks: [14, 45, 78, 115, 151, 184, 218],
    salary_cap: {
      cap_space_2024: 2952943
    },
    trade_tendencies: "Aggressive on draft day: traded up in 2022 for Chris Olave at #11 (sent picks 16, 98, 120 to WAS). Famously gave up 2019 1st-rounder to move up for Davenport in 2018. Loomis and Ireland often trade up for players they love and rarely trade down.",
    recent_draft_history: "Traded away their 2023 first-round pick in a 2022 deal with Philly, leaving them with WR Chris Olave (#11, 2022 after trade up) and OT Trevor Penning (#19, 2022). 2021 first-round DE Payton Turner has had limited impact.",
    logo: "/assets/logos/no.png"
  },
  {
    id: 24,
    name: "New York Giants",
    abbreviation: "NYG",
    colors: {
      primary: "#0B2265",
      secondary: "#A71930"
    },
    ownership: "John Mara & Steve Tisch",
    generalManager: "Joe Schoen",
    headCoach: "Brian Daboll",
    needs: ["OL", "WR", "EDGE"],
    picks: [6, 39, 71, 107, 139, 176, 213],
    salary_cap: {
      cap_space_2024: 2577158
    },
    trade_tendencies: "Historically conservative (rarely traded down early until 2021's Bears trade). Under Schoen, more open to movement: traded down in 2023 second round and traded for Waller. Giants will trade up if value aligns.",
    recent_draft_history: "Selected two top-7 picks in 2022: DE Kayvon Thibodeaux (#5) and OT Evan Neal (#7) to rebuild the trenches. In 2021, traded down from #11 to #20 (first trade-down in Round 1 for NYG in decades) and picked WR Kadarius Toney (later traded).",
    logo: "/assets/logos/nyg.png"
  },
  {
    id: 25,
    name: "New York Jets",
    abbreviation: "NYJ",
    colors: {
      primary: "#125740",
      secondary: "#000000"
    },
    ownership: "Woody & Christopher Johnson",
    generalManager: "Joe Douglas",
    headCoach: "Robert Saleh",
    needs: ["OL", "WR", "EDGE"],
    picks: [10, 42, 74, 111, 146, 173, 203],
    salary_cap: {
      cap_space_2024: 2592821
    },
    trade_tendencies: "Joe Douglas has been aggressive when needed: traded up in 2022 to secure three 1st-round talents. Also traded the #13 pick in 2023 as part of the Aaron Rodgers deal. Historically, the Jets made a huge trade up in 2018, giving three 2nd-rounders to move from #6 to #3 for QB Sam Darnold.",
    recent_draft_history: "Had a banner 2022 draft: CB Sauce Gardner (#4) and WR Garrett Wilson (#10) both won Rookie of the Year honors. Also drafted QB Zach Wilson #2 in 2021 (struggling). 2023 first-round pick DE Will McDonald IV was a surprise mid-1st selection.",
    logo: "/assets/logos/nyj.png"
  },
  {
    id: 26,
    name: "Philadelphia Eagles",
    abbreviation: "PHI",
    colors: {
      primary: "#004C54",
      secondary: "#A5ACAF"
    },
    ownership: "Jeffrey Lurie",
    generalManager: "Howie Roseman",
    headCoach: "Nick Sirianni",
    needs: ["LB", "S", "EDGE"],
    picks: [22, 54, 86, 119, 156, 188, 232],
    salary_cap: {
      cap_space_2024: 9364905
    },
    trade_tendencies: "Extremely active. Howie Roseman frequently trades picks: moved down and up to maximize value (e.g., 2022 trade with Saints to gain 2023 1st, trading up in 2023 for Carter). Not afraid to trade for veterans (gave 2022 1st + 3rd for A.J. Brown).",
    recent_draft_history: "Roseman is known for savvy draft maneuvering: in 2021 traded up two spots to #10 for WR DeVonta Smith; in 2022 traded one of three firsts for a 2023 1st (from NO) and used another to trade for A.J. Brown. Drafted DT Jordan Davis (#13) and C Cam Jurgens in 2022.",
    logo: "/assets/logos/phi.png"
  },
  {
    id: 27,
    name: "Pittsburgh Steelers",
    abbreviation: "PIT",
    colors: {
      primary: "#FFB612",
      secondary: "#101820"
    },
    ownership: "Rooney Family (Art Rooney II)",
    generalManager: "Omar Khan",
    headCoach: "Mike Tomlin",
    needs: ["QB", "OL", "CB"],
    picks: [20, 51, 83, 119, 153, 195, 227],
    salary_cap: {
      cap_space_2024: 9927701
    },
    trade_tendencies: "Typically conservative. The 2023 trade-up for Jones was a notable departure – Steelers usually stay put (last big 1st-round trade-up was 2019 for LB Devin Bush). They value their picks and rarely trade future capital.",
    recent_draft_history: "The Steelers typically pick in the mid-to-late 1st. In 2022, drafted QB Kenny Pickett at #20 as Big Ben's successor. Moved up in 2023 from #17 to #14 to select OT Broderick Jones (rare 1st-round trade-up). 2021 first-round RB Najee Harris became a Pro Bowler.",
    logo: "/assets/logos/pit.png"
  },
  {
    id: 28,
    name: "San Francisco 49ers",
    abbreviation: "SF",
    colors: {
      primary: "#AA0000",
      secondary: "#B3995D"
    },
    ownership: "Denise & John York (York family)",
    generalManager: "John Lynch",
    headCoach: "Kyle Shanahan",
    needs: ["OL", "CB", "EDGE"],
    picks: [31, 61, 94, 132, 164, 201, 229],
    salary_cap: {
      cap_space_2024: 50467685
    },
    trade_tendencies: "Aggressive when targeting a franchise QB: gave up three 1sts for Lance. Also traded mid-season 2022 for RB Christian McCaffrey (cost multiple Day 2 picks). Lynch/Shanahan will swing big – but also willing to trade players (dealt DT DeForest Buckner in 2020 for a 1st).",
    recent_draft_history: "Traded three 1st-rounders to move up and draft QB Trey Lance at #3 in 2021, a move that didn't pan out as Lance was later traded. Because of that trade and others, had no first-rounder in 2022 or 2023.",
    logo: "/assets/logos/sf.png"
  },
  {
    id: 29,
    name: "Seattle Seahawks",
    abbreviation: "SEA",
    colors: {
      primary: "#002244",
      secondary: "#69BE28"
    },
    ownership: "Paul G. Allen Trust (Jody Allen, Chair)",
    generalManager: "John Schneider",
    headCoach: "Pete Carroll",
    needs: ["DL", "OL", "QB"],
    picks: [16, 48, 81, 116, 150, 185, 219],
    salary_cap: {
      cap_space_2024: 14651185
    },
    trade_tendencies: "Previously famous for trading down – often didn't use their original 1st-round pick in early/mid 2010s. But they capitalized on the Wilson trade picks (stayed at #5 and #9). Schneider will trade players for picks (dealt Wilson for a massive haul).",
    recent_draft_history: "Absolutely nailed the 2022 draft: LT Charles Cross (#9) and OLB Boye Mafe (#40) plus RB Ken Walker and CB Tariq Woolen (Day 2/3) revitalized the roster. These picks were aided by the Russell Wilson trade which gave them Denver's #9 and #40.",
    logo: "/assets/logos/sea.png"
  },
  {
    id: 30,
    name: "Tampa Bay Buccaneers",
    abbreviation: "TB",
    colors: {
      primary: "#D50A0A",
      secondary: "#34302B"
    },
    ownership: "Glazer Family",
    generalManager: "Jason Licht",
    headCoach: "Todd Bowles",
    needs: ["QB", "OL", "DL"],
    picks: [17, 49, 82, 118, 152, 187, 226],
    salary_cap: {
      cap_space_2024: 815279
    },
    trade_tendencies: "Licht generally keeps picks but will move around within draft. Traded down in 2022 from late 1st to early 2nd. Not shy to trade Day 3 picks for role players. During Brady era, traded a 4th for Gronkowski (2020).",
    recent_draft_history: "Drafted OT Tristan Wirfs in 2020 (All-Pro) and OLB Joe Tryon-Shoyinka in 2021 late 1st. No 1st-round pick in 2022 (traded down, selected DT Logan Hall in 2nd). 2023 first-rounder DT Calijah Kancey (picked #19) fits their D-line tradition.",
    logo: "/assets/logos/tb.png"
  },
  {
    id: 31,
    name: "Tennessee Titans",
    abbreviation: "TEN",
    colors: {
      primary: "#0C2340",
      secondary: "#4B92DB"
    },
    ownership: "Amy Adams Strunk (Adams family)",
    generalManager: "Ran Carthon",
    headCoach: "Mike Vrabel",
    needs: ["OL", "WR", "EDGE"],
    picks: [23, 55, 86, 124, 156, 189, 231],
    salary_cap: {
      cap_space_2024: 15492667
    },
    trade_tendencies: "Have made significant trades: sent Pro Bowl WR A.J. Brown to Eagles for 1st (Burks) and 3rd. In 2023, traded up in second round to secure QB Levis, indicating aggressiveness for a QB.",
    recent_draft_history: "Drafted RT Peter Skoronski at #11 in 2023 and QB Will Levis in 2nd round 2023 (after trading up). 2022 first-rounder WR Treylon Burks was picked #18 (acquired via trading A.J. Brown to Eagles).",
    logo: "/assets/logos/ten.png"
  },
  {
    id: 32,
    name: "Washington Commanders",
    abbreviation: "WAS",
    colors: {
      primary: "#5A1414",
      secondary: "#FFB612"
    },
    ownership: "Josh Harris Group",
    generalManager: "Martin Mayhew",
    headCoach: "Ron Rivera",
    needs: ["QB", "OL", "LB"],
    picks: [2, 36, 67, 105, 140, 177, 212],
    salary_cap: {
      cap_space_2024: 24017815
    },
    trade_tendencies: "Rivera/Mayhew have mostly stayed put in Round 1. Traded down in 2022 (from 11 to 16) allowing Saints to get Olave and picking up extra mid-rounders. The franchise hasn't made huge draft-day trade-ups recently.",
    recent_draft_history: "Invested in defense with four straight 1st-round picks from 2017-2020 (all in the front seven, including DE Chase Young at #2 in 2020). Broke that streak with WR Jahan Dotson at #16 in 2022 after trading down with the Saints.",
    logo: "/assets/logos/was.png"
  }
];