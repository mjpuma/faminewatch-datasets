"""Build FamineWatch Datasets v0.2 from the beta workbook + Ljungqvist et al. (2024) Table A1.

Usage: python3 build.py <repo_dir> <tableA1_json>
"""
import json, re, sys, os, datetime
import pandas as pd

REPO, TA1 = sys.argv[1], sys.argv[2]
OUT = os.path.join(REPO, "data")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- references
REFS = {
 # key: full citation
 "Ljungqvist2024": "Ljungqvist, F. C., Seim, A., & Collet, D. (2024). Famines in medieval and early modern Europe—Connecting climate and society. WIREs Climate Change, 15(1), e859. https://doi.org/10.1002/wcc.859 (open access, CC BY 4.0; famine years from Appendix Table A1)",
 "AlfaniOGrada2017": "Alfani, G., & Ó Gráda, C. (Eds.) (2017). Famine in European History. Cambridge University Press. https://doi.org/10.1017/9781316841235",
 "AlfaniOGrada2018": "Alfani, G., & Ó Gráda, C. (2018). The timing and causes of famines in Europe. Nature Sustainability, 1, 283–288. https://doi.org/10.1038/s41893-018-0078-0",
 "AlfaniOGrada2020data": "Alfani, G., & Ó Gráda, C. (2020). The timing and causes of famines in Europe [dataset]. Inter-university Consortium for Political and Social Research (openICPSR). https://doi.org/10.3886/E120551V1",
 "Alfani2013": "Alfani, G. (2013). Calamities and the Economy in Renaissance Italy: The Grand Tour of the Horsemen of the Apocalypse. Palgrave Macmillan.",
 "AlfaniEtAl2017": "Alfani, G., Mocarelli, L., & Strangio, D. (2017). Italy. In G. Alfani & C. Ó Gráda (Eds.), Famine in European History (pp. 25–47). Cambridge University Press.",
 "PerezMoreda2017": "Pérez Moreda, V. (2017). Spain. In G. Alfani & C. Ó Gráda (Eds.), Famine in European History (pp. 48–72). Cambridge University Press. [cited as 'Moreda (2017)' in Ljungqvist et al. 2024]",
 "Parker2013": "Parker, G. (2013). Global Crisis: War, Climate Change and Catastrophe in the Seventeenth Century. Yale University Press.",
 "CurtisDijkman2019": "Curtis, D. R., & Dijkman, J. (2019). The escape from famine in the northern Netherlands: A reconsideration using the 1690s harvest failures and a broader northwest European perspective. The Seventeenth Century, 34, 229–258.",
 "Lassen2016": "Lassen, T. (2016). Hungerkrisen — Genese und Bewältigung von Hunger in ausgewählten Territorien Nordwestdeutschlands 1690–1750. Universitätsverlag Göttingen.",
 "Brazdil2018": "Brázdil, R., Kotyza, O., & Bauch, M. (2018). Climate and famines in the Czech Lands prior to AD 1500: Possible interconnections in a European context. In D. Collet & M. Schuh (Eds.), Famines During the 'Little Ice Age' (1300–1800) (pp. 91–114). Springer.",
 "PfisterWanner2021": "Pfister, C., & Wanner, H. (2021). Climate and Society in Europe: The Last Thousand Years. Haupt Verlag.",
 "Camenisch2015a": "Camenisch, C. (2015). Endless cold: A seasonal reconstruction of temperature and precipitation in the Burgundian Low Countries during the 15th century based on documentary evidence. Climate of the Past, 11, 1049–1066.",
 "Campbell2010": "Campbell, B. M. S. (2010). Nature as historical protagonist: Environment and society in pre-industrial England. The Economic History Review, 63, 281–314.",
 "Campbell2016": "Campbell, B. M. S. (2016). The Great Transition: Climate, Disease and Society in the Late-Medieval World. Cambridge University Press.",
 "DArrigo2020": "D'Arrigo, R., Klinger, P., Newfield, T., Rydval, M., & Wilson, R. (2020). Complexity in crisis: The volcanic cold pulse of the 1690s and the consequences of Scotland's failure to cope. Journal of Volcanology and Geothermal Research, 389, 106746.",
 "EnglerWerner2015": "Engler, S., & Werner, J. P. (2015). Processes prior and during the early 18th century Irish famines — Weather extremes and migration. Climate, 3, 1035–1056.",
 "CampbellLudlow2020": "Campbell, B. M. S., & Ludlow, F. (2020). Climate, disease and society in late-medieval Ireland. Proceedings of the Royal Irish Academy, 120C, 159–252.",
 "Larsson2006": "Larsson, D. (2006). Den dolda transitionen: Om ett demografiskt brytningsskede i det tidiga 1700-talets Sverige. University of Gothenburg.",
 "Lilja2008": "Lilja, S. (2008). Klimatet, döden och makten — 1690-talets klimatkris. In S. Lilja (Ed.), Leva vid Östersjöns kust (pp. 23–79). Södertörns högskola.",
 "Lilja2012": "Lilja, S. (2012). Klimat och skördar ca 1530–1820. In S. Lilja (Ed.), Fiske, jordbruk och klimat i Östersjöregionen under förmodern tid (pp. 59–119). Södertörns högskola.",
 "Hybel2002": "Hybel, N. (2002). Klima og hungersnød i middelalderen. Historisk Tidsskrift, 20, 265–281.",
 "Dybdahl2014": "Dybdahl, A. (2014). Klimatiske sjokk, uår, sykdom og demografiske kriser i Trøndelag på 1600- og 1700-tallet. Historisk Tidsskrift, 93, 243–275.",
 "LeijonhufvudRetso2021": "Leijonhufvud, L., & Retsö, D. (2021). Documentary evidence of droughts in Sweden between the Middle Ages and ca. 1800 CE. Climate of the Past, 17, 2015–2029.",
 "Huhtamaa2022": "Huhtamaa, H., Stoffel, M., & Corona, C. (2022). Recession or resilience? Long-range socioeconomic consequences of the 17th century volcanic eruptions in northern Fennoscandia. Climate of the Past, 18, 2077–2092.",
 "Kahan1968": "Kahan, A. (1968). Natural calamities and their effect upon the food supply in Russia (an introduction to a catalogue). Jahrbücher für Geschichte Osteuropas, 16, 353–377.",
 "Huhtamaa2015": "Huhtamaa, H., Helama, S., Holopainen, J., Rethorn, C., & Rohr, C. (2015). Crop yield responses to temperature fluctuations in 19th century Finland: Provincial variation in relation to climate and tree-rings. Boreal Environment Research, 20, 707–723.",
 # --- verification / new-event sources
 "CheccheRobinson2013": "Checchi, F., & Robinson, W. C. (2013). Mortality among populations of southern and central Somalia affected by severe food insecurity and famine during 2010–2012. FAO/FSNAU & FEWS NET, Rome/Washington. https://fsnau.org/downloads/Somalia_Mortality_Estimates_Final_Report_8May2013_upload.pdf",
 "McConnell2020": "McConnell, J. R., Sigl, M., Plunkett, G., et al. (2020). Extreme climate after massive eruption of Alaska's Okmok volcano in 43 BCE and effects on the late Roman Republic and Ptolemaic Kingdom. PNAS, 117(27), 15443–15449. https://doi.org/10.1073/pnas.2002722117",
 "Oppenheimer2018": "Oppenheimer, C., Orchard, A., Stoffel, M., et al. (2018). The Eldgjá eruption: timing, long-range impacts and influence on the Christianisation of Iceland. Climatic Change, 147, 369–381. https://doi.org/10.1007/s10584-018-2171-9",
 "PumaChonWada2015": "Puma, M. J., Chon, S., & Wada, Y. (2015). Exploring the potential impacts of historic volcanic eruptions on the contemporary global food system. PAGES Magazine, 23(2), 66–67. https://doi.org/10.22498/pages.23.2.66",
 "Robock2000": "Robock, A. (2000). Volcanic eruptions and climate. Reviews of Geophysics, 38(2), 191–219. https://doi.org/10.1029/1998RG000054",
 "Markevich2021": "Markevich, A., Naumenko, N., & Qian, N. (2021, rev. 2023). The causes of Ukrainian famine mortality, 1932–33. NBER Working Paper 29089. https://www.nber.org/papers/w29089",
 "IPC_FRC_Gaza2025": "IPC Famine Review Committee (2025). Famine Review Committee: Gaza Strip, August 2025 — Conclusions and Recommendations. Integrated Food Security Phase Classification, 22 August 2025.",
 "IPC_Sudan2024": "IPC Famine Review Committee (2024). Sudan: Famine (IPC Phase 5) in Zamzam camp, North Darfur. Integrated Food Security Phase Classification, August 2024.",
 "IPC_Sudan2025": "IPC (2025). Sudan: IPC Acute Food Insecurity Analysis, September 2025 – May 2026 (issued 3 November 2025); FRC confirms Famine (IPC Phase 5) in El Fasher and Kadugli. https://reliefweb.int/report/sudan/sudan-ipc-acute-food-insecurity-analysis-september-2025-may-2026-issued-november-2025",
 "Applebaum2017": "Applebaum, A. (2017). Red Famine: Stalin's War on Ukraine. Allen Lane (London) / Doubleday (New York).",
 "HURI_Ukraine": "Harvard Ukrainian Research Institute MAPA project (Wolowyna et al.). Total direct famine losses in Ukraine by region, 1932–1934. https://www.gis.huri.harvard.edu/media-gallery/detail/1381000/1082125",
 "IPC_Yemen2018": "IPC (2018). Yemen: Integrated Food Security Phase Classification Snapshot, December 2018 – January 2019. https://reliefweb.int/report/yemen/yemen-integrated-food-security-phase-classification-snapshot-december-2018-january-2019",
 "Sigl2015": "Sigl, M., Winstrup, M., McConnell, J. R., et al. (2015). Timing and climate forcing of volcanic eruptions for the past 2,500 years. Nature, 523, 543–549. https://doi.org/10.1038/nature14565",
 "Hartman2019": "Hartman, L. H., Kurbatov, A. V., Winski, D. A., et al. (2019). Volcanic glass properties from 1459 C.E. volcanic event in South Pole ice core dismiss Kuwae caldera as a potential source. Scientific Reports, 9. https://doi.org/10.1038/s41598-019-50939-x",
 "Abbott2021": "Abbott, P. M., Plunkett, G., Corona, C., et al. (2021). Cryptotephra from the Icelandic Veiðivötn 1477 CE eruption in a Greenland ice core: confirming the dating of volcanic events in the 1450s CE and assessing the eruption's climatic impact. Climate of the Past, 17, 565–585. https://doi.org/10.5194/cp-17-565-2021",
 "GVP_Agung": "Global Volcanism Program, Smithsonian Institution. Agung (Indonesia): eruption of 18 Feb 1963 – 27 Jan 1964, VEI 5. https://volcano.si.edu/volcano.cfm?vn=264020",
 "WPF2024": "World Peace Foundation (2024). Historic Famines [synthesis table of famines with ≥100,000 deaths since 1870]. https://worldpeacefoundation.org/",
 "AlfaniOGrada2017_T11": "Alfani, G., & Ó Gráda, C. (2017). Famines in Europe: An overview. In G. Alfani & C. Ó Gráda (Eds.), Famine in European History, Table 1.1 'Famines in Europe, 1250–1900'. Cambridge University Press.",
 "Esmaili_preprint": "Esmaili, E., Puma, M. J., Ludlow, F., Jobbová, E., Kumar, J., Holm, P., Ljungqvist, F. C., Matthews, J. A., Dahl, J. R., & Seim, A. El Niño amplified food insecurity in early modern Europe. Preprint, Research Square (2026). https://doi.org/10.21203/rs.3.rs-7812038/v1",
}

