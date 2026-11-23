import sys, os, pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

REPO = sys.argv[1]; D = os.path.join(REPO, "data")
ev = pd.read_csv(os.path.join(D, "faminewatch_events.csv"))
ep = pd.read_csv(os.path.join(D, "europe_famine_episodes_1250-1800_LjungqvistEtAl2024.csv"))
wide = pd.read_csv(os.path.join(D, "europe_famine_region_year_wide_1250-1800_LjungqvistEtAl2024.csv"))
refs = pd.read_csv(os.path.join(D, "references.csv"))
log = pd.read_csv(os.path.join(D, "changelog_v0.2.csv"))

F = "Arial"
HDR = Font(name=F, bold=True, color="FFFFFF"); HFILL = PatternFill("solid", fgColor="1C5CAB")
BODY = Font(name=F, size=10)

wb = Workbook()
ws = wb.active; ws.title = "README"
lines = [
 ("FamineWatch Datasets — Compilation of Select Famines and Food Disruptions Around the World (v0.2, beta)", True),
 ("Puma, M. J., & Chon, S. (2026). Center for Climate Systems Research, Columbia Climate School. Correspondence: mjp38@columbia.edu", False),
 ("", False),
 ("Licence: data CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); code MIT. Included third-party data: Ljungqvist, Seim & Collet (2024) — CC BY 4.0; Our World in Data (Hasell & Roser 2017) — CC BY 4.0; Mishra & Aadhar (2021) — CC BY 4.0; Kim (2025) — CC BY 4.0; REACHES (Lin et al. 2020) — NOAA public data archive. Credit these sources when reusing their records; see LICENSE-DATA.md.", False),
 ("", False),
 ("Sheets", True),
 ("Events — all records (beta compilation, v0.2 corrections and additions, and the European regional famine episodes). One row per event.", False),
 ("Europe_Episodes — famine episodes by region, 1250–1800, from Ljungqvist, Seim & Collet (2024), WIREs Climate Change 15(1):e859, Table A1 (CC BY 4.0). Please cite Ljungqvist et al. (2024) when using these famine years.", False),
 ("Europe_RegionYear — the same chronology as a year × region presence matrix (1 = famine recorded). Column K counts regions in famine (formula).", False),
 ("References — full citations. ChangeLog — corrections applied in v0.2 and items flagged for review.", False),
 ("", False),
 ("Important caveats", True),
 ("The European chronology records only the presence of famine conditions in a region-year, not severity or geographic extent within the region (Ljungqvist et al. 2024).", False),
 ("Entries citing Walford (1878) are 19th-century compilations of chronicle reports and have not been independently verified; Walford's Table 1 entries for 1832–1878 are not yet transcribed.", False),
 ("Mortality figures are approximate best estimates from the cited sources. Not for operational early warning without contextual validation.", False),
 ("When using the European famine years, cite Ljungqvist et al. (2024) and Alfani & Ó Gráda (2017, 2018), and the regional sources listed for each region.", False),
]
for i, (t, b) in enumerate(lines, 1):
    c = ws.cell(row=i, column=1, value=t); c.font = Font(name=F, bold=b, size=12 if i == 1 else 10)
ws.column_dimensions["A"].width = 150

def sheet(name, df, widths=None, wrap=()):
    s = wb.create_sheet(name)
    for j, col in enumerate(df.columns, 1):
        c = s.cell(row=1, column=j, value=col); c.font = HDR; c.fill = HFILL
    for i, row in enumerate(df.itertuples(index=False), 2):
        for j, v in enumerate(row, 1):
            if pd.isna(v): v = None
            c = s.cell(row=i, column=j, value=v); c.font = BODY
            if df.columns[j-1] in wrap: c.alignment = Alignment(wrap_text=True, vertical="top")
    s.freeze_panes = "B2"; s.auto_filter.ref = s.dimensions
    for j, col in enumerate(df.columns, 1):
        s.column_dimensions[get_column_letter(j)].width = (widths or {}).get(col, 14)
    return s

sheet("Events", ev, {"event_id":12,"source_dataset":30,"year_label":14,"area":26,"macro_region":20,"event_type":24,
      "primary_cause":28,"environmental_category":20,"description":70,"references":40,"verification_status":30,"qc_notes":50},
      wrap=("description","qc_notes","references"))
sheet("Europe_Episodes", ep, {"episode_id":16,"region":16,"as_printed":12,"regional_sources":60,"note":50,"citation":60})
s = sheet("Europe_RegionYear", wide, {"year":8})
k = len(wide.columns) + 1
c = s.cell(row=1, column=k, value="regions_in_famine"); c.font = HDR; c.fill = HFILL
last = get_column_letter(k - 1)
for i in range(2, len(wide) + 2):
    c = s.cell(row=i, column=k, value=f"=SUM(B{i}:{last}{i})"); c.font = BODY; c.number_format = "0"
s.column_dimensions[get_column_letter(k)].width = 18
sheet("References", refs, {"key":22,"citation":140,"group":40})
sheet("ChangeLog", log, {"event_id":12,"field":10,"old":40,"new":40,"note":90,"date":12}, wrap=("old","new","note"))
out = os.path.join(REPO, "famine_database_v0.2.xlsx")
wb.save(out); print(out)
