# Offline basemap

Everything here ships inside the app; nothing is downloaded at run time.

| File | What | License |
|---|---|---|
| `maplibre-gl.js/.css` 5.24.0 | map renderer | BSD-3-Clause |
| `pmtiles.js` 4.5.0 | reads one-file tile archives | BSD-3-Clause |
| `basemaps.js` (@protomaps/basemaps 5.7.2) | map style | BSD-3-Clause |
| `fonts/`, `sprites/` | glyphs (Noto Sans, OFL) and icons from protomaps/basemaps-assets | see that repo |
| `region/p0000.pmtiles`, `p0001.pmtiles` … and `region.json` | an extract of the world map for **your** region, cut into 1 MB pieces by the CI build, **not in git** (one big file cannot be read in parts on Android: its file server ignores the start of a Range request) | © OpenStreetMap contributors (ODbL), Protomaps build |

## Enabling a map for your region

By default the release has no basemap and draws routes as a clean line. To bundle a map, set a repository variable (Settings, Secrets and variables, Actions, Variables) named `BASEMAP_BBOX` to `west,south,east,north` in degrees, for example `13.0,52.3,13.8,52.7` for Berlin. The build downloads that extract (zoom up to 14) with the `pmtiles` tool, cuts it into pieces and writes `region.json`. Keep the box small: a city is a few tens of MB, a country is gigabytes and makes the app huge.

If `region/p0000.pmtiles` or `region.json` is missing, or a route lies outside the box, the app shows the plain line map.

The first-run setup tells users which region has a map (`MAP_REGION` in `index.html`, currently "Berlin, Germany"). Keep it in sync with `BASEMAP_BBOX`.