# corrected versions of the beta References sheet (key -> citation); short-form keys as used in the Reference(s) column
BETA_REF_FIXES = {
 "Alfani, G., & Ó Gr_x0013_ada, C. (2018).": "Alfani, G., & Ó Gráda, C. (2018). The timing and causes of famines in Europe. Nature Sustainability, 1, 283–288.",
 "Alfani, G., & Ó Gr_x0013_ada, C. (Eds.) (2017).": "Alfani, G., & Ó Gráda, C. (Eds.) (2017). Famine in European History. Cambridge University Press.",
 "Dijk, A. I.": "van Dijk, A. I. J. M., Beck, H. E., Crosbie, R. S., de Jeu, R. A. M., Liu, Y. Y., Podger, G. M., Timbal, B., & Viney, N. R. (2013). The Millennium Drought in southeast Australia (2001–2009). Water Resources Research, 49, 1040–1057.",
 "Fagan, B. M.": "Fagan, B. M. (2009). Floods, Famines, and Emperors: El Niño and the Fate of Civilizations (rev. ed.; orig. 1999). Basic Books, New York.",
 "Gráda, C. Ó. (2009)": "Ó Gráda, C. (2009). Famine: A Short History. Princeton University Press.",
 "Jordan, W. C. (1997)": "Jordan, W. C. (1996). The Great Famine: Northern Europe in the Early Fourteenth Century. Princeton University Press.",
 "Puma, M.J., Chon, S., Wada, Y. (In press)": REFS["PumaChonWada2015"],
 "Robock, A. (2002)": REFS["Robock2000"],
}

EXTRA_BETA_REFS = [
 "Dikötter, F. (2010). Mao's Great Famine: The History of China's Most Devastating Catastrophe, 1958–1962. Walker & Co.",
 "Yang, J. (2012). Tombstone: The Great Chinese Famine, 1958–1962. Farrar, Straus and Giroux.",
 "Walford, C. (1878). The famines of the world: past and present. Journal of the Statistical Society of London, 41(3), 433–535. [Table 1; Walford quotes earlier chroniclers incl. Short, Stow, Penkethman, Danvers (1877)]",
 "IPC (2017). South Sudan: Famine classification for Leer and Mayendit counties, February 2017. Integrated Food Security Phase Classification.  [full entry to be completed]",
 "UN OCHA (2021). Madagascar: Grand Sud humanitarian snapshot. [full entry to be completed]",
 "WFP (2021). Yemen emergency. [full entry to be completed]",
 "Brooks, E. C. (1916). The Story of Corn and the Westward Migration. Rand McNally. [verify]",
 "Dow, A. (1768–1772). The History of Hindostan. [as cited]",
 "Dando, W. A. (Ed.) (2012). Food and Famine in the 21st Century (2 vols.). ABC-CLIO. [cited as Dando (2012); distinct from Dando (1980) The Geography of Famine]",
 "Ludlow, F., Stine, A. R., Leahy, P., et al. (2013). Medieval Irish chronicles reveal persistent volcanic forcing of severe winter cold events, 431–1649 CE. Environmental Research Letters, 8, 024035.",
]

# ---------------------------------------------------------------- helpers
def parse_years(start, label):
    s = str(label).replace("–", "-").replace("AD", "").strip()
    bc = "BC" in s
    s = s.replace("BC", "").strip()
    nums = [int(n) for n in re.findall(r"\d+", s)]
    present = "present" in s
    if not nums:
        return int(start), int(start)
    a = nums[0]; b = nums[1] if len(nums) > 1 else a
    if bc:
        a, b = -a, -b
    if present:
        b = 2026
    if b < a and not bc:
        b = a
    return a, b

MACRO = {
 # area -> macro region
 "England":"Europe","Ireland":"Europe","Scotland":"Europe","Wales":"Europe","Britain":"Europe","United Kingdom":"Europe",
 "British Isles":"Europe","London":"Europe","Lancashire":"Europe","France":"Europe","Paris":"Europe","Italy":"Europe",
 "Rome":"Europe","Venice":"Europe","Sardinia":"Europe","Sicily":"Europe","Poland":"Europe","Hungary":"Europe",
 "Bohemia":"Europe","Carniola":"Europe","Dresden":"Europe","Germany":"Europe","Sweden":"Europe","Denmark":"Europe",
 "Thuringia, Poland, Silesia":"Europe","Albania":"Europe","Bulgaria":"Europe","Greece":"Europe","Europe":"Europe",
 "Finland":"Europe","Russia":"Europe","Russia and Poland":"Europe","Constantinople":"Europe","Byzantine Empire":"Europe",
 "India":"South Asia","Hindustan":"South Asia","India (Hindustan)":"South Asia","Bangladesh":"South Asia","Pegu":"Southeast Asia",
 "China":"East Asia","North Korea":"East Asia","Cambodia":"Southeast Asia",
 "Egypt":"Middle East & North Africa","Persia":"Middle East & North Africa","Syria":"Middle East & North Africa",
 "Antioch":"Middle East & North Africa","Northern Europe":"Europe","Jerusalem":"Middle East & North Africa","Judea":"Middle East & North Africa",
 "Barbary":"Middle East & North Africa","Syria and Libya":"Middle East & North Africa","Asia Minor":"Middle East & North Africa",
 "Yemen":"Middle East & North Africa","Gaza Strip":"Middle East & North Africa",
 "Cape de Verde":"Sub-Saharan Africa","Somalia":"Sub-Saharan Africa","Sudan":"Sub-Saharan Africa","South Sudan":"Sub-Saharan Africa",
 "Ethiopia":"Sub-Saharan Africa","Uganda":"Sub-Saharan Africa","Madagascar":"Sub-Saharan Africa","Sahel":"Sub-Saharan Africa",
 "Mexico":"Americas", "Africa":"Africa (unspecified)", "\"Northern Nations\"":"Europe", "Phrygia (Turkey)":"Middle East & North Africa","Brazil":"Americas","United States":"Americas","Australia":"Oceania",
}

def norm_area(p):
    if p is None: return None
    p = p.strip().rstrip(".")
    fixes = {"Irelend":"Ireland","Englnad":"England","england":"England","india":"India","England??":"England",
             "Scotland and Nort of England":"Scotland and North of England","Rome:":"Rome","????":"England",
             "and disease throughout Ireland":"Ireland","all over the world":"World (reported)",
             "northeastern Brazil; 1/3 of population died":"Brazil (northeast)"}
    return fixes.get(p, p)

def macro_of(area, text=""):
    if area in MACRO: return MACRO[area]
    a = area or ""
    for k, v in MACRO.items():
        if a.startswith(k): return v
    if any(w in a for w in ["England","Scotland","Wales","Ireland","France","Italy","Germany","Europe","Britain"]): return "Europe"
    if "Brazil" in a: return "Americas"
    if "World" in a or "Asia and Africa" in a: return "Multi-region / global"
    return "Unassigned"

# manual metadata for non-Walford rows (by 0-based row index in beta sheet)
MANUAL = {
 0:("Madagascar","Sub-Saharan Africa","Famine / food crisis"),
 1:("South Sudan","Sub-Saharan Africa","Famine / food crisis"),
 2:("Yemen","Middle East & North Africa","Famine / food crisis"),
 3:("Somalia","Sub-Saharan Africa","Famine / food crisis"),
 4:("Sahel","Sub-Saharan Africa","Famine / food crisis"),
 5:("Australia","Oceania","Production shock (drought)"),
 6:("Sudan (Bahr el Ghazal)","Sub-Saharan Africa","Famine / food crisis"),
 7:("Somalia","Sub-Saharan Africa","Famine / food crisis"),
 8:("North Korea","East Asia","Famine / food crisis"),
 10:("Ethiopia","Sub-Saharan Africa","Famine / food crisis"),
 11:("Sudan","Sub-Saharan Africa","Famine / food crisis"),
 13:("Uganda","Sub-Saharan Africa","Famine / food crisis"),
 15:("Cambodia","Southeast Asia","Famine / food crisis"),
 16:("Bangladesh","South Asia","Famine / food crisis"),
 17:("Ethiopia","Sub-Saharan Africa","Famine / food crisis"),
 18:("India (Maharashtra)","South Asia","Famine / food crisis"),
 20:("China","East Asia","Famine / food crisis"),
 21:("India (Bengal)","South Asia","Famine / food crisis"),
 22:("China (Henan)","East Asia","Famine / food crisis"),
 23:("United States","Americas","Production shock (drought)"),
 24:("Soviet Union (Ukraine, Kazakhstan, N. Caucasus, Volga, W. Siberia)","Europe","Famine / food crisis"),
 25:("China","East Asia","Famine / food crisis"),
 26:("Soviet Russia","Europe","Famine / food crisis"),
 30:("India","South Asia","Famine / food crisis"),
 31:("Russia","Europe","Famine / food crisis"),
 32:("Ethiopia","Sub-Saharan Africa","Famine / food crisis"),
 35:("India, China, Brazil, N. Africa (multi-region)","Multi-region / global","Famine / food crisis"),
 37:("Finland","Europe","Famine / food crisis"),
 38:("India (Orissa)","South Asia","Famine / food crisis"),
 39:("Ireland","Europe","Famine / food crisis"),
 43:("Brazil (northeast)","Americas","Famine / food crisis"),
 49:("Multi-region (Europe, N. America, Indonesia)","Multi-region / global","Volcanic eruption (climate forcing)"),
 61:("Multi-region (global)","Multi-region / global","Climate anomaly"),
 64:("Multi-region (Europe, Egypt, India, China, Japan)","Multi-region / global","Volcanic eruption (climate forcing)"),
 72:("India (Bengal)","South Asia","Famine / food crisis"),
 79:("Ireland","Europe","Famine / food crisis"),
 93:("France","Europe","Famine / food crisis"),
 106:("Multi-region (Russia, Japan, China, W. US)","Multi-region / global","Volcanic eruption (climate forcing)"),
 139:("Multi-region (Mexico, Europe, China, Korea, Japan)","Multi-region / global","Volcanic eruption (climate forcing)"),
 174:("Europe (northwest)","Europe","Famine / food crisis"),
 194:("Multi-region (Japan, Korea, W. Europe, Indonesia)","Multi-region / global","Volcanic eruption (climate forcing)"),
 203:("Multi-region (Japan, Korea, China, Russia, NE Africa, N. Great Plains)","Multi-region / global","Volcanic eruption (climate forcing)"),
 207:("Egypt","Middle East & North Africa","Famine / food crisis"),
 275:("Egypt","Middle East & North Africa","Famine / food crisis"),
 282:("Europe / Middle East","Multi-region / global","Volcanic eruption (climate forcing)"),
 292:("Europe, Asia and Africa (reported)","Multi-region / global","Famine / food crisis"),
 325:("Europe / Middle East","Multi-region / global","Volcanic eruption (climate forcing)"),
 335:("Europe / Middle East","Multi-region / global","Volcanic eruption (climate forcing)"),
 379:("Mediterranean","Multi-region / global","Volcanic eruption (climate forcing)"),
 380:("Egypt","Middle East & North Africa","Production shock (drought)"),
}
VOLC_ROWS = {9:"Philippines",12:"Mexico",14:"United States",19:"Indonesia",27:"United States",28:"Russia",29:"Guatemala",
             33:"New Zealand",34:"Indonesia",36:"Iceland",40:"Nicaragua"}

# ---------------------------------------------------------------- corrections & flags
# each: row index -> dict(field=new value, ...), log text, status
CORR = {}
FLAG = {}
def corr(i, note, **kw): CORR.setdefault(i, []).append((kw, note))
def flag(i, note): FLAG.setdefault(i, []).append(note)

corr(3, "Excess mortality was 0.258 million (258,000; 95% range 244,000–273,000), Oct 2010–Apr 2012, per the FAO/FSNAU–FEWS NET study; beta value 0.285 was a digit transposition. Reference replaced (beta cited 'FAO (2013)').",
     impacts="Somalia (southern & central); excess mortality 0.258 million (244,000–273,000), Oct 2010–Apr 2012; ~4.6% of population, ~10% of children under five",
     refs="Checchi & Robinson (2013)", years="AD 2010-2012", start=2010)
corr(20, "Fixed truncated 'ovt.' and swapped book titles: 'Tombstone' is Yang (2012); 'Mao's Great Famine' is Dikötter (2010).",
     cause='Govt. policy failure, "Great Leap Forward"', refs="Ó Gráda (2009); Dikötter (2010) Mao's Great Famine; Yang (2012) Tombstone")
corr(29, "Volcano name fixed (was 'Santa Maria (1902)').", cause="Santa María (Guatemala)")
corr(33, "Tarawera eruption was 10 June 1886, not 1885.", start=1886, years="AD 1886", cause="Tarawera, Ōkataina caldera (New Zealand)")
corr(49, "'Puma et al (in press)' published as Puma, Chon & Wada (2015), PAGES Magazine 23(2).",
     refs="Stothers (1999); Stommel & Stommel (1983); Oppenheimer (2003); McMichael (2012); Puma, Chon & Wada (2015)")
corr(64, "Fixed citation 'Grattan(2006)'.", refs="Tanguy et al. (1998); Stothers (1999); Thordarson & Self (2003); Oman et al. (2006); Grattan (2006); Grove (2007); Trigo et al. (2010); D'Arrigo et al. (2011); Dando (2012)")
# Dando (2012) = edited volume; added to references below
corr(106, "'Puma et al (in press)' → Puma, Chon & Wada (2015).", refs="Atwell (2001); Puma, Chon & Wada (2015)")
corr(139, "'Puma et al (in press)' → Puma, Chon & Wada (2015).", refs="Atwell (2001); Ó Gráda (2009); Puma, Chon & Wada (2015)")
corr(174, "Year range aligned to start year; 'Jordan WC (1996)' kept (Princeton 1996 is the first edition; References sheet year corrected from 1997).", years="AD 1315-1317")
corr(194, "'Puma et al (in press)' → Puma, Chon & Wada (2015).", refs="Lavigne et al. (2013); Stothers (1999); Puma, Chon & Wada (2015)")
corr(203, "'Puma et al (in press)' → Puma, Chon & Wada (2015).", refs="Atwell (2001); Ó Gráda (2009); Puma, Chon & Wada (2015)")
corr(275, "Typo ('dies').", impacts="Severe drought; 600,000 people died (1/4 of population)")
corr(282, "Eldgjá eruption re-dated: began spring 939 CE and continued to at least autumn 940 CE (Oppenheimer et al. 2018); the 934 date (Stothers) is superseded.",
     start=939, years="AD 939-940", refs="Stothers (1999); Oppenheimer et al. (2018)")
corr(379, "The 43 BCE climate shock is now attributed to the Okmok II eruption (Alaska), early 43 BCE (McConnell et al. 2020), not Etna.",
     cause="Okmok II (Alaska, USA); formerly attributed to Etna", start=-43, years="43-42 BC",
     impacts="Dry fog (started March for 9-10 months); First winter cold in Europe; Poor harvest and famine in the Mediterranean (43–42 BCE among the coldest years of recent millennia in the N. Hemisphere)",
     refs="Stothers (1999); McConnell et al. (2020)")

# ---- v0.2 review fixes (requested 23 Nov 2026)
corr(2, "Reworded to the IPC scale: the IPC classified ~63,500 people in Phase 5 (Catastrophe) in Dec 2018–Jan 2019 (238,000 without humanitarian food assistance), but no area was classified in Famine (Phase 5). Reference updated.",
     impacts="Yemen; severe acute food insecurity, not a classified Famine: IPC Dec 2018–Jan 2019 found 15.9 million people (53%) in IPC Phase 3+ incl. ~5 million in Phase 4 (Emergency) and ~63,500 in Phase 5 (Catastrophe) despite humanitarian food assistance (238,000 in Phase 5 without it)",
     refs="IPC (2018); WFP (2021)")
corr(8, "Dates corrected to the famine proper (the 'Arduous March', 1995–98); mortality estimate refers to 1995–2000.",
     start=1995, years="AD 1995-1998",
     impacts="North Korean Famine ('Arduous March', 1995–1998); 30% of grain crops lost in 1995; excess mortality 0.6–1 million (3–4% death rate) over 1995–2000")
corr(10, "Dates corrected: the Ethiopian famine was 1983–85 (peak 1984–85). Added the higher World Peace Foundation estimate.",
     start=1983, years="AD 1983-1985",
     impacts="Ethiopia (Wollo, Tigray and other areas), 1983–85; excess mortality 0.5 million (1% death rate) per Ó Gráda (2009); other estimates up to ~0.8 million (World Peace Foundation 2024)",
     refs="Ó Gráda (2009); World Peace Foundation (2024)")
corr(19, "Size corrected to VEI 5 per the Smithsonian Global Volcanism Program (Robock 2000 lists VEI 4).",
     env="Volcanic eruption (VEI: 5)", refs="Robock (2000); Smithsonian GVP")
corr(22, "Dates corrected: the Henan famine was 1942–43.",
     start=1942, years="AD 1942-1943", impacts="China (Henan province), 1942–43; possibly 2–3 million deaths")
corr(24, "Excess mortality replaced: beta value (1.2 million, 0.7%) was far below the literature. Now: at least 5 million famine deaths across the USSR in 1931–34, incl. ~3.9 million excess deaths in Ukraine (~13% of its population); published range 5.5–10.8 million. References added.",
     impacts="Soviet famine of 1931–33 (in Ukraine, the Holodomor of 1932–33); affected Ukraine, Northern Caucasus, Volga Region, Kazakhstan, the South Urals and West Siberia; at least 5 million famine deaths across the USSR in 1931–34 (Applebaum 2017), including ~3.9 million excess deaths in Ukraine, ~13% of its 1933 population (HURI MAPA); published estimates range 5.5–10.8 million (Markevich, Naumenko & Qian 2021)",
     cause="Govt. policy (forced collectivization, grain requisitions, blacklisting, movement restrictions); poor 1931–32 harvests",
     refs="Ó Gráda (2009); Applebaum (2017); HURI MAPA; Markevich, Naumenko & Qian (2021); Conquest (1987, 2001); Ellman (2005, 2007); Tauger (1991, 2001); Wheatcroft et al. (2004)")
corr(139, "Volcanic attribution corrected: ice-core work shows two 1450s events, a Northern Hemisphere eruption in 1452/early 1453 and a Southern Hemisphere eruption in 1457/58, and glass shards from the 1458/59 layer are chemically distinct from Kuwae, so Kuwae is no longer accepted as the source.",
     cause="Unidentified eruptions: N. Hemisphere 1452/early 1453 and S. Hemisphere 1457/58 (formerly attributed to Kuwae, Vanuatu)",
     start=1453, years="AD 1453-1458",
     refs="Atwell (2001); Ó Gráda (2009); Puma, Chon & Wada (2015); Sigl et al. (2015); Hartman et al. (2019); Abbott et al. (2021)")

flag(335, "Source of the 536 CE event remains unidentified (candidate high-latitude N. Hemisphere eruption; a second major eruption in 539/540).")

def find_rows(df, start, contains):
    return [i for i in df.index if df.at[i,"start"]==start and contains in str(df.at[i,"impacts"])]

# ---------------------------------------------------------------- load beta
xl = os.path.join(REPO, "famine_database_beta.xlsx")
df = pd.read_excel(xl, sheet_name="FoodDisruptionList", header=1)
df.columns = ["cause","env","start","years","impacts","refs"]

# text-level fixes for Walford rows, located by content
for i in find_rows(df, 1813, "Poland"):
    corr(i, "Removed stray text pasted from the 1822 Ireland entry (that event has its own row).",
         impacts='Famine in Poland: "Suffered from famine, consequent upon an inundation; also Drontheim (Norway), in consequence of the intercepting of supplies by Sweden; 5,000 perished."', cause="Floods", env="Floods")
for i in find_rows(df, 1598, "Pegu"):
    corr(i, "Typo 'Gamine Pegu'.", impacts='Famine in Pegu: "Very severe."')
REMOVE = {}
for i in find_rows(df, 1594, "siege of Paris"):
    corr(i, "Walford's quotation under this year describes the siege of Paris by Henry IV, which took place in 1590, not 1594; the quotation was moved to a separate 1590 Paris entry. The 1594 England famine itself is consistent with Alfani & Ó Gráda (England famine 1594–98).",
         impacts="Famine in England and Hungary")
for i in find_rows(df, 1286, "twenty-three years"):
    REMOVE[i] = "Removed: Walford (citing Short) describes 'a twenty-three years' famine' starting in 1286. A continuous 1286–1308 famine is ruled out by both modern chronologies (Britain: famine only in 1295–96 in Ljungqvist et al. 2024; England: no famine years 1290–1314 in the Alfani & Ó Gráda 2018 data), and the individual dearth years Walford reports in this period (1289, 1294, 1295, 1298) remain as separate entries."
dup = find_rows(df, 1586, "Famine in England")
bare = [i for i in dup if str(df.at[i,"impacts"]).strip()=="Famine in England"]
for i in bare:
    REMOVE[i] = "Removed: duplicate of the other 1586 England entry (Walford 1878, Table 1), which carries the full text."
for i in find_rows(df, 1831, "NEED TO ADD WALFORD"):
    corr(i, "Removed internal to-do note from the description (gap logged in README: Walford Table 1 entries 1832–1878 not yet transcribed).",
         impacts='Famine in Ireland: "Famine; Parliament granted 40,000l. for relief; 74,410l. subscriptions in England."')
for i in df.index:
    s = str(df.at[i,"impacts"])
    for a,b in [("Irelend","Ireland"),("Englnad","England"),("Famaine","Famine"),("Famine ????","Famine in England"),("Famine in England??","Famine in England"),("Nort of England","North of England"),("Famine Rome","Famine in Rome"),("Famine  in","Famine in")]:
        if a in s:
            s2 = s.replace(a,b)
            if i not in CORR or not any("impacts" in kw for kw,_ in CORR[i]):
                corr(i, f"Typo '{a}' → '{b}'.", impacts=s2)
            s = s2

rows = []
log = []
today = "2026-11-23"
removed_log = []
for i in df.index:
    r = df.loc[i].to_dict()
    if i in REMOVE:
        removed_log.append(dict(row=i, start=int(r["start"]), years=str(r["years"]), impacts=str(r["impacts"]), note=REMOVE[i]))
        continue
    for kw, note in CORR.get(i, []):
        for k, v in kw.items():
            old = r[k]; r[k] = v
            log.append(dict(event_id=None, row=i, field=k, old=str(old), new=str(v), note=note, date=today))
    start = int(r["start"])
    a, b = parse_years(start, r["years"])
    if a != start and abs(a-start) <= 2:  # keep explicit start column authoritative
        pass
    imp = None if pd.isna(r["impacts"]) else str(r["impacts"])
    # area / type
    if i in MANUAL:
        area, macro, etype = MANUAL[i]
    elif i in VOLC_ROWS:
        area, macro, etype = VOLC_ROWS[i], "Multi-region / global", "Volcanic eruption (climate forcing)"
    else:
        m = re.match(r'\s*F\w*ine\s+(?:in\s+)?([^:"]+?)\s*[:"]', imp or "") or re.match(r'\s*F\w*ine\s+(?:in\s+)?(.+)$', imp or "")
        area = norm_area(m.group(1)) if m else None
        if area and area.startswith("Rome"): area = "Rome"
        if (imp or "").startswith('Famine in "Northern Nations"'): area = "Northern Europe (\"Northern Nations\")"
        if area == "Antioch and": area = "Antioch; Goths"
        macro = macro_of(area); etype = "Famine / food crisis"
    status = "as compiled (beta); not yet re-verified"
    if i in CORR: status = "corrected in v0.2"
    if i in FLAG: status = "flagged for review" if i not in CORR else "corrected in v0.2; further review flagged"
    refs = "" if pd.isna(r["refs"]) else str(r["refs"])
    src = "Walford (1878)" if "Walford" in refs else "Puma & Chon compilation"
    rows.append(dict(
        source_dataset="Puma & Chon (2025) beta compilation",
        start_year=start, end_year=max(b, start) if start>=0 else max(b,start),
        year_label=str(r["years"]).replace("  "," ").strip(),
        area=area, macro_region=macro, event_type=etype,
        primary_cause=None if pd.isna(r["cause"]) or str(r["cause"]).strip() in ("","N/A") else str(r["cause"]).strip(),
        environmental_category=None if pd.isna(r["env"]) or str(r["env"]).strip() in ("","N/A") else str(r["env"]).strip(),
        description=imp, references=refs, severity_info=None,
        verification_status=status,
        qc_notes=" | ".join([n for _,n in CORR.get(i,[])] + FLAG.get(i,[])) or None,
        _row=i))

# fix end_year for BC rows (both negative)
for r in rows:
    if r["start_year"] < 0:
        a, b = parse_years(r["start_year"], r["year_label"])
        r["end_year"] = max(a, b)
        if r["end_year"] < r["start_year"]: r["end_year"] = r["start_year"]

# ---------------------------------------------------------------- new modern events (verified this release)
NEW = [
 dict(start_year=2024, end_year=2026, year_label="AD 2024-present", area="Sudan (North Darfur; South Kordofan)", macro_region="Sub-Saharan Africa",
      event_type="Famine / food crisis", primary_cause="Armed conflict (SAF–RSF war since April 2023), siege, displacement, blocked humanitarian access",
      environmental_category="Minor/no env.",
      description="Sudan; IPC Famine Review Committee confirmed Famine (IPC Phase 5) in Zamzam camp (Aug 2024), in displacement camps around El Fasher (Dec 2024), and in El Fasher and Kadugli towns (Sep 2025 analysis, issued Nov 2025); ~21.2 million people (45%) in high acute food insecurity",
      references="IPC FRC (2024); IPC (2025)", verification_status="added in v0.2 (source-checked)",
      qc_notes="New entry. Area-level Famine classifications are localized; national excess-mortality estimates not yet available."),
 dict(start_year=2025, end_year=2025, year_label="AD 2025", area="Gaza Strip (Gaza Governorate)", macro_region="Middle East & North Africa",
      event_type="Famine / food crisis", primary_cause="Armed conflict, restrictions on humanitarian and commercial access",
      environmental_category="Minor/no env.",
      description="Gaza Strip; IPC Famine Review Committee determined on 22 Aug 2025 that Famine (IPC Phase 5) was occurring in Gaza Governorate, projected to expand to Deir al-Balah and Khan Younis; ~641,000 people projected in Phase 5 by end Sep 2025. The Government of Israel rejected the finding.",
      references="IPC FRC (2025)", verification_status="added in v0.2 (source-checked)",
      qc_notes="New entry. First IPC-confirmed Famine in the Middle East region."),
]
NEW.append(dict(start_year=1590, end_year=1590, year_label="AD 1590", area="Paris", macro_region="Europe",
      event_type="Famine / food crisis", primary_cause="War (siege of Paris by Henry IV)", environmental_category="Minor/no env.",
      description='Famine in Paris during the siege by Henry IV: "During the siege of Paris by Henry IV this year, owing to famine, bread which had been sold, while any remained, for a crown a-pound, was at last made from the bones of the charnel-house of the Holy Innocents.-Hinault." (Walford prints this under 1594; the siege was in 1590.)',
      references="Walford (1878), Table 1", verification_status="corrected in v0.2",
      qc_notes="Split from Walford's 1594 England/Hungary entry and re-dated to 1590, the year of the siege."))
for n in NEW:
    n.update(source_dataset="Puma & Chon compilation — v0.2 additions", severity_info=None, _row=None)
    rows.append(n)

# ---------------------------------------------------------------- Ljungqvist et al. Table A1
REGION_SRC = {
 "Italy": "Alfani (2013); Alfani, Mocarelli & Strangio (2017)",
 "Spain": "Pérez Moreda (2017)",
 "France": "Parker (2013); Curtis & Dijkman (2019)",
 "Central Europe": "Parker (2013); Lassen (2016); Brázdil, Kotyza & Bauch (2018); Pfister & Wanner (2021)",
 "Low Countries": "Camenisch (2015a); Curtis & Dijkman (2019)",
 "Great Britain": "Campbell (2010, 2016); D'Arrigo et al. (2020)",
 "Ireland": "Engler & Werner (2015); Campbell & Ludlow (2020)",
 "Nordic": "Larsson (2006); Lilja (2008, 2012); Hybel (2002); Dybdahl (2014); Leijonhufvud & Retsö (2021); Huhtamaa, Stoffel & Corona (2022)",
 "Russia/Ukraine": "Kahan (1968); Huhtamaa et al. (2015)",
}
REGION_ORDER = list(REGION_SRC)
REGION_ID = {"Italy":"IT","Spain":"ES","France":"FR","Central Europe":"CE","Low Countries":"LC","Great Britain":"GB","Ireland":"IE","Nordic":"NO","Russia/Ukraine":"RU"}

def parse_cell(s):
    out = []
    for part in [p.strip() for p in s.split(",")]:
        m = re.match(r"^(\d{4})(?:–(\d{2,4}))?$", part)
        a = int(m.group(1)); b = m.group(2)
        if b is None: e = a
        elif len(b) == 4: e = int(b)
        else:
            e = int(str(a)[:2] + b)
            if e < a: e += 100
        out.append((a, e, part))
    return out

ta1 = json.load(open(TA1))
eps = []
for page, y, cells in ta1:
    for reg, v in cells.items():
        for a, e, txt in parse_cell(v):
            eps.append(dict(region=reg, start_year=a, end_year=e, as_printed=txt, table_page=29 if page==254 else 30))
eps.sort(key=lambda d: (REGION_ORDER.index(d["region"]), d["start_year"]))
for d in eps:
    d["episode_id"] = f"LJ24-{REGION_ID[d['region']]}-{d['start_year']}"
    d["n_years"] = d["end_year"] - d["start_year"] + 1
    note = None
    d["end_year_corrected"] = d["end_year"]
    if d["region"]=="Italy" and d["as_printed"]=="1539–49":
        d["end_year_corrected"] = 1540
        note = "Printed as 1539–49 in Table A1, overlapping the separate Italy 1544–45 entry. Almost certainly a typesetting error for 1539–40: the Alfani & Ó Gráda (2018) replication data code Italy famine years as 1539–1540. end_year keeps the printed value; end_year_corrected = 1540."
    if d["region"]=="Russia/Ukraine" and d["start_year"] in (1279,1282,1468,1472,1674,1677):
        note = "Printed as a comma-separated list in one cell; split into separate single-year episodes here."
    d["note"] = note
    d["regional_sources"] = REGION_SRC[d["region"]]
    d["citation"] = "Ljungqvist, Seim & Collet (2024), WIREs Climate Change 15(1):e859, Table A1 (revised from Alfani & Ó Gráda 2017, 2018)"
ep_df = pd.DataFrame(eps)[["episode_id","region","start_year","end_year","end_year_corrected","n_years","as_printed","regional_sources","note","table_page","citation"]]

# region-year long table (presence/absence), 1250-1800
ry = []
for reg in REGION_ORDER:
    yrs = {}; yrc = set()
    for d in eps:
        if d["region"]==reg:
            for yy in range(d["start_year"], d["end_year"]+1):
                yrs.setdefault(yy, []).append(d["episode_id"])
            yrc.update(range(d["start_year"], d["end_year_corrected"]+1))
    for yy in range(1250, 1801):
        ry.append(dict(region=reg, year=yy, famine=int(yy in yrs), famine_corrected=int(yy in yrc), episode_ids=";".join(yrs.get(yy, [])) or None))
ry_df = pd.DataFrame(ry)
wide = ry_df.pivot(index="year", columns="region", values="famine")[REGION_ORDER].reset_index()

for d in eps:
    rows.append(dict(
        source_dataset="Ljungqvist et al. (2024) Table A1",
        start_year=d["start_year"], end_year=d["end_year"], year_label=d["as_printed"],
        area=d["region"], macro_region="Europe", event_type="Famine (regional famine years)",
        primary_cause=None, environmental_category=None,
        description=f"Famine conditions recorded in {d['region']} ({d['as_printed']}) in the updated European famine-year chronology. Presence only: the list does not record severity or geographic extent within the region.",
        references="Ljungqvist, Seim & Collet (2024), Table A1; base lists: Alfani & Ó Gráda (2017, 2018); regional revisions: " + d["regional_sources"],
        severity_info=None, verification_status="transcribed from published table (v0.2)",
        qc_notes=d["note"], _row=None, episode_id=d["episode_id"]))

AOG_1800s = [("Spain","1803–04"),("Germany/Switzerland/Austria","1805"),
             ("Italy","1817"),("Germany/Switzerland/Austria","1815–17"),("Low Countries","1816–17"),("Ireland","1816–18"),
             ("Germany/Switzerland/Austria","1845–48"),("Low Countries","1845–50"),("Ireland","1845–52"),
             ("Nordic Europe","1866–68"),("Russia/Ukraine","1866–68")]
aog_rows = []
for reg, txt in AOG_1800s:
    a, e, _ = parse_cell(txt)[0]
    rid = "AOG17-" + re.sub(r"[^A-Z]", "", reg.upper())[:3] + f"-{a}"
    aog_rows.append(dict(episode_id=rid, region=reg, start_year=a, end_year=e, as_printed=txt,
                         citation="Alfani & Ó Gráda (2017), Famine in European History, Table 1.1 'Famines in Europe, 1250–1900'"))
    rows.append(dict(source_dataset="Alfani & Ó Gráda (2017) Table 1.1, 1800–1900",
        start_year=a, end_year=e, year_label=txt, area=reg, macro_region="Europe", event_type="Famine (regional famine years)",
        primary_cause=None, environmental_category=None,
        description=f"Famine years recorded for {reg} ({txt}) in Table 1.1 of Alfani & Ó Gráda (2017). Table 1.1 lists only the major famines reported in at least two European regions, so single-region 19th-century famines are not included here.",
        references="Alfani & Ó Gráda (2017), Table 1.1", severity_info=None,
        verification_status="transcribed from published table (v0.2)", qc_notes=None, _row=None, episode_id=rid))
pd.DataFrame(aog_rows).to_csv(os.path.join(OUT, "europe_famine_episodes_1800-1900_AlfaniOGrada2017_Table1-1.csv"), index=False)
ev = pd.DataFrame(rows)
ev = ev.sort_values(["start_year","source_dataset","area"], ascending=[False, True, True]).reset_index(drop=True)
ids = []
cnt = 0
for _, r in ev.iterrows():
    if isinstance(r.get("episode_id"), str): ids.append(r["episode_id"])
    else:
        cnt += 1; ids.append(None)
ev["event_id"] = ids
# stable ids for compilation rows, numbered chronologically ascending
mask = ev["event_id"].isna()
order = ev[mask].sort_values(["start_year","area"], na_position="last").index
for k, idx in enumerate(order, 1):
    ev.at[idx, "event_id"] = f"FW-{k:04d}"
# map log rows to ids
row2id = {int(r["_row"]): r["event_id"] for _, r in ev.iterrows() if pd.notna(r["_row"])}
for l in log: l["event_id"] = row2id.get(l["row"])
for _, r in ev.iterrows():
    if pd.notna(r["_row"]) and int(r["_row"]) in FLAG:
        for n in FLAG[int(r["_row"])]:
            log.append(dict(event_id=r["event_id"], row=int(r["_row"]), field="(flag)", old="", new="", note=n, date=today))
for n in NEW:
    pass
COLS = ["event_id","source_dataset","start_year","end_year","year_label","area","macro_region","event_type",
        "primary_cause","environmental_category","description","references","verification_status","qc_notes"]
ev = ev[COLS]

refs_out = [dict(key=k, citation=v, group="v0.2 sources") for k, v in REFS.items()]
beta_refs = pd.read_excel(xl, sheet_name="References", header=None)[0].dropna().tolist()[2:]
for c in beta_refs:
    c = str(c).replace("\n", " ").strip()
    if c.startswith("Ó Gráda, C. (2009) - Famine"):  # misc cell → split
        continue
    new = c
    for pre, fix in BETA_REF_FIXES.items():
        if c.startswith(pre): new = fix
    new = new.replace("Gr_x0013_ada", "Gráda")
    refs_out.append(dict(key="", citation=new, group="beta reference list (corrected)"))
for c in EXTRA_BETA_REFS:
    refs_out.append(dict(key="", citation=c, group="beta in-text citations missing from reference list (added)"))
refs_df = pd.DataFrame(refs_out)

for rr in removed_log:
    log.append(dict(event_id="(removed)", row=rr["row"], field="(row removed)", old=f'{rr["years"]}: {rr["impacts"]}', new="", note=rr["note"], date=today))
log_df = pd.DataFrame(log)[["event_id","field","old","new","note","date"]]

# ---------------------------------------------------------------- write
ev.to_csv(os.path.join(OUT, "faminewatch_events.csv"), index=False)
ep_df.to_csv(os.path.join(OUT, "europe_famine_episodes_1250-1800_LjungqvistEtAl2024.csv"), index=False)
ry_df.to_csv(os.path.join(OUT, "europe_famine_region_year_1250-1800_LjungqvistEtAl2024.csv"), index=False)
wide.to_csv(os.path.join(OUT, "europe_famine_region_year_wide_1250-1800_LjungqvistEtAl2024.csv"), index=False)
refs_df.to_csv(os.path.join(OUT, "references.csv"), index=False)
log_df.to_csv(os.path.join(OUT, "changelog_v0.2.csv"), index=False)
ev.to_json(os.path.join(OUT, "faminewatch_events.json"), orient="records", force_ascii=False, indent=0)

# JSON bundle for the explorer
bundle = dict(
    generated=today,
    events=json.loads(ev.to_json(orient="records", force_ascii=False)),
    europe=dict(regions=REGION_ORDER, episodes=json.loads(ep_df.to_json(orient="records", force_ascii=False))),
    references=json.loads(refs_df.to_json(orient="records", force_ascii=False)),
    changelog=json.loads(log_df.groupby(["event_id","note"], sort=False).agg(field=("field", lambda f: ", ".join(dict.fromkeys(f)))).reset_index().to_json(orient="records", force_ascii=False)),
    region_sources=REGION_SRC)
tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "explorer_template.html")).read()
os.makedirs(os.path.join(REPO, "docs"), exist_ok=True)
data_js = json.dumps(bundle, ensure_ascii=False).replace("</", "<\\/")
open(os.path.join(REPO, "docs", "index.html"), "w").write(tpl.replace("/*__DATA__*/null", data_js))

print("events", len(ev), ev.source_dataset.value_counts().to_dict())
print("episodes", len(ep_df), "region-years", int(ry_df.famine.sum()))
print("log", len(log_df), "flags", (log_df.field=="(flag)").sum())
print(ev.macro_region.value_counts().to_dict())
print(ev[ev.area.isna()|(ev.macro_region=="Unassigned")][["event_id","start_year","description"]].head(30).to_string(max_colwidth=60))
